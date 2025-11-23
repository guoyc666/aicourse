from typing import List, Dict, Any
from py2neo import Node, Relationship
from crud.progress import calc_progress
from db.neo4j import get_graph
from models import KnowledgePoint, Resource, KnowledgeResourceLink, LearningRecord
from sqlalchemy.orm import Session

def get_node_depths():
    graph = get_graph()
    query = """
    MATCH (course:Course), (n)
    WHERE course <> n
    OPTIONAL MATCH p = shortestPath((course)-[:包含*]->(n))
    RETURN n.id AS id, 
           CASE WHEN p IS NULL THEN NULL ELSE length(p) END AS depth
    UNION
    MATCH (course:Course)
    RETURN course.id AS id, 0 AS depth
    """
    result = graph.run(query).data()
    return {row["id"]: row["depth"] for row in result if row["id"] is not None}

def get_all_nodes_and_links():
    graph = get_graph()
    nodes = []
    links = []
    
    depths = get_node_depths()

    # 只查询Concept和Course节点
    for n in graph.nodes.match():
        if n["category"] not in ["Concept", "Course"]:
            continue
        node_data = dict(n)
        node_data["id"] = n["id"]
        node_data["category"] = n["category"]
        node_data["name"] = n["name"]
        node_data["description"] = n.get("description")
        if node_data["category"] == "Course":
            node_data["depth"] = 0
        elif node_data["category"] == "Concept":
            node_data["depth"] = depths.get(node_data["id"], None)
            node_data["difficulty"] = n.get("difficulty")
            node_data["importance"] = n.get("importance")
        nodes.append(node_data)

    # 查询所有关系（不变）
    rels = graph.match()
    for r in rels:
        links.append({
            "source": r.start_node["id"],
            "target": r.end_node["id"],
            "relation": r.__class__.__name__
        })

    return nodes, links

def get_node_detail(node_id: str, student_id: int, db: Session):
    graph = get_graph()
    # 查询节点基本信息（Neo4j）
    n = graph.nodes.match(id=node_id).first()
    if not n:
        return None

    # 查询所有资源（直接和子关联），用is_child标记
    # resource_query = f"""
    # MATCH (k:Concept {{id: '{node_id}'}})-[:关联]->(r:Resource)
    # RETURN r.id AS id, r.name AS name, r.type AS type, false AS is_child
    # UNION
    # MATCH (k:Concept {{id: '{node_id}'}})-[:子关联]->(r:Resource)
    # RETURN r.id AS id, r.name AS name, r.type AS type, true AS is_child
    # """
    # resources = graph.run(resource_query).data()

    # 查询所有资源在关系数据库KnowledgeResourceLink
    kr_links = db.query(KnowledgeResourceLink).filter(
        KnowledgeResourceLink.knowledge_id == node_id
    ).all()
    resources = []
    for link in kr_links:
        res = db.query(Resource).filter(Resource.id == link.resource_id).first()
        if res:
            resources.append({
                "id": res.id,
                "name": res.name,
                "type": "ppt",
                "is_child": link.is_child,
            })


    # 查询资源的学习记录
    resource_ids = [r["id"] for r in resources]
    records = db.query(LearningRecord).filter(
        LearningRecord.resource_id.in_(resource_ids),
    ).all()
    # 筛选该学生的学习记录
    student_records = [r for r in records if r.student_id == student_id]
    # 计算总学习时长
    total_time = int(sum(r.total_time for r in student_records)/60)  # 转为分钟
    # 计算所有学生的平均学习时长，先从records中筛选出有多少不同学生学习过这些资源，然后计算平均值
    student_ids = set(r.student_id for r in records)
    total_times = sum(r.total_time for r in records)
    average_time = int(total_times / len(student_ids)/60) if student_ids else 0  # 转为分钟

    # 前置知识点（Neo4j）
    pre_query = f"""
    MATCH (pre:Concept)-[:前置]->(n:Concept {{id: '{node_id}'}})
    RETURN pre.id AS id, pre.name AS name
    """
    prerequisites = graph.run(pre_query).data()

    # 后续知识点（Neo4j）
    suc_query = f"""
    MATCH (n:Concept {{id: '{node_id}'}})-[:前置]->(suc:Concept)
    RETURN suc.id AS id, suc.name AS name
    """
    successors = graph.run(suc_query).data()

    return {
        "id": n["id"],
        "name": n["name"],
        "description": n.get("description", ""),
        "total_time": total_time,
        "average_time": average_time,
        "resources": resources,
        "prerequisites": prerequisites,
        "successors": successors,
    }

def save_knowledge_graph(nodes: List[Dict[str, Any]], links: List[Dict[str, Any]]):
    graph = get_graph()
    # 清空现有图谱
    graph.delete_all()

    node_map = {}
    # 创建节点
    for node in nodes:
        props = {k: v for k, v in node.items() if v is not None and k not in ["x", "y"]}
        n = Node(node["category"], **props)
        graph.create(n)
        node_map[node["id"]] = n

    # 创建关系
    for link in links:
        source_node = node_map.get(link["source"])
        target_node = node_map.get(link["target"])
        if source_node and target_node:
            r = Relationship(source_node, link["relation"], target_node)
            graph.create(r)

def batch_add_nodes_and_links(nodes: List[Dict[str, Any]], links: List[Dict[str, Any]]):
    # nodes: [{"id": ..., "category": ..., "name": ..., ...}, ...]
    # links: [{"source": ..., "target": ..., "relation": ...}, ...]
    graph = get_graph()
    # 批量添加节点
    for node_data in nodes:
        node = Node(node_data.get("category", "Concept"), **node_data)
        graph.merge(node, node_data.get("category", "Concept"), "id")

    # 批量添加关系
    for link_data in links:
        source = graph.nodes.match("Concept", id=link_data["source"]).first()
        if not source:
            source = graph.nodes.match("Course", id=link_data["source"]).first()
        target = graph.nodes.match("Concept", id=link_data["target"]).first()
        if not target:
            target = graph.nodes.match("Course", id=link_data["target"]).first()
        if source and target:
            rel = Relationship(source, link_data["relation"], target)
            graph.merge(rel)

def create_node(node: Dict[str, Any]):
    graph = get_graph()
    props = {k: v for k, v in node.items() if v is not None and k not in ["x", "y"]}
    n = Node(node["category"], **props)
    graph.create(n)

def update_node(node_id: str, updates: Dict[str, Any]):
    graph = get_graph()
    updates = {k: v for k, v in updates.items() if k not in ["x", "y"]}
    n = graph.nodes.match(id=node_id).first()
    if n:
        for k, v in updates.items():
            n[k] = v
        graph.push(n)

def delete_node(node_id: str):
    graph = get_graph()
    n = graph.nodes.match(id=node_id).first()
    if n:
        graph.delete(n)

def create_link(link: Dict[str, Any]):
    graph = get_graph()
    a = graph.nodes.match(id=link["source"]).first()
    b = graph.nodes.match(id=link["target"]).first()
    if a and b:
        r = Relationship(a, link["relation"], b)
        graph.create(r)

def delete_link(source: str, target: str, relation: str):
    graph = get_graph()
    a = graph.nodes.match(id=source).first()
    b = graph.nodes.match(id=target).first()
    if a and b:
        rels = graph.match((a, b), r_type=relation)
        for r in rels:
            graph.separate(r)