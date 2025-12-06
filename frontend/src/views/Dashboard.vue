<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <!-- 欢迎信息 -->
      <el-col :span="24">
        <el-card class="welcome-card">
          <div class="welcome-content">
            <div class="welcome-text">
              <h2>欢迎回来，{{ userStore.user?.full_name || userStore.user?.username }}！</h2>
              <div class="user-role">
                <span v-if="userStore.hasRole('student')">学生</span>
                <span v-else-if="userStore.hasRole('teacher')">教师</span>
                <span v-else-if="userStore.hasRole('admin')">管理员</span>
                <span v-else>访客</span>
              </div>
              <p v-if="userStore.hasRole('student')">今天是学习的好日子，让我们继续探索知识的海洋吧</p>
              <p v-else>欢迎使用AI学习系统</p>
            </div>
            <div class="welcome-avatar">
              <el-avatar :size="80" :src="userStore.user?.avatar">
                {{ userStore.user?.full_name?.charAt(0) }}
              </el-avatar>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 只在学生角色显示学习统计 -->
    <template v-if="userStore.hasRole('student')">
      <el-row :gutter="20" style="margin-top: 20px;">
        <!-- 学习统计 -->
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon learning">
                <el-icon><Reading /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.learningNodes }}</div>
                <div class="stat-label">已学知识点</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon questions">
                <el-icon><EditPen /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.questionsAnswered }}</div>
                <div class="stat-label">已答题目</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon accuracy">
                <el-icon><TrendCharts /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stats.accuracy }}%</div>
                <div class="stat-label">答题正确率</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-icon tasks">
                <el-icon><Document /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ pendingTasks.length }}</div>
                <div class="stat-label">未完成任务</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <!-- 未完成任务列表 -->
      <el-row style="margin-top: 20px;">
        <el-col :span="24">
          <el-card class="task-card">
            <div class="card-header">
              <h3>待完成任务</h3>
              <router-link to="/student-tasks" class="view-all-link">
                查看全部 <el-icon><ArrowRight /></el-icon>
              </router-link>
            </div>
            
            <div v-if="taskLoading" class="loading-state">
              <el-skeleton :rows="3" />
            </div>
            
            <div v-else-if="pendingTasks.length === 0" class="empty-state">
              <el-empty description="暂无待完成任务" />
            </div>
            
            <div v-else class="task-list">
              <div v-for="task in pendingTasks.slice(0, 3)" :key="task.id" class="task-item">
                <div class="task-main">
                  <h4 class="task-title">{{ task.task.title }}</h4>
                  <p class="task-description">{{ task.task.description }}</p>
                </div>
                <div class="task-meta">
                  <div class="task-date">
                    <span :class="{ 'due-soon': isDueSoon(task.task.due_date) }">
                      截止日期：{{ formatDate(task.task.due_date) }}
                    </span>
                  </div>
                  <router-link 
                    :to="{ name: 'StudentTasks' }" 
                    class="view-task-link"
                  >
                    查看详情
                  </router-link>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </template>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { getAssignedTasks } from '@/api/tasks'
import { getLearningStats } from '@/api/questions'
import { recordsAPI } from '../api'

const router = useRouter()
const userStore = useUserStore()

// 统计数据
const stats = reactive({
  learningNodes: 0,
  questionsAnswered: 0,
  accuracy: 0,
  learningTime: 0
})

// 未完成任务数据
const pendingTasks = ref([])
const taskLoading = ref(false)

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 检查任务是否即将到期（24小时内）
const isDueSoon = (dueDateString) => {
  if (!dueDateString) return false
  const now = new Date()
  const dueDate = new Date(dueDateString)
  const diffHours = (dueDate - now) / (1000 * 60 * 60)
  return diffHours > 0 && diffHours <= 24
}

// 加载未完成任务
const loadPendingTasks = async () => {
  taskLoading.value = true
  try {
    console.log('开始加载未完成任务...')
    const taskData = await getAssignedTasks()
    console.log('获取到的原始任务数据:', taskData)
    // 过滤出未完成的任务
    pendingTasks.value = Array.isArray(taskData) ? taskData.filter(task => !task.is_completed) : []
    console.log('过滤后的未完成任务数量:', pendingTasks.value.length)
    console.log('过滤后的未完成任务数据:', pendingTasks.value)
  } catch (error) {
    console.error('加载任务列表失败的详细错误:', error)
    ElMessage.error('加载任务列表失败')
  } finally {
    taskLoading.value = false
  }
}

