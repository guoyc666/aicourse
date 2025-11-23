<template>
  <div class="topic-detail-container">
    <div class="back-button-container">
      <el-button type="default" @click="handleBack">返回上一页</el-button>
    </div>
    <el-card v-if="topic" class="topic-detail-card">
      <div class="topic-header">
        <h1>{{ topic.title }}</h1>
        <div class="topic-meta">
          <span class="author">发布者：{{ topic.created_by_name }}</span>
          <span class="time">发布时间：{{ formatDate(topic.created_at) }}</span>
          <span v-if="topic.updated_at" class="update-time">更新时间：{{ formatDate(topic.updated_at) }}</span>
          <span class="replies-count">回复数：{{ topic.replies_count }}</span>
        </div>
      </div>
      <div class="topic-content">
        {{ topic.content }}
      </div>
      <div v-if="isCreatorOrAdmin(topic)" class="topic-actions">
        <el-button type="primary" size="small" @click="handleUpdateTopic(topic)">编辑</el-button>
        <el-button type="danger" size="small" @click="handleDeleteTopic(topic.id)">删除</el-button>
      </div>
    </el-card>
    
    <div v-if="topic" class="replies-section">
      <h2>回复列表</h2>
      <div v-if="topic.is_closed" class="closed-notice">
        <el-alert title="该主题已关闭，无法回复" type="warning" :closable="false" />
      </div>
      
      <div v-for="reply in replies" :key="reply.id" class="reply-item">
        <div class="reply-header">
          <span class="reply-author">{{ reply.created_by_name }}</span>
          <span class="reply-time">{{ formatDate(reply.created_at) }}</span>
          <span v-if="reply.updated_at" class="reply-update-time">（已编辑）</span>
          <div v-if="isReplyOwnerOrAdmin(reply)" class="reply-actions">
            <el-button type="text" size="small" @click="handleUpdateReply(reply)">编辑</el-button>
            <el-button type="text" size="small" danger @click="handleDeleteReply(reply.id)">删除</el-button>
          </div>
        </div>
        <div class="reply-content">
          {{ reply.content }}
        </div>
      </div>
      
      <div v-if="replies.length === 0" class="no-replies">
        暂无回复，快来抢沙发吧！
      </div>
      
      <div v-if="!topic.is_closed" class="reply-form">
        <el-form ref="replyFormRef" :model="replyForm" :rules="replyFormRules">
          <el-form-item prop="content">
            <el-input
              v-model="replyForm.content"
              type="textarea"
              :rows="4"
              placeholder="请输入回复内容"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleCreateReply">回复</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    
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
    
    <!-- 更新回复对话框 -->
    <el-dialog
      v-model="updateReplyDialogVisible"
      title="编辑回复"
      width="600px"
    >
      <el-form ref="updateReplyFormRef" :model="updateReplyForm" :rules="updateReplyFormRules" label-width="80px">
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="updateReplyForm.content"
            type="textarea"
            :rows="4"
            placeholder="请输入回复内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="updateReplyDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleUpdateReplyConfirm">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getTopicDetail, getTopicReplies, createReply, updateReply, deleteReply, updateTopic as updateTopicApi, deleteTopic as deleteTopicApi } from '@/api/topics'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 主题数据
const topic = ref(null)
const replies = ref([])
const loading = ref(false)

