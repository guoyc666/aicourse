import type { KnowledgeLink, KnowledgeNode } from "../types";
import api from "./request";

const mockNodeData: KnowledgeNode[] = [
  {
    id: "IntroductionToAI",
    category: "Course",
    depth: 0,
    name: "人工智能导论",
    description: "AI课程",
  },
  { id: "DeepLearning", category: "Concept", depth: 1, name: "深度学习" },
  { id: "MachineLearning", category: "Concept", depth: 1, name: "机器学习" },
  { id: "NeuralNetwork", category: "Concept", depth: 2, name: "神经网络" },
  { id: "child1", category: "Concept", depth: 3, name: "子节点1" },
  { id: "child2", category: "Concept", depth: 4, name: "子节点2" },
  { id: "child3", category: "Concept", depth: 5, name: "子节点3" },
];

const mockLinks: KnowledgeLink[] = [
  { source: "IntroductionToAI", target: "MachineLearning", relation: "包含" },
  { source: "IntroductionToAI", target: "DeepLearning", relation: "包含" },
  { source: "DeepLearning", target: "NeuralNetwork", relation: "包含" },
  { source: "NeuralNetwork", target: "child1", relation: "包含" },
  { source: "child1", target: "child2", relation: "包含" },
  { source: "child2", target: "child3", relation: "包含" },
  { source: "MachineLearning", target: "DeepLearning", relation: "前置" },
];

export const graphAPI = {
  // 获取知识图谱数据
  async fetchKnowledgeGraph() {
    const res = await api.get("/graph");
    return res.data;
  },
  // 获取模拟知识图谱数据
  async fetchMockKnowledgeGraph() {
    return {
      nodes: mockNodeData,
      links: mockLinks,
    };
  },
  // 获取节点详情
  async fetchNodeDetail(nodeId: string) {
    const studentId = 1; // 临时使用固定学生ID，后续可改为动态传入
    const res = await api.get(`/node/detail/${nodeId}/${studentId}`);
    return res.data;
  },
  // 提交知识图谱数据
  async updateKnowledgeGraph(nodes: any[], links: any[]) {
    const res = await api.put("/graph", { nodes, links });
    return res.data;
  },
  // 创建节点
  async createNode(node: KnowledgeNode) {
    const res = await api.post("/node", node);
    return res.data;
  },
};
