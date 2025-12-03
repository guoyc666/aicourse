import api from "./request";

export const progressAPI = {
  // 获取某学生在某知识点的学习进度
  async fetchProgress( knowledgeId: string) {
    const res = await api.get('/api/progress', {
      params: { knowledge_id: knowledgeId }
    });
    return res;
  },
  // 获取某学生在所有知识点的学习进度
  async fetchAllProgress() {
    const res = await api.get('/api/progress/all');
    return res;
  },
  // 获取某知识点的平均学习进度
  async fetchAverageProgress( knowledgeId: string) {
    const res = await api.get('/api/progress/average', {
      params: { knowledge_id: knowledgeId }
    });
    return res;
  },
  // 获取所有学生在所有知识点的平均学习进度
  async fetchAllAverageProgress() {
    const res = await api.get('/api/progress/average/all');
    return res;
  },
  // 获取某知识点所有学生的学习进度列表
  async fetchProgressList( knowledgeId: string) {
    const res = await api.get('/api/progress/list', {
      params: { knowledge_id: knowledgeId }
    });
    return res;
  },
  // 获取所有学生在所有知识点的学习进度列表
  async fetchAllProgressList() {
    const res = await api.get('/api/progress/list/all');
    return res;
  },
};
