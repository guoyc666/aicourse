<template>
  <div class="student-progress-container">
    <el-card class="page-card">
      <template #header>
        <div class="card-header">
          <span>学生学习状况</span>
        </div>
      </template>

      <!-- 筛选条件 -->
      <div class="filter-section">
        <el-form :inline="true" size="small">
          <el-form-item label="学生姓名">
            <el-input v-model="searchParams.studentName" placeholder="请输入学生姓名" clearable />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="searchStudents">查询</el-button>
            <el-button @click="resetFilters">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 学生列表表格 -->
      <div class="table-section">
        <el-table
          v-loading="loading"
          :data="studentsData"
          style="width: 100%"
          @row-click="viewStudentDetail"
        >
          <el-table-column prop="studentId" label="学生ID" width="100" />
          <el-table-column prop="studentName" label="学生姓名" width="120" />
          <el-table-column prop="totalQuestions" label="答题数" width="100" />
          <el-table-column prop="accuracyRate" label="正确率" width="120">
            <template #default="scope">
              <span>{{ scope.row.accuracyRate }}%</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click.stop="viewStudentDetail(scope.row)">详情</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 分页 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 学生详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="`学生详情 - ${currentStudent?.studentName}`"
      width="80%"
    >
      <div v-if="currentStudent" class="student-detail">
        <div class="detail-header">
          <div class="student-info">
            <h3>{{ currentStudent.studentName }}</h3>
            <p>学号：{{ currentStudent.studentId }}</p>
            <p>平均成绩：{{ currentStudent.averageScore.toFixed(1) }}</p>
            <p>答题数：{{ currentStudent.totalQuestions }} | 正确率：{{ currentStudent.accuracyRate }}%</p>
          </div>
        </div>

        <el-tabs v-model="activeTab">
          <el-tab-pane label="学习记录">
            <el-table :data="currentStudent.learningRecords" style="width: 100%">
              <el-table-column prop="contentType" label="内容类型" width="100" />
              <el-table-column prop="contentName" label="内容名称" />
              <el-table-column prop="accessTime" label="访问时间" width="180">
                <template #default="scope">
                  <span>{{ formatDate(scope.row.accessTime) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="duration" label="学习时长(分钟)" width="120" />
              <el-table-column prop="score" label="得分" width="80">
                <template #default="scope">
                  <span v-if="scope.row.score !== null">{{ scope.row.score }}</span>
                  <span v-else>-</span>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <!-- 新增答题记录标签页 -->
          <el-tab-pane label="答题记录">
            <div class="question-records-section">
              <div class="records-stats" v-if="currentStudent.totalQuestions > 0">
                <el-statistic title="总答题数" :value="currentStudent.totalQuestions" suffix="题" />
                <el-statistic title="正确题数" :value="currentStudent.totalCorrect" suffix="题" />
                <el-statistic title="正确率" :value="currentStudent.accuracyRate" suffix="%" />
              </div>
              <el-empty v-else description="暂无答题记录" />
              
              <!-- 答题记录详情表格 -->
              <el-table v-if="currentStudent.records && currentStudent.records.length > 0" :data="currentStudent.records" style="width: 100%; margin-top: 20px">
                <el-table-column prop="knowledge_name" label="知识点" min-width="120">
                  <template #default="scope">
                    <span>{{ scope.row.knowledge_name || scope.row.topic_name || scope.row.knowledge_id || '综合练习' }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="答题时间" width="180">
                  <template #default="scope">
                    <span>{{ formatDate(scope.row.submit_time || scope.row.created_at || scope.row.timestamp) }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="答题时长" width="100">
                  <template #default="scope">
                    <span>{{ Math.round((scope.row.time_spent || scope.row.duration || scope.row.learning_time || 0) / 60) }}分钟</span>
                  </template>
                </el-table-column>
                <el-table-column label="题目数量" width="100">
                  <template #default="scope">
                    <span>{{ getQuestionCount(scope.row) }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="正确题数" width="100">
                  <template #default="scope">
                    <span>{{ getCorrectCount(scope.row) }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="正确率" width="100">
                  <template #default="scope">
                    <span>{{ getAccuracyRate(scope.row) }}%</span>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>

      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getUsers } from '@/api/users'
import request from '@/api/request'

// 搜索参数
const searchParams = reactive({
  studentName: '',
  contentType: ''
})

// 日期范围
const dateRange = ref([])

// 分页信息
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 学生数据
const studentsData = ref([])
const loading = ref(false)

// 详情对话框
const detailDialogVisible = ref(false)
const currentStudent = ref(null)
const activeTab = ref('0')

// 获取学生答题记录的函数
const getStudentQuestionRecords = async (userId) => {
  if (!userId) {
    return {
      totalQuestions: 0,
      totalCorrect: 0,
      accuracyRate: 0,
      records: [],
      learningRecords: []
    }
  }

  try {
    const response = await request.get('/api/question/record/list', {
      params: {
        user_id: userId,
        limit: 100
      }
    })

    let practiceHistory = []
    if (Array.isArray(response?.data?.list)) {
      practiceHistory = response.data.list
    } else if (Array.isArray(response?.data?.data?.list)) {
      practiceHistory = response.data.data.list
    } else if (Array.isArray(response?.data)) {
      practiceHistory = response.data
    } else if (Array.isArray(response?.list)) {
      practiceHistory = response.list
    } else if (Array.isArray(response)) {
      practiceHistory = response
    }

    const normalizedRecords = practiceHistory.map(record => ({
      ...record,
      knowledge_name: record?.knowledge_name || record?.knowledge_id || '综合练习'
    }))

    let totalQuestions = 0
    let totalCorrect = 0

    const learningRecords = normalizedRecords.map(record => {
      const questionsCount = Number(record?.total_questions) || (Array.isArray(record?.questions) ? record.questions.length : 0)
      const accuracyValue = typeof record?.accuracy === 'number'
        ? (record.accuracy > 1 ? record.accuracy / 100 : record.accuracy)
        : 0
      const correctCount = Math.round(questionsCount * accuracyValue)

      totalQuestions += questionsCount
      totalCorrect += correctCount

      return {
        contentType: 'question',
        contentName: `答题练习 - ${record?.knowledge_name || record?.knowledge_id || '综合练习'}`,
        accessTime: record?.submit_time || record?.created_at || record?.timestamp || new Date().toISOString(),
        duration: Math.round((record?.time_spent ?? record?.duration ?? 0) / 60),
        score: questionsCount > 0 ? Math.round((correctCount / questionsCount) * 100) : 0,
        totalQuestions: questionsCount,
        correctQuestions: correctCount
      }
    })

    return {
      totalQuestions,
      totalCorrect,
      accuracyRate: totalQuestions > 0 ? Math.round((totalCorrect / totalQuestions) * 100) : 0,
      records: normalizedRecords,
      learningRecords
    }
  } catch (error) {
    console.error(`获取用户${userId}的答题记录失败:`, error)
    ElMessage.error('获取学生答题记录失败')
    return {
      totalQuestions: 0,
      totalCorrect: 0,
      accuracyRate: 0,
      records: [],
      learningRecords: []
    }
  }
}

// 初始化加载数据
onMounted(() => {
  searchStudents()
})

// 搜索学生
const searchStudents = async () => {
  loading.value = true
  
  try {
    // 构建查询参数
    const params = {
      skip: (pagination.currentPage - 1) * pagination.pageSize,
      limit: pagination.pageSize,
      keyword: searchParams.studentName
    }
    
    console.log('查询参数:', params)
    
    // 调用API获取用户列表
    const response = await getUsers(params)
    
    console.log('API响应:', response)
    
    // 处理响应数据 - 支持多种响应格式
    let userList = [];
    
    // 格式1: 直接返回数组
    if (Array.isArray(response)) {
      userList = response;
    }
    // 格式2: {data: [...]}
    else if (response && response.data && Array.isArray(response.data)) {
      userList = response.data;
    }
    // 格式3: {data: {data: [...]}}
    else if (response && response.data && response.data.data && Array.isArray(response.data.data)) {
      userList = response.data.data;
    }
    // 格式4: {data: {code: 200, data: [...]}}
    else if (response && response.data && response.data.code === 200 && Array.isArray(response.data.data)) {
      userList = response.data.data;
    }
    // 格式5: {code: 200, data: [...]}
    else if (response && response.code === 200 && Array.isArray(response.data)) {
      userList = response.data;
    }
    else {
      console.warn(`未知的用户列表响应格式:`, response);
    }
    
    console.log('用户列表:', userList)
      
    // 首先筛选出具有学生角色的用户
    const studentUsers = userList.filter(user => {
      console.log('处理用户:', user)
      
      // 默认不是学生
      let isStudent = false
      
      // 根据角色信息判断是否为学生
      if (user.roles && Array.isArray(user.roles)) {
        isStudent = user.roles.some(role => 
          role && (role.name === 'student' || role.name === '学生' || role.name === 'student'.toUpperCase() || role.name === 'STUDENT')
        )
        console.log(`用户${user.username || user.id}的角色检查结果:`, isStudent, user.roles)
      } else {
        // 如果没有角色信息，也可以根据其他字段判断，比如user_type
        isStudent = user.user_type === 'student' || user.user_type === '学生';
        console.log(`用户${user.username || user.id}没有角色信息，根据user_type判断:`, isStudent)
      }
      
      return isStudent
    })
    
    console.log('筛选后的学生用户:', studentUsers)
    
    // 转换学生用户数据为前端所需格式
    const students = studentUsers.map(async user => {
      // 获取学生答题统计数据
      let totalQuestions = 0;
      let totalCorrect = 0;
      let accuracyRate = 0;
      
      try {
        const statsResult = await getStudentQuestionRecords(user.id);
        totalQuestions = statsResult.totalQuestions;
        totalCorrect = statsResult.totalCorrect;
        accuracyRate = statsResult.accuracyRate;
        console.log(`用户${user.id}的答题统计: 题目数=${totalQuestions}, 正确数=${totalCorrect}, 正确率=${accuracyRate}%`);
      } catch (error) {
        console.error(`获取用户${user.id}的答题记录失败:`, error);
      }
      
      return {
        studentId: user.id.toString(),
        studentName: user.full_name || user.username || user.name || `用户${user.id}`,
        totalStudyHours: 0,
        completionRate: 0,
        averageScore: 0,
        lastStudyTime: new Date().toISOString(), // 给一个默认时间以便显示
        userId: user.id,
        totalQuestions: totalQuestions,
        accuracyRate: accuracyRate
      };
    });
    
    // 等待所有异步映射操作完成
    const resolvedStudents = await Promise.all(students);
    
    console.log('转换后的学生数据:', resolvedStudents)
    studentsData.value = resolvedStudents
    pagination.total = resolvedStudents.length // 在实际应用中，应该使用后端返回的total
    
    // 如果没有学生数据，显示提示
    if (studentUsers.length === 0) {
      ElMessage.warning('未找到学生数据，请尝试调整筛选条件')
    }
  } catch (error) {
    console.error('获取学生列表失败:', error)
    console.error('错误详情:', error.message, error.response)
    ElMessage.error(`获取学生列表失败: ${error.message || '未知错误'}`)
  } finally {
    loading.value = false
  }
}

// 重置筛选条件
const resetFilters = () => {
  searchParams.studentName = ''
  searchParams.contentType = ''
  dateRange.value = []
  pagination.currentPage = 1
  searchStudents()
}

// 查看学生详情
const viewStudentDetail = async (student) => {
  console.log('===========================================');
  console.log('开始查看学生详情:', JSON.stringify(student, null, 2));
  
  // 验证学生ID
  const studentId = student.userId;
  if (!studentId) {
    console.error('学生信息中缺少有效的ID');
    ElMessage.error('学生信息不完整，无法查看详情');
    return;
  }
  
  loading.value = true
  
  try {
    console.log(`开始获取学生${studentId}的详细信息...`);
    
    const startTime = performance.now();
    // 获取学生答题记录和统计数据
    const statsResult = await getStudentQuestionRecords(studentId)
    const endTime = performance.now();
    
    console.log(`获取学生${studentId}答题记录完成，耗时: ${(endTime - startTime).toFixed(2)}ms`);
    
    // 安全地解构数据
    const learningRecords = Array.isArray(statsResult.learningRecords) ? statsResult.learningRecords : [];
    const totalQuestions = statsResult.totalQuestions || 0;
    const totalCorrect = statsResult.totalCorrect || 0;
    const accuracyRate = statsResult.accuracyRate || 0;
    
    console.log(`学生${studentId}的答题统计: 总数=${totalQuestions}, 正确数=${totalCorrect}, 正确率=${accuracyRate}%`);
    
    // 计算统计数据
    const totalStudyHours = learningRecords.reduce((sum, record) => sum + (record.duration || 0), 0) / 60;
    
    // 计算平均分数
    const validRecords = learningRecords.filter(record => record.score !== null && record.score !== undefined);
    const totalScore = validRecords.reduce((sum, record) => sum + (record.score || 0), 0);
    const averageScore = validRecords.length > 0 ? totalScore / validRecords.length : 0;
    
    // 计算最后学习时间
    let lastStudyTime = null;
    if (validRecords.length > 0) {
      try {
        const validDates = validRecords
          .map(record => record.accessTime ? new Date(record.accessTime) : null)
          .filter(date => date && !isNaN(date.getTime()));
        
        if (validDates.length > 0) {
          lastStudyTime = Math.max(...validDates.map(date => date.getTime()));
        }
      } catch (dateError) {
        console.warn('计算最后学习时间时出错:', dateError);
      }
    }
    
    // 构建学生详情数据
    currentStudent.value = {
      ...student,
      totalStudyHours,
      averageScore,
      lastStudyTime: lastStudyTime ? new Date(lastStudyTime).toISOString() : null,
      learningRecords,
      totalQuestions,
      totalCorrect,
      accuracyRate,
      records: Array.isArray(statsResult.records) ? statsResult.records : []
    }
    
    console.log('构建的学生详情数据:', currentStudent.value);
    
    detailDialogVisible.value = true
    activeTab.value = '0'
    
    console.log(`学生${studentId}详情对话框已显示`);
  } catch (error) {
    console.error('获取学生详情失败:', {
      error: error?.message || String(error),
      stack: error?.stack,
      studentId: studentId
    });
    ElMessage.error(`获取学生详情失败: ${error?.message || '未知错误'}`);
  } finally {
    loading.value = false
    console.log('查看学生详情流程结束');
    console.log('===========================================');
  }
}

// 分页处理
const handleSizeChange = (size) => {
  pagination.pageSize = size
  searchStudents()
}

const handleCurrentChange = (current) => {
  pagination.currentPage = current
  searchStudents()
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 计算答题记录中的题目数量
const getQuestionCount = (record) => {
  if (!record) return 0
  if (typeof record.total_questions === 'number') {
    return record.total_questions
  }
  if (Array.isArray(record.questions)) {
    return record.questions.length
  }
  if (typeof record.count === 'number') {
    return record.count
  }
  return 0
}

// 计算答题记录中的正确题数
const getCorrectCount = (record) => {
  if (!record) return 0

  const questionsCount = getQuestionCount(record)
  if (questionsCount === 0) return 0

  if (typeof record.correct_count === 'number') {
    return record.correct_count
  }
  if (typeof record.correct_answers === 'number') {
    return record.correct_answers
  }
  if (Array.isArray(record.results)) {
    return record.results.filter(r => r && (r.is_correct || r.answer_correct === 1 || r.correctness === 1)).length
  }
  if (Array.isArray(record.questions)) {
    return record.questions.filter(q => q && (q.is_correct || q.answer_correct === 1 || q.correctness === 1)).length
  }
  if (typeof record.accuracy === 'number') {
    const accuracyValue = record.accuracy > 1 ? record.accuracy / 100 : record.accuracy
    return Math.round(questionsCount * accuracyValue)
  }
  return 0
}

// 计算答题记录的正确率
const getAccuracyRate = (record) => {
  if (!record) return 0

  const questionsCount = getQuestionCount(record)
  if (questionsCount === 0) return 0

  const correctCount = getCorrectCount(record)
  return Math.round((correctCount / questionsCount) * 100)
}
</script>

<style scoped>
.student-progress-container {
  padding: 20px;
}

.page-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-section {
  margin-bottom: 20px;
}

.table-section {
  margin-bottom: 20px;
}

.pagination-section {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.student-detail {
  padding: 10px;
}

.detail-header {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eaeaea;
}

.student-info h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.student-info p {
  margin: 5px 0;
  color: #666;
}

.question-records-section {
  padding: 10px 0;
}

.records-stats {
  display: flex;
  gap: 40px;
  margin-bottom: 20px;
}

.records-stats .el-statistic {
  background: #f7f8fa;
  padding: 20px;
  border-radius: 8px;
  flex: 1;
  text-align: center;
}

.records-stats .el-statistic__label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.records-stats .el-statistic__content {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.records-stats .el-statistic__suffix {
  font-size: 16px;
  color: #606266;
  margin-left: 4px;
}

</style>