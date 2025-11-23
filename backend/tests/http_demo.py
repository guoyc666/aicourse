# encoding:UTF-8
import json
import os
import requests


# 请替换XXXXXXXXXX为您的 APIpassword, 获取地址：https://console.xfyun.cn/services/bmx1
api_key = "Bearer UACmRjIgTshEEJtiJEME:AdxGbuUuGqKvfAHnggoU"
url = "https://spark-api-open.xf-yun.com/v1/chat/completions"

course_prompt = """
你是一个课程知识图谱构建助手，专门为大学计算机学院的《大数据分析》课程服务。你的任务是从给定的文本片段中提取知识点及其关系，并为当前知识图谱补充这些信息。
以下是当前知识图谱：
<当前知识图谱>
{
  "course": "大数据分析",
  "nodes": [
    {
      "id": "root",
      "name": "大数据分析",
      "category": "Course",
      "description": "课程核心知识点，涵盖大数据相关的系统、工具、应用与挑战。"
    },
    {
      "id": "concept",
      "name": "大数据基础概念",
      "category": "Concept",
      "description": "阐述大数据的定义、特征和发展趋势。"
    },
    {
      "id": "acquisition",
      "name": "数据获取",
      "category": "Concept",
      "description": "介绍大数据采集的方式和工具。"
    },
    {
      "id": "quality",
      "name": "数据质量与预处理",
      "category": "Concept",
      "description": "说明数据清洗、预处理的重要性和方法。"
    },
    {
      "id": "storage",
      "name": "数据存储系统",
      "category": "Concept",
      "description": "讲解大数据存储的原理和技术。"
    },
    {
      "id": "processing",
      "name": "数据处理系统",
      "category": "Concept",
      "description": "介绍大数据处理的基本方法和常用系统。"
    },
    {
      "id": "platform",
      "name": "大数据平台与工具",
      "category": "Concept",
      "description": "列举主流大数据平台和工具。"
    },
    {
      "id": "application",
      "name": "大数据应用与挑战",
      "category": "Concept",
      "description": "分析大数据在实际应用中的机遇与挑战。"
    }
  ],
  "links": [
    { "source": "root", "target": "concept", "relation": "包含" },
    { "source": "root", "target": "acquisition", "relation": "包含" },
    { "source": "root", "target": "quality", "relation": "包含" },
    { "source": "root", "target": "storage", "relation": "包含" },
    { "source": "root", "target": "processing", "relation": "包含" },
    { "source": "root", "target": "platform", "relation": "包含" },
    { "source": "root", "target": "application", "relation": "包含" },
    { "source": "concept", "target": "acquisition", "relation": "前置" },
    { "source": "acquisition", "target": "quality", "relation": "前置" },
    { "source": "quality", "target": "storage", "relation": "前置" },
    { "source": "storage", "target": "processing", "relation": "前置" },
    { "source": "processing", "target": "platform", "relation": "前置" },
    { "source": "platform", "target": "application", "relation": "前置" }
  ]
}
</当前知识图谱>
请从我给出的文本片段中提取知识点及它们的关系。
提取知识点时，请确保知识点属于《大数据分析》课程范畴，且仅为当前节点寻找子节点或者为找到的节点寻找子节点。不要提取重复的知识点，知识点与自身不存在任何关系。知识点之间的关系只考虑包含和前置关系，且两种关系不能同时存在。
请严格按照以下JSON格式返回结果：
{
  "nodes": [
    {
      "id": "节点唯一标识",
      "name": "知识点名称",
      "category": "Concept",
      "description": "知识点描述"
    },
    ...
  ],
  "links": [
    { "source": "起始节点id", "target": "结尾节点id", "relation": "包含或前置" },
    ...
  ]
}
请不要返回除上述JSON以外的内容。
"""

# 请求模型，并将结果输出
def get_answer(message):
    #初始化请求体
    headers = {
        'Authorization':api_key,
        'content-type': "application/json"
    }
    body = {
        "model": "lite",
        "user": "zhangzhao",
        "messages": message,
        # 下面是可选参数
        "tools": [
            {
                "type": "web_search",
                "web_search": {
                    "enable": False,
                }
            }
        ]
    }
    response = requests.post(url=url, json=body, headers=headers)
    resp_json = response.json()
    code = resp_json.get("code", -1)
    if code != 0:
        # 错误码处理
        error_msg = resp_json.get("message", "未知错误")
        print(f"请求失败，错误码：{code}，原因：{error_msg}")
        return f"ERROR: {code} {error_msg}"
    choices = resp_json.get("choices", [])
    if choices and "message" in choices[0]:
        content = choices[0]["message"].get("content", "")
        return content
    else:
        print("未获取到有效回复")
        return ""


# 管理对话历史，按序编为列表
def getText(text,role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

folder = 'f:\\StudyFiles\\ZYGC2025\\aicourse\\backend\\output\\TXT讲稿'
output_folder = 'f:\\StudyFiles\\ZYGC2025\\aicourse\\backend\\output\\KnowledgeGraph'
chatHistory = []
#getText(chatHistory, "system", course_prompt)

if __name__ == '__main__':
    for filename in os.listdir(folder):
        if filename.endswith('1.0.txt'):
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                file_content = f.read()
            # 临时组织本轮对话
            tempHistory = chatHistory.copy()
            getText(tempHistory, "user", file_content)
            getText(tempHistory, "user", course_prompt)
            print(f"\n解析文件：{filename}")
            result = get_answer(tempHistory)
            # 保存结果到文件
            output_path = os.path.join(output_folder, filename.replace('.txt', '_knowledge_graph.json'))
            with open(output_path, 'w', encoding='utf-8') as out_f:
                out_f.write(result)