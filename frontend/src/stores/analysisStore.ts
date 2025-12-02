import { defineStore } from "pinia";
import { progressAPI } from "../api";
import { masteryAPI } from "../api";
import { recordsAPI } from "../api";
import type { DailyEvent } from "../types";

// 定义 Store 的类型
interface AnalysisState {

  masteryRecords: Record<string, number>; // knowledgeId -> mastery
  progressRecords: Record<string, number>; // knowledgeId -> progress

  calendarDurationRecords: [string, number][]; // [日期, 时长]
  selectedDay: string | null;
  selectedDayRecords: DailyEvent[]; // 存储所选日期的学习记录详情

  loading: boolean;
  error: string | null;
}

export const useAnalysisStore = defineStore("Analysis", {
  state: (): AnalysisState => ({
    masteryRecords: {},
    progressRecords: {},

    calendarDurationRecords: [],
    selectedDay: null,
    selectedDayRecords: [],

    loading: false,
    error: null,
  }),
  actions: {
    async fetchStudentRecords() {
      this.loading = true;
      this.error = null;
      try {
        const mastery_response = await masteryAPI.fetchAllMastery();
        const progress_response = await progressAPI.fetchAllProgress();
        this.masteryRecords = {};
        this.progressRecords = {};
        mastery_response.forEach((record: any) => {
          this.masteryRecords[record.knowledge_id] = record.mastery;
        });
        progress_response.forEach((record: any) => {
          this.progressRecords[record.knowledge_id] = record.progress;
        });
      } catch (err: any) {
        this.error = err.message || "获取掌握度失败";
      } finally {
        this.loading = false;
      }
    },
    
    async fetchAverageRecords() {
      this.loading = true;
      this.error = null;
      try {
        const mastery_response = await masteryAPI.fetchAllAverageMastery();
        const progress_response = await progressAPI.fetchAllAverageProgress();
        this.masteryRecords = {};
        this.progressRecords = {};
        mastery_response.forEach((record: any) => {
          this.masteryRecords[record.knowledge_id] = record.average_mastery;
        });
        progress_response.forEach((record: any) => {
          this.progressRecords[record.knowledge_id] = record.average_progress;
        });
      } catch (err: any) {
        this.error = err.message || "获取平均掌握度失败";
      } finally {
        this.loading = false;
      }
    },

    async fetchCalendarDurations(year: number, studentId: number) {
      this.loading = true;
      this.error = null;
      try {
        const response = await recordsAPI.fetchCalendarDurationRecords(year, studentId);
        this.calendarDurationRecords = response;
      } catch (err: any) {
        this.error = err.message || "获取日历学习时长失败";
      } finally {
        this.loading = false;
      }
    },
    setSelectedDay(day: string | null) {
      // 检查格式是否为 "YYYY-MM-DD"
      if (day && !/^\d{4}-\d{2}-\d{2}$/.test(day)) {
        this.error = "日期格式错误，应为 YYYY-MM-DD";
        return;
      }
      this.selectedDay = day;
    },
    async fetchSelectedDayRecords(studentId: number) {
      if (!this.selectedDay) return;
      this.loading = true;
      this.error = null;
      try {
        const response = await recordsAPI.fetchDailyRecords(this.selectedDay, studentId);
        this.selectedDayRecords = response;
      } catch (err: any) {
        this.error = err.message || "获取所选日期学习记录失败";
      } finally {
        this.loading = false;
      }
    },
  },
  getters: {
    getMasteryByKnowledgeId: (state) => {
      return (knowledgeId: string) => state.masteryRecords[knowledgeId] || 0.0;
    },
    getProgressByKnowledgeId: (state) => {
      return (knowledgeId: string) => state.progressRecords[knowledgeId] || 0.0;
    },
  },
});