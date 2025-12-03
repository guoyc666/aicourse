import json
from typing import List, Dict, Any
from py2neo import Node, Relationship
from neo4j import get_graph
from schemas_.graph import KnowledgeInfo
from models import Question, LearningRecord
from sqlalchemy.orm import Session

def get_all_knowledge_points():
    graph = get_graph()
    knowledge_query = """
    MATCH (k:Concept)
    RETURN k.id AS id
    """
    knowledge_points = graph.run(knowledge_query).data()
    knowledge_ids = [kp["id"] for kp in knowledge_points]
    return knowledge_ids

def get_all_knowledge_nodes(db: Session):
    graph = get_graph()
    knowledge_query = """
    MATCH (k:Concept)
    RETURN k.id AS id, k.name AS name
    """
    knowledge_points = graph.run(knowledge_query).data()
    # 获取所有题库题目
    questions = db.query(Question).all()
    result = []
    for kp in knowledge_points:
        kp_id = kp["id"]
        kp_name = kp["name"]
        # 统计题目数量（knowledge_id为JSON格式的ID列表）
        count = 0
        for q in questions:
            try:
                knowledge_ids = json.loads(q.knowledge_id)
            except Exception:
                knowledge_ids = []
            if kp_id in knowledge_ids:
                count += 1
        info = KnowledgeInfo(id=kp_id, name=kp_name, question_count=count)
        result.append(info)
    return result

def get_resources_by_knowledge(knowledge_id: str):
    graph = get_graph()
    resource_query = f"""
    MATCH (k:Concept {{id: '{knowledge_id}'}})-[:关联]->(r:Resource)
    RETURN r.id AS id
    UNION
    MATCH (k:Concept {{id: '{knowledge_id}'}})-[:包含*1..]->(sub:Concept)-[:关联]->(r:Resource)
    RETURN DISTINCT r.id AS id
    """
    resources = graph.run(resource_query).data()
    resource_ids = [r["id"] for r in resources]
    return resource_ids

def get_all_students(db: Session):
    from models import User, Role, UserRole
    # 查询学生角色id
    student_role = db.query(Role).filter(Role.name == "student").first()
    if not student_role:
        return []
    # 查询所有拥有学生角色的用户
    student_ids = db.query(UserRole.user_id).filter(UserRole.role_id == student_role.id)
    students = db.query(User).filter(User.id.in_(student_ids)).all()
    return students

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

def get_all_nodes_and_edges():
    graph = get_graph()
    concept_nodes = list(graph.nodes.match("Concept"))
    course_nodes = list(graph.nodes.match("Course"))
    nodes = concept_nodes + course_nodes
    resources = list(graph.nodes.match("Resource")) 

    # 只查询包含和前置关系
    query = """
    MATCH (a)-[r:包含]->(b)
    RETURN a.id AS source, b.id AS target, '包含' AS relation
    UNION
    MATCH (a)-[r:前置]->(b)
    RETURN a.id AS source, b.id AS target, '前置' AS relation
    UNION
    MATCH (a)-[r:关联]->(b)
    RETURN a.id AS source, b.id AS target, '关联' AS relation
    """
    edges = graph.run(query).data()

    return nodes, edges, resources

def get_node_detail(db: Session, node_id: str, user_id: int, is_student: bool):
    graph = get_graph()
    # 查询节点基本信息（Neo4j）
    n = graph.nodes.match(id=node_id).first()
    if not n:
        return None

    # 查询所有资源
    resource_query = f"""
    MATCH (k:Concept {{id: '{node_id}'}})-[:关联]->(r:Resource)
    RETURN r.id AS id, r.name AS name, r.type AS type, r.download_url AS download_url, false AS is_child
    UNION
    MATCH (k:Concept {{id: '{node_id}'}})-[:包含*1..]->(sub:Concept)-[:关联]->(r:Resource)
    RETURN DISTINCT r.id AS id, r.name AS name, r.type AS type, r.download_url AS download_url, true AS is_child
    """
    resources = graph.run(resource_query).data()

    # 去重资源列表，优先保留 is_child=False
    unique_resources = {}
    for r in resources:
        rid = r["id"]
        # 如果已存在且 is_child=False，则不覆盖
        if rid in unique_resources:
            if not unique_resources[rid]["is_child"]:
                continue
        unique_resources[rid] = r
    resources = list(unique_resources.values())

    # 查询资源的学习记录
    resource_ids = [r["id"] for r in resources]
    records = db.query(LearningRecord).filter(
        LearningRecord.resource_id.in_(resource_ids),
    ).all()
    total_time = 0
    if is_student:
        # 筛选该学生的学习记录
        student_records = [r for r in records if r.student_id == user_id]
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

