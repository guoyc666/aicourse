<template>
  <div class="student-tasks-container">
    <div class="header">
      <h2>我的任务</h2>
    </div>
    
    <el-table v-loading="loading" :data="assignedTasks" style="width: 100%">
      <el-table-column prop="task.id" label="ID" width="80" />
      <el-table-column prop="task.title" label="任务标题" min-width="200">
        <template #default="scope">
          <el-link @click="showTaskDetail(scope.row)">{{ scope.row.task.title }}</el-link>
        </template>
      </el-table-column>
      <el-table-column prop="task.description" label="任务描述" min-width="300" show-overflow-tooltip />
      <el-table-column prop="task.due_date" label="截止日期" width="180">
        <template #default="scope">
          <span :class="{ 'due-warning': isDueSoon(scope.row.task.due_date) }">
            {{ formatDate(scope.row.task.due_date) }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="分配时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column prop="is_completed" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.is_completed ? 'success' : 'info'">
            {{ scope.row.is_completed ? '已完成' : '未完成' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="scope">
          <el-button 
            v-if="!scope.row.is_completed"
            type="primary" 
            link 
            size="small" 
            @click="confirmTaskCompletion(scope.row)"
          >
            确认完成
          </el-button>
          <span v-else class="completed">已确认</span>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 任务详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="selectedTask?.task?.title + ' - 详情'" width="600px">
      <div v-if="selectedTask" class="task-detail">
        <div class="detail-item">
          <span class="detail-label">ID：</span>
          <span class="detail-value">{{ selectedTask.task.id }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">标题：</span>
          <span class="detail-value">{{ selectedTask.task.title }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">描述：</span>
          <span class="detail-value">{{ selectedTask.task.description }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">分配时间：</span>
          <span class="detail-value">{{ formatDate(selectedTask.created_at) }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">截止日期：</span>
          <span class="detail-value">
            <span :class="{ 'due-warning': isDueSoon(selectedTask.task.due_date) }">
              {{ formatDate(selectedTask.task.due_date) }}
            </span>
          </span>
        </div>
        <div class="detail-item">
          <span class="detail-label">状态：</span>
          <span class="detail-value">
            <el-tag :type="selectedTask.is_completed ? 'success' : 'info'">
              {{ selectedTask.is_completed ? '已完成' : '未完成' }}
            </el-tag>
          </span>
        </div>
        <div v-if="!selectedTask.is_completed" class="detail-item">
          <el-button type="primary" @click="confirmTaskCompletion(selectedTask)">确认完成任务</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAssignedTasks, confirmTaskCompleted } from '@/api/tasks'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 状态管理
const loading = ref(false)
const assignedTasks = ref([])

// 对话框状态
const detailDialogVisible = ref(false)
const selectedTask = ref(null)

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 检查任务是否即将到期（24小时内）
const isDueSoon = (dueDateString) => {
  if (!dueDateString) return false
  const now = new Date()
  const dueDate = new Date(dueDateString)
  const diffHours = (dueDate - now) / (1000 * 60 * 60)
  return diffHours > 0 && diffHours <= 24
}

// 加载分配的任务列表
const loadAssignedTasks = async () => {
  loading.value = true
  try {
    const response = await getAssignedTasks()
    assignedTasks.value = response.data || response
  } catch (error) {
    ElMessage.error('获取任务列表失败')
    console.error('获取任务列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 显示任务详情
const showTaskDetail = (task) => {
  selectedTask.value = task
  detailDialogVisible.value = true
}

// 确认任务完成
const confirmTaskCompletion = async (task) => {
  try {
    await ElMessageBox.confirm(
      '确认完成此任务？完成后将无法撤销。',
      '确认完成',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 调用后端API确认任务完成
    await confirmTaskCompleted(task.id)
    
    ElMessage.success('任务确认完成成功')
    loadAssignedTasks() // 重新加载任务列表
    
    if (task.id === selectedTask.value?.id) {
      // 如果当前打开的详情是已确认的任务，更新状态
      selectedTask.value.is_completed = true
    }
  } catch (error) {
    if (error === 'cancel') {
      return
    }
    ElMessage.error('任务确认完成失败')
    console.error('确认任务完成失败:', error)
  }
}

// 初始化数据
onMounted(() => {
  loadAssignedTasks()
})
</script>

<style scoped>
.student-tasks-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.task-detail {
  padding: 20px 0;
}

.detail-item {
  margin-bottom: 16px;
}

.detail-label {
  display: inline-block;
  width: 100px;
  color: #606266;
}

.detail-value {
  font-weight: 500;
}

.due-warning {
  color: #f56c6c;
  font-weight: bold;
}

.completed {
  color: #67c23a;
  font-size: 12px;
}
</style>