import api from "./request";
import type { LearningRecord } from "../types";

export const recordsAPI = {
  // 获取某学生的学习记录（按日期汇总的学习时长）
  async fetchCalendarDurationRecords(year: number, studentId: number) {
    const res = await api.get(`/api/records/${year}/${studentId}`);
    return res; // 应返回 [ [日期字符串, 时长], ... ]
  },
  // 获取某学生某一天的学习记录详情，天数格式为 "YYYY-MM-DD"
  async fetchDailyRecords(date: string, studentId: number) {
    const res = await api.get(`/api/records/detail/${date}/${studentId}`);
    return res; // 应返回 LearningRecord 数组
  },
  // 添加学习记录
  async addLearningRecord(record: LearningRecord) {
    console.log("Adding learning record:", record);
    const res = await api.post(`/api/records/`, record);
    return res; // 应返回添加成功的记录
  },
  async getCompleteCount() {
    const res = await api.get(`/api/complete_count`);
    return res.complete_count; // 假设返回的数据格式为 { complete_count: number }
  },
};