def save_knowledge_graph(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]):
    graph = get_graph()

    # 更新或新增节点
    node_map = {}
    for node in nodes:
        props = {k: v for k, v in node.items() if v is not None and k not in ["x", "y"]}
        n = graph.nodes.match(node["category"], id=node["id"]).first()
        if n:
            # 更新已有节点属性
            for k, v in props.items():
                n[k] = v
            graph.push(n)
        else:
            # 新建节点
            n = Node(node["category"], **props)
            graph.create(n)
        node_map[node["id"]] = n

    # 删除未在 nodes 列表中的节点
    for n in graph.nodes.match():
        if n["id"] not in node_map:
            graph.delete(n)

    # 更新或新增关系
    exist_rels = set()
    for edge in edges:
        source_node = node_map.get(edge["source"])
        target_node = node_map.get(edge["target"])
        if source_node and target_node:
            rel = Relationship(source_node, edge["relation"], target_node)
            graph.merge(rel)
            exist_rels.add((edge["source"], edge["target"], edge["relation"]))

    # 删除未在 edges 列表中的关系
    for r in graph.match():
        sid = r.start_node["id"]
        tid = r.end_node["id"]
        rel_type = r.__class__.__name__
        if (sid, tid, rel_type) not in exist_rels:
            graph.separate(r)

def batch_add_nodes_and_edges(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]):
    # nodes: [{"id": ..., "category": ..., "name": ..., ...}, ...]
    # edges: [{"source": ..., "target": ..., "relation": ...}, ...]
    graph = get_graph()
    # 批量添加节点
    for node_data in nodes:
        node = Node(node_data.get("category", "Concept"), **node_data)
        graph.merge(node, node_data.get("category", "Concept"), "id")

    # 批量添加关系
    for edge_data in edges:
        source = graph.nodes.match("Concept", id=edge_data["source"]).first()
        if not source:
            source = graph.nodes.match("Course", id=edge_data["source"]).first()
        if edge_data["relation"] == "关联":
            target = graph.nodes.match("Resource", id=edge_data["target"]).first()
        else:
            target = graph.nodes.match("Concept", id=edge_data["target"]).first()
        if source and target:
            rel = Relationship(source, edge_data["relation"], target)
            graph.merge(rel)

def create_node(node: Dict[str, Any]):
    graph = get_graph()
    n = Node(node["category"], **node)
    graph.create(n)

def update_node(node: Dict[str, Any]):
    graph = get_graph()
    n = graph.nodes.match(id=node["id"]).first()
    if n:
        for k, v in node.items():
            n[k] = v
        graph.push(n)

def delete_node(node_id: str):
    graph = get_graph()
    n = graph.nodes.match(id=node_id).first()
    if n:
        graph.run("MATCH (n {id: $id}) DETACH DELETE n", id=node_id)

def create_edge(edge: Dict[str, Any]):
    graph = get_graph()
    a = graph.nodes.match(id=edge["source"]).first()
    b = graph.nodes.match(id=edge["target"]).first()
    if a and b:
        r = Relationship(a, edge["relation"], b)
        graph.create(r)

def delete_edge(source: str, target: str, relation: str):
    graph = get_graph()
    a = graph.nodes.match(id=source).first()
    b = graph.nodes.match(id=target).first()
    if a and b:
        rels = graph.match((a, b), r_type=relation)
        for r in rels:
            graph.separate(r)

def delete_all_nodes_and_edges():
    graph = get_graph()
    graph.delete_all()