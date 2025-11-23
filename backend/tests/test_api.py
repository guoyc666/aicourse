import requests

BASE_URL = "http://localhost:8000/api"


# nodes = [
#     {"id": "IntroductionToAI", "category": "Course", "depth": 0, "name": "人工智能导论", "description": "AI课程"},
#     {"id": "DeepLearning", "category": "Concept", "depth": 1, "name": "深度学习"},
#     {"id": "MachineLearning", "category": "Concept", "depth": 1, "name": "机器学习"},
#     {"id": "DataPreprocessing", "category": "Concept", "depth": 1, "name": "数据预处理"},
#     {"id": "ModelEvaluation", "category": "Concept", "depth": 1, "name": "模型评估"},
#     {"id": "NeuralNetwork", "category": "Concept", "depth": 2, "name": "神经网络"},
#     {"id": "SupervisedLearning", "category": "Concept", "depth": 2, "name": "监督学习"},
#     {"id": "UnsupervisedLearning", "category": "Concept", "depth": 2, "name": "无监督学习"},
#     {"id": "ReinforcementLearning", "category": "Concept", "depth": 2, "name": "强化学习"},
#     {"id": "CNN", "category": "Concept", "depth": 3, "name": "卷积神经网络"},
#     {"id": "RNN", "category": "Concept", "depth": 3, "name": "循环神经网络"},
# ]

# links = [
#     {"source": "IntroductionToAI", "target": "MachineLearning", "relation": "包含"},
#     {"source": "IntroductionToAI", "target": "DeepLearning", "relation": "包含"},
#     {"source": "IntroductionToAI", "target": "DataPreprocessing", "relation": "包含"},
#     {"source": "IntroductionToAI", "target": "ModelEvaluation", "relation": "包含"},
#     {"source": "DeepLearning", "target": "NeuralNetwork", "relation": "包含"},
#     {"source": "MachineLearning", "target": "SupervisedLearning", "relation": "包含"},
#     {"source": "MachineLearning", "target": "UnsupervisedLearning", "relation": "包含"},
#     {"source": "MachineLearning", "target": "ReinforcementLearning", "relation": "包含"},
#     {"source": "NeuralNetwork", "target": "CNN", "relation": "包含"},
#     {"source": "NeuralNetwork", "target": "RNN", "relation": "包含"},
#     {"source": "MachineLearning", "target": "DeepLearning", "relation": "前置"},
#     {"source": "CNN", "target": "RNN", "relation": "前置"},
# ]

nodes = [
{
    "id": "root",
    "name": "大数据分析",
    "category": "Course",
    "description": "课程核心知识点，涵盖大数据相关的系统、工具、应用与挑战。"
},
{
    "id": "base_concept",
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
]
links = [
{ "source": "root", "target": "base_concept", "relation": "包含" },
{ "source": "root", "target": "acquisition", "relation": "包含" },
{ "source": "root", "target": "quality", "relation": "包含" },
{ "source": "root", "target": "storage", "relation": "包含" },
{ "source": "root", "target": "processing", "relation": "包含" },
{ "source": "root", "target": "platform", "relation": "包含" },
{ "source": "root", "target": "application", "relation": "包含" },
{ "source": "base_concept", "target": "acquisition", "relation": "前置" },
{ "source": "acquisition", "target": "quality", "relation": "前置" },
{ "source": "quality", "target": "storage", "relation": "前置" },
{ "source": "storage", "target": "processing", "relation": "前置" },
{ "source": "processing", "target": "platform", "relation": "前置" },
{ "source": "platform", "target": "application", "relation": "前置" }
]

requests.post(f"{BASE_URL}/graph", json={"nodes": nodes, "links": links})
print(f"新增节点数：{len(nodes)}，新增关系数：{len(links)}")

# 批量删除所有节点
# for node in nodes:
#     resp = requests.delete(f"{BASE_URL}/node/{node['id']}")
#     print("删除节点：", node["id"], resp.json())