const loadDashboardData = async () => {
  try {
    // 获取学习统计数据
    const statsResponse = await getLearningStats();
    
    if (statsResponse.data.code === 200 && statsResponse.data.data) {
      const learningData = statsResponse.data.data;
      // 注意：这里的字段映射需要根据实际返回的数据结构调整
      stats.learningNodes = await recordsAPI.getCompleteCount();
      stats.questionsAnswered = learningData.answeredQuestions || 0;
      stats.accuracy = learningData.accuracy || 0;
      stats.learningTime = 0; // 暂未从API获取
    }
    
    // 加载未完成任务
    if (userStore.hasRole('student')) {
      await loadPendingTasks()
    }
  } catch (error) {
    console.error('加载统计数据失败:', error);
    ElMessage.error('加载数据失败')
  }
}

onMounted(() => {
  loadDashboardData()
})
</script>

<style lang="scss" scoped>
.dashboard {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
  
  .welcome-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .welcome-text {
      h2 {
        margin: 0 0 5px 0;
        color: #333;
      }
      
      .user-role {
        margin: 5px 0 10px 0;
        
        span {
          display: inline-block;
          padding: 2px 10px;
          border-radius: 12px;
          font-size: 12px;
          font-weight: 500;
        }
        
        span:nth-child(1) {
          background-color: #e6f7ff;
          color: #1890ff;
        }
        
        span:nth-child(2) {
          background-color: #f6ffed;
          color: #52c41a;
        }
        
        span:nth-child(3) {
          background-color: #fff7e6;
          color: #fa8c16;
        }
        
        span:nth-child(4) {
          background-color: #f5f5f5;
          color: #606266;
        }
      }
      
      p {
        margin: 0;
        color: #666;
        font-size: 14px;
      }
    }
  }
}

.stat-card {
  .stat-content {
    display: flex;
    align-items: center;
    
    .stat-icon {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 16px;
      font-size: 24px;
      color: white;
      
      &.learning {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      }
      
      &.questions {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      }
      
      &.accuracy {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      }
      
      &.time {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
      }
      
      &.tasks {
        background: linear-gradient(135deg, #f5a623 0%, #ff7e5f 100%);
      }
    }
    
    .stat-info {
      .stat-value {
        font-size: 28px;
        font-weight: bold;
        color: #333;
        line-height: 1;
      }
      
      .stat-label {
        font-size: 14px;
        color: #666;
        margin-top: 4px;
      }
    }
  }
}

.task-card {
  margin-top: 20px;
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    
    h3 {
      margin: 0;
      font-size: 18px;
      font-weight: 500;
    }
    
    .view-all-link {
      color: #1890ff;
      text-decoration: none;
      display: flex;
      align-items: center;
      font-size: 14px;
      
      el-icon {
        margin-left: 4px;
        font-size: 12px;
      }
    }
  }
  
  .loading-state {
    padding: 20px 0;
  }
  
  .empty-state {
    padding: 40px 0;
  }
  
  .task-list {
    .task-item {
      padding: 16px;
      border: 1px solid #f0f0f0;
      border-radius: 8px;
      margin-bottom: 12px;
      transition: all 0.3s;
      
      &:hover {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      }
      
      .task-main {
        .task-title {
          margin: 0 0 8px 0;
          font-size: 16px;
          font-weight: 500;
          color: #333;
        }
        
        .task-description {
          margin: 0;
          font-size: 14px;
          color: #666;
          line-height: 1.5;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
          text-overflow: ellipsis;
        }
      }
      
      .task-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 12px;
        
        .task-date {
          font-size: 12px;
          color: #909399;
          
          .due-soon {
            color: #f56c6c;
            font-weight: 500;
          }
        }
        
        .view-task-link {
          color: #1890ff;
          text-decoration: none;
          font-size: 14px;
        }
      }
    }
  }
}
</style>
