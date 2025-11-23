<template>
  <div class="knowledge-graph-container">
    <!-- 页面标题和操作 -->
    <div class="page-header">
      <div class="page-title">
        <h2>知识图谱管理</h2>
        <p>构建和管理课程知识图谱，建立知识点之间的关系</p>
      </div>
      <div class="page-actions">
        <el-button type="primary" @click="showCreateNodeDialog = true">
          <el-icon><Plus /></el-icon>
          添加节点
        </el-button>
        <el-button @click="showCreateRelationDialog = true">
          <el-icon><Link /></el-icon>
          添加关系
        </el-button>
        <el-button @click="toggleVisualization">
          <el-icon><View /></el-icon>
          {{ showGraph ? '隐藏图谱' : '显示图谱' }}
        </el-button>
      </div>
    </div>
    
    <el-row :gutter="20">
      <!-- 左侧：节点和关系管理 -->
      <el-col :span="showGraph ? 12 : 24">
        <el-row :gutter="20">
          <!-- 知识节点列表 -->
          <el-col :span="12">
            <el-card title="知识节点">
              <template #header>
                <div class="card-header">
                  <span>知识节点</span>
                  <el-button size="small" @click="showCreateNodeDialog = true">添加</el-button>
                </div>
              </template>
              
              <div class="search-bar">
                <el-input
                  v-model="nodeSearchKeyword"
                  placeholder="搜索节点..."
                  clearable
                  @input="filterNodes"
                >
                  <template #prefix>
                    <el-icon><Search /></el-icon>
                  </template>
                </el-input>
              </div>
              
              <div class="node-list">
                <div 
                  v-for="node in filteredNodes" 
                  :key="node.id"
                  class="node-item"
                  :class="{ active: selectedNode?.id === node.id }"
                  @click="selectNode(node)"
                >
                  <div class="node-info">
                    <div class="node-name">{{ node.name }}</div>
                    <div class="node-meta">
                      <el-tag :type="getNodeTypeTag(node.node_type)" size="small">
                        {{ getNodeTypeName(node.node_type) }}
                      </el-tag>
                      <span class="node-level">L{{ node.level }}</span>
                    </div>
                    <div class="node-desc" v-if="node.description">
                      {{ node.description }}
                    </div>
                  </div>
                  <div class="node-actions">
                    <el-button size="small" type="text" @click.stop="editNode(node)">编辑</el-button>
                    <el-button size="small" type="text" @click.stop="deleteNode(node)">删除</el-button>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <!-- 关系列表 -->
          <el-col :span="12">
            <el-card title="节点关系">
              <template #header>
                <div class="card-header">
                  <span>节点关系</span>
                  <el-button size="small" @click="showCreateRelationDialog = true">添加</el-button>
                </div>
              </template>
              
              <div class="relation-list">
                <div 
                  v-for="relation in relations" 
                  :key="relation.id"
                  class="relation-item"
                >
                  <div class="relation-info">
                    <div class="relation-nodes">
                      <span class="source-node">{{ getNodeName(relation.source_node_id) }}</span>
                      <el-icon class="relation-arrow"><Right /></el-icon>
                      <span class="target-node">{{ getNodeName(relation.target_node_id) }}</span>
                    </div>
                    <div class="relation-meta">
                      <el-tag :type="getRelationTypeTag(relation.relation_type)" size="small">
                        {{ getRelationTypeName(relation.relation_type) }}
                      </el-tag>
                      <span class="relation-weight">权重: {{ relation.weight }}</span>
                    </div>
                  </div>
                  <div class="relation-actions">
                    <el-button size="small" type="text" @click="deleteRelation(relation)">删除</el-button>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
      
      <!-- 右侧：图谱可视化 -->
      <el-col :span="12" v-if="showGraph">
        <el-card title="知识图谱可视化">
          <template #header>
            <div class="card-header">
              <span>知识图谱可视化</span>
              <div class="graph-controls">
                <el-button size="small" @click="resetGraph">重置视图</el-button>
                <el-button size="small" @click="exportGraph">导出</el-button>
              </div>
            </div>
          </template>
          
          <div id="graph-container" class="graph-container"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 创建/编辑节点对话框 -->
    <el-dialog
      v-model="showCreateNodeDialog"
      :title="editingNode ? '编辑节点' : '创建节点'"
      width="600px"
    >
      <el-form
        ref="nodeFormRef"
        :model="nodeForm"
        :rules="nodeRules"
        label-width="100px"
      >
        <el-form-item label="节点名称" prop="name">
          <el-input v-model="nodeForm.name" placeholder="请输入节点名称" />
        </el-form-item>
        
        <el-form-item label="节点类型" prop="node_type">
          <el-select v-model="nodeForm.node_type" placeholder="请选择节点类型">
            <el-option label="概念" value="concept" />
            <el-option label="技能" value="skill" />
            <el-option label="资源" value="resource" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="难度级别" prop="level">
          <el-input-number v-model="nodeForm.level" :min="1" :max="10" />
        </el-form-item>
        
        <el-form-item label="前置节点">
          <el-select
            v-model="nodeForm.prerequisites"
            multiple
            placeholder="请选择前置节点"
            style="width: 100%"
          >
            <el-option
              v-for="node in nodes"
              :key="node.id"
              :label="node.name"
              :value="node.id"
              :disabled="node.id === editingNode?.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="节点描述">
          <el-input
            v-model="nodeForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入节点描述"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showCreateNodeDialog = false">取消</el-button>
          <el-button type="primary" @click="handleNodeSubmit">保存</el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 创建关系对话框 -->
    <el-dialog
      v-model="showCreateRelationDialog"
      title="创建关系"
      width="500px"
    >
      <el-form
        ref="relationFormRef"
        :model="relationForm"
        :rules="relationRules"
        label-width="100px"
      >
        <el-form-item label="源节点" prop="source_node_id">
          <el-select v-model="relationForm.source_node_id" placeholder="请选择源节点" style="width: 100%">
            <el-option
              v-for="node in nodes"
              :key="node.id"
              :label="node.name"
              :value="node.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="目标节点" prop="target_node_id">
          <el-select v-model="relationForm.target_node_id" placeholder="请选择目标节点" style="width: 100%">
            <el-option
              v-for="node in nodes"
              :key="node.id"
              :label="node.name"
              :value="node.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="关系类型" prop="relation_type">
          <el-select v-model="relationForm.relation_type" placeholder="请选择关系类型">
            <el-option label="依赖关系" value="depends_on" />
            <el-option label="包含关系" value="contains" />
            <el-option label="相关关系" value="related_to" />
            <el-option label="前置关系" value="prerequisite" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="权重" prop="weight">
          <el-input-number v-model="relationForm.weight" :min="0.1" :max="2.0" :step="0.1" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showCreateRelationDialog = false">取消</el-button>
          <el-button type="primary" @click="handleRelationSubmit">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Network } from 'vis-network'
