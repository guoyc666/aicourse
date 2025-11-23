<template>
  <div class="learning-path-container">
    <div class="page-header">
      <h1>学习路径管理</h1>
      <p class="sub-title">个性化学习路径，助您高效掌握知识点</p>
    </div>

    <div class="path-card">
      <div class="path-header">
        <div class="path-info">
          <h2>{{ currentPath.name }}</h2>
          <p>{{ currentPath.description }}</p>
          <div class="path-meta">
            <span class="meta-item"><Clock class="meta-icon" /> 预计学习时长: {{ currentPath.duration }}</span>
            <span class="meta-item"><Star class="meta-icon" /> 难度: {{ currentPath.difficulty }}</span>
          </div>
        </div>
        <el-button type="primary" @click="generatePersonalizedPath">
          生成个性化路径
        </el-button>
      </div>

      <div class="path-content">
        <div class="section-header">
          <h3>推荐学习内容</h3>
        </div>
        <div class="recommendations">
          <div v-for="(item, index) in recommendations" :key="index" class="recommendation-card">
            <h4>{{ item.title }}</h4>
            <p>{{ item.description }}</p>
            <div class="recommendation-meta">
              <span class="node-type" :class="getNodeTypeTag(item.type)">{{ getNodeTypeName(item.type) }}</span>
              <span class="completion-rate">{{ item.completionRate }}% 已完成</span>
            </div>
          </div>
        </div>
      </div>

      <div class="path-steps">
        <div class="section-header">
          <h3>学习步骤</h3>
        </div>
        <div class="steps-container">
          <div v-for="(step, index) in pathSteps" :key="index" class="step-item">
            <div class="step-header">
              <div class="step-number">{{ index + 1 }}</div>
              <h4>{{ step.title }}</h4>
              <el-tag v-if="step.status === 'completed'" type="success">
                <CircleCheck /> 已完成
              </el-tag>
              <el-tag v-else-if="step.status === 'in-progress'" type="primary">
                <Loading /> 进行中
              </el-tag>
              <el-tag v-else type="info">
                未开始
              </el-tag>
            </div>
            <div class="step-content">
              <p>{{ step.description }}</p>
              <div class="step-actions">
                <el-button size="small" @click="startStep(step)">开始学习</el-button>
                <el-button size="small" type="text" @click="viewDetails(step)">查看详情</el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Star, CircleCheck, Loading, Clock } from '@element-plus/icons-vue'

// 响应式数据
const currentPath = ref({
  name: 'Python编程基础路径',
  description: '从零开始学习Python编程',
  duration: '4周',
  difficulty: '初级'
})

// 推荐学习
const recommendations = ref([])

// 路径步骤
const pathSteps = ref([])

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

// 生成个性化路径
const generatePersonalizedPath = async () => {
  try {
    ElMessage.info('正在生成个性化学习路径...')
    
    // 这里应该调用实际的API
    // const response = await generatePersonalizedLearningPath()
    
    // 模拟生成过程
    setTimeout(() => {
      ElMessage.success('个性化学习路径生成完成！')
      loadPathData()
    }, 2000)
  } catch (error) {
    ElMessage.error('生成个性化学习路径失败：' + error.message)
  }
}

// 加载路径数据
const loadPathData = () => {
  // 模拟加载数据
  recommendations.value = [
    {
      title: 'Python变量和数据类型',
      description: '学习Python的基本数据类型、变量声明和操作',
      type: 'concept',
      completionRate: 0
    },
    {
      title: 'Python流程控制',
      description: '学习条件语句和循环结构',
      type: 'skill',
      completionRate: 0
    },
    {
      title: 'Python官方文档',
      description: 'Python官方教程和文档资源',
      type: 'resource',
      completionRate: 0
    }
  ]

  pathSteps.value = [
    {
      title: '环境搭建',
      description: '安装Python和开发环境，准备开始编程',
      status: 'in-progress',
      nodes: []
    },
    {
      title: '基础语法',
      description: '学习Python的基本语法和数据类型',
      status: 'pending',
      nodes: []
    },
    {
      title: '函数和模块',
      description: '掌握函数定义和模块使用',
      status: 'pending',
      nodes: []
    },
    {
      title: '实践项目',
      description: '通过小型项目巩固所学知识',
      status: 'pending',
      nodes: []
    }
  ]
}

// 开始学习步骤
const startStep = (step) => {
  ElMessage.info(`开始学习：${step.title}`)
  step.status = 'in-progress'
}

// 查看详情
const viewDetails = (step) => {
  ElMessage.info(`查看${step.title}详情`)
}

// 组件挂载时加载数据
onMounted(() => {
  loadPathData()
})
</script>

<style scoped>
.learning-path-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
}

.sub-title {
  font-size: 16px;
  color: #606266;
}

.path-card {
  background: #ffffff;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.path-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.path-info h2 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.path-info p {
  font-size: 16px;
  color: #606266;
  margin-bottom: 15px;
}

.path-meta {
  display: flex;
  gap: 20px;
}

.meta-item {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #909399;
}

.meta-icon {
  margin-right: 5px;
}

.section-header {
  margin-bottom: 20px;
}

.section-header h3 {
  font-size: 18px;
  font-weight: bold;
}

.recommendations {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.recommendation-card {
  background: #fafafa;
  border-radius: 8px;
  padding: 20px;
  transition: all 0.3s;
}

.recommendation-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.recommendation-card h4 {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}

.recommendation-card p {
  font-size: 14px;
  color: #606266;
  margin-bottom: 15px;
  line-height: 1.5;
}

.recommendation-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.node-type {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.node-type.primary {
  background: #ecf5ff;
  color: #409eff;
}

.node-type.success {
  background: #f0f9eb;
  color: #67c23a;
}

.node-type.warning {
  background: #fdf6ec;
  color: #e6a23c;
}

.completion-rate {
  font-size: 14px;
  color: #909399;
}

.path-steps {
  margin-top: 30px;
}

.steps-container {
  position: relative;
}

.step-item {
  padding: 20px;
  margin-bottom: 20px;
  background: #fafafa;
  border-radius: 8px;
  position: relative;
}

.step-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 20px;
  top: calc(100% + 10px);
  width: 2px;
  height: 10px;
  background: #dcdfe6;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.step-number {
  width: 32px;
  height: 32px;
  background: #409eff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.step-header h4 {
  font-size: 16px;
  font-weight: bold;
  flex: 1;
}

.step-content p {
  font-size: 14px;
  color: #606266;
  margin-bottom: 15px;
  line-height: 1.5;
}

.step-actions {
  display: flex;
  gap: 10px;
}
</style>