import { recordsAPI } from "../api";
import type { LearningRecord } from "../types";
import { useUserStore } from "../stores/user";

const userStore = useUserStore();

async function reportProgress(data: LearningRecord) {
  recordsAPI.addLearningRecord(data); 
}

// 1. 分页资源（如 PPT）
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

// 2. 滚动资源（如文档、长网页）
export function trackScrollResource(resourceId: string) {
  const startTime = Date.now();
  let learned = false;

  function onScroll(e: Event) {
    if (learned) return;
    const el = e.target as HTMLElement;
    if (el.scrollHeight - el.scrollTop - el.clientHeight < 2) {
      // 滚动到底
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

  function onDocClosed() {
    if (learned) return;
    const totalTime = Math.floor((Date.now() - startTime) / 1000);
    reportProgress({
      student_id: userStore.user.id,
      resource_id: resourceId,
      status: 0,
      total_time: totalTime,
    });
  }

  return { onScroll, onDocClosed };
}

// 3. 视频资源
export function trackVideoResource(
  resourceId: string,
  videoEl: HTMLVideoElement
) {
  let startTime = 0;
  let totalTime = 0;
  let learned = false;

  function onPlay() {
    if (startTime === 0) {
      startTime = Date.now();
    }
  }
  
  function onEnded() {
    if (startTime !== 0) {
      learned = true;
      totalTime = (Date.now() - startTime) / 1000;
      // 这里可以上报学习时长
      reportProgress({
        student_id: userStore.user.id,
        resource_id: resourceId,
        status: 1,
        total_time: Math.floor(totalTime),
      });
    }
    startTime = 0;
  }

  function onClosed() {
    if (learned) return;
    if (startTime !== 0) {
      totalTime += (Date.now() - startTime) / 1000;
      // 这里可以上报学习时长
      reportProgress({
        student_id: userStore.user.id,
        resource_id: resourceId,
        status: 0,
        total_time: Math.floor(totalTime),
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
