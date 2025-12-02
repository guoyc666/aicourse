<template>
  <el-dialog
    v-model="showCourseDialog"
    title="创建课程"
    align-center
    width="400px"
    :close-on-click-modal="false"
    :show-close="false"
  >
    <el-form :model="courseForm">
      <el-form-item label="课程名称" required>
        <el-input v-model="courseForm.name" placeholder="请输入课程名称" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input
          v-model="courseForm.description"
          type="textarea"
          placeholder="可选"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button type="primary" @click="submitCourseForm">创建</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { KnowledgeNode } from '../../types';
import { graphAPI } from '../../api';
import { ElMessage } from 'element-plus';
// 创建课程弹窗相关
const showCourseDialog = ref(false);
const courseForm = ref({
  name: "",
  description: "",
});

// 提交创建课程表单
async function submitCourseForm() {
  try {
    // 创建课程节点
    const courseNode: KnowledgeNode = {
      id: "node_" + Date.now(),
      category: "Course",
      name: courseForm.value.name,
      description: courseForm.value.description,
      depth: 0,
    };
    await graphAPI.createNode(courseNode);
    showCourseDialog.value = false;
    ElMessage.success("课程创建成功！");
  } catch (e) {
    ElMessage.error("课程创建失败，请重试！");
  }
}
</script>

<style scoped>
</style>