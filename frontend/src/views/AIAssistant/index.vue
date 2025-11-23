<template>
  <div class="ai-assistant-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="page-title">
        <h2>AI助教</h2>
        <p>智能问答助手，基于课程知识库为您提供专业解答</p>
      </div>
      
    </div>
    
    <el-row :gutter="20">
      <!-- 左侧：会话列表 -->
      <el-col :span="6">
        <el-card title="会话列表">
          <template #header>
            <div class="card-header">
              <span>会话列表</span>
              <el-button size="small" @click="showSessionDialog = true">新建</el-button>
            </div>
          </template>
          
          <div class="session-list">
            <div 
              v-for="session in sessions" 
              :key="session.id"
              class="session-item"
              :class="{ active: selectedSession?.id === session.id }"
              @click="selectSession(session)"
            >
              <div class="session-info">
                <div class="session-name">{{ session.session_name }}</div>
                <div class="session-time">{{ formatDate(session.created_at) }}</div>
              </div>
              <div class="session-actions">
                <el-button size="small" type="text" @click.stop="deleteSession(session)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 右侧：聊天区域 -->
      <el-col :span="18">
        <el-card class="chat-card">
          <template #header>
            <div class="chat-header">
              <span>{{ selectedSession?.session_name || '选择会话开始聊天' }}</span>
              <div class="chat-actions">
                <el-button size="small" @click="clearChat">清空聊天</el-button>
                <el-button size="small" @click="exportChat">导出聊天</el-button>
              </div>
            </div>
          </template>
          
          <!-- 聊天消息区域 -->
          <div class="chat-messages" ref="messagesContainer">
            <div 
              v-for="message in messages" 
              :key="message.id"
              class="message-item"
              :class="{ 'user-message': message.role === 'user', 'ai-message': message.role === 'assistant' }"
            >
              <div class="message-avatar">
                <el-avatar v-if="message.role === 'user'" :size="32">
                  {{ userStore.user?.full_name?.charAt(0) }}
                </el-avatar>
                <el-avatar v-else :size="32" class="ai-avatar">
                  AI
                </el-avatar>
              </div>
              
              <div class="message-content">
                <div class="message-bubble">
                  <div class="message-text" v-html="formatMessage(message.content)"></div>
                  
                  <!-- 消息元数据 -->
                  <div v-if="message.metadata" class="message-metadata">
                    <div v-if="message.metadata.sources" class="message-sources">
                      <h5>参考资料：</h5>
                      <ul>
                        <li v-for="source in message.metadata.sources" :key="source">
                          {{ source }}
                        </li>
                      </ul>
                    </div>
                    
                    <div v-if="message.metadata.confidence" class="message-confidence">
                      置信度: {{ (message.metadata.confidence * 100).toFixed(1) }}%
                    </div>
                  </div>
                </div>
                
                <div class="message-time">{{ formatTime(message.created_at) }}</div>
                
                <!-- 消息操作 -->
                <div class="message-actions">
                  <el-button size="small" type="text" @click="copyMessage(message.content)">
                    <el-icon><CopyDocument /></el-icon>
                  </el-button>
                  <el-button size="small" type="text" @click="likeMessage(message)">
                    点赞
                  </el-button>
                  <el-button size="small" type="text" @click="dislikeMessage(message)">
                    点踩
                  </el-button>
                </div>
              </div>
            </div>
            
            <!-- 加载状态 -->
            <div v-if="loading" class="message-item ai-message">
              <div class="message-avatar">
                <el-avatar :size="32" class="ai-avatar">
                  AI
                </el-avatar>
              </div>
              <div class="message-content">
                <div class="message-bubble">
                  <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 输入区域 -->
          <div class="chat-input">
            <el-input
              v-model="inputMessage"
              type="textarea"
              :rows="3"
              placeholder="请输入您的问题..."
              @keydown.ctrl.enter="sendMessage"
              :disabled="!selectedSession || loading"
            />
            <div class="input-actions">
              <div class="input-tips">
                <span>按 Ctrl+Enter 发送</span>
              </div>
              <el-button 
                type="primary" 
                @click="sendMessage"
                :loading="loading"
                :disabled="!inputMessage.trim() || !selectedSession"
              >
                发送
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 新建会话对话框 -->
    <el-dialog v-model="showSessionDialog" title="新建会话" width="400px">
      <el-form :model="newSessionForm" label-width="80px">
        <el-form-item label="会话名称">
          <el-input v-model="newSessionForm.session_name" placeholder="请输入会话名称" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showSessionDialog = false">取消</el-button>
          <el-button type="primary" @click="createSession">创建</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const userStore = useUserStore()

