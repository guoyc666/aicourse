<template>
  <div class="question-management-container">
    <div class="header">
      <h2>题目管理</h2>
      <el-button type="primary" @click="showCreateDialog">添加题目</el-button>
    </div>

    <!-- 筛选条件 -->
    <el-form :inline="true" :model="filterForm" class="filter-form">
      <el-form-item label="知识点">
        <el-select v-model="filterForm.knowledge_id" placeholder="选择知识点" clearable style="width: 200px;">
          <el-option label="全部" value="" />
          <el-option v-for="node in knowledgeNodes" :key="node.id" :label="node.name" :value="node.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="题目类型">
        <el-select v-model="filterForm.type" placeholder="选择类型" clearable style="width: 200px;">
          <el-option label="全部" value="" />
          <el-option label="选择题" value="choice" />
          <el-option label="填空题" value="fill" />
          <el-option label="编程题" value="code" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleFilter">查询</el-button>
        <el-button @click="resetFilter">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 题目列表 -->
    <el-table v-loading="loading" :data="questions" style="width: 100%">
      <el-table-column prop="question_id" label="ID" width="80" />
      <el-table-column prop="text" label="题目内容" min-width="400">
        <template #default="scope">
          <el-tooltip :content="scope.row.text" placement="top">
            <span>{{ truncateText(scope.row.text, 100) }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column prop="type" label="类型" width="100">
        <template #default="scope">
          <el-tag :type="getTypeTag(scope.row.type)">
            {{ getTypeName(scope.row.type) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="knowledge_id" label="知识点" min-width="150">
        <template #default="scope">
          <div v-for="(kid, index) in scope.row.knowledge_id" :key="`knowledge_${index}_${kid}`" class="knowledge-tag">
            {{ getKnowledgeName(kid) }}
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="difficulty" label="难度" width="180">
          <template #default="scope">
            <div style="display: flex; align-items: center; justify-content: center;">
              <el-rate disabled :max="5" :model-value="convertedDifficulty(scope.row.difficulty)" />
              <span style="margin-left: 5px;">{{ Math.round(scope.row.difficulty * 100) }}%</span>
            </div>
          </template>
        </el-table-column>
      <el-table-column prop="correct_rate" label="正确率" width="100">
        <template #default="scope">
          <el-progress :percentage="Math.round(scope.row.correct_rate * 100)" :color="getProgressColor(scope.row.correct_rate)" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="scope">
          <el-button type="primary" link size="small" @click="showEditDialog(scope.row)">
            编辑
          </el-button>
          <el-button type="danger" link size="small" @click="handleDelete(scope.row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="pagination.current"
        v-model:page-size="pagination.size"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 添加题目对话框 -->
    <el-dialog v-model="createDialogVisible" title="添加题目" width="800px">
      <el-form ref="createFormRef" :model="createForm" :rules="formRules" label-width="100px">
        <el-form-item label="题目内容" prop="text">
          <el-input v-model="createForm.text" type="textarea" placeholder="请输入题目内容" :rows="4" />
        </el-form-item>
        <el-form-item label="题目类型" prop="type">
          <el-radio-group v-model="createForm.type" @change="handleTypeChange">
            <el-radio label="choice">选择题</el-radio>
            <el-radio label="fill">填空题</el-radio>
            <el-radio label="code">编程题</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="createForm.type === 'code'" label="编程语言" prop="code_language">
          <el-select v-model="createForm.code_language" placeholder="选择编程语言" style="width: 200px" @change="handleLanguageChange('create')">
            <el-option label="Python" value="python" />
            <el-option label="C" value="c" />
            <el-option label="C++" value="cpp" />
            <el-option label="Java" value="java" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="createForm.type === 'choice'" label="选项" prop="options">
          <div class="options-container">
            <div v-for="(option, index) in createForm.optionsList" :key="`create_option_${index}_${option.value}`" class="option-item">
              <el-input v-model="option.value" placeholder="选项内容" prefix-icon="el-icon-circle-check" />
              <el-button type="danger" icon="el-icon-delete" circle size="small" @click="removeOption(index)" />
            </div>
            <el-button type="primary" link @click="addOption">添加选项</el-button>
          </div>
        </el-form-item>
        <el-form-item label="正确答案" prop="answer">
          <el-input v-model="createForm.answer" :placeholder="createForm.type === 'code' ? '可填写参考说明或函数签名（学生答案以代码为准）' : '请输入正确答案'" />
          <div v-if="createForm.type === 'choice'" class="hint">提示：请输入选项字母（如A、B、C、D）</div>
        </el-form-item>
        <el-form-item label="知识点" prop="knowledge_id">
          <el-select v-model="createForm.knowledge_id" multiple placeholder="选择知识点" collapse-tags style="width: 100%" clearable>
            <el-option v-for="node in knowledgeNodes" :key="node.id" :label="node.name" :value="node.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="难度系数" prop="difficulty">
          <div style="display: flex; align-items: center;">
            <el-rate v-model="createForm.difficultyDisplay" :max="5" />
            <span style="margin-left: 10px;">{{ Math.round((createForm.difficulty || 0) * 100) }}%</span>
          </div>
          <div class="hint">（0%表示最简单，100%表示最难）</div>
        </el-form-item>
        <el-form-item v-if="createForm.type === 'code'" label="测试用例">
          <div class="code-examples-container">
            <div
              v-for="(example, index) in createForm.codeExamples"
              :key="`create_example_${index}_${example.input}_${example.output}`"
              class="code-example-item"
            >
              <el-input
                v-model="example.input"
                type="textarea"
                :rows="2"
                placeholder="输入示例（作为 solve(input_str) 的参数 input_str）"
                class="code-example-input"
              />
              <el-input
                v-model="example.output"
                type="textarea"
                :rows="2"
                placeholder="期望输出（将与 solve 返回值的字符串进行精确比较）"
                class="code-example-output"
              />
              <el-button
                type="danger"
                icon="el-icon-delete"
                circle
                size="small"
                @click="removeCreateCodeExample(index)"
              />
            </div>
            <el-button type="primary" link @click="addCreateCodeExample">添加测试用例</el-button>
            <div class="hint">
              {{ getLanguageHint(createForm.code_language) }}
            </div>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleCreateQuestion">添加</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑题目对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑题目" width="800px">
      <el-form ref="editFormRef" :model="editForm" :rules="formRules" label-width="100px">
        <el-form-item label="题目内容" prop="text">
          <el-input v-model="editForm.text" type="textarea" placeholder="请输入题目内容" :rows="4" />
        </el-form-item>
        <el-form-item label="题目类型" prop="type">
          <el-radio-group v-model="editForm.type" @change="handleEditTypeChange">
            <el-radio label="choice">选择题</el-radio>
            <el-radio label="fill">填空题</el-radio>
            <el-radio label="code">编程题</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="editForm.type === 'code'" label="编程语言" prop="code_language">
          <el-select v-model="editForm.code_language" placeholder="选择编程语言" style="width: 200px" @change="handleLanguageChange('edit')">
            <el-option label="Python" value="python" />
            <el-option label="C" value="c" />
            <el-option label="C++" value="cpp" />
            <el-option label="Java" value="java" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="editForm.type === 'choice'" label="选项" prop="options">
          <div class="options-container">
            <div v-for="(option, index) in editForm.optionsList" :key="`edit_option_${index}_${option.value}`" class="option-item">
              <el-input v-model="option.value" placeholder="选项内容" prefix-icon="el-icon-circle-check" />
              <el-button type="danger" icon="el-icon-delete" circle size="small" @click="removeEditOption(index)" />
            </div>
            <el-button type="primary" link @click="addEditOption">添加选项</el-button>
          </div>
        </el-form-item>
        <el-form-item label="正确答案" prop="answer">
          <el-input v-model="editForm.answer" :placeholder="editForm.type === 'code' ? '可填写参考说明或函数签名（学生答案以代码为准）' : '请输入正确答案'" />
          <div v-if="editForm.type === 'choice'" class="hint">提示：请输入选项字母（如A、B、C、D）</div>
        </el-form-item>
        <el-form-item label="知识点" prop="knowledge_id">
          <el-select v-model="editForm.knowledge_id" multiple placeholder="选择知识点" collapse-tags style="width: 100%" clearable>
            <el-option v-for="node in knowledgeNodes" :key="node.id" :label="node.name" :value="node.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="难度系数" prop="difficulty">
          <div style="display: flex; align-items: center;">
            <el-rate v-model="editForm.difficultyDisplay" :max="5" />
            <span style="margin-left: 10px;">{{ Math.round((editForm.difficulty || 0) * 100) }}%</span>
          </div>
          <div class="hint">0%表示最简单，100%表示最难</div>
        </el-form-item>
        <el-form-item v-if="editForm.type === 'code'" label="测试用例">
          <div class="code-examples-container">
            <div
              v-for="(example, index) in editForm.codeExamples"
              :key="`edit_example_${index}_${example.input}_${example.output}`"
              class="code-example-item"
            >
              <el-input
                v-model="example.input"
                type="textarea"
                :rows="2"
                placeholder="输入示例（作为 solve(input_str) 的参数 input_str）"
                class="code-example-input"
              />
              <el-input
                v-model="example.output"
                type="textarea"
                :rows="2"
                placeholder="期望输出（将与 solve 返回值的字符串进行精确比较）"
                class="code-example-output"
              />
              <el-button
                type="danger"
                icon="el-icon-delete"
                circle
                size="small"
                @click="removeEditCodeExample(index)"
              />
            </div>
            <el-button type="primary" link @click="addEditCodeExample">添加测试用例</el-button>
            <div class="hint">
              {{ getLanguageHint(editForm.code_language) }}
            </div>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleUpdateQuestion">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { addQuestion, deleteQuestion, getQuestionList } from '@/api/questions'
import { graphAPI } from '../../api'

// 状态管理
const loading = ref(false)
const questions = ref([])
const total = ref(0)
const knowledgeNodes = ref([])

// 分页
const pagination = reactive({
  current: 1,
  size: 20
})

// 筛选表单
const filterForm = reactive({
  knowledge_id: '',
  type: ''
})

// 创建题目表单
const createDialogVisible = ref(false)
const createForm = reactive({
  text: '',
  type: 'choice',
  optionsList: [{ value: '' }, { value: '' }],
  answer: '',
  knowledge_id: [],
  difficulty: 0.5,
  difficultyDisplay: 3, // 默认3星
  code_language: '', // 不设置默认值
  codeExamples: [
    { input: '', output: '' }
  ]
})

// 编辑题目表单
const editDialogVisible = ref(false)
const editForm = reactive({
  question_id: '',
  text: '',
  type: 'choice',
  optionsList: [{ value: '' }, { value: '' }],
  answer: '',
  knowledge_id: [],
  difficulty: 0.5,
  difficultyDisplay: 3, // 默认3星
  code_language: '', // 不设置默认值
  codeExamples: [
    { input: '', output: '' }
  ]
})

// 表单验证规则
const formRules = {
  text: [{ required: true, message: '请输入题目内容', trigger: 'blur' }],
  type: [{ required: true, message: '请选择题目类型', trigger: 'change' }],
  answer: [{ required: true, message: '请输入正确答案', trigger: 'blur' }],
  knowledge_id: [{ required: true, message: '请选择至少一个知识点', trigger: 'change' }]
}

// 加载题目列表
const loadQuestions = async () => {
  loading.value = true
  try {
    console.log('请求参数:', {
      page: pagination.current,
      pageSize: pagination.size,
      knowledge_id: filterForm.knowledge_id || null,
      type: filterForm.type || null
    })
    const data = await getQuestionList(
      pagination.current,
      pagination.size,
      filterForm.knowledge_id || null,
      filterForm.type || null
    )
    console.log('获取题目列表响应数据:', data)
    // 由于响应拦截器直接返回了response.data，所以这里直接使用data
    if (data.code === 200) {
      questions.value = data.data?.list || []
      total.value = data.data?.total || 0
    } else {
      ElMessage.error(data.message || '获取题目列表失败')
      console.error('接口返回错误:', data.message)
    }
  } catch (error) {
    ElMessage.error('获取题目列表失败')
    console.error('获取题目列表异常:', error)
    console.error('错误详情:', error.response ? error.response.data : error)
  } finally {
    loading.value = false
  }
}

// 加载知识点列表
const loadKnowledgeNodes = async () => {
  try {
    const data = await graphAPI.fetchAllKnowledgeNodes()
    console.log('获取知识点列表响应:', data)
    knowledgeNodes.value = data
  } catch (error) {
    console.error('获取知识点列表失败:', error)
    // 如果获取失败，设置默认的空数组
    knowledgeNodes.value = []
  }
}

// 处理筛选
const handleFilter = () => {
  pagination.current = 1
  loadQuestions()
}

// 重置筛选
const resetFilter = () => {
  filterForm.knowledge_id = ''
  filterForm.type = ''
  pagination.current = 1
  loadQuestions()
}

// 分页处理
const handleSizeChange = (size) => {
  pagination.size = size
  loadQuestions()
}

const handleCurrentChange = (current) => {
  pagination.current = current
  loadQuestions()
}

// 显示创建对话框
const showCreateDialog = () => {
  createForm.text = ''
  createForm.type = 'choice'
  createForm.optionsList = [{ value: '' }, { value: '' }]
  createForm.answer = ''
  createForm.knowledge_id = []
  createForm.difficulty = 0.5
  createForm.difficultyDisplay = 3
  createForm.codeExamples = [{ input: '', output: '' }]
  createDialogVisible.value = true
}

// 显示编辑对话框
const showEditDialog = (question) => {
  editForm.question_id = question.question_id
  editForm.text = question.text
  editForm.type = question.type
  
  // 处理选项
  if (question.type === 'choice' && question.options) {
    editForm.optionsList = Object.entries(question.options).map(([key, value]) => ({
      value: value
    }))
  } else {
    editForm.optionsList = []
  }
  
  editForm.answer = question.answer
  editForm.knowledge_id = question.knowledge_id || []
  editForm.difficulty = question.difficulty || 0.5
  editForm.difficultyDisplay = Math.round((question.difficulty || 0.5) * 5) // 转换为1-5星星
  editForm.code_language = question.code_language || '' // 不设置默认值
  
  // 处理编程题测试用例
  if (question.type === 'code') {
    try {
      if (question.code_examples) {
        const examples = JSON.parse(question.code_examples)
        editForm.codeExamples = Array.isArray(examples) && examples.length > 0 
          ? examples.map(ex => ({
              input: ex.input || '',
              output: ex.output || ''
            }))
          : [{ input: '', output: '' }]
      } else {
        editForm.codeExamples = [{ input: '', output: '' }]
      }
    } catch (error) {
      console.error('解析测试用例失败:', error)
      editForm.codeExamples = [{ input: '', output: '' }]
    }
  } else {
    editForm.codeExamples = [{ input: '', output: '' }]
  }
  
  editDialogVisible.value = true
}

// 处理题目类型变化（创建）
const handleTypeChange = () => {
  if (createForm.type !== 'choice') {
    createForm.optionsList = []
  } else if (createForm.optionsList.length === 0) {
    createForm.optionsList = [{ value: '' }, { value: '' }]
  }
  if (createForm.type === 'code' && (!createForm.codeExamples || createForm.codeExamples.length === 0)) {
    createForm.codeExamples = [{ input: '', output: '' }]
  }
}

// 处理题目类型变化（编辑）
const handleEditTypeChange = () => {
  if (editForm.type !== 'choice') {
    editForm.optionsList = []
  } else if (editForm.optionsList.length === 0) {
    editForm.optionsList = [{ value: '' }, { value: '' }]
  }
  if (editForm.type === 'code' && (!editForm.codeExamples || editForm.codeExamples.length === 0)) {
    editForm.codeExamples = [{ input: '', output: '' }]
  }
}

// 获取编程语言提示信息
const getLanguageHint = (codeLanguage) => {
  const hints = {
    python: '学生需要在答案中实现函数 solve(input_str: str) -> str，所有测试用例的输出都匹配才判定为正确。',
    c: '学生需要在答案中实现函数 solve(input_str) -> str（使用char*），所有测试用例的输出都匹配才判定为正确。',
    cpp: '学生需要在答案中实现函数 solve(input_str) -> std::string，所有测试用例的输出都匹配才判定为正确。',
    java: '学生需要在答案中实现类中的solve(input_str) -> String方法，所有测试用例的输出都匹配才判定为正确。'
  }
  
  // 处理枚举值格式（如 "CodeLanguage.java"）
  if (codeLanguage && typeof codeLanguage === 'string') {
    let languageKey = codeLanguage
    // 如果包含点号，提取枚举值部分
    if (codeLanguage.includes('.')) {
      languageKey = codeLanguage.split('.').pop()
      console.log(`处理枚举值提示: ${codeLanguage} -> ${languageKey}`)
    }
    return hints[languageKey] || hints.python
  }
  
  return hints.python
}

// 处理编程语言变化
const handleLanguageChange = (formType) => {
  const form = formType === 'create' ? createForm : editForm
  const codeLanguage = form.code_language
  console.log(`切换到${formType}表单的${codeLanguage}语言提示`)
}

// 编程题测试用例（创建）
const addCreateCodeExample = () => {
  createForm.codeExamples.push({ input: '', output: '' })
}

const removeCreateCodeExample = (index) => {
  if (createForm.codeExamples.length <= 1) {
    ElMessage.warning('至少需要一个测试用例')
    return
  }
  createForm.codeExamples.splice(index, 1)
}

// 编程题测试用例（编辑）
const addEditCodeExample = () => {
  editForm.codeExamples.push({ input: '', output: '' })
}

const removeEditCodeExample = (index) => {
  if (editForm.codeExamples.length <= 1) {
    ElMessage.warning('至少需要一个测试用例')
    return
  }
  editForm.codeExamples.splice(index, 1)
}

// 添加选项（创建）
const addOption = () => {
  createForm.optionsList.push({ value: '' })
}

// 移除选项（创建）
const removeOption = (index) => {
  if (createForm.optionsList.length > 2) {
    createForm.optionsList.splice(index, 1)
  } else {
    ElMessage.warning('至少需要两个选项')
  }
}

// 添加选项（编辑）
const addEditOption = () => {
  editForm.optionsList.push({ value: '' })
}

// 移除选项（编辑）
const removeEditOption = (index) => {
  if (editForm.optionsList.length > 2) {
    editForm.optionsList.splice(index, 1)
  } else {
    ElMessage.warning('至少需要两个选项')
  }
}

// 创建题目
const handleCreateQuestion = async () => {
  try {
    // 构建选项（选择题）
    let options = null
    if (createForm.type === 'choice') {
      const optionsObj = {}
      const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
      createForm.optionsList.forEach((option, index) => {
        if (option.value) {
          optionsObj[letters[index]] = option.value
        }
      })
      options = JSON.stringify(optionsObj)
    }

    // 构建表单数据
    const formData = new FormData()
    formData.append('text', createForm.text)
    formData.append('type', createForm.type)
    if (options) {
      formData.append('options', options)
    }
    formData.append('answer', createForm.answer)
    // 编程题测试用例
    if (createForm.type === 'code') {
      const examples = (createForm.codeExamples || [])
        .map(ex => ({
          input: (ex.input || '').trim(),
          output: (ex.output || '').trim()
        }))
        .filter(ex => ex.input !== '' && ex.output !== '')
      if (examples.length === 0) {
        ElMessage.warning('请至少填写一个完整的测试用例（输入和输出都不能为空）')
        return
      }
      formData.append('code_examples', JSON.stringify(examples))
    }
    formData.append('knowledge_id', JSON.stringify(createForm.knowledge_id))
    formData.append('difficulty', createForm.difficulty.toString())
    // 编程题添加编程语言字段（仅在有值时才提交）
    if (createForm.type === 'code' && createForm.code_language) {
      formData.append('code_language', createForm.code_language)
    }

    const data = await addQuestion(formData)
    console.log('添加题目响应:', data)
    if (data.code === 200) {
      ElMessage.success('题目添加成功')
      createDialogVisible.value = false
      loadQuestions()
    } else {
      ElMessage.error(data.message || '添加失败')
    }
  } catch (error) {
    ElMessage.error('添加题目失败')
    console.error('添加题目失败:', error)
  }
}

// 更新题目
const handleUpdateQuestion = async () => {
  try {
    // 构建选项（选择题）
    let options = null
    if (editForm.type === 'choice') {
      const optionsObj = {}
      const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
      editForm.optionsList.forEach((option, index) => {
        if (option.value) {
          optionsObj[letters[index]] = option.value
        }
      })
      options = JSON.stringify(optionsObj)
    }

    // 构建表单数据
    const formData = new FormData()
    formData.append('text', editForm.text)
    formData.append('type', editForm.type)
    if (options) {
      formData.append('options', options)
    }
    formData.append('answer', editForm.answer)
    // 编程题测试用例
    if (editForm.type === 'code') {
      const examples = (editForm.codeExamples || [])
        .map(ex => ({
          input: (ex.input || '').trim(),
          output: (ex.output || '').trim()
        }))
        .filter(ex => ex.input !== '' && ex.output !== '')
      if (examples.length === 0) {
        ElMessage.warning('请至少填写一个完整的测试用例（输入和输出都不能为空）')
        return
      }
      formData.append('code_examples', JSON.stringify(examples))
    }
    formData.append('knowledge_id', JSON.stringify(editForm.knowledge_id))
    formData.append('difficulty', editForm.difficulty.toString())
    // 编程题添加编程语言字段（仅在有值时才提交）
    if (editForm.type === 'code' && editForm.code_language) {
      formData.append('code_language', editForm.code_language)
    }

    // 这里应该调用更新接口，但目前后端没有提供更新接口，可以先删除再创建
    await deleteQuestion(editForm.question_id)
    const data = await addQuestion(formData)
    console.log('更新题目响应:', data)
    
    if (data.code === 200) {
      ElMessage.success('题目更新成功')
      editDialogVisible.value = false
      loadQuestions()
    } else {
      ElMessage.error(data.message || '更新失败')
    }
  } catch (error) {
    ElMessage.error('更新题目失败')
    console.error('更新题目失败:', error)
  }
}

// 删除题目
const handleDelete = async (question) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除题目「${truncateText(question.text, 50)}」吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const data = await deleteQuestion(question.question_id)
    console.log('删除题目响应:', data)
    if (data.code === 200) {
      ElMessage.success('题目删除成功')
      loadQuestions()
    } else {
      ElMessage.error(data.message || '删除失败')
    }
  } catch (error) {
    if (error === 'cancel') {
      return
    }
    ElMessage.error('删除题目失败')
    console.error('删除题目失败:', error)
  }
}

// 辅助函数
const truncateText = (text, maxLength) => {
  if (!text || text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const convertedDifficulty = (value) => {
  // 0-1 转换到 1-5
  return Math.round((value || 0) * 5)
}

// 监听难度显示变化，更新实际难度值
watch(() => createForm.difficultyDisplay, (newVal) => {
  createForm.difficulty = newVal / 5
}, { immediate: true })

watch(() => editForm.difficultyDisplay, (newVal) => {
  editForm.difficulty = newVal / 5
}, { immediate: true })

const getTypeName = (type) => {
  const typeMap = {
    choice: '选择题',
    fill: '填空题',
    code: '编程题'
  }
  return typeMap[type] || type
}

const getTypeTag = (type) => {
  const tagMap = {
    choice: 'primary',
    fill: 'success',
    code: 'warning'
  }
  return tagMap[type] || 'info'
}

const getKnowledgeName = (knowledgeId) => {
  const node = knowledgeNodes.value.find(n => n.id === knowledgeId)
  return node ? node.name : knowledgeId
}

const getProgressColor = (rate) => {
  if (rate >= 0.8) return '#67c23a'
  if (rate >= 0.6) return '#e6a23c'
  return '#f56c6c'
}

// 初始化
onMounted(() => {
  loadQuestions()
  loadKnowledgeNodes()
})
</script>

<style scoped>
.question-management-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-form {
  margin-bottom: 20px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}

.options-container {
  margin-top: 10px;
}

.option-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.option-item .el-input {
  flex: 1;
  margin-right: 10px;
}

.knowledge-tag {
  display: inline-block;
  background: #ecf5ff;
  color: #409eff;
  padding: 2px 8px;
  margin-right: 5px;
  margin-bottom: 5px;
  border-radius: 3px;
  font-size: 12px;
}

.hint {
  color: #909399;
  font-size: 12px;
  margin-top: 5px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>