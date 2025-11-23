import api from "./request";

export const progressAPI = {
  // 获取某学生在某知识点的学习进度
  async fetchProgress(studentId: number, knowledgeId: string) {
    const res = await api.get(`/progress/${studentId}/${knowledgeId}`);
    return res.data;
  },
  // 获取某学生在所有知识点的学习进度
  async fetchAllProgress(studentId: number) {
    const res = await api.get(`/progress/${studentId}`);
    return res.data;
  },
  // 获取所有学生在所有知识点的平均学习进度
  async fetchAllAverageProgress() {
    const res = await api.get(`/progress/average`);
    return res.data;
  },
};
