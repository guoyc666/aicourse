import requests
import os
import json

BASE_URL = "http://localhost:8000/api"
output_folder = 'f:\\StudyFiles\\ZYGC2025\\aicourse\\backend\\output\\KnowledgeGraph'

def batch_insert_from_folder(folder):
    for filename in os.listdir(folder):
        if filename.endswith('_kg.json'):
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                kg = json.load(f)
                nodes = kg.get("nodes", [])
                links = kg.get("links", [])
                print(f"\n插入文件：{filename}，节点数：{len(nodes)}，关系数：{len(links)}")
                # 插入节点
                for node in nodes:
                    resp = requests.post(f"{BASE_URL}/node", json=node)
                    print("创建节点：", node.get("id"), resp.json())
                # 插入关系
                for link in links:
                    resp = requests.post(f"{BASE_URL}/link", json=link)
                    print("创建关系：", link, resp.json())

if __name__ == '__main__':
    batch_insert_from_folder(output_folder)