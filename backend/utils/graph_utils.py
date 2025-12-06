import os
import json
from openai import OpenAI
import requests
import time
from typing import Optional
from pydantic import BaseModel
from typing import Literal
from crud.graph import batch_add_nodes_and_edges

class ConceptNode(BaseModel):
    id: str
    category: Literal["Concept"]
    name: str
    description: Optional[str] = None

class GraphEdge(BaseModel):
    source: str
    target: str
    relation: Literal["包含", "前置"]

BASE_URL = "http://localhost:8000/api"

kg_path = './utils/knowledgeGraph.json'

def load_knowledge_graph(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_knowledge_graph(path, graph):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

def build_course_prompt(graph):
    graph_str = json.dumps(graph, ensure_ascii=False, indent=2)
    return f"""
你是一个课程知识图谱构建助手，专门为大学计算机学院的《大数据分析》课程服务。你的任务是从给定的文本片段中精准提取知识点及其关系，为当前知识图谱补充这些信息。
以下是当前知识图谱：
<当前知识图谱>
{graph_str}
</当前知识图谱>
提取知识点时，请确保知识点属于《大数据分析》课程范畴，且仅为当前知识图谱寻找子节点或者为找到的节点寻找子节点。
不要提取重复的知识点，知识点与自身不存在任何关系。
知识点之间的关系仅考虑“包含”和“前置”两种，且两种关系不能同时存在于同一对节点之间。提取关系时需严格依据文本片段中的逻辑关联，确保关系精准对应知识点间的实际层级或先后逻辑。
请严格按照以下JSON格式返回结果：
{{
  "nodes": [
    {{
      "id": "节点唯一标识",
      "name": "知识点名称",
      "category": "Concept",
      "description": "知识点描述"
    }},
    ...
  ],
  "edges": [
    {{ "source": "起始节点id", "target": "结尾节点id", "relation": "包含或前置" }},
    ...
  ]
}}
请不要返回除上述JSON以外的内容。
请从以下文本片段中提取知识点及它们的关系：
"""

def validate_format(nodes, edges):
    valid_nodes = []
    valid_edges = []

    for node in nodes:
        try:
            valid_node = ConceptNode(**node)
            valid_nodes.append(valid_node)  
        except Exception as e:
            pass

    for edge in edges:
        try:
            valid_edge = GraphEdge(**edge)
            valid_edges.append(valid_edge)  
        except Exception as e:
            pass
    return valid_nodes, valid_edges

def filter_nodes_and_edges(new_nodes, new_edges):
    valid_nodes, valid_edges = validate_format(new_nodes, new_edges)
    timestamp = str(int(time.time() * 1000))
    # 构建 id 映射表
    id_map = {node.id: f"{node.id}_{timestamp}" for node in valid_nodes}

    # 批量更新节点 id
    for node in valid_nodes:
        node.id = id_map[node.id]

    # 批量更新边的 source/target
    for edge in valid_edges:
        if edge.source in id_map:
            edge.source = id_map[edge.source]
        if edge.target in id_map:
            edge.target = id_map[edge.target]
        
    # 构建所有包含边
    include_edges = [e for e in valid_edges if e.relation == "包含"]
    # 构建父节点映射
    child_to_parents = {}
    for edge in include_edges:
        child_to_parents.setdefault(edge.target, set()).add(edge.source)

    # 只保留有且仅有一个父节点的节点
    filtered_nodes = []
    for node in valid_nodes:
        parents = child_to_parents.get(node.id, set())
        if len(parents) != 1:
            continue
        filtered_nodes.append(node)
    filtered_node_ids = set(n.id for n in filtered_nodes)

    # 构建子节点映射
    parent_to_children = {}
    for edge in include_edges:
        parent_to_children.setdefault(edge.source, set()).add(edge.target)

    # 路径查找：从根到某节点的路径
    def get_path_to_node(node_id):
        path = []
        current = node_id
        while True:
            parents = child_to_parents.get(current, set())
            if not parents:
                break
            parent = list(parents)[0]
            path.insert(0, parent)
            current = parent
        return path

    # 子树查找：以某节点为根的所有子节点
    def get_subtree_nodes(root_id):
        result = set()
        result.add(root_id)
        stack = [root_id]
        while stack:
            nid = stack.pop()
            children = parent_to_children.get(nid, set())
            for child in children:
                if child not in result:
                    result.add(child)
                    stack.append(child)
        return result
    
    # 过滤前置边
    filtered_edges = []
    for edge in valid_edges:
        if edge.relation == "前置":
            target_id = edge.target
            source_id = edge.source
            # 前置节点不能为路径上的节点或子树上的节点
            path_nodes = set(get_path_to_node(target_id))
            subtree_nodes = get_subtree_nodes(target_id)
            if source_id in path_nodes or source_id in subtree_nodes:
                continue  # 不合法，跳过
        # 只保留target在filtered_nodes中的边
        if edge.target in filtered_node_ids:
            filtered_edges.append(edge)

    return [n.model_dump() for n in filtered_nodes], [e.model_dump() for e in filtered_edges]

def getAnswer(course_prompt, CONTENT: str):
    client = OpenAI(
        api_key="sk-7Uz2z1DZrn0TNUwI0Bo8SwYQW1FJg4wxlnCF5cMmPRW48Ze9", 
        base_url = 'https://api.chatanywhere.tech'
    )
    response = client.chat.completions.create(
        model='gpt-5-mini',
        messages=[
            {
                "role": "system",
                "content": "你是一位知识助手，请根据用户的问题和相关片段生成准确的回答。不要编造信息。"
            },
            {
                "role": "user",
                "content": course_prompt
            },
            {
                "role": "user",
                "content": CONTENT
            }
        ]
    )
    return response.choices[0].message.content

def addResourseToGraph(id: str, name: str, type: str, download_url: str, content: str):
    knowledge_graph = load_knowledge_graph(kg_path)
    prompt = build_course_prompt(knowledge_graph)
    result_str = getAnswer(prompt, content)
    result = json.loads(result_str)
    # 过滤和验证新节点及边
    new_nodes, new_edges = filter_nodes_and_edges(result['nodes'], result['edges'])

    # 构建旧图的包含关系邻接表
    include_adj = {}
    for edge in knowledge_graph['edges']:
        if edge['relation'] == '包含':
            include_adj.setdefault(edge['source'], []).append(edge['target'])
    # 新图的包含关系也加进去
    for edge in new_edges:
        if edge['relation'] == '包含':
            include_adj.setdefault(edge['source'], []).append(edge['target'])

    # 构建节点查找表（旧+新）
    node_map = {node['id']: node for node in knowledge_graph['nodes'] + new_nodes}

    # 先给Course节点depth设为0（假设只有一个Course节点，id为'root'）
    node_map['root']['depth'] = 0

    # DFS计算新节点的depth
    def dfs_depth(node_id, depth):
        children = include_adj.get(node_id, [])
        for child_id in children:
            if child_id in node_map and node_map[child_id].get('category') == 'Concept':
                node_map[child_id]['depth'] = depth + 1
                dfs_depth(child_id, depth + 1)
    dfs_depth('root', 0)

    # 只保留new_nodes部分（已赋depth）
    final_nodes = [node_map[node['id']] for node in [n for n in new_nodes if n.get('category') == 'Concept']]
    # 添加资源节点
    resource_node = {
        "id": id,
        "name": name,
        "category": "Resource",
        "download_url": download_url,
        "type": type
    }
    final_nodes.append(resource_node)

    # 给每个新知识点加关联边
    for node in new_nodes:
        if node.get("category") == "Concept":
            new_edges.append({
                "source": node["id"],
                "target": id,
                "relation": "关联"
            })

    print(f"新增有效知识点数：{len(final_nodes)}，新增关系数：{len(new_edges)}")
    batch_add_nodes_and_edges(final_nodes, new_edges)
    return

folder = 'f:\\StudyFiles\\ZYGC2025\\aicourse\\backend\\output\\TXT讲稿_无标点'

if __name__ == '__main__':
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                file_content = f.read()
                print(f"处理文件：{filename}")
                addResourseToGraph(filename[:-4], filename, "text", file_content)
                break  # 仅处理一个文件进行测试