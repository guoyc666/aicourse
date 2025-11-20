// 定义进度数据类型
type ProgressData = {
  studentId: number;
  resourceId: string;
  status: number;
  totalTime: number;
  pageTimes?: number[];
};

// 模拟后端日志记录
function reportProgress(data: ProgressData) {
  // 实际开发中可用 axios.post('/api/progress', data)
  console.log("上报学习进度：", data);
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
    pageTimes[currentPage] += Math.floor((now - pageEnterTime) / 1000);
    currentPage = newPage;
    pageEnterTime = now;
    if (currentPage === totalPages - 1) {
      learned = true;
      // 到达最后一页
      const totalTime = Math.floor((Date.now() - startTime) / 1000);
      reportProgress({
        studentId: 1,
        resourceId,
        status: 1,
        totalTime,
        pageTimes,
      });
    }
  }

  function onPPTClosed() {
    if (learned) return;
    const totalTime = Math.floor((Date.now() - startTime) / 1000);
    reportProgress({
      studentId: 1,
      resourceId,
      status: 0,
      totalTime,
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
        studentId: 1,
        resourceId,
        status: 1,
        totalTime,
      });
    }
  }

  function onDocClosed() {
    if (learned) return;
    const totalTime = Math.floor((Date.now() - startTime) / 1000);
    reportProgress({
      studentId: 1,
      resourceId,
      status: 0,
      totalTime,
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

  function onPlay() {
    if (startTime === 0) {
      startTime = Date.now();
    }
  }
  
  function onEnded() {
    if (startTime !== 0) {
      totalTime = (Date.now() - startTime) / 1000;
      // 这里可以上报学习时长
      reportProgress({
        studentId: 1,
        resourceId,
        status: 1,
        totalTime: Math.floor(totalTime),
      });
    }
    startTime = 0;
  }

  videoEl.addEventListener("play", onPlay);
  videoEl.addEventListener("ended", onEnded);
  
  return () => {
    videoEl.removeEventListener("play", onPlay);
    videoEl.removeEventListener("ended", onEnded);
  };
}