import { DataSet } from 'vis-data'

// 响应式数据
const showCreateNodeDialog = ref(false)
const showCreateRelationDialog = ref(false)
const showGraph = ref(false)
const nodeSearchKeyword = ref('')
const selectedNode = ref(null)
const editingNode = ref(null)

const nodeFormRef = ref()
const relationFormRef = ref()

// 图谱可视化相关
let network = null
let nodesDataSet = null
let edgesDataSet = null

// 节点表单
const nodeForm = reactive({
  name: '',
  description: '',
  node_type: '',
  level: 1,
  prerequisites: []
})

// 关系表单
const relationForm = reactive({
  source_node_id: null,
  target_node_id: null,
  relation_type: '',
  weight: 1.0
})

// 表单验证规则
const nodeRules = {
  name: [
    { required: true, message: '请输入节点名称', trigger: 'blur' }
  ],
  node_type: [
    { required: true, message: '请选择节点类型', trigger: 'change' }
  ],
  level: [
    { required: true, message: '请设置难度级别', trigger: 'blur' }
  ]
}

const relationRules = {
  source_node_id: [
    { required: true, message: '请选择源节点', trigger: 'change' }
  ],
  target_node_id: [
    { required: true, message: '请选择目标节点', trigger: 'change' }
  ],
  relation_type: [
    { required: true, message: '请选择关系类型', trigger: 'change' }
  ]
}

// 数据
const nodes = ref([])
const relations = ref([])

// 过滤后的节点
const filteredNodes = computed(() => {
  if (!nodeSearchKeyword.value) return nodes.value
  return nodes.value.filter(node => 
    node.name.toLowerCase().includes(nodeSearchKeyword.value.toLowerCase())
  )
})

