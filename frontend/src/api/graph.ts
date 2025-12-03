import type { KnowledgeEdge, KnowledgeNode } from "../types";
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

const mockEdges: KnowledgeEdge[] = [
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
    const res = await api.get("/api/graph");
    return res;
  },
  // 获取模拟知识图谱数据
  async fetchMockKnowledgeGraph() {
    return {
      nodes: mockNodeData,
      edges: mockEdges,
    };
  },
  // 获取节点详情
  async fetchNodeDetail(nodeId: string) {
    const res = await api.get(`/api/node/detail/${nodeId}`);
    return res;
  },
  // 提交知识图谱数据
  async updateKnowledgeGraph(nodes: any[], edges: any[]) {
    const res = await api.put("/api/graph", { nodes: nodes, edges: edges });
    return res;
  },
  // 创建节点
  async createNode(node: KnowledgeNode) {
    const res = await api.post("/api/node", node);
    return res;
  },
  // 获取所有知识点
  async fetchAllKnowledgeNodes() {
    const res = await api.get("/api/node/knowledge/all");
    return res;
  },
};