// 响应式数据
const showSessionDialog = ref(false)
const loading = ref(false)
const selectedSession = ref(null)
const inputMessage = ref('')
const messagesContainer = ref()

// 新建会话表单
const newSessionForm = reactive({
  session_name: ''
})

// 数据
const sessions = ref([])
const messages = ref([])

// 格式化日期
const formatDate = (date) => {
  return new Date(date).toLocaleDateString('zh-CN')
}

// 格式化时间
const formatTime = (date) => {
  return new Date(date).toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// 格式化消息内容
const formatMessage = (content) => {
  // 简单的Markdown渲染
  return content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>')
}

// 加载会话列表
const loadSessions = async () => {
  try {
    // 调用实际的API
    // const response = await getChatSessions()
    // sessions.value = response.data
    
    // 初始为空数组，等待API数据
    sessions.value = []
  } catch (error) {
    ElMessage.error('加载会话列表失败')
  }
}

// 选择会话
const selectSession = async (session) => {
  selectedSession.value = session
  await loadMessages(session.id)
}

// 加载消息
const loadMessages = async (sessionId) => {
  try {
    // 调用实际的API
    // const response = await getChatMessages(sessionId)
    // messages.value = response.data
    
    // 初始为空数组，等待API数据
    messages.value = []
    
    // 滚动到底部
    nextTick(() => {
      scrollToBottom()
    })
  } catch (error) {
    ElMessage.error('加载消息失败')
  }
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim() || !selectedSession.value || loading.value) return
  
  const userMessage = {
    id: Date.now(),
    session_id: selectedSession.value.id,
    role: 'user',
    content: inputMessage.value,
    created_at: new Date().toISOString()
  }
  
  messages.value.push(userMessage)
  const question = inputMessage.value
  inputMessage.value = ''
  
  // 滚动到底部
  nextTick(() => {
    scrollToBottom()
  })
  
  loading.value = true
  
  try {
    // 调用实际的API
    // const response = await askAI({
    //   question: question,
    //   session_id: selectedSession.value.id
    // })
    // const aiMessage = response.data
    // messages.value.push(aiMessage)
    // loading.value = false
    
    // 目前暂时不实现模拟回复功能
    loading.value = false
    ElMessage.warning('AI回复功能正在开发中')
    
    // 滚动到底部
    nextTick(() => {
      scrollToBottom()
    })
  } catch (error) {
    ElMessage.error('发送消息失败')
    loading.value = false
  }
}