// 获取节点名称
const getNodeName = (nodeId) => {
  const node = nodes.value.find(n => n.id === nodeId)
  return node ? node.name : '未知节点'
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

// 获取关系类型标签
const getRelationTypeTag = (type) => {
  const typeTags = {
    depends_on: 'danger',
    contains: 'success',
    related_to: 'info',
    prerequisite: 'warning'
  }
  return typeTags[type] || ''
}

// 加载数据
const loadData = async () => {
  try {
    // 这里应该调用实际的API
    // const [nodesResponse, relationsResponse] = await Promise.all([
    //   getKnowledgeNodes(),
    //   getKnowledgeRelations()
    // ])
    
    // 模拟数据
    nodes.value = [
      {
        id: 1,
        name: 'Python基础语法',
        description: 'Python编程语言的基础语法知识',
        node_type: 'concept',
        level: 1,
        prerequisites: []
      },
      {
        id: 2,
        name: '变量和数据类型',
        description: 'Python中的变量定义和基本数据类型',
        node_type: 'concept',
        level: 1,
        prerequisites: [1]
      },
      {
        id: 3,
        name: '控制流程',
        description: '条件语句和循环语句的使用',
        node_type: 'concept',
        level: 2,
        prerequisites: [1, 2]
      },
      {
        id: 4,
        name: '函数定义',
        description: '如何定义和调用函数',
        node_type: 'skill',
        level: 2,
        prerequisites: [1, 2]
      },
      {
        id: 5,
        name: '面向对象编程',
        description: '类和对象的概念及使用',
        node_type: 'concept',
        level: 3,
        prerequisites: [1, 2, 3, 4]
      }
    ]
    
    relations.value = [
      {
        id: 1,
        source_node_id: 1,
        target_node_id: 2,
        relation_type: 'prerequisite',
        weight: 1.0
      },
      {
        id: 2,
        source_node_id: 2,
        target_node_id: 3,
        relation_type: 'prerequisite',
        weight: 1.0
      },
      {
        id: 3,
        source_node_id: 2,
        target_node_id: 4,
        relation_type: 'prerequisite',
        weight: 1.0
      },
      {
        id: 4,
        source_node_id: 3,
        target_node_id: 5,
        relation_type: 'prerequisite',
        weight: 1.0
      },
      {
        id: 5,
        source_node_id: 4,
        target_node_id: 5,
        relation_type: 'prerequisite',
        weight: 1.0
      }
    ]
  } catch (error) {
    ElMessage.error('加载数据失败')
  }
}

// 初始化图谱可视化
const initGraph = () => {
  const container = document.getElementById('graph-container')
  if (!container) return
  
  // 准备数据
  const nodesData = nodes.value.map(node => ({
    id: node.id,
    label: node.name,
    group: node.node_type,
    level: node.level,
    title: `${node.name}\n类型: ${getNodeTypeName(node.node_type)}\n级别: ${node.level}\n描述: ${node.description || '无'}`
  }))
  
  const edgesData = relations.value.map(relation => ({
    id: relation.id,
    from: relation.source_node_id,
    to: relation.target_node_id,
    label: getRelationTypeName(relation.relation_type),
    width: relation.weight * 2,
    title: `${getNodeName(relation.source_node_id)} → ${getNodeName(relation.target_node_id)}\n类型: ${getRelationTypeName(relation.relation_type)}\n权重: ${relation.weight}`
  }))
  
  // 创建数据集
  nodesDataSet = new DataSet(nodesData)
  edgesDataSet = new DataSet(edgesData)
  
  // 配置选项
  const options = {
    nodes: {
      shape: 'box',
      font: {
        size: 14
      },
      borderWidth: 2,
      shadow: true
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
      const node = nodes.value.find(n => n.id === nodeId)
      if (node) {
        selectNode(node)
      }
    }
  })
}

// 切换可视化
const toggleVisualization = () => {
  showGraph.value = !showGraph.value
  if (showGraph.value) {
    nextTick(() => {
      initGraph()
    })
  }
}

// 重置图谱
const resetGraph = () => {
  if (network) {
    network.fit()
  }
}

// 导出图谱
const exportGraph = () => {
  if (network) {
    const canvas = document.querySelector('#graph-container canvas')
    if (canvas) {
      const link = document.createElement('a')
      link.download = 'knowledge-graph.png'
      link.href = canvas.toDataURL()
      link.click()
    }
  }
}

// 选择节点
const selectNode = (node) => {
  selectedNode.value = node
  if (network) {
    network.selectNodes([node.id])
    network.focus(node.id, {
      scale: 1.2,
      animation: true
    })
  }
}

// 过滤节点
const filterNodes = () => {
  // 过滤逻辑已在computed中实现
}

// 创建节点
const handleNodeSubmit = async () => {
  if (!nodeFormRef.value) return
  
  await nodeFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (editingNode.value) {
          // 编辑节点
          const index = nodes.value.findIndex(n => n.id === editingNode.value.id)
          if (index !== -1) {
            nodes.value[index] = { ...nodes.value[index], ...nodeForm }
          }
          ElMessage.success('节点更新成功')
        } else {
          // 创建节点
          const newNode = {
            id: Date.now(), // 临时ID
            ...nodeForm
          }
          nodes.value.push(newNode)
          ElMessage.success('节点创建成功')
        }
        
        showCreateNodeDialog.value = false
        resetNodeForm()
        
        // 如果图谱已显示，重新初始化
        if (showGraph.value) {
          nextTick(() => {
            initGraph()
          })
        }
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }
  })
}

