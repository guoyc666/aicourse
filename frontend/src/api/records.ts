import api from "./request";
import type { LearningRecord } from "../types";

export const recordsAPI = {
  // 获取所有学生的学习记录（按日期汇总的学习时长）
  async fetchAllStudentsCalendarDurationRecords(year: number) {
    const res = await api.get(`/records/${year}`);
    return res.data; // 应返回 { student_id: 学生唯一标志, records: [ [日期字符串, 时长], ... ] }[]
  },
  // 获取某学生的学习记录（按日期汇总的学习时长）
  async fetchCalendarDurationRecords(year: number, studentId: number) {
    const res = await api.get(`/records/${year}/${studentId}`);
    return res.data; // 应返回 [ [日期字符串, 时长], ... ]
  },
  // 获取所有学生某一天的学习记录详情，天数格式为 "YYYY-MM-DD"
  async fetchAllStudentsDailyRecords(date: string) {
    const res = await api.get(`/records/detail/${date}`);
    return res.data; // 应返回 { student_id: 学生唯一标志, records: LearningRecord[] }[]
  },
  // 获取某学生某一天的学习记录详情，天数格式为 "YYYY-MM-DD"
  async fetchDailyRecords(date: string, studentId: number) {
    const res = await api.get(`/records/detail/${date}/${studentId}`);
    return res.data; // 应返回 LearningRecord 数组
  },
  // 添加学习记录
  async addLearningRecord(record: LearningRecord) {
    const res = await api.post(`/records/`, record);
    return res.data; // 应返回添加成功的记录
  },
  // 批量添加学习记录
  async addLearningRecords(records: LearningRecord[]) {
    const res = await api.post(`/records/batch`, records);
    return res.data; // 应返回添加成功的记录数组
  },
  // 删除所有学生的某一年学习记录
  async deleteAllStudentsYearlyRecords(year: number) {
    const res = await api.delete(`/records/${year}`);
    return res.data; // 应返回删除结果
  },
  // 删除某学生某年的所有学习记录
  async deleteYearlyRecords(year: number, studentId: number) {
    const res = await api.delete(`/records/${year}/${studentId}`);
    return res.data; // 应返回删除结果
  },
  // 删除所有学生某一天的学习记录，天数格式为 "YYYY-MM-DD"
  async deleteAllStudentsDailyRecords(date: string) {
    const res = await api.delete(`/records/detail/${date}`);
    return res.data; // 应返回删除结果
  },
  // 删除某学生某一天的所有学习记录，天数格式为 "YYYY-MM-DD"
  async deleteDailyRecords(date: string, studentId: number) {
    const res = await api.delete(`/records/detail/${date}/${studentId}`);
    return res.data; // 应返回删除结果
  },
};
