<template>
  <div class="teacher-tasks-container">
    <div class="header">
      <h2>任务管理</h2>
      <el-button type="primary" @click="showCreateDialog">创建任务</el-button>
    </div>
    
    <el-table v-loading="loading" :data="tasks" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="任务标题" min-width="200">
        <template #default="scope">
          <el-link @click="showTaskDetail(scope.row)">{{ scope.row.title }}</el-link>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="任务描述" min-width="300" show-overflow-tooltip />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column prop="due_date" label="截止日期" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.due_date) }}
        </template>
      </el-table-column>
      <el-table-column prop="assigned_count" label="已分配" width="80" />
      <el-table-column prop="completed_count" label="已完成" width="80" />
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="scope">
          <el-button type="primary" link size="small" @click="showEditDialog(scope.row)">
            编辑
          </el-button>
          <el-button type="danger" link size="small" @click="handleDelete(scope.row.id, scope.row.title)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 创建任务对话框 -->
    <el-dialog v-model="createDialogVisible" title="创建任务" width="600px">
      <el-form ref="createFormRef" :model="createForm" :rules="createRules" label-width="100px">
        <el-form-item label="任务标题" prop="title">
          <el-input v-model="createForm.title" placeholder="请输入任务标题" />
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input v-model="createForm.description" type="textarea" placeholder="请输入任务描述" :rows="4" />
        </el-form-item>
        <el-form-item label="截止日期" prop="due_date">
          <el-date-picker
            v-model="createForm.due_date"
            type="datetime"
            placeholder="选择截止日期"
            style="width: 100%"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DDTHH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="分配学生" prop="student_ids">
          <el-select
            v-model="createForm.student_ids"
            multiple
            placeholder="请选择要分配的学生"
            collapse-tags
            style="width: 100%"
          >
            <el-option v-for="student in students" :key="student.id" :label="student.full_name || student.username" :value="student.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleCreateTask">创建</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 编辑任务对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑任务" width="600px">
      <el-form ref="editFormRef" :model="editForm" :rules="editRules" label-width="100px">
        <el-form-item label="任务标题" prop="title">
          <el-input v-model="editForm.title" placeholder="请输入任务标题" />
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input v-model="editForm.description" type="textarea" placeholder="请输入任务描述" :rows="4" />
        </el-form-item>
        <el-form-item label="截止日期" prop="due_date">
          <el-date-picker
            v-model="editForm.due_date"
            type="datetime"
            placeholder="选择截止日期"
            style="width: 100%"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DDTHH:mm:ss"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleUpdateTask">保存</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 任务详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="currentTask?.title + ' - 详情'" width="600px">
      <div v-if="currentTask" class="task-detail">
        <div class="detail-item">
          <span class="detail-label">ID：</span>
          <span class="detail-value">{{ currentTask.id }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">标题：</span>
          <span class="detail-value">{{ currentTask.title }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">描述：</span>
          <span class="detail-value">{{ currentTask.description }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">创建时间：</span>
          <span class="detail-value">{{ formatDate(currentTask.created_at) }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">截止日期：</span>
          <span class="detail-value">{{ formatDate(currentTask.due_date) }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">已分配学生：</span>
          <span class="detail-value">{{ currentTask.assigned_count }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">已完成学生：</span>
          <span class="detail-value">{{ currentTask.completed_count }}</span>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getTasks, createTask, updateTask, deleteTask, getTask } from '@/api/tasks'
import { getUsers } from '@/api/users'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 状态管理
const loading = ref(false)
const tasks = ref([])
const students = ref([])

// 对话框状态
const createDialogVisible = ref(false)
const editDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const currentTask = ref(null)
const currentTaskId = ref(null)

// 创建任务表单
const createForm = reactive({
  title: '',
  description: '',
  due_date: '',
  student_ids: []
})

// 编辑任务表单
const editForm = reactive({
  title: '',
  description: '',
  due_date: ''
})

// 表单验证规则
const createRules = {
  title: [
    { required: true, message: '请输入任务标题', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入任务描述', trigger: 'blur' }
  ],
  due_date: [
    { required: true, message: '请选择截止日期', trigger: 'change' }
  ],
  student_ids: [
    { required: true, message: '请至少选择一个学生', trigger: 'change' }
  ]
}

const editRules = {
  title: [
    { required: true, message: '请输入任务标题', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入任务描述', trigger: 'blur' }
  ],
  due_date: [
    { required: true, message: '请选择截止日期', trigger: 'change' }
  ]
}

const createFormRef = ref(null)
const editFormRef = ref(null)

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 加载任务列表
const loadTasks = async () => {
  loading.value = true
  try {
    const response = await getTasks()
    // 确保tasks.value始终是一个数组
    tasks.value = Array.isArray(response) ? response : []
  } catch (error) {
    ElMessage.error('获取任务列表失败')
    console.error('获取任务列表失败:', error)
    tasks.value = [] // 出错时设置为空数组
  } finally {
    loading.value = false
  }
}

// 加载学生列表
const loadStudents = async () => {
  try {
    const response = await getUsers()
    // 只获取学生角色的用户
    students.value = (response.data || response).filter(user => 
      user.roles.some(role => role.name === 'student')
    )
  } catch (error) {
    console.error('获取学生列表失败:', error)
  }
}

// 处理创建任务
const handleCreateTask = async () => {
  console.log('开始处理创建任务')
  try {
    console.log('验证表单数据')
    await createFormRef.value.validate()
    
    console.log('发送创建任务请求:', createForm)
    await createTask(createForm)
    ElMessage.success('任务创建成功')
    createDialogVisible.value = false
    loadTasks() // 重新加载任务列表
    
    // 重置表单
    createForm.title = ''
    createForm.description = ''
    createForm.due_date = ''
    createForm.student_ids = []
  } catch (error) {
    console.error('创建任务时出错:', error)
    if (error.name === 'ValidationError') {
      return
    }
    ElMessage.error('任务创建失败')
    console.error('创建任务失败:', error)
  }
}

// 处理更新任务
const handleUpdateTask = async () => {
  try {
    await editFormRef.value.validate()
    
    await updateTask(currentTaskId.value, editForm)
    ElMessage.success('任务更新成功')
    editDialogVisible.value = false
    loadTasks() // 重新加载任务列表
  } catch (error) {
    if (error.name === 'ValidationError') {
      return
    }
    ElMessage.error('任务更新失败')
    console.error('更新任务失败:', error)
  }
}

// 处理删除任务
const handleDelete = async (taskId, taskTitle) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除任务 "${taskTitle}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await deleteTask(taskId)
    ElMessage.success('任务删除成功')
    loadTasks() // 重新加载任务列表
  } catch (error) {
    if (error === 'cancel') {
      return
    }
    ElMessage.error('任务删除失败')
    console.error('删除任务失败:', error)
  }
}

// 显示创建任务对话框
const showCreateDialog = () => {
  console.log('显示创建任务对话框')
  createForm.title = ''
  createForm.description = ''
  createForm.due_date = ''
  createForm.student_ids = []
  createDialogVisible.value = true
  console.log('创建对话框状态:', createDialogVisible.value)
}

// 显示编辑任务对话框
const showEditDialog = async (task) => {
  currentTaskId.value = task.id
  // 复制任务数据到编辑表单
  editForm.title = task.title
  editForm.description = task.description
  editForm.due_date = task.due_date
  editDialogVisible.value = true
}

// 显示任务详情
const showTaskDetail = async (task) => {
  try {
    const response = await getTask(task.id)
    currentTask.value = response.data || response
    detailDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取任务详情失败')
    console.error('获取任务详情失败:', error)
  }
}

// 初始化数据
onMounted(() => {
  loadTasks()
  loadStudents()
})
</script>

<style scoped>
.teacher-tasks-container {
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
</style>