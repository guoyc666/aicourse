<template>
  <div class="visualization-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="page-title">
        <h2>学习过程可视化</h2>
        <p>以知识图谱形式展示学习进度和掌握情况</p>
      </div>
      <div class="page-actions">
        <el-button-group>
          <el-button @click="viewMode = 'overview'" :type="viewMode === 'overview' ? 'primary' : ''">
            总览
          </el-button>
          <el-button @click="viewMode = 'detailed'" :type="viewMode === 'detailed' ? 'primary' : ''">
            详细
          </el-button>
          <el-button @click="viewMode = 'comparison'" :type="viewMode === 'comparison' ? 'primary' : ''">
            对比
          </el-button>
        </el-button-group>
      </div>
    </div>
    
    <el-row :gutter="20">
      <!-- 学习概览 -->
      <el-col :span="6">
        <el-card title="学习概览">
          <div class="overview-stats">
            <div class="stat-item">
              <div class="stat-icon nodes">
                <el-icon><Share /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ overview.totalNodes }}</div>
                <div class="stat-label">知识点总数</div>
              </div>
            </div>
            
            <div class="stat-item">
              <div class="stat-icon completed">
                <el-icon><CircleCheck /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ overview.completedNodes }}</div>
                <div class="stat-label">已完成</div>
              </div>
            </div>
            
            <div class="stat-item">
              <div class="stat-icon in-progress">
                <el-icon><Loading /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ overview.inProgressNodes }}</div>
                <div class="stat-label">进行中</div>
              </div>
            </div>
            
            <div class="stat-item">
              <div class="stat-icon not-started">
                <el-icon><Clock /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ overview.notStartedNodes }}</div>
                <div class="stat-label">未开始</div>
              </div>
            </div>
          </div>
          
          <div class="overall-progress">
            <div class="progress-label">整体完成度</div>
            <el-progress 
              :percentage="overview.overallProgress" 
              :color="getProgressColor(overview.overallProgress)"
            />
          </div>
        </el-card>
      </el-col>
      
      <!-- 主要可视化区域 -->
      <el-col :span="18">
        <el-card class="visualization-card">
          <template #header>
            <div class="card-header">
              <span>知识图谱可视化</span>
              <div class="visualization-controls">
                <el-button size="small" @click="resetView">重置视图</el-button>
                <el-button size="small" @click="exportImage">导出图片</el-button>
                <el-dropdown @command="handleFilter">
                  <el-button size="small">
                    筛选<el-icon><ArrowDown /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="all">显示全部</el-dropdown-item>
                      <el-dropdown-item command="completed">仅已完成</el-dropdown-item>
                      <el-dropdown-item command="in-progress">仅进行中</el-dropdown-item>
                      <el-dropdown-item command="not-started">仅未开始</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </template>
          
          <div class="visualization-container">
            <div id="knowledge-graph" class="graph-container"></div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <!-- 学习进度分析 -->
      <el-col :span="12">
        <el-card title="学习进度分析">
          <div class="progress-analysis">
            <div class="analysis-tabs">
              <el-tabs v-model="activeAnalysisTab">
                <el-tab-pane label="时间趋势" name="trend">
                  <div id="progress-trend-chart" class="chart-container"></div>
                </el-tab-pane>
                <el-tab-pane label="知识点分布" name="distribution">
                  <div id="knowledge-distribution-chart" class="chart-container"></div>
                </el-tab-pane>
                <el-tab-pane label="难度分析" name="difficulty">
                  <div id="difficulty-analysis-chart" class="chart-container"></div>
                </el-tab-pane>
              </el-tabs>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 掌握情况详情 -->
      <el-col :span="12">
        <el-card title="掌握情况详情">
          <div class="mastery-details">
            <div class="mastery-filter">
              <el-select v-model="selectedCategory" placeholder="选择分类" @change="filterMasteryData">
                <el-option label="全部" value="all" />
                <el-option label="概念" value="concept" />
                <el-option label="技能" value="skill" />
                <el-option label="资源" value="resource" />
              </el-select>
            </div>
            
            <div class="mastery-list">
              <div 
                v-for="node in filteredMasteryData" 
                :key="node.id"
                class="mastery-item"
                @click="focusOnNode(node)"
              >
                <div class="mastery-info">
                  <div class="mastery-name">{{ node.name }}</div>
                  <div class="mastery-type">{{ getNodeTypeName(node.type) }}</div>
                </div>
                
                <div class="mastery-visual">
                  <div class="mastery-progress">
                    <el-progress 
                      :percentage="node.mastery" 
                      :color="getMasteryColor(node.mastery)"
                      :show-text="false"
                    />
                  </div>
                  <div class="mastery-level">{{ getMasteryLevel(node.mastery) }}</div>
                </div>
                
                <div class="mastery-stats">
                  <div class="stat-item">
                    <span class="stat-label">掌握度</span>
                    <span class="stat-value">{{ node.mastery }}%</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">学习时间</span>
                    <span class="stat-value">{{ node.studyTime }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">练习次数</span>
                    <span class="stat-value">{{ node.practiceCount }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 节点详情对话框 -->
    <el-dialog v-model="showNodeDetail" title="节点详情" width="600px">
      <div v-if="selectedNode" class="node-detail">
        <div class="node-header">
          <h3>{{ selectedNode.name }}</h3>
          <el-tag :type="getNodeTypeTag(selectedNode.type)">
            {{ getNodeTypeName(selectedNode.type) }}
          </el-tag>
        </div>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="节点ID">{{ selectedNode.id }}</el-descriptions-item>
          <el-descriptions-item label="难度级别">{{ selectedNode.level }}</el-descriptions-item>
          <el-descriptions-item label="掌握度">{{ selectedNode.mastery }}%</el-descriptions-item>
          <el-descriptions-item label="学习时间">{{ selectedNode.studyTime }}</el-descriptions-item>
          <el-descriptions-item label="练习次数">{{ selectedNode.practiceCount }}</el-descriptions-item>
          <el-descriptions-item label="最后学习">{{ selectedNode.lastStudy }}</el-descriptions-item>
        </el-descriptions>
        
        <div class="node-description">
          <h4>描述</h4>
          <p>{{ selectedNode.description }}</p>
        </div>
        
        <div class="node-relations">
          <h4>相关节点</h4>
          <div class="relations-list">
            <div 
              v-for="relation in selectedNode.relations" 
              :key="relation.id"
              class="relation-item"
            >
              <span class="relation-node">{{ relation.targetName }}</span>
              <el-tag size="small">{{ getRelationTypeName(relation.type) }}</el-tag>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Network } from 'vis-network'
import { DataSet } from 'vis-data'

// 响应式数据
const viewMode = ref('overview')
const activeAnalysisTab = ref('trend')
const selectedCategory = ref('all')
const showNodeDetail = ref(false)
const selectedNode = ref(null)

// 概览数据
const overview = reactive({
  totalNodes: 25,
  completedNodes: 8,
  inProgressNodes: 3,
  notStartedNodes: 14,
  overallProgress: 32
})

// 掌握情况数据
const masteryData = ref([])

// 图谱网络实例
let network = null

// 过滤后的掌握数据
const filteredMasteryData = computed(() => {
  if (selectedCategory.value === 'all') {
    return masteryData.value
  }
  return masteryData.value.filter(node => node.type === selectedCategory.value)
})

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

// 获取关系类型名称
const getRelationTypeName = (type) => {
  const typeNames = {
    depends_on: '依赖',
    contains: '包含',
    related_to: '相关',
    prerequisite: '前置'
  }
  return typeNames[type] || type
}

// 获取进度颜色
const getProgressColor = (percentage) => {
  if (percentage >= 80) return '#67c23a'
  if (percentage >= 60) return '#e6a23c'
  return '#f56c6c'
}

// 获取掌握程度
const getMasteryLevel = (percentage) => {
  if (percentage >= 90) return '精通'
  if (percentage >= 70) return '熟练'
  if (percentage >= 50) return '了解'
  if (percentage >= 30) return '入门'
  return '未学'
}

// 获取掌握颜色
const getMasteryColor = (percentage) => {
  if (percentage >= 90) return '#67c23a'
  if (percentage >= 70) return '#5dade2'
  if (percentage >= 50) return '#f39c12'
  if (percentage >= 30) return '#e74c3c'
  return '#95a5a6'
}

// 初始化知识图谱
const initKnowledgeGraph = () => {
  const container = document.getElementById('knowledge-graph')
  if (!container) return
  
  // 准备节点数据
  const nodesData = masteryData.value.map(node => ({
    id: node.id,
    label: node.name,
    group: node.type,
    level: node.level,
    mastery: node.mastery,
    status: node.status,
    title: `${node.name}\n类型: ${getNodeTypeName(node.type)}\n掌握度: ${node.mastery}%\n状态: ${node.status}`
  }))
  
  // 准备边数据
  const edgesData = [
    { id: 1, from: 1, to: 2, label: '依赖', arrows: 'to' },
    { id: 2, from: 2, to: 3, label: '依赖', arrows: 'to' },
    { id: 3, from: 2, to: 4, label: '依赖', arrows: 'to' },
    { id: 4, from: 3, to: 5, label: '依赖', arrows: 'to' },
    { id: 5, from: 4, to: 5, label: '依赖', arrows: 'to' }
  ]
  
  // 创建数据集
  const nodesDataSet = new DataSet(nodesData)
  const edgesDataSet = new DataSet(edgesData)
  
  // 配置选项
  const options = {
    nodes: {
      shape: 'box',
      font: {
        size: 14
      },
      borderWidth: 2,
      shadow: true,
      chosen: {
        node: function(values, id, selected, hovering) {
          if (selected || hovering) {
            values.borderWidth = 4
            values.borderColor = '#ff6b6b'
          }
        }
      }
    },
    edges: {
      font: {
        size: 12
      },
      arrows: {
        to: {
          enabled: true,
          scaleFactor: 1
        }
      },
      smooth: {
        type: 'continuous'
      }
    },
    groups: {
      concept: {
        color: {
          background: '#e1f5fe',
          border: '#01579b'
        }
      },
      skill: {
        color: {
          background: '#e8f5e8',
          border: '#2e7d32'
        }
      },
      resource: {
        color: {
          background: '#fff3e0',
          border: '#ef6c00'
        }
      }
    },
    physics: {
      enabled: true,
      stabilization: {
        iterations: 100
      }
    },
    interaction: {
      hover: true,
      selectConnectedEdges: false
    }
  }
  
  // 创建网络
  network = new Network(container, { nodes: nodesDataSet, edges: edgesDataSet }, options)
  
  // 添加事件监听
  network.on('selectNode', (params) => {
    if (params.nodes.length > 0) {
      const nodeId = params.nodes[0]
      const node = masteryData.value.find(n => n.id === nodeId)
      if (node) {
        selectedNode.value = node
        showNodeDetail.value = true
      }
    }
  })
}

// 重置视图
const resetView = () => {
  if (network) {
    network.fit()
  }
}

// 导出图片
const exportImage = () => {
  if (network) {
    const canvas = document.querySelector('#knowledge-graph canvas')
    if (canvas) {
      const link = document.createElement('a')
      link.download = 'knowledge-graph.png'
      link.href = canvas.toDataURL()
      link.click()
    }
  }
}

// 处理筛选
const handleFilter = (command) => {
  ElMessage.info(`筛选模式: ${command}`)
}

// 聚焦到节点
const focusOnNode = (node) => {
  if (network) {
    network.focus(node.id, {
      scale: 1.2,
      animation: true
    })
    network.selectNodes([node.id])
  }
}

// 过滤掌握数据
const filterMasteryData = () => {
  // 过滤逻辑已在computed中实现
}

// 加载数据
const loadData = () => {
  // 掌握情况数据
  masteryData.value = [
    {
      id: 1,
      name: 'Python基础语法',
      type: 'concept',
      level: 1,
      mastery: 95,
      status: 'completed',
      studyTime: '3小时',
      practiceCount: 15,
      lastStudy: '2024-01-15',
      description: 'Python编程语言的基础语法知识',
      relations: [
        { id: 1, targetName: '变量和数据类型', type: 'depends_on' }
      ]
    },
    {
      id: 2,
      name: '变量和数据类型',
      type: 'concept',
      level: 1,
      mastery: 88,
      status: 'completed',
      studyTime: '2小时',
      practiceCount: 12,
      lastStudy: '2024-01-14',
      description: 'Python中的变量定义和基本数据类型',
      relations: [
        { id: 2, targetName: '控制流程', type: 'depends_on' },
        { id: 3, targetName: '函数定义', type: 'depends_on' }
      ]
    },
    {
      id: 3,
      name: '控制流程',
      type: 'skill',
      level: 2,
      mastery: 65,
      status: 'in-progress',
      studyTime: '1.5小时',
      practiceCount: 8,
      lastStudy: '2024-01-13',
      description: '条件语句和循环语句的使用',
      relations: [
        { id: 4, targetName: '面向对象编程', type: 'depends_on' }
      ]
    },
    {
      id: 4,
      name: '函数定义',
      type: 'skill',
      level: 2,
      mastery: 45,
      status: 'in-progress',
      studyTime: '1小时',
      practiceCount: 5,
      lastStudy: '2024-01-12',
      description: '如何定义和调用函数',
      relations: [
        { id: 5, targetName: '面向对象编程', type: 'depends_on' }
      ]
    },
    {
      id: 5,
      name: '面向对象编程',
      type: 'concept',
      level: 3,
      mastery: 20,
      status: 'not-started',
      studyTime: '0.5小时',
      practiceCount: 2,
      lastStudy: '2024-01-11',
      description: '类和对象的概念及使用',
      relations: []
    }
  ]
}

onMounted(() => {
  loadData()
  nextTick(() => {
    initKnowledgeGraph()
  })
})
</script>

<style lang="scss" scoped>
.visualization-container {
  padding: 20px;
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

.overview-stats {
  .stat-item {
    display: flex;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #f0f0f0;
    
    &:last-child {
      border-bottom: none;
    }
    
    .stat-icon {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 12px;
      color: white;
      font-size: 18px;
      
      &.nodes {
        background: #409eff;
      }
      
      &.completed {
        background: #67c23a;
      }
      
      &.in-progress {
        background: #e6a23c;
      }
      
      &.not-started {
        background: #909399;
      }
    }
    
    .stat-content {
      flex: 1;
      
      .stat-value {
        font-size: 20px;
        font-weight: bold;
        color: #333;
        line-height: 1;
      }
      
      .stat-label {
        font-size: 12px;
        color: #666;
        margin-top: 4px;
      }
    }
  }
}

.overall-progress {
  margin-top: 20px;
  
  .progress-label {
    font-size: 14px;
    color: #666;
    margin-bottom: 8px;
  }
}

.visualization-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .visualization-controls {
      display: flex;
      gap: 8px;
    }
  }
}