// 编辑节点
const editNode = (node) => {
  editingNode.value = node
  Object.assign(nodeForm, {
    name: node.name,
    description: node.description || '',
    node_type: node.node_type,
    level: node.level,
    prerequisites: node.prerequisites || []
  })
  showCreateNodeDialog.value = true
}

// 删除节点
const deleteNode = async (node) => {
  try {
    await ElMessageBox.confirm('确定要删除这个节点吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 检查是否有相关关系
    const relatedRelations = relations.value.filter(r => 
      r.source_node_id === node.id || r.target_node_id === node.id
    )
    
    if (relatedRelations.length > 0) {
      ElMessage.warning('该节点存在关联关系，请先删除相关关系')
      return
    }
    
    const index = nodes.value.findIndex(n => n.id === node.id)
    if (index !== -1) {
      nodes.value.splice(index, 1)
      ElMessage.success('节点删除成功')
      
      // 如果图谱已显示，重新初始化
      if (showGraph.value) {
        nextTick(() => {
          initGraph()
        })
      }
    }
  } catch (error) {
    // 用户取消
  }
}

// 创建关系
const handleRelationSubmit = async () => {
  if (!relationFormRef.value) return
  
  await relationFormRef.value.validate(async (valid) => {
    if (valid) {
      if (relationForm.source_node_id === relationForm.target_node_id) {
        ElMessage.error('源节点和目标节点不能相同')
        return
      }
      
      // 检查关系是否已存在
      const existingRelation = relations.value.find(r => 
        r.source_node_id === relationForm.source_node_id &&
        r.target_node_id === relationForm.target_node_id &&
        r.relation_type === relationForm.relation_type
      )
      
      if (existingRelation) {
        ElMessage.error('该关系已存在')
        return
      }
      
      try {
        const newRelation = {
          id: Date.now(), // 临时ID
          ...relationForm
        }
        relations.value.push(newRelation)
        ElMessage.success('关系创建成功')
        
        showCreateRelationDialog.value = false
        resetRelationForm()
        
        // 如果图谱已显示，重新初始化
        if (showGraph.value) {
          nextTick(() => {
            initGraph()
          })
        }
      } catch (error) {
        ElMessage.error('创建失败')
      }
    }
  })
}

// 删除关系
const deleteRelation = async (relation) => {
  try {
    await ElMessageBox.confirm('确定要删除这个关系吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const index = relations.value.findIndex(r => r.id === relation.id)
    if (index !== -1) {
      relations.value.splice(index, 1)
      ElMessage.success('关系删除成功')
      
      // 如果图谱已显示，重新初始化
      if (showGraph.value) {
        nextTick(() => {
          initGraph()
        })
      }
    }
  } catch (error) {
    // 用户取消
  }
}

// 重置表单
const resetNodeForm = () => {
  Object.assign(nodeForm, {
    name: '',
    description: '',
    node_type: '',
    level: 1,
    prerequisites: []
  })
  editingNode.value = null
  nodeFormRef.value?.resetFields()
}

const resetRelationForm = () => {
  Object.assign(relationForm, {
    source_node_id: null,
    target_node_id: null,
    relation_type: '',
    weight: 1.0
  })
  relationFormRef.value?.resetFields()
}

onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
.knowledge-graph-container {
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
  
  .page-actions {
    display: flex;
    gap: 12px;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-bar {
  margin-bottom: 16px;
}

.node-list {
  max-height: 400px;
  overflow-y: auto;
  
  .node-item {
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
    
    .node-info {
      flex: 1;
      
      .node-name {
        font-weight: 500;
        color: #333;
        margin-bottom: 4px;
      }
      
      .node-meta {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
        
        .node-level {
          font-size: 12px;
          color: #666;
        }
      }
      
      .node-desc {
        font-size: 12px;
        color: #666;
        line-height: 1.4;
      }
    }
    
    .node-actions {
      display: flex;
      gap: 4px;
    }
  }
}

.relation-list {
  max-height: 400px;
  overflow-y: auto;
  
  .relation-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    border: 1px solid #e4e7ed;
    border-radius: 6px;
    margin-bottom: 8px;
    
    .relation-info {
      flex: 1;
      
      .relation-nodes {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
        
        .relation-arrow {
          color: #409eff;
        }
        
        .source-node,
        .target-node {
          font-size: 14px;
          color: #333;
        }
      }
      
      .relation-meta {
        display: flex;
        align-items: center;
        gap: 8px;
        
        .relation-weight {
          font-size: 12px;
          color: #666;
        }
      }
    }
    
    .relation-actions {
      display: flex;
      gap: 4px;
    }
  }
}

.graph-container {
  height: 500px;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
}

.graph-controls {
  display: flex;
  gap: 8px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