// 回复表单
const replyFormRef = ref()
const replyForm = ref({
  content: ''
})
const replyFormRules = {
  content: [
    { required: true, message: '请输入回复内容', trigger: 'blur' },
    { min: 2, message: '回复内容至少为2个字符', trigger: 'blur' }
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

// 更新回复对话框
const updateReplyDialogVisible = ref(false)
const updateReplyFormRef = ref()
const updateReplyForm = ref({
  id: '',
  content: ''
})
const updateReplyFormRules = {
  content: [
    { required: true, message: '请输入回复内容', trigger: 'blur' },
    { min: 2, message: '回复内容至少为2个字符', trigger: 'blur' }
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

// 判断是否是回复的所有者或管理员
const isReplyOwnerOrAdmin = (reply) => {
  const currentUserId = userStore.user?.id
  const isAdmin = userStore.user?.roles.some(role => role.name === 'admin')
  return currentUserId === reply.created_by_id || isAdmin
}

// 返回上一页
const handleBack = () => {
  router.back()
}

// 获取主题详情
const fetchTopicDetail = async () => {
  const topicId = route.params.id
  if (!topicId) return
  
  loading.value = true
  try {
    const response = await getTopicDetail(topicId)
    topic.value = response
  } catch (error) {
    ElMessage.error('获取主题详情失败')
    console.error('获取主题详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 获取回复列表
const fetchReplies = async () => {
  const topicId = route.params.id
  if (!topicId) return
  
  loading.value = true
  try {
    const response = await getTopicReplies(topicId)
    replies.value = response
  } catch (error) {
    ElMessage.error('获取回复列表失败')
    console.error('获取回复列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 处理创建回复
const handleCreateReply = async () => {
  try {
    await replyFormRef.value.validate()
    const topicId = route.params.id
    await createReply(topicId, replyForm.value)
    ElMessage.success('回复成功')
    replyForm.value.content = ''
    fetchReplies() // 重新获取回复列表
    fetchTopicDetail() // 重新获取主题详情以更新回复数
  } catch (error) {
    if (error.name === 'Error') {
      // 表单验证失败不显示错误提示
      return
    }
    ElMessage.error('回复失败')
    console.error('回复失败:', error)
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
    await updateTopicApi(id, formData)
    ElMessage.success('主题更新成功')
    updateDialogVisible.value = false
    fetchTopicDetail() // 重新获取主题详情
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
    await deleteTopicApi(topicId)
    ElMessage.success('主题删除成功')
    router.push('/topics') // 删除成功后返回主题列表页
  } catch (error) {
    if (error === 'cancel') {
      // 用户取消删除
      return
    }
    ElMessage.error('主题删除失败')
    console.error('主题删除失败:', error)
  }
}

// 处理更新回复
const handleUpdateReply = (reply) => {
  updateReplyForm.value = {
    id: reply.id,
    content: reply.content
  }
  updateReplyDialogVisible.value = true
}

// 处理更新回复确认
const handleUpdateReplyConfirm = async () => {
  try {
    await updateReplyFormRef.value.validate()
    const { id, ...formData } = updateReplyForm.value
    await updateReply(id, formData)
    ElMessage.success('回复更新成功')
    updateReplyDialogVisible.value = false
    fetchReplies() // 重新获取回复列表
  } catch (error) {
    if (error.name === 'Error') {
      // 表单验证失败不显示错误提示
      return
    }
    ElMessage.error('回复更新失败')
    console.error('回复更新失败:', error)
  }
}

// 处理删除回复
const handleDeleteReply = async (replyId) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个回复吗？删除后将无法恢复。',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await deleteReply(replyId)
    ElMessage.success('回复删除成功')
    fetchReplies() // 重新获取回复列表
    fetchTopicDetail() // 重新获取主题详情以更新回复数
  } catch (error) {
    if (error === 'cancel') {
      // 用户取消删除
      return
    }
    ElMessage.error('回复删除失败')
    console.error('回复删除失败:', error)
  }
}

// 初始加载
onMounted(() => {
  fetchTopicDetail()
  fetchReplies()
})

// 监听路由变化
let routeUpdateHandler = null
onMounted(() => {
  routeUpdateHandler = () => {
    fetchTopicDetail()
    fetchReplies()
  }
  routeUpdateHandler()
})

onBeforeUnmount(() => {
  // 清理工作
})
</script>

<style scoped>
.topic-detail-container {
  padding: 20px;
}

.topic-detail-card {
  margin-bottom: 20px;
}

.topic-header h1 {
  margin: 0 0 10px 0;
  font-size: 24px;
  color: #333;
}

.topic-meta {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #606266;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.topic-content {
  color: #303133;
  line-height: 1.8;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.topic-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.replies-section {
  margin-top: 20px;
}

.replies-section h2 {
  margin: 0 0 15px 0;
  font-size: 20px;
  color: #333;
}

.closed-notice {
  margin-bottom: 15px;
}

.reply-item {
  padding: 15px;
  border-bottom: 1px solid #ebeef5;
}

.reply-item:last-child {
  border-bottom: none;
}

.reply-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.reply-author {
  font-weight: bold;
  color: #409eff;
  margin-right: 10px;
}

.reply-time {
  font-size: 12px;
  color: #909399;
  margin-right: 10px;
}

.reply-update-time {
  font-size: 12px;
  color: #f56c6c;
}

.reply-actions {
  margin-left: auto;
  display: flex;
  gap: 5px;
}

.reply-content {
  color: #303133;
  line-height: 1.6;
}

.no-replies {
  text-align: center;
  color: #909399;
  padding: 20px;
}

.reply-form {
  margin-top: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

/* 返回按钮样式 */
.back-button-container {
  margin-bottom: 16px;
}
</style>