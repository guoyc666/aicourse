<template>
  <div class="user-management-container">
    <div class="header">
      <h2>用户管理</h2>
      <div class="search-filter-container">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索用户名"
          clearable
          style="width: 200px; margin-right: 10px;"
          @keyup.enter="handleSearch"
        >
          <template #append>
            <el-button icon="Search" @click="handleSearch" />
          </template>
        </el-input>
        <el-select
          v-model="selectedRoleIdFilter"
          placeholder="选择角色"
          clearable
          style="width: 120px; margin-right: 10px;"
          @change="handleSearch"
        >
          <el-option label="全部" value="" />
          <el-option v-for="role in allRoles" :key="role.id" :label="role.name" :value="role.id" />
        </el-select>
        <el-button type="primary" @click="showCreateDialog">创建用户</el-button>
      </div>
    </div>
    
    <el-table v-loading="loading" :data="users" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" width="180" />
      <el-table-column prop="full_name" label="姓名" width="180" />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column prop="roles" label="角色" width="200">
        <template #default="scope">
          <span v-for="role in scope.row.roles" :key="role.id" class="role-tag">
            {{ role.name }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="scope">
          <el-button type="primary" link @click="showUserDetail(scope.row)">
            详情
          </el-button>
          <el-button type="danger" link @click="handleDelete(scope.row.id, scope.row.username)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 创建用户对话框 -->
    <el-dialog v-model="createDialogVisible" title="创建用户" width="500px">
      <el-form ref="createFormRef" :model="createForm" :rules="createRules" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="createForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="createForm.full_name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="createForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
            <el-select v-model="createForm.role" placeholder="请选择角色">
              <el-option label="学生" value="student" />
              <el-option label="教师" value="teacher" />
            </el-select>
          </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleCreateUser">创建</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 用户详情对话框 -->
    <el-dialog v-model="detailDialogVisible" :title="currentUser?.username + ' - 详情'" width="600px">
      <div v-if="currentUser" class="user-detail">
        <div class="detail-item">
          <span class="detail-label">ID：</span>
          <span class="detail-value">{{ currentUser.id }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">用户名：</span>
          <span class="detail-value">{{ currentUser.username }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">姓名：</span>
          <span class="detail-value">{{ currentUser.full_name }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">创建时间：</span>
          <span class="detail-value">{{ formatDate(currentUser.created_at) }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">当前角色：</span>
          <span v-for="role in currentUser.roles" :key="role.id" class="role-tag">
            {{ role.name }}
          </span>
        </div>
        <div class="detail-item" v-if="allRoles.length > 0">
          <span class="detail-label">分配角色：</span>
          <el-select v-model="selectedRoleId" placeholder="请选择角色" style="width: 200px;">
            <el-option v-for="role in allRoles" :key="role.id" :label="role.name" :value="role.id" />
          </el-select>
          <el-button type="primary" size="small" @click="handleAssignRole">分配</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsers, deleteUser, getRoles, assignRoleToUser, removeRoleFromUser } from '@/api/users'
import { register } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 状态管理
const loading = ref(false)
const users = ref([])
const allRoles = ref([])
const searchKeyword = ref('')
const selectedRoleIdFilter = ref('')

// 对话框状态
const createDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const currentUser = ref(null)
const selectedRoleId = ref('')

// 创建用户表单
const createForm = reactive({
  username: '',
  full_name: '',
  password: '',
  role: 'student'
})

const createRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  full_name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}

const createFormRef = ref(null)

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 加载用户列表
const loadUsers = async (keyword = '', roleId = '') => {
  loading.value = true
  try {
    // 构建查询参数
    const params = {}
    if (keyword) params.keyword = keyword
    if (roleId) params.role_id = roleId
    
    const response = await getUsers(params)
    users.value = response.data || response
  } catch (error) {
    ElMessage.error('获取用户列表失败')
    console.error('获取用户列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 处理搜索
const handleSearch = () => {
  loadUsers(searchKeyword.value, selectedRoleIdFilter.value)
}

// 加载角色列表
const loadRoles = async () => {
  try {
    const response = await getRoles()
    allRoles.value = response.data || response
  } catch (error) {
    console.error('获取角色列表失败:', error)
  }
}

// 显示创建用户对话框
const showCreateDialog = () => {
  Object.keys(createForm).forEach(key => {
    createForm[key] = key === 'role' ? 'student' : ''
  })
  createDialogVisible.value = true
}

// 处理创建用户
const handleCreateUser = async () => {
  try {
    await createFormRef.value.validate()
    
    const userData = {
      ...createForm,
      role: createForm.role // 传递角色信息给后端
    }
    
    await register(userData)
    ElMessage.success('用户创建成功')
    createDialogVisible.value = false
    loadUsers() // 重新加载用户列表
  } catch (error) {
    if (error.name === 'ValidationError') {
      return
    }
    ElMessage.error('用户创建失败')
    console.error('创建用户失败:', error)
  }
}

// 显示用户详情
const showUserDetail = async (user) => {
  currentUser.value = { ...user }
  selectedRoleId.value = ''
  detailDialogVisible.value = true
}

// 处理删除用户
const handleDelete = async (userId, username) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${username}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await deleteUser(userId)
    ElMessage.success('用户删除成功')
    loadUsers() // 重新加载用户列表
  } catch (error) {
    if (error === 'cancel') {
      return
    }
    ElMessage.error('用户删除失败')
    console.error('删除用户失败:', error)
  }
}

// 处理分配角色
const handleAssignRole = async () => {
  if (!selectedRoleId.value || !currentUser.value) {
    ElMessage.warning('请选择角色')
    return
  }
  
  try {
    // 检查用户是否已有角色
    if (currentUser.value.roles && currentUser.value.roles.length > 0) {
      // 移除用户已有的所有角色
      for (const role of currentUser.value.roles) {
        // 如果已有角色与要分配的角色相同，则跳过
        if (role.id === parseInt(selectedRoleId.value)) {
          ElMessage.info('用户已有该角色，无需重复分配')
          return
        }
        await removeRoleFromUser(currentUser.value.id, role.id)
      }
    }
    
    // 分配新角色
    await assignRoleToUser(currentUser.value.id, selectedRoleId.value)
    ElMessage.success('角色分配成功')
    loadUsers() // 重新加载用户列表
    showUserDetail(currentUser.value) // 刷新当前用户详情
  } catch (error) {
    ElMessage.error('角色分配失败')
    console.error('分配角色失败:', error)
  }
}

// 初始化数据
onMounted(() => {
  loadUsers()
  loadRoles()
})
</script>

<style scoped>
.user-management-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-filter-container {
  display: flex;
  align-items: center;
}

.search-filter-container .el-input {
  vertical-align: middle;
}

.role-tag {
  display: inline-block;
  padding: 4px 10px;
  background-color: #f0f2f5;
  border-radius: 10px;
  margin-right: 8px;
  font-size: 12px;
}

.user-detail {
  padding: 20px 0;
}

.detail-item {
  margin-bottom: 16px;
}

.detail-label {
  display: inline-block;
  width: 100px;
  color: #606266;
}

.detail-value {
  font-weight: 500;
}
</style>