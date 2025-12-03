<template>
  <div class="detail-panel">
    <h2 class="detail-title">{{ graphStore.nodeDetail?.name }}</h2>
    <el-tabs v-model="detailTab" stretch class="detail-tabs">
      <el-tab-pane label="概览" name="overview">
        <!-- 知识点解释 -->
        <section class="detail-section">
          <div class="section-title">知识点解释</div>
          <div class="section-content">
            <span>
              {{ showFullDesc ? graphStore.nodeDetail?.description : (graphStore.nodeDetail?.description?.slice(0, 60) + '...') }}
            </span>
            <span
              v-if="graphStore.nodeDetail?.description && graphStore.nodeDetail?.description.length > 60"
              class="expand-link"
              @click="showFullDesc = !showFullDesc"
            >
              {{ showFullDesc ? '收起' : '展开' }}
            </span>
          </div>
        </section>
        <!-- 学情概览 -->
        <section class="detail-section">
          <div class="section-title">学情概览 <span class="update-tip">数据次日更新</span></div>
          <div v-if="isStudent">
            <div class="overview-row">
              <div class="overview-item">
                <div class="overview-label">学习完成度</div>
                <div class="overview-value">{{ progressPercent}}%</div>
              </div>
              <div class="overview-item">
                <div class="overview-label">知识点掌握度</div>
                <div class="overview-value">{{ masteryPercent }}%</div>
              </div>
              <div class="overview-item">
                <div class="overview-label">学习时长</div>
                <div class="overview-value">{{ graphStore.nodeDetail?.total_time }}分钟</div>
              </div>
            </div>
          </div>
          <div v-else>
            <!-- 老师/管理员视角：展示平均和每个学生 -->
            <div class="overview-row">
              <div class="overview-item">
                <div class="overview-label">平均完成度</div>
                <div class="overview-value">{{ progressPercent }}%</div>
              </div>
              <div class="overview-item">
                <div class="overview-label">平均掌握度</div>
                <div class="overview-value">{{ masteryPercent }}%</div>
              </div>
              <div class="overview-item">
                <div class="overview-label">平均学习时长</div>
                <div class="overview-value">{{ graphStore.nodeDetail?.average_time }}分钟</div>
              </div>
            </div>
          </div>
        </section>
        <!-- 知识点关系 -->
        <section class="detail-section">
          <div class="section-title">知识点关系</div>
          <div class="relation-row">
            <div class="relation-label">前置知识点</div>
            <div class="relation-tags">
              <el-tag
                v-for="pre in graphStore.nodeDetail?.prerequisites"
                :key="pre.id"
                type="success"
                size="small"
                style="margin-right: 4px;"
              >
                {{ pre.name }}
              </el-tag>
            </div>
          </div>
          <div class="relation-row">
            <div class="relation-label">后续知识点</div>
            <div class="relation-tags">
              <el-tag
                v-for="suc in graphStore.nodeDetail?.successors"
                :key="suc.id"
                type="info"
                size="small"
                style="margin-right: 4px;"
              >
                {{ suc.name }}
              </el-tag>
            </div>
          </div>
        </section>
      </el-tab-pane>
      <el-tab-pane label="关联资源" name="resource">
        <section class="detail-section">
          <div class="section-title">本课资源</div>
          <div v-if="graphStore.nodeDetail?.resources && graphStore.nodeDetail?.resources.length">
            <div
              v-for="res in graphStore.nodeDetail?.resources"
              :key="res.id"
              class="resource-item"
              style="cursor:pointer;"
              @click="handlePreviewResource(res)"
            >
              <div class="resource-type">{{ res.type }}</div>
              <div class="resource-name">{{ res.name }}</div>
              <div class="resource-desc" v-if="res.is_child">来自子节点</div>
            </div>
          </div>
          <div v-else class="empty-tip">暂无资源</div>

          <el-dialog
            v-model="previewVisible"
            :title="previewTitle"
            width="60%"
            @close="handleDialogClose"
          >
            <template v-if="previewType === 'video'">
              <video :src="previewUrl" controls style="width:100%;max-height:500px;" />
            </template>
            <template v-else-if="previewType === 'image'">
              <img :src="previewUrl" style="max-width:100%;max-height:500px;" />
            </template>
            <template v-else-if="previewType === 'pdf'">
              <iframe :src="previewUrl" width="100%" height="500px" />
            </template>
            <template v-else-if="previewType === 'txt' || previewType === 'text'">
              <div style="white-space: pre-wrap; max-height:500px; overflow:auto;">
                {{ previewContent }}
              </div>
            </template>
            <template v-else>
              <a :href="previewUrl" target="_blank">下载/预览资源</a>
            </template>
          </el-dialog>
        </section>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, ref } from "vue";
import { useGraphStore } from "../../stores/graphStore";
import { useAnalysisStore } from "../../stores/analysisStore";
import { useUserStore } from "../../stores/user";
import type { NodeDetail } from "../../types";
import {
  trackVideoResource,
  trackImageResource,
  trackDocumentResource,
  trackPagingResource
} from "../../composable/useProgressTracker";

const userStore = useUserStore();

const isStudent = userStore.hasRole("student")
const showFullDesc = ref(false);

const detailTab = ref('overview');
const graphStore = useGraphStore();
const analysisStore = useAnalysisStore();