.visualization-container {
  height: 500px;
  
  .graph-container {
    width: 100%;
    height: 100%;
    border: 1px solid #e4e7ed;
    border-radius: 6px;
  }
}

.progress-analysis {
  .analysis-tabs {
    .chart-container {
      height: 300px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f5f7fa;
      border-radius: 6px;
      color: #666;
    }
  }
}

.mastery-details {
  .mastery-filter {
    margin-bottom: 16px;
  }
  
  .mastery-list {
    max-height: 400px;
    overflow-y: auto;
    
    .mastery-item {
      display: flex;
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
      
      .mastery-info {
        width: 120px;
        
        .mastery-name {
          font-size: 14px;
          color: #333;
          margin-bottom: 4px;
          font-weight: 500;
        }
        
        .mastery-type {
          font-size: 12px;
          color: #666;
        }
      }
      
      .mastery-visual {
        flex: 1;
        margin: 0 16px;
        
        .mastery-progress {
          margin-bottom: 8px;
        }
        
        .mastery-level {
          font-size: 12px;
          color: #666;
          text-align: center;
        }
      }
      
      .mastery-stats {
        width: 120px;
        
        .stat-item {
          display: flex;
          justify-content: space-between;
          margin-bottom: 4px;
          
          .stat-label {
            font-size: 12px;
            color: #666;
          }
          
          .stat-value {
            font-size: 12px;
            color: #333;
            font-weight: 500;
          }
        }
      }
    }
  }
}

.node-detail {
  .node-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    
    h3 {
      margin: 0;
      color: #333;
    }
  }
  
  .node-description {
    margin: 20px 0;
    
    h4 {
      margin: 0 0 8px 0;
      color: #333;
    }
    
    p {
      margin: 0;
      color: #666;
      line-height: 1.6;
    }
  }
  
  .node-relations {
    h4 {
      margin: 0 0 12px 0;
      color: #333;
    }
    
    .relations-list {
      .relation-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 12px;
        border: 1px solid #e4e7ed;
        border-radius: 4px;
        margin-bottom: 8px;
        
        .relation-node {
          font-size: 14px;
          color: #333;
        }
      }
    }
  }
}
</style>
