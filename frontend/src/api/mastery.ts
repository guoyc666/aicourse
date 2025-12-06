import api from "./request";

const mockData = [
  {
    knowledge_id: "MachineLearning",
    mastery: 0.9,
  },
  {
    knowledge_id: "DeepLearning",
    mastery: 0.6,
  },
  {
    knowledge_id: "NeuralNetwork",
    mastery: 0.4,
  },
  {
    knowledge_id: "child1",
    mastery: 0.4,
  },
  {
    knowledge_id: "child2",
    mastery: 0.2,
  },
  {
    knowledge_id: "child3",
    mastery: 0.1,
  },
];

export const masteryAPI = {
  // 获取某学生在某知识点的掌握度
  async fetchMastery(knowledgeId: string) {
    const res = await api.get("/mastery", {
      params: { knowledge_id: knowledgeId }
    });
    return res;
  },
  // 获取某学生在所有知识点的掌握度
  async fetchAllMastery() {
    const res = await api.get("/mastery/all");
    return res;
  },
  // 获取某知识点的平均掌握度
  async fetchAverageMastery(knowledgeId: string) {
    const res = await api.get("/mastery/average", {
      params: { knowledge_id: knowledgeId }
    });
    return res;
  },
  // 获取所有学生在所有知识点的平均掌握度
  async fetchAllAverageMastery() {
    const res = await api.get("/mastery/average/all");
    return res;
  },
  // 获取某知识点所有学生的掌握度列表
  async fetchMasteryList(knowledgeId: string) {
    const res = await api.get("/mastery/list", {
      params: { knowledge_id: knowledgeId }
    });
    return res;
  },
  // 获取所有学生在所有知识点的掌握度列表
  async fetchAllMasteryList() {
    const res = await api.get("/mastery/list/all");
    return res;
  },
  // 获取模拟数据
  async fetchAllMockMastery(studentId: number) {
    return mockData;
  },
};
