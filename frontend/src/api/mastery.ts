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
  async fetchMastery(studentId: number, knowledgeId: string) {
    const res = await api.get(`/mastery/${studentId}/${knowledgeId}`);
    return res.data;
  },
  // 获取某学生在所有知识点的掌握度
  async fetchAllMastery(studentId: number) {
    const res = await api.get(`/mastery/${studentId}`);
    return res.data;
  },
  // 获取所有学生在所有知识点的平均掌握度
  async fetchAllAverageMastery() {
    const res = await api.get(`/mastery/average`);
    return res.data;
  },
  async fetchAllMockMastery(studentId: number) {
    return mockData;
  },
};
