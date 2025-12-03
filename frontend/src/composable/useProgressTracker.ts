import { recordsAPI } from "../api";
import type { LearningRecord } from "../types";
import { useUserStore } from "../stores/user";

const userStore = useUserStore();

const isStudent = userStore.hasRole("student")

async function reportProgress(data: LearningRecord) {
  if (!isStudent) return;
  recordsAPI.addLearningRecord(data); 
}

// 分页资源（如 PPT）
export function trackPagingResource(resourceId: string, totalPages: number) {
  const pageTimes: number[] = Array(totalPages).fill(0);
  let currentPage = 0;
  const startTime = Date.now();
  let pageEnterTime = Date.now();
  let learned = false;

  function onPageChange(newPage: number) {
    const now = Date.now();
    pageTimes[currentPage]! += Math.floor((now - pageEnterTime) / 1000);
    currentPage = newPage;
    pageEnterTime = now;
    if (currentPage === totalPages - 1) {
      learned = true;
      // 到达最后一页
      const totalTime = Math.floor((Date.now() - startTime) / 1000);
      reportProgress({
        student_id: userStore.user.id,
        resource_id: resourceId,
        status: 1,
        total_time: totalTime,
        page_times: pageTimes,
      });

    }
  }

  function onPPTClosed() {
    if (learned) return;
    const totalTime = Math.floor((Date.now() - startTime) / 1000);
    reportProgress({
      student_id: userStore.user.id,
      resource_id: resourceId,
      status: 0,
      total_time: totalTime,
      page_times: pageTimes,
    });
  }

  return { onPageChange, onPPTClosed  };
}

// 视频资源追踪
export function trackVideoResource(resourceId: string, videoEl: HTMLVideoElement) {
  let startTime = 0;
  let learned = false;

  function onPlay() {
    if (startTime === 0) {
      startTime = Date.now();
    }
  }

  function onEnded() {
    if (startTime !== 0 && !learned) {
      learned = true;
      const totalTime = Math.floor((Date.now() - startTime) / 1000);
      reportProgress({
        student_id: userStore.user.id,
        resource_id: resourceId,
        status: 1,
        total_time: totalTime,
      });
    }
    startTime = 0;
  }

  function onClosed() {
    if (!learned && startTime !== 0) {
      const totalTime = Math.floor((Date.now() - startTime) / 1000);
      reportProgress({
        student_id: userStore.user.id,
        resource_id: resourceId,
        status: 0,
        total_time: totalTime,
      });
    }
  }

  videoEl.addEventListener("play", onPlay);
  videoEl.addEventListener("ended", onEnded);

  return () => {
    videoEl.removeEventListener("play", onPlay);
    videoEl.removeEventListener("ended", onEnded);
    onClosed();
  };
}

// 图片资源追踪（至少停留10秒算完成）
export function trackImageResource(resourceId: string) {
  const startTime = Date.now();
  let timer: number | null = null;
  let learned = false;

  function onClosed() {
    const totalTime = Math.floor((Date.now() - startTime) / 1000);
    if (totalTime >= 10 && !learned) {
      learned = true;
      reportProgress({
        student_id: userStore.user.id,
        resource_id: resourceId,
        status: 1,
        total_time: totalTime,
      });
    } else if (!learned) {
      reportProgress({
        student_id: userStore.user.id,
        resource_id: resourceId,
        status: 0,
        total_time: totalTime,
      });
    }
    if (timer) clearTimeout(timer);
  }

  // 自动完成（10秒后）
  timer = window.setTimeout(() => {
    learned = true;
    const totalTime = Math.floor((Date.now() - startTime) / 1000);
    reportProgress({
      student_id: userStore.user.id,
      resource_id: resourceId,
      status: 1,
      total_time: totalTime,
    });
  }, 10000);

  return onClosed;
}

// 文档资源追踪（滚动到底部算完成）
export function trackDocumentResource(resourceId: string, scrollEl: HTMLElement) {
  const startTime = Date.now();
  let learned = false;

  function onScroll(e: Event) {
    if (learned) return;
    const el = e.target as HTMLElement;
    if (el.scrollHeight - el.scrollTop - el.clientHeight < 2) {
      learned = true;
      const totalTime = Math.floor((Date.now() - startTime) / 1000);
      reportProgress({
        student_id: userStore.user.id,
        resource_id: resourceId,
        status: 1,
        total_time: totalTime,
      });
    }
  }

  function onClosed() {
    if (!learned) {
      const totalTime = Math.floor((Date.now() - startTime) / 1000);
      reportProgress({
        student_id: userStore.user.id,
        resource_id: resourceId,
        status: 0,
        total_time: totalTime,
      });
    }
    scrollEl.removeEventListener("scroll", onScroll);
  }

  scrollEl.addEventListener("scroll", onScroll);

  return onClosed;
}
