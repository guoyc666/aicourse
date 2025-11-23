<template>
  <div class="questions-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="page-title">
        <h2>题库与练习</h2>
      </div>
      <div>
        <el-button type="primary" @click="showQuickPracticeDialog = true">
          <el-icon><EditPen /></el-icon>
          快速练习
        </el-button>
      </div>
    </div>
    
    <el-row :gutter="20">
      <!-- 练习统计 -->
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon total">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalQuestions || 0 }}</div>
              <div class="stat-label">总题目数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon answered">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.answeredQuestions || 0 }}</div>
              <div class="stat-label">已答题目</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon correct">
              <el-icon><CircleCheck /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.correctAnswers || 0 }}</div>
              <div class="stat-label">正确答题</div>
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
              <div class="stat-value">{{ stats.accuracy || 0 }}%</div>
              <div class="stat-label">正确率</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <!-- 知识点练习 -->
      <el-col :span="12">
        <el-card class="main-card">
          <template #header>
            <div class="card-header">
              <span>知识点练习</span>
              <el-button size="small" @click="loadKnowledgeNodes" :loading="loading.knowledge">刷新</el-button>
            </div>
          </template>
          
          <div v-if="loading.knowledge" class="loading-container">
            <el-skeleton :rows="4" animated />
          </div>
          
          <div v-else-if="knowledgeNodes.length === 0" class="empty-container">
            <el-empty description="暂无知识点数据" />
          </div>
          
          <div v-else class="master-list">
            <div 
              v-for="node in knowledgeNodes" 
              :key="node.id"
              class="master-item"
              @click="practiceByNode(node)"
            >
              <div class="master-info">
                <h4>{{ node.name }}</h4>
                <p>{{ node.description }}</p>
                <div class="master-meta">
                  <el-tag :type="getNodeTypeTag(node.node_type)" size="small">
                    {{ getNodeTypeName(node.node_type) }}
                  </el-tag>
                  <el-tag size="small" type="info">等级: {{ node.level }}</el-tag>
                  <span class="question-count">{{ getQuestionCount(node.id) }}题</span>
                </div>
              </div>
              <div class="master-progress">
                <div class="progress-label">掌握度: {{ getNodeProgress(node.id) }}%</div>
                <el-progress 
                  :percentage="getNodeProgress(node.id)"
                  :color="getProgressColor(getNodeProgress(node.id))"
                />
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 练习记录 -->
      <el-col :span="12">
        <el-card class="main-card">
          <template #header>
            <div class="card-header">
              <span>练习记录</span>
              <el-button size="small" @click="loadPracticeHistory" :loading="loading.history">刷新</el-button>
            </div>
          </template>
          
          <div v-if="loading.history" class="loading-container">
            <el-skeleton :rows="3" animated />
          </div>
          
          <div v-else-if="practiceHistory.length === 0" class="empty-container">
            <el-empty description="暂无练习记录" />
          </div>
          
          <div v-else class="practice-history">
            <div 
              v-for="record in practiceHistory" 
              :key="record.record_id"
              class="history-item"
              @click="viewPracticeDetail(record)"
            >
              <div class="history-info">
                <div class="history-title">{{ getKnowledgeNameById(record.knowledge_id) }}</div>
                <div class="history-meta">
                  <span class="history-time">{{ formatDateTime(record.submit_time) }}</span>
                  <span class="history-duration">用时: {{ formatDuration(record.time_spent) }}</span>
                </div>
              </div>
              <div class="history-result">
                <el-tag :type="getResultTag(record.accuracy * 100)">
                  {{ Math.round(record.accuracy * 100) }}%
                </el-tag>
                <span class="history-score">{{ getCorrectCount(record) }}题正确</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 快速练习对话框 -->
    <el-dialog
      v-model="showQuickPracticeDialog"
      title="选择练习模式"
      width="500px"
    >
      <div class="practice-mode-selection">
        <div class="mode-grid">
          <div class="mode-item" @click="startKnowledgePractice">
            <div class="mode-icon">
              <el-icon><Collection /></el-icon>
            </div>
            <h4>知识点练习</h4>
            <p>选择特定知识点进行针对性练习</p>
          </div>
          <div class="mode-item" @click="startRandomPractice">
            <div class="mode-icon">
              <el-icon><Refresh /></el-icon>
            </div>
            <h4>随机练习</h4>
            <p>随机抽取题目进行综合能力测试</p>
          </div>
        </div>
      </div>
    </el-dialog>
    
    <!-- 练习对话框 -->
    <el-dialog
      v-model="showPracticeDialog"
      :title="`练习 - ${selectedNode?.name || '综合练习'}`"
      width="800px"
      :before-close="handleClosePractice"
    >
      
      <!-- 加载状态 -->
      <div v-if="loading.questions" class="loading-container">
        <el-skeleton :rows="6" animated />
      </div>
      
      <!-- 有题目时显示练习内容 -->
      <div v-else-if="currentQuestions.length > 0 && !showResult" class="practice-content">
        <!-- 练习进度 -->
        <div class="practice-progress">
          <el-progress 
            :percentage="Math.min(100, Math.max(0, Math.round((currentQuestionIndex + 1) / (currentQuestions.length || 1) * 100)))"
            :format="() => `${currentQuestionIndex + 1}/${currentQuestions.length}`"
          />
          <div class="progress-info">
            <span>知识点: {{ selectedNode?.name || '综合' }}</span>
            <span>剩余时间: {{ formatTime(remainingTime) }}</span>
          </div>
        </div>
        
        <!-- 题目内容 -->
        <div class="question-content">
          <div class="question-header">
            <h3>第 {{ currentQuestionIndex + 1 }} 题</h3>
            <span class="question-type">{{ getQuestionTypeText(currentQuestion.type) }}</span>
            <el-tag :type="getDifficultyTag(currentQuestion.difficulty)" style="margin-left: 10px;">
              {{ getDifficultyText(currentQuestion.difficulty) }}
            </el-tag>
          </div>
          
          <div class="question-body">
            <p class="question-text">{{ currentQuestion.text }}</p>
            
            <!-- 选择题选项 -->
            <div v-if="currentQuestion.type === 'choice'" class="question-options">
              <template v-if="currentQuestion.options && typeof currentQuestion.options === 'object'">
                <!-- 处理平面对象格式 {A: '选项A', B: '选项B'} -->
                <div 
                  v-for="(value, key) in currentQuestion.options" 
                  :key="key"
                  class="option-item"
                  :class="{ selected: selectedAnswer === key }"
                  @click="selectAnswer(key)"
                >
                  <span class="option-label">{{ key }}.</span>
                  <span class="option-text">{{ value }}</span>
                </div>
              </template>
            </div>
            
            <!-- 填空题 -->
            <div v-else-if="currentQuestion.type === 'fill'" class="question-input">
              <el-input 
                v-model="selectedAnswer"
                placeholder="请输入答案"
                @keyup.enter="submitAnswer"
                clearable
              />
            </div>
            
            <!-- 编程题 -->
            <div v-else-if="currentQuestion.type === 'code'" class="question-code">
              <!-- 显示编程语言 -->
              <div class="code-language-tag">
                <el-tag type="success" size="small">
                  <el-icon><Document /></el-icon>
                  编程语言: {{ getCodeLanguageName(currentQuestion.code_language) }}
                </el-tag>
              </div>
              <el-input
                v-model="selectedAnswer"
                type="textarea"
                :rows="10"
                :placeholder="getCodePlaceholder(currentQuestion.code_language)"
                class="code-editor"
                clearable
              />
              <div class="code-tips">
                {{ getCodeTips(currentQuestion.code_language) }}
              </div>
            </div>
          </div>
        </div>
        
        <!-- 操作按钮 -->
        <div class="question-actions">
          <el-button @click="skipQuestion">跳过</el-button>
          <el-button type="primary" @click="submitAnswer" :disabled="!selectedAnswer.trim()">
            提交答案
          </el-button>
        </div>
      </div>
      
      <!-- 没有题目时显示提示 -->
      <div v-else-if="!showResult" class="no-questions">
        <el-empty description="当前没有可用题目" :image-size="150" />
        <p style="text-align: center; margin-top: 20px;">{{ selectedNode === null ? '系统暂无题目可供随机练习' : '当前知识点暂无题目' }}</p>
      </div>
      
      <!-- 练习结果 -->
      <div v-if="showResult" class="practice-result">
        <div class="result-header">
          <h3>练习完成！</h3>
          <p>知识点: {{ selectedNode?.name || '综合练习' }}</p>
        </div>
        
        <div class="result-stats">
          <div class="stat-item">
            <div class="stat-value">{{ result.correctCount }}</div>
            <div class="stat-label">正确题数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ result.totalCount }}</div>
            <div class="stat-label">总题数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ result.accuracy }}%</div>
            <div class="stat-label">正确率</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ result.duration }}</div>
            <div class="stat-label">用时</div>
          </div>
        </div>
        
        <!-- 掌握度变化 -->
        <div v-if="result.masteryUpdates && Object.keys(result.masteryUpdates).length > 0" class="mastery-updates">
          <h4>掌握度变化</h4>
          <div class="mastery-list">
            <div v-for="(update, knowledgeId) in result.masteryUpdates" :key="knowledgeId" class="mastery-item">
              <span class="knowledge-name">{{ getKnowledgeNameById(knowledgeId) }}</span>
              <div class="progress-wrapper">
                <el-progress 
                  :percentage="Math.round(update.new_value * 100)"
                  :color="getProgressColor(update.new_value * 100)"
                  :format="() => `${Math.round(update.new_value * 100)}%`"
                />
              </div>
              <span class="change-indicator" :class="{ positive: update.new_value > update.old_value }">
                {{ update.new_value > update.old_value ? '↑' : '↓' }} 
                {{ Math.abs(update.new_value - update.old_value).toFixed(2) * 100 }}%
              </span>
            </div>
          </div>
        </div>
        
        <div class="result-actions">
          <el-button @click="restartPractice">重新练习</el-button>
          <el-button type="primary" @click="continuePractice">完成</el-button>
        </div>
      </div>
    </el-dialog>
    
    <!-- 知识点选择对话框 -->
    <el-dialog
      v-model="showKnowledgeSelectDialog"
      title="选择知识点"
      width="500px"
    >
      <div class="knowledge-selection">
        <!-- 搜索框 -->
        <div class="search-container" style="margin-bottom: 16px;">
          <el-input
            v-model="knowledgeSearchQuery"
            placeholder="搜索知识点名称或描述"
            prefix-icon="el-icon-search"
            clearable
          />
        </div>
        
        <div v-if="filteredKnowledgeNodes.length === 0" class="empty-container">
          <el-empty description="未找到匹配的知识点" />
        </div>
        <el-scrollbar style="height: 300px;">
          <div
            v-for="node in filteredKnowledgeNodes"
            :key="node.id"
            class="knowledge-item"
            @click="confirmKnowledgeSelection(node)"
          >
            <div class="knowledge-info">
              <h4>{{ node.name }}</h4>
              <p>{{ node.description }}</p>
              <div class="knowledge-meta">
                <el-tag :type="getNodeTypeTag(node.node_type)" size="small">
                  {{ getNodeTypeName(node.node_type) }}
                </el-tag>
                <el-tag size="small" type="info">等级: {{ node.level }}</el-tag>
                <span class="question-count">{{ getQuestionCount(node.id) }}题</span>
              </div>
            </div>
            <div class="knowledge-progress">
              <div class="progress-label">掌握度: {{ getNodeProgress(node.id) }}%</div>
              <el-progress
                :percentage="getNodeProgress(node.id)"
                :color="getProgressColor(getNodeProgress(node.id))"
                size="small"
              />
            </div>
          </div>
        </el-scrollbar>
      </div>
    </el-dialog>

    <!-- 练习详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="练习详情"
      width="900px"
    >
      <div v-if="loading.detail" class="loading-container">
        <el-skeleton :rows="10" animated />
      </div>
      
      <div v-else-if="currentDetail" class="detail-content">
        <div class="detail-header">
          <div class="detail-meta">
            <div class="meta-item">
              <el-icon><Collection /></el-icon>
              <span>{{ getKnowledgeNameById(currentDetail.knowledge_id) }}</span>
            </div>
            <div class="meta-item">
              <el-icon><Calendar /></el-icon>
              <span>{{ formatDateTime(currentDetail.submit_time) }}</span>
            </div>
            <div class="meta-item">
              <el-icon><Timer /></el-icon>
              <span>用时: {{ formatDuration(currentDetail.time_spent) }}</span>
            </div>
            <el-tag :type="getResultTag(currentDetail.accuracy * 100)">
              正确率: {{ Math.round(currentDetail.accuracy * 100) }}%
            </el-tag>
          </div>
        </div>
        
        <div class="questions-detail">
          <div 
            v-for="(question, index) in currentDetail.questions" 
            :key="`detail_question_${index}_${question.id}_${question.type}`"
            class="detail-question-item"
            :class="{ correct: question.is_correct, incorrect: !question.is_correct }"
          >
            <div class="question-header">
              <div class="question-number">第 {{ index + 1 }} 题</div>
              <span class="result-status" :class="{ correct: question.is_correct, incorrect: !question.is_correct }">
                {{ question.is_correct ? '正确' : '错误' }}
              </span>
            </div>
            
            <div class="question-content">
              <div class="question-text">{{ question.text }}</div>
              <!-- 编程题显示编程语言 -->
              <div v-if="question.type === 'code'" class="question-language">
                <el-tag type="success" size="small">
                  <el-icon><Document /></el-icon>
                  编程语言: {{ getCodeLanguageName(question.code_language) }}
                </el-tag>
              </div>
            </div>
            
            <!-- 选择题详情 -->
            <div v-if="question.type === 'choice'" class="question-options">
              <template v-if="question.options && typeof question.options === 'object'">
                <!-- 处理平面对象格式 {A: '选项A', B: '选项B'} -->
                <div 
                  v-for="(value, key) in question.options" 
                  :key="key"
                  class="option-item"
                  :class="{
                    'correct': key === question.correct_answer,
                    'selected': key === question.student_answer
                  }"
                >
                  <span class="option-label">{{ key }}.</span>
                  <span class="option-text">{{ value }}</span>
                </div>
              </template>
            </div>

            <!-- 编程题详情 -->
            <div v-if="question.type === 'code'" class="code-question-detail">
              <div class="code-question-header">
                <el-tag type="info" size="small">编程题</el-tag>
              </div>
              
              <!-- 编程题代码展示 -->
              <div class="code-content">
                <div class="code-label">你的代码：</div>
                <div class="code-block" :class="{ 'error-code': !question.is_correct }">
                  <pre>{{ question.student_answer || '未提交代码' }}</pre>
                </div>
              </div>
              
              <!-- 编程题错误信息 -->
              <div v-if="!question.is_correct && question.code_error" class="code-error-info">
                <div class="error-title">
                  <el-icon><Warning /></el-icon>
                  代码执行错误
                </div>
                <div class="error-content">
                  <div class="error-message">{{ getCodeErrorMessage(question.code_error) }}</div>
                  <div v-if="question.error_details" class="error-details">
                    <pre>{{ question.error_details }}</pre>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 填空题详情 -->
            <div v-if="question.type === 'fill'" class="fill-question-detail">
              <div class="fill-question-header">
                <el-tag type="warning" size="small">填空题</el-tag>
              </div>
            </div>
            
            <!-- 答案对比 -->
            <div class="answer-comparison">
              <div class="comparison-title">答案对比</div>
              <div class="answer-item">
                <div class="answer-label">正确答案：</div>
                <div class="answer-content correct">{{ formatAnswer(question) }}</div>
              </div>
              <div class="answer-item">
                <div class="answer-label">你的答案：</div>
                <div class="answer-content" :class="{ correct: question.is_correct, incorrect: !question.is_correct }">
                  {{ question.student_answer || '未作答' }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { EditPen, Document, Check, CircleCheck, TrendCharts, Collection, Refresh, Calendar, Timer, Warning } from '@element-plus/icons-vue'
import { getPracticeQuestions, submitQuestionAnswer, getLearningStats, getKnowledgeNodes, getPracticeHistory, getPracticeDetail, getKnowledgeMastery } from '@/api/questions'

// 响应式数据
const showPracticeDialog = ref(false)
const showQuickPracticeDialog = ref(false)
const showDetailDialog = ref(false)
const showKnowledgeSelectDialog = ref(false) // 知识点选择对话框
const showResult = ref(false)
const selectedNode = ref(null)
const selectedAnswer = ref('')
const currentQuestionIndex = ref(0)
const currentQuestions = ref([])
const currentDetail = ref(null)
const remainingTime = ref(0)
const timer = ref(null)
const startTime = ref(0)
const knowledgeSearchQuery = ref('') // 知识点搜索关键词

// 加载状态
const loading = reactive({
  knowledge: false,
  history: false,
  questions: false,
  detail: false
})

// 保存每个题目的用户答案
const userAnswers = ref({})

// 统计数据
const stats = reactive({
  totalQuestions: 0,
  answeredQuestions: 0,
  correctAnswers: 0,
  accuracy: 0
})

// 练习结果
const result = reactive({
  correctCount: 0,
  totalCount: 0,
  accuracy: 0,
  duration: '',
  masteryUpdates: {}
})

// 数据
const knowledgeNodes = ref([])
const practiceHistory = ref([])
const knowledgeMastery = ref({})

// 过滤后的知识点列表
const filteredKnowledgeNodes = computed(() => {
  if (!knowledgeSearchQuery.value.trim()) {
    return knowledgeNodes.value
  }
  
  const query = knowledgeSearchQuery.value.toLowerCase().trim()
  return knowledgeNodes.value.filter(node => 
    node.name.toLowerCase().includes(query) || 
    (node.description && node.description.toLowerCase().includes(query))
  )
})

// 当前题目 - 添加详细调试
const currentQuestion = computed(() => {
  console.log('计算currentQuestion - 索引:', currentQuestionIndex.value)
  console.log('计算currentQuestion - 题目列表长度:', currentQuestions.value.length)
  
  if (currentQuestions.value.length === 0) {
    console.log('计算currentQuestion - 题目列表为空')
    return {}
  }
  
  if (currentQuestionIndex.value >= currentQuestions.value.length) {
    console.log('计算currentQuestion - 索引越界')
    return {}
  }
  
  const question = currentQuestions.value[currentQuestionIndex.value]
  console.log('计算currentQuestion - 当前题目:', question)
  
  if (!question) {
    console.log('计算currentQuestion - 题目不存在')
    return {}
  }
  
  return question
})

// 获取题目类型文本
const getQuestionTypeText = (type) => {
  const typeMap = {
    'choice': '选择题',
    'fill': '填空题',
    'code': '编程题'
  }
  return typeMap[type] || '未知类型'
}

// 获取节点类型名称
const getNodeTypeName = (type) => {
  const typeNames = {
    concept: '概念',
    skill: '技能',
    resource: '资源'
  }
  return typeNames[type] || type
}

// 获取节点类型标签
const getNodeTypeTag = (type) => {
  const typeTags = {
    concept: 'primary',
    skill: 'success',
    resource: 'warning'
  }
  return typeTags[type] || ''
}

// 获取题目数量
const getQuestionCount = (nodeId) => {
  if (!nodeId) return 0
  const node = knowledgeNodes.value.find(item => item.id === nodeId)
  if (!node) return 0
  if (typeof node.question_count === 'number') {
    return node.question_count
  }
  if (typeof node.questionCount === 'number') {
    return node.questionCount
  }
  if (node.statistics && typeof node.statistics.question_count === 'number') {
    return node.statistics.question_count
  }
  return 0
}

// 获取节点进度
const getNodeProgress = (nodeId) => {
  // 从掌握度数据中获取，如果没有则使用默认值
  const progress = knowledgeMastery.value[nodeId]?.progress || 0
  // 确保返回值在0-100之间
  return Math.round(Math.min(Math.max(progress, 0), 100))
}

// 获取进度颜色
const getProgressColor = (percentage) => {
  if (percentage >= 80) return '#67c23a'
  if (percentage >= 60) return '#e6a23c'
  return '#f56c6c'
}

// 获取难度标签
const getDifficultyTag = (difficulty) => {
  if (difficulty <= 0.3) return 'success'
  if (difficulty <= 0.7) return 'warning'
  return 'danger'
}

// 获取难度文本
const getDifficultyText = (difficulty) => {
  if (difficulty <= 0.3) return '简单'
  if (difficulty <= 0.7) return '中等'
  return '困难'
}

// 获取结果标签
const getResultTag = (accuracy) => {
  if (accuracy >= 80) return 'success'
  if (accuracy >= 60) return 'warning'
  return 'danger'
}

// 格式化日期时间
const formatDateTime = (dateString) => {
  try {
    const date = new Date(dateString)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateString
  }
}

// 格式化时间（秒转分:秒）
const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 格式化时长
const formatDuration = (seconds) => {
  if (seconds < 60) return `${seconds}秒`
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}分${remainingSeconds}秒`
}

// 根据ID获取知识点名称
const getKnowledgeNameById = (knowledgeId) => {
  // 特殊处理随机练习的情况
  if (knowledgeId === 'random') return '随机练习'
  const node = knowledgeNodes.value.find(n => n.id === knowledgeId)
  return node ? node.name : `知识点${knowledgeId}`
}

// 计算正确题目数量
const getCorrectCount = (record) => {
  // 如果有准确率字段，使用它来计算
  if (record.accuracy !== undefined) {
    // 检查是否有总题数字段（使用后端返回的total_questions字段名）
    if (record.total_questions) {
      return Math.round(record.total_questions * record.accuracy);
    }
    
    // 检查是否有results数组可以直接统计
    if (record.results && Array.isArray(record.results)) {
      return record.results.filter(r => r.is_correct).length;
    }
    
    // 根据系统实际情况，每次练习可能有4道题
    // 这里保留一个合理的默认值，但添加注释说明这是后备方案
    // 未来应该从API返回中获取准确的总题数
    const estimatedTotalQuestions = 4;
    return Math.round(record.accuracy * estimatedTotalQuestions);
  }
  
  // 如果所有方法都失败，返回0作为安全默认值
  return 0;
}

// 格式化答案显示
const formatAnswer = (question) => {
  if (question.type === 'choice') {
    // 检查options类型，如果是对象则直接访问，避免使用find方法
    if (typeof question.options === 'object' && question.options !== null) {
      const optionText = question.options[question.correct_answer] || ''
      return `${question.correct_answer}. ${optionText}`
    }
    return question.correct_answer
  } else if (question.type === 'code') {
    return '代码已提交，请查看代码执行结果'
  }
  return question.correct_answer
}

// 获取编程题代码编辑器占位符文本
const getCodePlaceholder = (codeLanguage) => {
  const placeholders = {
    'python': '请在此编写 Python 代码，并实现函数：solve(input_str: str) -> str',
    'c': '请在此编写 C 代码，并实现函数：char* solve(char* input_str)',
    'cpp': '请在此编写 C++ 代码，并实现函数：std::string solve(const std::string& input_str)',
    'java': '请在此编写 Java 代码，并在类中实现方法：public static String solve(String input_str)'
  }
  
  // 处理枚举值格式（如 "CodeLanguage.java"）
  if (codeLanguage && typeof codeLanguage === 'string') {
    let languageKey = codeLanguage
    // 如果包含点号，提取枚举值部分
    if (codeLanguage.includes('.')) {
      languageKey = codeLanguage.split('.').pop()
      
    }
    return placeholders[languageKey] || placeholders.python
  }
  
  return placeholders.python
}

// 获取编程题提示信息
const getCodeTips = (codeLanguage) => {
  const tips = {
    'python': '系统会使用多个隐藏测试用例调用 solve(input_str)，每个用例的返回值与标准输出完全一致时，该编程题才判定为正确。',
    'c': '系统会使用多个隐藏测试用例调用 solve(input_str)，每个用例的返回值与标准输出完全一致时，该编程题才判定为正确。请使用malloc动态分配内存并返回结果。',
    'cpp': '系统会使用多个隐藏测试用例调用 solve(input_str)，每个用例的返回值与标准输出完全一致时，该编程题才判定为正确。请使用std::string处理字符串。',
    'java': '系统会使用多个隐藏测试用例调用 solve(input_str)，每个用例的返回值与标准输出完全一致时，该编程题才判定为正确。请在类中实现静态方法。'
  }
  
  // 处理枚举值格式（如 "CodeLanguage.java"）
  if (codeLanguage && typeof codeLanguage === 'string') {
    let languageKey = codeLanguage
    // 如果包含点号，提取枚举值部分
    if (codeLanguage.includes('.')) {
      languageKey = codeLanguage.split('.').pop()
      
    }
    return tips[languageKey] || tips.python
  }
  
  return tips.python
}

// 获取编程语言名称
const getCodeLanguageName = (codeLanguage) => {
  const languageNames = {
    'python': 'Python',
    'c': 'C语言',
    'cpp': 'C++',
    'java': 'Java'
  }
  
  // 处理枚举值格式（如 "CodeLanguage.java"）
  if (codeLanguage && typeof codeLanguage === 'string') {
    // 如果包含点号，提取枚举值部分
    if (codeLanguage.includes('.')) {
      const enumValue = codeLanguage.split('.').pop()
      
      return languageNames[enumValue] || 'Python'
    }
    // 直接使用原始值
    return languageNames[codeLanguage] || 'Python'
  }
  
  return 'Python'
}

// 获取编程题错误信息
const getCodeErrorMessage = (errorCode) => {
  const errorMessages = {
    'syntax_error': '语法错误：代码存在语法问题，请检查语法是否正确',
    'undefined_solve': '未定义solve函数：请确保定义了solve(input_str)函数',
    'test_case_failed': '测试用例未通过：您的代码未通过某些测试用例，请检查算法逻辑',
    'runtime_error': '运行时错误：代码执行过程中发生错误，请检查代码逻辑',
    'timeout_error': '执行超时：代码运行时间超过限制，请优化算法效率',
    'import_error': '模块导入错误：请检查是否正确导入了所需的模块',
    'function_error': '函数定义错误：请确保函数名称和参数正确',
    'input_error': '输入处理错误：请确保正确处理输入参数',
    'output_error': '输出格式错误：请确保输出格式符合要求'
  }
  
  return errorMessages[errorCode] || `代码执行失败：${errorCode}`
}

// 加载知识点
const loadKnowledgeNodes = async () => {
  loading.knowledge = true
  try {
    const response = await getKnowledgeNodes()
    if (response?.code === 200 && Array.isArray(response.data)) {
      knowledgeNodes.value = response.data
    } else if (response?.data?.code === 200 && Array.isArray(response.data.data)) {
      knowledgeNodes.value = response.data.data
    } else {
      knowledgeNodes.value = []
    }
    
    // 加载每个知识点的掌握度
    for (const node of knowledgeNodes.value) {
      try {
        const masteryResponse = await getKnowledgeMastery(node.id)
        knowledgeMastery.value[node.id] = masteryResponse.data.data
      } catch (error) {
        // 如果获取失败，使用默认值
        knowledgeMastery.value[node.id] = { progress: 0 }
      }
    }
  } catch (error) {
    ElMessage.error('加载知识点失败')
    knowledgeNodes.value = []
  } finally {
    loading.knowledge = false
  }
}

// 加载练习历史
const loadPracticeHistory = async () => {
  loading.history = true
  try {
    const response = await getPracticeHistory()
    console.log('练习历史响应:', response)
    // 根据API实际返回的结构访问数据
    practiceHistory.value = response.data?.list || []
  } catch (error) {
    console.error('加载练习历史错误:', error)
    // 从错误响应中获取更详细的错误信息
    const errorMsg = error.response?.data?.message || '加载练习历史失败'
    ElMessage.error(errorMsg)
    practiceHistory.value = []
  } finally {
    loading.history = false
  }
}

// 加载学习统计
const loadStats = async () => {
  try {
    console.log('开始加载学习统计数据...')
    const response = await getLearningStats()
    console.log('学习统计响应完整结构:', JSON.stringify(response, null, 2))
    
    // 增强的响应数据检查，处理多种可能的响应格式
    let hasValidStats = false
    
    if (response) {
      // 检查响应格式类型1: {data: {code: 200, data: {统计数据}}}
      if (response.data && response.data.code === 200 && response.data.data) {
        const statsData = response.data.data
        console.log('从响应格式1获取统计数据:', statsData)
        
        // 验证统计数据是否有实际值
        if (statsData.answeredQuestions > 0 || statsData.correctAnswers > 0 || statsData.accuracy > 0) {
          hasValidStats = true
        }
        
        stats.totalQuestions = statsData.totalQuestions || 0 // 按真实数据显示
        stats.answeredQuestions = statsData.answeredQuestions || 0
        stats.correctAnswers = statsData.correctAnswers || 0
        stats.accuracy = statsData.accuracy || 0
      }
      // 检查响应格式类型2: {code: 200, data: {统计数据}}
      else if (response.code === 200 && response.data) {
        console.log('从响应格式2获取统计数据:', response.data)
        
        if (response.data.answeredQuestions > 0 || response.data.correctAnswers > 0 || response.data.accuracy > 0) {
          hasValidStats = true
        }
        
        stats.totalQuestions = response.data.totalQuestions || 0
        stats.answeredQuestions = response.data.answeredQuestions || 0
        stats.correctAnswers = response.data.correctAnswers || 0
        stats.accuracy = response.data.accuracy || 0
      }
      // 检查响应格式类型3: 直接是统计数据对象
      else if (response.totalQuestions !== undefined) {
        console.log('从响应格式3获取统计数据:', response)
        
        if (response.answeredQuestions > 0 || response.correctAnswers > 0 || response.accuracy > 0) {
          hasValidStats = true
        }
        
        stats.totalQuestions = response.totalQuestions || 0
        stats.answeredQuestions = response.answeredQuestions || 0
        stats.correctAnswers = response.correctAnswers || 0
        stats.accuracy = response.accuracy || 0
      }
      else {
        console.warn('无法识别的响应格式:', response)
      }
    }
    
    // 如果API返回的统计数据无效（都是0），尝试从练习历史计算
    if (!hasValidStats) {
      console.log('API返回的统计数据无效或全为0，尝试从练习历史计算...')
      
      // 尝试使用练习历史手动计算统计数据
      try {
        console.log('尝试从练习历史手动计算统计数据...')
        if (practiceHistory.value && practiceHistory.value.length > 0) {
          let totalAnswered = 0
          let totalCorrect = 0
          
          for (const record of practiceHistory.value) {
            if (record && record.accuracy !== undefined) {
              console.log('处理历史记录:', JSON.stringify(record, null, 2))
              
              // 使用记录中的实际题目数，如果没有则默认为4
              const recordQuestions = record.total_questions || 4
              
              // 处理不同类型的accuracy值
              let recordCorrect = 0
              let accuracyValue = record.accuracy
              console.log(`本地计算 - Accuracy值: ${accuracyValue}`)
              
              if (typeof accuracyValue === 'number') {
                // 特殊处理: 如果accuracy是1，应该表示100%正确
                if (accuracyValue === 1) {
                  recordCorrect = recordQuestions // 全部正确
                  console.log('本地计算 - Accuracy为1，设置全部题目正确')
                } else {
                  // 检查是否是百分比
                  if (accuracyValue >= 1 && accuracyValue <= 100) {
                    accuracyValue = accuracyValue / 100
                  }
                  recordCorrect = Math.round(recordQuestions * accuracyValue)
                }
              } else {
                accuracyValue = 0
                recordCorrect = 0
              }
              
              console.log(`记录计算: 题目数=${recordQuestions}, 正确率=${accuracyValue}, 正确数=${recordCorrect}`)
              totalAnswered += recordQuestions
              totalCorrect += recordCorrect
              
              console.log(`记录计算: 题目数=${recordQuestions}, 正确率=${accuracyValue}, 正确数=${recordCorrect}`)
            }
          }
          
          if (totalAnswered > 0) {
            stats.answeredQuestions = totalAnswered
            stats.correctAnswers = totalCorrect
            stats.accuracy = Math.round((totalCorrect / totalAnswered) * 100)
            hasValidStats = true
            console.log('从练习历史手动计算的统计数据:', { ...stats })
          }
        }
      } catch (calcError) {
        console.error('手动计算统计数据失败:', calcError)
      }
    }
    
    console.log('最终更新的统计数据:', { ...stats })
    
    // 按真实数据显示总题目数，不再强制设置最小值
    
    // 强制Vue更新UI
    nextTick(() => {
      console.log('UI已更新，统计数据应显示正确值')
    })
    
  } catch (error) {
    console.error('加载统计数据失败:', error)
    console.error('错误详情:', error.response || error)
  }
}

// 知识点练习
const practiceByNode = async (node) => {
  selectedNode.value = node
  showQuickPracticeDialog.value = false
  await loadQuestions(node.id)
}

// 快速练习-知识点练习
const startKnowledgePractice = () => {
  showQuickPracticeDialog.value = false
  // 显示知识点选择对话框
  if (knowledgeNodes.value.length > 0) {
    showKnowledgeSelectDialog.value = true
  } else {
    ElMessage.warning('请先加载知识点数据')
  }
}

// 选择知识点并开始练习
const confirmKnowledgeSelection = (node) => {
  selectedNode.value = node
  showKnowledgeSelectDialog.value = false
  loadQuestions(node.id)
}

// 快速练习-随机练习
const startRandomPractice = async () => {
  showQuickPracticeDialog.value = false
  selectedNode.value = null
  
  // 对于随机练习，使用特殊标识符'random'来获取任意知识点的随机题目
  // 这样后端可以更灵活地处理随机练习的情况
  await loadQuestions('random')
}

// 加载题目
const loadQuestions = async (knowledgeId) => {
  loading.questions = true
  try {
    console.log('加载知识点ID:', knowledgeId, '的题目')
    const response = await getPracticeQuestions(knowledgeId)
    console.log('题目加载响应类型:', typeof response)
    console.log('题目加载响应完整结构:', JSON.stringify(response, null, 2))
    console.log('响应数据结构检查 - response.code:', response.code)
    console.log('响应数据结构检查 - response.data:', response.data)
    console.log('响应数据结构检查 - response.data?.list:', response.data?.list)
    console.log('响应数据结构检查 - 是否有list属性:', 'list' in response)
    console.log('响应数据结构检查 - 是否有data属性:', 'data' in response)
    
    // 基于后端返回的实际数据格式: {code: 200, message: '题目获取成功', data: {count: 4, list: Array(4)}}
    // 由于axios响应拦截器，response已经是处理后的数据对象
    const rawQuestions = response.data && response.data.list ? response.data.list : []
    console.log('原始题目数据数量:', rawQuestions.length)
    console.log('原始题目数据:', rawQuestions)
    
    // 处理题目数据，确保格式正确
    const processedQuestions = []
    for (let i = 0; i < rawQuestions.length; i++) {
      try {
        const q = rawQuestions[i]
        console.log(`处理第${i+1}道题目:`, q)
        
        // 安全处理options字段
        let safeOptions = null
        try {
          if (q.options) {
            // 如果options是字符串，尝试解析为JSON
            if (typeof q.options === 'string' && (q.options.startsWith('{') || q.options.startsWith('['))) {
              safeOptions = JSON.parse(q.options)
            } else {
              safeOptions = q.options
            }
          }
        } catch (e) {
          console.warn('解析options失败:', e)
          safeOptions = null
        }
        
        // 安全处理knowledge_id字段
        let safeKnowledgeId = []
        try {
          if (q.knowledge_id) {
            if (typeof q.knowledge_id === 'string' && (q.knowledge_id.startsWith('{') || q.knowledge_id.startsWith('['))) {
              const parsed = JSON.parse(q.knowledge_id)
              safeKnowledgeId = Array.isArray(parsed) ? parsed : [parsed]
            } else if (Array.isArray(q.knowledge_id)) {
              safeKnowledgeId = q.knowledge_id
            } else {
              safeKnowledgeId = [q.knowledge_id]
            }
          }
        } catch (e) {
          console.warn('解析knowledge_id失败:', e)
          safeKnowledgeId = []
        }
        
        const processedQ = {
          question_id: q.question_id || `unknown_${Math.random()}`,
          text: q.text || '题目文本缺失',
          type: q.type || 'unknown',
          options: safeOptions,
          knowledge_id: safeKnowledgeId,
          difficulty: q.difficulty || 1,
          // 只保留后端返回的code_language字段，不设置默认值
          ...(q.code_language !== undefined && { code_language: q.code_language })
        }
        
        processedQuestions.push(processedQ)
        console.log(`成功处理第${i+1}道题目`, processedQ)
      } catch (e) {
        console.error(`处理第${i+1}道题目时出错:`, e)
      }
    }
    
    currentQuestions.value = processedQuestions
    console.log('处理后的题目数量:', currentQuestions.value.length)
    
    // 对于随机练习和知识点练习使用不同的提示信息
    if (currentQuestions.value.length === 0) {
      const warningMessage = knowledgeId === 'random' ? '当前系统暂无可用题目' : '当前知识点暂无题目'
      console.log('警告: ' + warningMessage)
      ElMessage.warning(warningMessage)
      return
    } else {
      console.log('成功加载到题目，数量:', currentQuestions.value.length)
      console.log('题目详情:', currentQuestions.value)
    }
    
    // 重置状态
    currentQuestionIndex.value = 0
    selectedAnswer.value = ''
    userAnswers.value = {}
    showResult.value = false
    remainingTime.value = 1800 // 30分钟
    startTime.value = Date.now()
    
    // 强制设置showPracticeDialog为true，确保对话框显示
    console.log('设置showPracticeDialog为true')
    showPracticeDialog.value = true
    
    // 确保有题目可显示
    if (currentQuestions.value.length > 0) {
      console.log('确认有题目，当前索引:', currentQuestionIndex.value)
      console.log('当前题目:', currentQuestions.value[currentQuestionIndex.value])
    }
    
    // 开始计时
    startTimer()
  } catch (error) {
    console.error('加载题目错误详情:', error)
    // 从错误响应中获取更详细的错误信息
    let errorMsg = '加载题目失败'
    if (error.response) {
      errorMsg = error.response.data?.message || errorMsg
    } else if (error.message) {
      errorMsg = error.message
    }
    ElMessage.error(errorMsg)
  } finally {
    loading.questions = false
  }
}

// 开始计时
const startTimer = () => {
  stopTimer() // 确保之前的计时器已停止
  timer.value = setInterval(() => {
    if (remainingTime.value > 0) {
      remainingTime.value--
    } else {
      // 时间到，自动提交所有答案
      finishPractice()
    }
  }, 1000)
}

// 停止计时
const stopTimer = () => {
  if (timer.value) {
    clearInterval(timer.value)
    timer.value = null
  }
}

// 选择答案
const selectAnswer = (answer) => {
  // 如果点击的是已选中的选项，则取消选择
  if (selectedAnswer.value === answer) {
    selectedAnswer.value = ''
    // 保存当前题目的答案（清空）
    const question = currentQuestions.value[currentQuestionIndex.value]
    if (question) {
      userAnswers.value[question.question_id] = ''
    }
  } else {
    selectedAnswer.value = answer
    // 保存当前题目的答案
    const question = currentQuestions.value[currentQuestionIndex.value]
    if (question) {
      userAnswers.value[question.question_id] = answer
    }
  }
}

// 提交答案（当前题目）
const submitAnswer = () => {
  if (!selectedAnswer.value.trim()) {
    ElMessage.warning('请选择或输入答案')
    return
  }
  
  const question = currentQuestions.value[currentQuestionIndex.value]
  
  // 保存当前题目的答案
  userAnswers.value[question.question_id] = selectedAnswer.value
  
  // 下一题
  nextQuestion()
}

// 跳过题目
const skipQuestion = () => {
  nextQuestion()
}

// 下一题
const nextQuestion = () => {
  currentQuestionIndex.value++
  
  // 加载下一题的已保存答案（如果有）
  if (currentQuestionIndex.value < currentQuestions.value.length) {
    const nextQuestion = currentQuestions.value[currentQuestionIndex.value]
    selectedAnswer.value = userAnswers.value[nextQuestion.question_id] || ''
  } else {
    // 练习完成
    finishPractice()
  }
}

// 完成练习并提交所有答案
const finishPractice = async () => {
  stopTimer()
  
  try {
    // 计算用时
    const timeSpent = Math.floor((Date.now() - startTime.value) / 1000)
    
    // 构建答案数据并统一提交
    const answers = Object.entries(userAnswers.value).map(([questionId, answer]) => {
      return {
        question_id: parseInt(questionId),
        student_answer: answer
      }
    })
    
    // 调用API提交所有答案，添加knowledge_id参数以区分随机练习
    const response = await submitQuestionAnswer({
      answers,
      time_spent: timeSpent,
      knowledge_id: selectedNode?.id || 'random'
    })
    
    // 处理响应结果
    if (response.code === 200) {
      const data = response.data
      result.accuracy = Math.round(data.accuracy * 100)
      result.duration = formatDuration(timeSpent)
      result.totalCount = answers.length
      
      // 计算正确题数
      result.correctCount = data.results.filter(r => r.is_correct).length
      
      // 保存掌握度更新
      result.masteryUpdates = data.mastery || {}
      
      // 更新练习历史和统计数据
      await Promise.all([
        loadPracticeHistory(),
        loadStats()
      ])
      
    } else {
      ElMessage.error(response.message || '提交答案失败')
    }
    
  } catch (error) {
    ElMessage.error('提交练习结果失败')
  }
  
  showResult.value = true
}

// 重新练习
const restartPractice = () => {
  result.correctCount = 0
  result.totalCount = 0
  result.accuracy = 0
  result.masteryUpdates = {}
  showResult.value = false
  currentQuestionIndex.value = 0
  selectedAnswer.value = ''
  userAnswers.value = {}
  remainingTime.value = 1800
  startTime.value = Date.now()
  startTimer()
}

// 继续练习
const continuePractice = () => {
  showPracticeDialog.value = false
  selectedNode.value = null
  showResult.value = false
  stopTimer()
}

// 关闭练习对话框
const handleClosePractice = () => {
  if (showResult.value) {
    continuePractice()
  } else {
    ElMessageBox.confirm('确定要退出练习吗？未完成的练习将不会保存。', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      continuePractice()
    }).catch(() => {
      // 用户取消
    })
  }
}

// 查看练习详情
const viewPracticeDetail = async (record) => {
  loading.detail = true
  try {
    console.log('请求查看练习详情:', record.record_id)
    const response = await getPracticeDetail(record.record_id)
    console.log('练习详情响应:', response)
    
    // 直接检查response对象的code属性，因为后端返回的结构是{code, message, data}
    if (response.code === 200) {
      currentDetail.value = response.data
      showDetailDialog.value = true
    } else if (response.code === 403) {
      ElMessage.warning('您只能查看自己的练习记录')
    } else if (response.code === 404) {
      ElMessage.warning('练习记录不存在或已被删除')
    } else {
      ElMessage.error(response.message || '加载练习详情失败')
    }
  } catch (error) {
    console.error('加载练习详情错误:', error)
    
    // 处理不同类型的错误
    if (error.response?.status === 403) {
      ElMessage.warning('您只能查看自己的练习记录')
    } else if (error.response?.status === 404) {
      ElMessage.warning('练习记录不存在或已被删除')
    } else {
      ElMessage.error('加载练习详情失败')
    }
    currentDetail.value = null
  } finally {
    loading.detail = false
  }
}

// 生命周期钩子
onMounted(() => {
  // 初始化加载数据
  loadKnowledgeNodes()
  loadPracticeHistory()
  loadStats()
})

onUnmounted(() => {
  stopTimer()
})
</script>

<style lang="scss" scoped>
.questions-container {
  padding: 20px;
  min-height: calc(100vh - 60px);
  background-color: #f0f2f5;
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
      font-size: 24px;
    }
    
    p {
      margin: 0;
      color: #666;
      font-size: 14px;
    }
  }
  
  .quick-practice-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    &:hover {
      background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
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
      
      &.total {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      }
      
      &.answered {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      }
      
      &.correct {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      }
      
      &.accuracy {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.master-list {
  .master-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border: 1px solid #e4e7ed;
    border-radius: 8px;
    margin-bottom: 12px;
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      border-color: #409eff;
      box-shadow: 0 2px 8px rgba(64, 158, 255, 0.2);
    }
    
    .master-info {
      flex: 1;
      
      h4 {
        margin: 0 0 8px 0;
        color: #333;
      }
      
      p {
        margin: 0 0 8px 0;
        color: #666;
        font-size: 14px;
      }
      
      .master-meta {
        display: flex;
        align-items: center;
        gap: 8px;
        
        .question-count {
          font-size: 12px;
          color: #999;
        }
      }
    }
    
    .master-progress {
      width: 160px;
      margin-left: 16px;
      
      .progress-label {
        font-size: 12px;
        color: #666;
        margin-bottom: 4px;
        text-align: right;
      }
    }
  }
}

.practice-history {
  .history-item {
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
    
    .history-info {
      flex: 1;
      
      .history-title {
        font-weight: 500;
        color: #333;
        margin-bottom: 4px;
      }
      
      .history-meta {
        display: flex;
        gap: 12px;
        font-size: 12px;
        color: #666;
      }
    }
    
    .history-result {
      display: flex;
      align-items: center;
      gap: 8px;
      
      .history-score {
        font-size: 12px;
        color: #666;
      }
    }
  }
}

.practice-mode-selection {
  padding: 30px 0;
  
  .mode-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 24px;
    
    .mode-item {
      text-align: center;
      padding: 24px;
      border: 2px solid #e4e7ed;
      border-radius: 12px;
      cursor: pointer;
      transition: all 0.3s;
      
      &:hover {
        border-color: #409eff;
        box-shadow: 0 4px 16px rgba(64, 158, 255, 0.2);
        transform: translateY(-2px);
      }
      
      .mode-icon {
        width: 64px;
        height: 64px;
        background-color: #f0f9ff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 16px;
        font-size: 32px;
        color: #409eff;
      }
      
      h4 {
        margin: 0 0 8px 0;
        font-size: 18px;
        color: #333;
      }
      
      p {
        margin: 0;
        font-size: 14px;
        color: #666;
      }
    }
  }
}

.practice-content {
  .practice-progress {
    margin-bottom: 20px;
    
    .progress-info {
      display: flex;
      justify-content: space-between;
      margin-top: 8px;
      font-size: 14px;
      color: #666;
    }
  }
  
  .question-content {
    margin-bottom: 20px;
    
    .question-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      
      h3 {
        margin: 0;
        color: #333;
      }
      
      .question-type {
        font-size: 12px;
        padding: 4px 12px;
        background-color: #f0f9ff;
        color: #409eff;
        border-radius: 12px;
      }
    }
    
    .question-body {
      .question-text {
        font-size: 16px;
        line-height: 1.6;
        color: #333;
        margin-bottom: 20px;
      }
      
      .option-item {
        display: flex;
        align-items: flex-start;
        padding: 12px 16px;
        border: 1px solid #e4e7ed;
        border-radius: 6px;
        margin-bottom: 12px;
        cursor: pointer;
        transition: all 0.3s;
        
        &:hover {
          border-color: #409eff;
          background-color: #f5f7fa;
        }
        
        &.selected {
          border-color: #409eff;
          background-color: #ecf5ff;
        }
      }
      
      .option-label {
        font-size: 16px;
        font-weight: 500;
        color: #333;
        margin-right: 12px;
        min-width: 24px;
      }
      
      .option-text {
        flex: 1;
        font-size: 16px;
        color: #333;
        line-height: 1.5;
      }
    }
  }
}

.knowledge-selection {
  .knowledge-item {
    cursor: pointer;
    padding: 16px;
    border: 2px solid transparent;
    border-radius: 8px;
    margin-bottom: 12px;
    transition: all 0.3s;
    
    &:hover {
      border-color: #409eff;
      background-color: #f5f7fa;
    }
    
    .knowledge-info {
      h4 {
        margin: 0 0 8px 0;
        color: #333;
        font-size: 16px;
      }
      
      p {
        margin: 0 0 12px 0;
        color: #666;
        font-size: 14px;
        line-height: 1.5;
      }
      
      .knowledge-meta {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
        
        .question-count {
          font-size: 12px;
          color: #909399;
        }
      }
    }
    
    .knowledge-progress {
      .progress-label {
        font-size: 12px;
        color: #606266;
        margin-bottom: 4px;
      }
    }
  }
}

      

.practice-result {
  text-align: center;
  
  .result-header {
    margin-bottom: 24px;
    
    h3 {
      margin: 0 0 8px 0;
      color: #333;
      font-size: 24px;
    }
    
    p {
      margin: 0;
      color: #666;
      font-size: 16px;
    }
  }
  
  .result-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 24px;
    
    .stat-item {
      text-align: center;
      
      .stat-value {
        font-size: 32px;
        font-weight: bold;
        color: #409eff;
        margin-bottom: 8px;
      }
      
      .stat-label {
        font-size: 14px;
        color: #666;
      }
    }
  }
  
  .mastery-updates {
    margin: 24px 0;
    
    h4 {
      text-align: left;
      margin: 0 0 16px 0;
      font-size: 16px;
      color: #333;
    }
    
    .mastery-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      
      .mastery-item {
        display: flex;
        align-items: center;
        gap: 16px;
        
        .knowledge-name {
          min-width: 150px;
          font-size: 14px;
          color: #333;
        }
        
        .progress-wrapper {
          flex: 1;
        }
        
        .change-indicator {
          min-width: 80px;
          text-align: right;
          font-size: 14px;
          font-weight: 500;
          color: #f56c6c;
          
          &.positive {
            color: #67c23a;
          }
        }
      }
    }
  }
  
  .result-actions {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 32px;
  }
}

.detail-content {
  .detail-header {
    margin-bottom: 24px;
    
    .detail-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 16px;
      
      .meta-item {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 14px;
        color: #666;
      }
    }
  }
  
  .questions-detail {
    max-height: 60vh;
    overflow-y: auto;
    
    .detail-question-item {
      padding: 16px;
      border-radius: 8px;
      border: 2px solid #e4e7ed;
      margin-bottom: 16px;
      
      &.correct {
        border-color: #67c23a;
        background-color: #f0f9eb;
      }
      
      &.incorrect {
        border-color: #f56c6c;
        background-color: #fef0f0;
      }
      
      .question-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        
        .question-number {
          font-weight: 500;
          color: #333;
        }
        
        .result-status {
          font-size: 12px;
          padding: 2px 8px;
          border-radius: 10px;
          
          &.correct {
            background-color: #67c23a;
            color: white;
          }
          
          &.incorrect {
            background-color: #f56c6c;
            color: white;
          }
        }
      }
      
      .question-content {
        margin-bottom: 16px;
        
        .question-text {
          font-size: 15px;
          line-height: 1.5;
          color: #333;
        }
        
        .question-language {
          margin-top: 8px;
          
          .el-tag {
            font-size: 12px;
            padding: 4px 8px;
            
            .el-icon {
              margin-right: 4px;
            }
          }
        }
      }
      
      .answer-comparison {
        background-color: white;
        border-radius: 6px;
        padding: 12px;
        
        .comparison-title {
          font-size: 14px;
          font-weight: 500;
          color: #333;
          margin-bottom: 8px;
        }
        
        .answer-item {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          margin-bottom: 8px;
          
          &:last-child {
            margin-bottom: 0;
          }
          
          .answer-label {
            min-width: 80px;
            font-size: 13px;
            font-weight: 500;
            color: #666;
          }
          
          .answer-content {
            flex: 1;
            font-size: 13px;
            color: #333;
            
            &.correct {
              color: #67c23a;
            }
            
            &.incorrect {
              color: #f56c6c;
            }
          }
        }
      }
      
      // 编程题样式
      .code-question-detail {
        .code-question-header {
          margin-bottom: 12px;
        }
        
        .code-content {
          margin-bottom: 16px;
          
          .code-label {
            font-size: 14px;
            font-weight: 500;
            color: #333;
            margin-bottom: 8px;
          }
          
          .code-block {
            background-color: #f5f7fa;
            border: 1px solid #e4e7ed;
            border-radius: 6px;
            padding: 12px;
            overflow-x: auto;
            
            pre {
              margin: 0;
              font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
              font-size: 13px;
              line-height: 1.4;
              color: #333;
              white-space: pre-wrap;
              word-wrap: break-word;
            }
            
            &.error-code {
              border-color: #f56c6c;
              background-color: #fef0f0;
            }
          }
        }
        
        .code-error-info {
          background-color: #fef0f0;
          border: 1px solid #f56c6c;
          border-radius: 6px;
          padding: 12px;
          margin-bottom: 16px;
          
          .error-title {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 14px;
            font-weight: 500;
            color: #f56c6c;
            margin-bottom: 8px;
          }
          
          .error-content {
            .error-message {
              font-size: 13px;
              color: #f56c6c;
              margin-bottom: 8px;
            }
            
            .error-details {
              background-color: #fff;
              border-radius: 4px;
              padding: 8px;
              overflow-x: auto;
              
              pre {
                margin: 0;
                font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                font-size: 12px;
                line-height: 1.3;
                color: #666;
              }
            }
          }
        }
      }
      
      // 填空题样式
      .fill-question-detail {
        .fill-question-header {
          margin-bottom: 12px;
        }
      }
    }
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .questions-container {
    padding: 12px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .result-stats {
    grid-template-columns: repeat(2, 1fr) !important;
  }
  
  .mastery-item {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 8px !important;
    
    .knowledge-name,
    .change-indicator {
      min-width: unset !important;
      text-align: left !important;
    }
  }
  
  .mode-grid {
    grid-template-columns: 1fr !important;
  }
  
  .detail-meta {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
