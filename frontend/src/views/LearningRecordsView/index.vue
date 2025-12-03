<template>
  <div class="records-layout">
    <el-row :gutter="24">
      <el-col :span="12">
        <el-card class="records-card" header="掌握度列表">
          <el-table :data="masteryPageData" style="width: 100%">
            <el-table-column
              v-if="!isStudent"
              prop="student_id"
              label="学生ID"
              width="120"
              :filters="studentIdFilters"
              :filter-method="filterStudentId"
            />
            <el-table-column
              v-if="!isStudent"
              prop="student_name"
              label="学生姓名"
              width="120"
              :filters="studentNameFilters"
              :filter-method="filterStudentName"
            />
            <el-table-column
              prop="knowledge_id"
              label="知识点ID"
              width="180"
              :filters="knowledgeIdFilters"
              :filter-method="filterKnowledgeId"
            />
            <el-table-column
              prop="knowledge_name"
              label="知识点名称"
              width="180"
              :filters="knowledgeNameFilters"
              :filter-method="filterKnowledgeName"
            />
            <el-table-column fixed="right"prop="mastery" label="掌握度" width="120" sortable>
              <template #default="scope">
                {{ (scope.row.mastery * 100).toFixed(2) }}%
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            v-model:current-page="masteryPage"
            v-model:page-size="masteryPageSize"
            :total="masteryData.length"
            layout="prev, pager, next"
            style="margin-top: 10px"
          />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="records-card" header="进度列表">
          <el-table :data="progressPageData" style="width: 100%">
            <el-table-column
              v-if="!isStudent"
              prop="student_id"
              label="学生ID"
              width="120"
              :filters="studentIdFilters"
              :filter-method="filterStudentId"
            />
            <el-table-column
              v-if="!isStudent"
              prop="student_name"
              label="学生姓名"
              width="120"
              :filters="studentNameFilters"
              :filter-method="filterStudentName"
            />
            <el-table-column
              prop="knowledge_id"
              label="知识点ID"
              width="180"
              :filters="knowledgeIdFilters"
              :filter-method="filterKnowledgeId"
            />
            <el-table-column
              prop="knowledge_name"
              label="知识点名称"
              width="180"
              :filters="knowledgeNameFilters"
              :filter-method="filterKnowledgeName"
            />
            <el-table-column fixed="right" prop="progress" label="进度" width="120" sortable>
              <template #default="scope">
                {{ (scope.row.progress * 100).toFixed(2) }}%
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            v-model:current-page="progressPage"
            v-model:page-size="progressPageSize"
            :total="progressData.length"
            layout="prev, pager, next"
            style="margin-top: 10px"
          />
        </el-card>
      </el-col>
    </el-row>
    <el-card class="records-card" header="学习记录">
      <CalendarHeatmap />
      <DetailRecords />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import CalendarHeatmap from './CalendarHeatmap.vue';
import DetailRecords from './DetailRecords.vue';
import { graphAPI } from '../../api';
import { progressAPI } from "../../api/progress";
import { masteryAPI } from "../../api/mastery";
import { useUserStore } from "../../stores/user";

const userStore = useUserStore();
const isStudent = userStore.hasRole("student");

interface ProgressRecord {
  knowledge_id: string;
  knowledge_name: string;
  student_id: string;
  student_name: string;
  progress: number;
}
interface MasteryRecord {
  knowledge_id: string;
  knowledge_name: string;
  student_id: string;
  student_name: string;
  mastery: number;
}
const masteryData = ref<MasteryRecord[]>([]);
const progressData = ref<ProgressRecord[]>([]);

// 分页相关
const masteryPage = ref(1);
const masteryPageSize = ref(10);
const progressPage = ref(1);
const progressPageSize = ref(10);

const masteryPageData = computed(() => {
  const start = (masteryPage.value - 1) * masteryPageSize.value;
  return masteryData.value.slice(start, start + masteryPageSize.value);
});
const progressPageData = computed(() => {
  const start = (progressPage.value - 1) * progressPageSize.value;
  return progressData.value.slice(start, start + progressPageSize.value);
});

// 筛选相关
const knowledgeIdFilters = computed(() => {
  const ids = new Set([
    ...masteryData.value.map(r => (r as any).knowledge_id),
    ...progressData.value.map(r => (r as any).knowledge_id)
  ]);
  return Array.from(ids).map(id => ({ text: id + '', value: id }));
});
const knowledgeNameFilters = computed(() => {
  const names = new Set([
    ...masteryData.value.map(r => (r as any).knowledge_name),
    ...progressData.value.map(r => (r as any).knowledge_name)
  ]);
  return Array.from(names).map(name => ({ text: name, value: name }));
});
function filterKnowledgeId(value: any, row: any) {
  return row.knowledge_id === value;
}
function filterKnowledgeName(value: any, row: any) {
  return row.knowledge_name === value;
}

const studentIdFilters = computed(() => {
  const ids = new Set([
    ...masteryData.value.map(r => (r as any).student_id),
    ...progressData.value.map(r => (r as any).student_id)
  ]);
  return Array.from(ids).map(id => ({ text: id + '', value: id }));
});
const studentNameFilters = computed(() => {
  const names = new Set([
    ...masteryData.value.map(r => (r as any).student_name),
    ...progressData.value.map(r => (r as any).student_name)
  ]);
  return Array.from(names).map(name => ({ text: name, value: name }));
});
function filterStudentId(value: any, row: any) {
  return row.student_id === value;
}
function filterStudentName(value: any, row: any) {
  return row.student_name === value;
}

onMounted(async () => {
  const knowledgeNodes = await graphAPI.fetchAllKnowledgeNodes();
  const knowledgeMap = Object.fromEntries(
    knowledgeNodes.map((k: any) => [k.id, k.name])
  );
  if (isStudent) {
    masteryData.value = await masteryAPI.fetchAllMastery();
    progressData.value = await progressAPI.fetchAllProgress();
  } else {
    masteryData.value = await masteryAPI.fetchAllMasteryList();
    progressData.value = await progressAPI.fetchAllProgressList();
  }
  masteryData.value = masteryData.value.map((item: any) => ({
    ...item,
    knowledge_name: knowledgeMap[item.knowledge_id] || item.knowledge_id
  }));
  progressData.value = progressData.value.map((item: any) => ({
    ...item,
    knowledge_name: knowledgeMap[item.knowledge_id] || item.knowledge_id
  }));
});
</script>

<style scoped>
.records-layout {
  padding: 20px;
}
.records-card {
  margin-bottom: 20px;
}
</style>