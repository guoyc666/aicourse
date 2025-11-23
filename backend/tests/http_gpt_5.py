# encoding:UTF-8
import os
import json
from openai import OpenAI
import requests

BASE_URL = "http://localhost:8000/api"

kg_path = 'f:\\StudyFiles\\ZYGC2025\\aicourse\\backend\\tests\\knowledgeGraph.json'

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
  "links": [
    {{ "source": "起始节点id", "target": "结尾节点id", "relation": "包含或前置" }},
    ...
  ]
}}
请不要返回除上述JSON以外的内容。
请从以下文本片段中提取知识点及它们的关系：
"""

def filter_nodes_and_links(new_nodes, new_links, old_graph):
    # 合并所有节点id
    old_ids = set(node['id'] for node in old_graph['nodes'])

    def get_include_links(links):
        return [l for l in links if l.get('relation') == '包含']

    include_links = get_include_links(old_graph['links']) + get_include_links(new_links)

    # 构建父节点映射
    child_to_parents = {}
    for link in include_links:
        child_to_parents.setdefault(link['target'], set()).add(link['source'])

    # 过滤孤立点和有多个父节点的点
    filtered_nodes = []
    for node in new_nodes:
        node_id = node['id']
        parents = child_to_parents.get(node_id, set())
        # 孤立点：没有父节点且不在原图
        if not parents and node_id not in old_ids:
            continue
        # 多个父节点
        if len(parents) > 1:
            continue
        filtered_nodes.append(node)

    # 过滤links，保留target在filtered_nodes中的
    filtered_ids = set(n['id'] for n in filtered_nodes)
    filtered_links = [l for l in new_links if l['target'] in filtered_ids]

    return filtered_nodes, filtered_links

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

def addResourseToGraph(CONTENT: str):
    knowledge_graph = load_knowledge_graph(kg_path)
    prompt = build_course_prompt(knowledge_graph)
    result_str = getAnswer(prompt, CONTENT)
    result = json.loads(result_str)
    new_nodes, new_links = filter_nodes_and_links(result['nodes'], result['links'], knowledge_graph)
    requests.post(f"{BASE_URL}/graph", json={"nodes": new_nodes, "links": new_links})
    print(f"新增节点数：{len(new_nodes)}，新增关系数：{len(new_links)}")
    # merged_nodes = knowledge_graph['nodes'] + [n for n in new_nodes if n['id'] not in set(node['id'] for node in knowledge_graph['nodes'])]
    # merged_links = knowledge_graph['links'] + [l for l in new_links if l not in knowledge_graph['links']]
    # knowledge_graph = {
    #     "course": knowledge_graph.get("course", "大数据分析"),
    #     "nodes": merged_nodes,
    #     "links": merged_links
    # }
    # save_knowledge_graph(kg_path, knowledge_graph)
    # print(f"知识图谱已保存到：{kg_path}")
    # 返回提取出的知识点id列表
    return [n['id'] for n in new_nodes]

folder = 'f:\\StudyFiles\\ZYGC2025\\aicourse\\backend\\output\\TXT讲稿_无标点'

if __name__ == '__main__':
    for filename in os.listdir(folder):
        knowledge_graph = load_knowledge_graph(kg_path)
        if filename.endswith('.txt'):
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                file_content = f.read()
                print(f"处理文件：{filename}")
                addResourseToGraph(file_content)