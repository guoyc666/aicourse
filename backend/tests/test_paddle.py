import warnings
warnings.filterwarnings("ignore")

import os
import uuid
from paddlenlp import Taskflow

import requests

BASE_URL = "http://localhost:8000/api"

def parse_extraction_result(result):
    nodes = []
    links = []
    node_map = {}  # text -> id
    synonym_map = {}  # text -> 主节点text
    description_map = {}  # 概念id -> description

    # 1. 处理同义关系，建立同义映射
    for item in result:
        for kp in item.get("知识点", []):
            text = kp["text"]
            synonym_map[text] = text  # 默认自己是主节点
            relations = kp.get("relations", {})
            for rel_type, rel_list in relations.items():
                if rel_type == "同义":
                    for rel in rel_list:
                        synonym_map[rel["text"]] = text  # 合并到主节点

    def get_or_create_node(text, category, description=""):
        main_text = synonym_map.get(text, text)
        if main_text not in node_map:
            node_id = str(uuid.uuid4())
            node_map[main_text] = node_id
            nodes.append({
                "id": node_id,
                "name": main_text,
                "category": category,
                "description": description
            })
        return node_map[main_text]

    # 2. 处理知识点和关系
    for item in result:
        for kp in item.get("知识点", []):
            kp_id = get_or_create_node(kp["text"], "Concept")
            relations = kp.get("relations", {})
            for rel_type, rel_list in relations.items():
                if rel_type == "同义":
                    continue  # 已处理
                for rel in rel_list:
                    rel_id = get_or_create_node(rel["text"], "Concept")
                    if kp_id == rel_id:
                        continue
                    links.append({
                        "source": kp_id,
                        "target": rel_id,
                        "relation": rel_type
                    })
        # 3. 处理含义，作为描述字段
        for meaning in item.get("含义", []):
            relations = meaning.get("relations", {})
            for rel_type, rel_list in relations.items():
                if rel_type == "描述":
                    for rel in rel_list:
                        concept_id = get_or_create_node(rel["text"], "Concept")
                        description_map[concept_id] = meaning["text"]

    # 4. 更新节点的 description 字段
    for node in nodes:
        if node["id"] in description_map:
            node["description"] = description_map[node["id"]]

    # 5. 优化包含链，只保留最长链
    # 构建包含关系图
    include_graph = {}
    for link in links:
        if link["relation"] == "包含":
            include_graph.setdefault(link["source"], set()).add(link["target"])
    # 检查冗余链
    def is_redundant(source, target):
        # 如果 source 能通过多步到达 target，则冗余
        visited = set()
        def dfs(cur):
            if cur == target:
                return True
            visited.add(cur)
            for nxt in include_graph.get(cur, []):
                if nxt not in visited and dfs(nxt):
                    return True
            return False
        for mid in include_graph.get(source, []):
            if mid != target and dfs(mid):
                return True
        return False

    new_links = []
    for link in links:
        if link["relation"] == "包含":
            if is_redundant(link["source"], link["target"]):
                continue  # 冗余，跳过
        new_links.append(link)

    return nodes, new_links

def upload_to_backend(nodes, links):
    # 上传节点
    for node in nodes:
        resp = requests.post(f"{BASE_URL}/node", json=node)
        print("创建节点：", node["id"], resp.json())
    # 上传关系
    for link in links:
        resp = requests.post(f"{BASE_URL}/link", json=link)
        print("创建关系：", link, resp.json())

# PaddleNLP抽取和解析流程
schema = [{'知识点': ['包含', '依赖', '同义']}, {'含义': ['描述']}]
ie = Taskflow(
    'information_extraction',
    schema=schema,
    task_path='f:\\StudyFiles\\ZYGC2025\\aicourse\\backend\\model_zoo\\checkpoint\\model_best',)

folder = 'f:\\StudyFiles\\ZYGC2025\\aicourse\\backend\\output\\output'
output_file = 'f:\\StudyFiles\\ZYGC2025\\aicourse\\backend\\output\\parse_results.txt'

with open(output_file, 'w', encoding='utf-8') as out_f:
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            filepath = os.path.join(folder, filename)
            with open(filepath, encoding='utf-8') as f:
                text = f.read()
                result = ie(text)
                nodes, links = parse_extraction_result(result)
                upload_to_backend(nodes, links)