const masteryPercent = computed(() => {
  const mastery = analysisStore.getMasteryByKnowledgeId(graphStore.selectedNodeID!);
  return +(mastery * 100).toFixed(2);
});

const progressPercent = computed(() => {
  const progress = analysisStore.getProgressByKnowledgeId(graphStore.selectedNodeID!);
  return +(progress * 100).toFixed(2);
});

const previewVisible = ref(false);
const previewType = ref("");
const previewTitle = ref("");
const previewUrl = ref("");
const previewContent = ref("");

// 追踪器清理函数
let cleanupTracker: (() => void) | null = null;

function handlePreviewResource(res: NodeDetail["resources"][number]) {
  previewType.value = res.type.toLowerCase();
  previewTitle.value = res.name;
  previewUrl.value = res.download_url;
  previewVisible.value = true;
  previewContent.value = "";

  // 清理上一次追踪
  if (cleanupTracker) {
    cleanupTracker();
    cleanupTracker = null;
  }

  // 视频
  if (previewType.value === "video") {
    nextTick(() => {
      const videoEl = document.querySelector(".el-dialog video") as HTMLVideoElement;
      if (videoEl) {
        cleanupTracker = trackVideoResource(res.id, videoEl);
      }
    });
  }
  // 图片
  else if (previewType.value === "image") {
    cleanupTracker = trackImageResource(res.id);
  }
  // 文档（pdf、txt、text、doc、docx等）
  else if (["pdf", "txt", "text", "doc", "docx"].includes(previewType.value)) {
    if (["txt", "text"].includes(previewType.value)) {
      // 文本内容异步加载
      fetch(previewUrl.value)
        .then(resp => resp.text())
        .then(text => {
          previewContent.value = text;
        })
        .catch(() => {
          previewContent.value = "内容加载失败";
        });
    }
    nextTick(() => {
      // pdf、doc等用iframe，txt用div，但都可以监听el-dialog内容区的滚动
      let scrollEl: HTMLElement | null = null;
      if (previewType.value === "pdf" || previewType.value === "doc" || previewType.value === "docx") {
        const iframe = document.querySelector(".el-dialog iframe") as HTMLIFrameElement;
        if (iframe && iframe.contentDocument) {
          scrollEl = iframe.contentDocument.scrollingElement as HTMLElement;
        }
      } else {
        // txt/text用el-dialog内容区
        scrollEl = document.querySelector(".el-dialog__body div[style*='pre-wrap']") as HTMLElement;
      }
      if (scrollEl) {
        cleanupTracker = trackDocumentResource(res.id, scrollEl);
      }
    });
  }
  // PPT（分页资源，举例，需你根据实际情况传 totalPages）
  else if (previewType.value === "ppt") {
    // 假设你能获取总页数 totalPages
    const totalPages = 10; // 示例
    const tracker = trackPagingResource(res.id, totalPages);
    // 你需要在分页切换时调用 tracker.onPageChange(newPage)
    // 关闭弹窗时调用 tracker.onPPTClosed()
    cleanupTracker = tracker.onPPTClosed;
  }
}

function handleDialogClose() {
  previewVisible.value = false;
  previewType.value = "";
  previewTitle.value = "";
  previewUrl.value = "";
  previewContent.value = "";
  if (cleanupTracker) {
    cleanupTracker();
    cleanupTracker = null;
  }
}

</script>

<style scoped>
.detail-panel {
  position: absolute;
  right: 0;
  top: 0;
  height: 100%;
  width: 30%;
  background: #f7f7f7;
  padding: 24px;
  box-sizing: border-box;
  overflow-y: auto;
  z-index: 20;
  font-family: "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
}
.detail-title {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 18px;
  color: #222;
}
.detail-tabs {
  margin-bottom: 12px;
}
.detail-section {
  margin-bottom: 24px;
}
.section-title {
  font-size: 16px;
  font-weight: 500;
  color: #1abc9c;
  margin-bottom: 8px;
}
.section-content {
  font-size: 14px;
  color: #444;
  line-height: 1.7;
}
.expand-link {
  color: #409eff;
  cursor: pointer;
  margin-left: 8px;
  font-size: 13px;
}
.update-tip {
  font-size: 12px;
  color: #aaa;
  margin-left: 8px;
}
.overview-row {
  display: flex;
  gap: 16px;
  margin-top: 8px;
}
.overview-item {
  background: #f8f8f8;
  border-radius: 8px;
  padding: 12px 16px;
  flex: 1;
  text-align: center;
}
.overview-label {
  font-size: 13px;
  color: #888;
  margin-bottom: 4px;
}
.overview-value {
  font-size: 18px;
  font-weight: bold;
  color: #222;
}
.relation-row {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}
.relation-label {
  font-size: 13px;
  color: #666;
  width: 90px;
}
.relation-tags {
  flex: 1;
}
.resource-item {
  background: #f8f8f8;
  border-radius: 8px;
  padding: 10px 14px;
  margin-bottom: 8px;
}
.resource-type {
  font-size: 13px;
  color: #1abc9c;
  margin-bottom: 2px;
}
.resource-name {
  font-size: 15px;
  font-weight: 500;
  color: #222;
}
.resource-desc {
  font-size: 13px;
  color: #888;
}
.empty-tip {
  color: #aaa;
  font-size: 14px;
  margin-top: 12px;
}
</style>
