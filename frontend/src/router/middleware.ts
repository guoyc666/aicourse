import { useGraphStore } from "../stores/graphStore";
import { useAnalysisStore } from "../stores/analysisStore";
import type { Router } from "vue-router";

export function setupGraphMiddleware(router: Router) {
  router.beforeEach(async (to, from) => {
    const graphStore = useGraphStore();
    // 如果目标路由是知识图谱视图，确保图数据已加载
    if (to.name === "graph") {
      await graphStore.fetchGraph();
      if (graphStore.error) {
        return { name: "home" };
      }
    }
  });
}

export function setupAnalysisMiddleware(router: Router) {
  router.beforeEach(async (to, from) => {
    const analysisStore = useAnalysisStore();
    const studentId = 1;
    // 如果目标路由是学习分析视图，确保学习数据已加载
    if (to.name === "records" || to.name === "graph") {
      await analysisStore.fetchAllMastery(studentId);
      await analysisStore.fetchAllProgress(studentId);
      const currentYear = new Date().getFullYear();
      await analysisStore.fetchCalendarDurations(currentYear, studentId);
      if (analysisStore.error) {
        return { name: "home" };
      }
    }
  });
}