// 生成AI回复（已移除模拟数据）
// 实际应用中应通过API获取AI回复
const generateAIResponse = (question) => {
  return ''
}

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 创建会话
const createSession = async () => {
  if (!newSessionForm.session_name.trim()) {
    ElMessage.warning('请输入会话名称')
    return
  }
  
  try {
    // 调用实际的API
    // const response = await createChatSession(newSessionForm)
    // const newSession = response.data
    // sessions.value.unshift(newSession)
    // selectedSession.value = newSession
    // messages.value = []
    
    // 模拟创建会话成功（保留基础功能）
    const newSession = {
      id: Date.now(),
      session_name: newSessionForm.session_name,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    
    sessions.value.unshift(newSession)
    selectedSession.value = newSession
    messages.value = []
    newSessionForm.session_name = ''
    showSessionDialog.value = false
    
    ElMessage.success('会话创建成功')
  } catch (error) {
    ElMessage.error('创建会话失败')
  }
}

// 删除会话
const deleteSession = async (session) => {
  try {
    await ElMessageBox.confirm('确定要删除这个会话吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const index = sessions.value.findIndex(s => s.id === session.id)
    if (index !== -1) {
      sessions.value.splice(index, 1)
      
      if (selectedSession.value?.id === session.id) {
        selectedSession.value = null
        messages.value = []
      }
      
      ElMessage.success('删除成功')
    }
  } catch (error) {
    // 用户取消
  }
}

// 清空聊天
const clearChat = () => {
  ElMessageBox.confirm('确定要清空当前聊天记录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    messages.value = []
    ElMessage.success('聊天记录已清空')
  }).catch(() => {
    // 用户取消
  })
}

// 导出聊天
const exportChat = () => {
  if (!selectedSession.value || messages.value.length === 0) {
    ElMessage.warning('没有聊天记录可导出')
    return
  }
  
  const chatData = {
    session: selectedSession.value,
    messages: messages.value,
    exportTime: new Date().toISOString()
  }
  
  const dataStr = JSON.stringify(chatData, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  
  const link = document.createElement('a')
  link.href = url
  link.download = `chat_${selectedSession.value.session_name}_${new Date().getTime()}.json`
  link.click()
  
  URL.revokeObjectURL(url)
  ElMessage.success('聊天记录导出成功')
}

// 复制消息
const copyMessage = (content) => {
  navigator.clipboard.writeText(content).then(() => {
    ElMessage.success('已复制到剪贴板')
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}

// 点赞消息
const likeMessage = (message) => {
  ElMessage.success('感谢您的反馈！')
}

// 点踩消息
const dislikeMessage = (message) => {
  ElMessage.info('我们会改进回答质量，感谢您的反馈！')
}

onMounted(() => {
  loadSessions()
})
</script>

<style lang="scss" scoped>
.ai-assistant-container {
  padding: 20px;
  height: calc(100vh - 120px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  
  .page-title {
    h2 {
      margin: 0 0 8px 0;
      color: #333;
    }
    
    p {
      margin: 0;
      color: #666;
      font-size: 14px;
    }
  }
}

.session-list {
  .session-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    border: 1px solid #e4e7ed;
    border-radius: 6px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      border-color: #409eff;
      background-color: #f0f9ff;
    }
    
    &.active {
      border-color: #409eff;
      background-color: #e6f7ff;
    }
    
    .session-info {
      flex: 1;
      
      .session-name {
        font-weight: 500;
        color: #333;
        margin-bottom: 4px;
      }
      
      .session-time {
        font-size: 12px;
        color: #666;
      }
    }
    
    .session-actions {
      display: flex;
      gap: 4px;
    }
  }
}

.chat-card {
  height: calc(100vh - 200px);
  
  .chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .chat-actions {
      display: flex;
      gap: 8px;
    }
  }
}

.chat-messages {
  height: calc(100vh - 350px);
  overflow-y: auto;
  padding: 16px;
  border-bottom: 1px solid #e4e7ed;
  
  .message-item {
    display: flex;
    margin-bottom: 16px;
    
    &.user-message {
      flex-direction: row-reverse;
      
      .message-content {
        margin-right: 12px;
        margin-left: 0;
      }
      
      .message-bubble {
        background: #409eff;
        color: white;
      }
    }
    
    &.ai-message {
      .message-content {
        margin-left: 12px;
        margin-right: 0;
      }
      
      .message-bubble {
        background: #f5f7fa;
        color: #333;
      }
    }
    
    .message-avatar {
      flex-shrink: 0;
    }
    
    .message-content {
      max-width: 70%;
      
      .message-bubble {
        padding: 12px 16px;
        border-radius: 12px;
        word-wrap: break-word;
        
        .message-text {
          line-height: 1.5;
          
          :deep(code) {
            background: rgba(0, 0, 0, 0.1);
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
          }
          
          :deep(strong) {
            font-weight: bold;
          }
          
          :deep(em) {
            font-style: italic;
          }
        }
        
        .message-metadata {
          margin-top: 12px;
          padding-top: 12px;
          border-top: 1px solid rgba(0, 0, 0, 0.1);
          
          .message-sources {
            margin-bottom: 8px;
            
            h5 {
              margin: 0 0 4px 0;
              font-size: 12px;
              opacity: 0.8;
            }
            
            ul {
              margin: 0;
              padding-left: 16px;
              font-size: 12px;
              opacity: 0.8;
            }
          }
          
          .message-confidence {
            font-size: 12px;
            opacity: 0.8;
          }
        }
      }
      
      .message-time {
        font-size: 12px;
        color: #999;
        margin-top: 4px;
        text-align: right;
      }
      
      .message-actions {
        display: flex;
        gap: 4px;
        margin-top: 4px;
        opacity: 0;
        transition: opacity 0.3s;
      }
      
      &:hover .message-actions {
        opacity: 1;
      }
    }
  }
}

.chat-input {
  padding: 16px;
  
  .input-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
    
    .input-tips {
      font-size: 12px;
      color: #999;
    }
  }
}

.ai-avatar {
  background: #67c23a;
  color: white;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  
  span {
    width: 8px;
    height: 8px;
    background: #409eff;
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;
    
    &:nth-child(1) {
      animation-delay: -0.32s;
    }
    
    &:nth-child(2) {
      animation-delay: -0.16s;
    }
  }
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
