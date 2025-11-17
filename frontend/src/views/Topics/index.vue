<template>
  <div class="topics-container">
    <div class="topics-header">
      <h1>讨论区</h1>
      <div class="search-container">
        <el-input
          v-model="searchQuery"
          placeholder="搜索主题或内容..."
          prefix-icon="Search"
          class="search-input"
          @keyup.enter="handleSearch"
          clearable
          @clear="clearSearch"
        />
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button v-if="searchQuery" @click="clearSearch">清除</el-button>
      </div>
      <el-button type="primary" @click="showCreateTopicDialog">发布新主题</el-button>
    </div>
    
    <div class="topics-list">
      <el-card v-for="topic in topics" :key="topic.id" class="topic-card">
        <div class="topic-header">
          <div class="topic-title">
            <router-link :to="`/topics/${topic.id}`">
              <h3>{{ topic.title }}</h3>
            </router-link>
            <div class="topic-meta">
              <span class="author">发布者：{{ topic.created_by_name }}</span>
              <span class="time">发布时间：{{ formatDate(topic.created_at) }}</span>
              <span class="replies-count">回复数：{{ topic.replies_count }}</span>
            </div>
          </div>
          <div v-if="isCreatorOrAdmin(topic)" class="topic-actions">
            <el-button type="text" size="small" @click="handleUpdateTopic(topic)">编辑</el-button>
            <el-button type="text" size="small" danger @click="handleDeleteTopic(topic.id)">删除</el-button>
          </div>
        </div>
        <div class="topic-content">
          {{ topic.content }}
        </div>
      </el-card>
    </div>
    
    <div class="pagination" v-if="total > pageSize">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
    
    <!-- 创建主题对话框 -->
    <el-dialog
      v-model="createDialogVisible"
      title="发布新主题"
      width="600px"
    >
      <el-form ref="createFormRef" :model="createForm" :rules="createFormRules" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="createForm.title" placeholder="请输入主题标题" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="createForm.content"
            type="textarea"
            :rows="6"
            placeholder="请输入主题内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleCreateTopic">发布</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 更新主题对话框 -->
    <el-dialog
      v-model="updateDialogVisible"
      title="编辑主题"
      width="600px"
    >
      <el-form ref="updateFormRef" :model="updateForm" :rules="updateFormRules" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="updateForm.title" placeholder="请输入主题标题" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="updateForm.content"
            type="textarea"
            :rows="6"
            placeholder="请输入主题内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="updateDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleUpdateConfirm">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getTopics, createTopic, updateTopic, deleteTopic } from '@/api/topics'

const router = useRouter()
const userStore = useUserStore()

// 主题列表数据
const topics = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const loading = ref(false)
const searchQuery = ref('')

// 创建主题对话框
const createDialogVisible = ref(false)
const createFormRef = ref()
const createForm = ref({
  title: '',
  content: ''
})
const createFormRules = {
  title: [
    { required: true, message: '请输入主题标题', trigger: 'blur' },
    { min: 2, max: 100, message: '标题长度应在2-100个字符之间', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入主题内容', trigger: 'blur' },
    { min: 5, message: '内容长度至少为5个字符', trigger: 'blur' }
  ]
}

// 更新主题对话框
const updateDialogVisible = ref(false)
const updateFormRef = ref()
const updateForm = ref({
  id: '',
  title: '',
  content: ''
})
const updateFormRules = {
  title: [
    { required: true, message: '请输入主题标题', trigger: 'blur' },
    { min: 2, max: 100, message: '标题长度应在2-100个字符之间', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入主题内容', trigger: 'blur' },
    { min: 5, message: '内容长度至少为5个字符', trigger: 'blur' }
  ]
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 判断是否是创建者或管理员
const isCreatorOrAdmin = (topic) => {
  const currentUserId = userStore.user?.id
  const isAdmin = userStore.user?.roles.some(role => role.name === 'admin')
  return currentUserId === topic.created_by_id || isAdmin
}

// 获取主题列表
const fetchTopics = async () => {
  loading.value = true
  try {
    const response = await getTopics({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      search: searchQuery.value || undefined
    })
    topics.value = response
    // 这里假设后端返回的是总条数，如果不是，需要调整
    total.value = response.length
  } catch (error) {
    ElMessage.error('获取主题列表失败')
    console.error('获取主题列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchTopics()
}

// 清除搜索
const clearSearch = () => {
  searchQuery.value = ''
  currentPage.value = 1
  fetchTopics()
}

// 显示创建主题对话框
const showCreateTopicDialog = () => {
  createForm.value = {
    title: '',
    content: ''
  }
  createDialogVisible.value = true
}

// 处理创建主题
const handleCreateTopic = async () => {
  try {
    await createFormRef.value.validate()
    const response = await createTopic(createForm.value)
    ElMessage.success('主题创建成功')
    createDialogVisible.value = false
    fetchTopics() // 重新获取主题列表
  } catch (error) {
    if (error.name === 'Error') {
      // 表单验证失败不显示错误提示
      return
    }
    ElMessage.error('主题创建失败')
    console.error('主题创建失败:', error)
  }
}

// 处理更新主题
const handleUpdateTopic = (topic) => {
  updateForm.value = {
    id: topic.id,
    title: topic.title,
    content: topic.content
  }
  updateDialogVisible.value = true
}

// 处理更新确认
const handleUpdateConfirm = async () => {
  try {
    await updateFormRef.value.validate()
    const { id, ...formData } = updateForm.value
    const response = await updateTopic(id, formData)
    ElMessage.success('主题更新成功')
    updateDialogVisible.value = false
    fetchTopics() // 重新获取主题列表
  } catch (error) {
    if (error.name === 'Error') {
      // 表单验证失败不显示错误提示
      return
    }
    ElMessage.error('主题更新失败')
    console.error('主题更新失败:', error)
  }
}

// 处理删除主题
const handleDeleteTopic = async (topicId) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个主题吗？删除后将无法恢复，并且会删除所有相关回复。',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await deleteTopic(topicId)
    ElMessage.success('主题删除成功')
    fetchTopics() // 重新获取主题列表
  } catch (error) {
    if (error === 'cancel') {
      // 用户取消删除
      return
    }
    ElMessage.error('主题删除失败')
    console.error('主题删除失败:', error)
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchTopics()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  fetchTopics()
}

// 初始加载
onMounted(() => {
  fetchTopics()
})
</script>

<style scoped>
.topics-container {
  padding: 20px;
}

.topics-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  gap: 15px;
}

.search-container {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  max-width: 400px;
}

.search-input {
  width: 100%;
}

.topics-header h1 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.topics-list {
  margin-bottom: 20px;
}

.topic-card {
  margin-bottom: 16px;
}

.topic-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.topic-title h3 {
  margin: 0 0 8px 0;
  font-size: 18px;
  color: #409eff;
}

.topic-title h3:hover {
  color: #66b1ff;
}

.topic-meta {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #606266;
}

.topic-actions {
  display: flex;
  gap: 5px;
}

.topic-content {
  color: #303133;
  line-height: 1.6;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>