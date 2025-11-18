<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapse ? '64px' : '200px'" class="sidebar">
      <div class="logo">
        <span v-if="!isCollapse">AI学习系统</span>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :unique-opened="true"
        :collapse-transition="false"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/dashboard">
          <el-icon><House /></el-icon>
          <template #title>HOME</template>
        </el-menu-item>
        
        <!-- 教师和管理员菜单 -->
        <template v-if="userStore.hasRole('teacher') || userStore.hasRole('admin')">
          <el-menu-item index="/resources">
            <el-icon><Folder /></el-icon>
            <template #title>知识资源管理</template>
          </el-menu-item>
          
          <el-menu-item index="/knowledge-graph">
            <el-icon><Share /></el-icon>
            <template #title>知识图谱管理</template>
          </el-menu-item>
          
          <el-menu-item index="/student-progress">
            <el-icon><DataAnalysis /></el-icon>
            <template #title>学生学习状况</template>
          </el-menu-item>
          
          <!-- 仅管理员可见 -->
          <template v-if="userStore.hasRole('admin')">
            <el-menu-item index="/user-management">
              <el-icon><User /></el-icon>
              <template #title>用户管理</template>
            </el-menu-item>
          </template>
        </template>
        
        <!-- 仅教师和管理员可见的菜单 -->
        <template v-if="userStore.hasRole('teacher') || userStore.hasRole('admin')">
          <el-menu-item index="/teacher-tasks">
            <el-icon><Document /></el-icon>
            <template #title>任务管理</template>
          </el-menu-item>
          <el-menu-item index="/question-management">
            <el-icon><Collection /></el-icon>
            <template #title>题目管理</template>
          </el-menu-item>
        </template>
        

        
        <!-- 学生菜单 -->
        <template v-if="userStore.hasRole('student')">
          <el-menu-item index="/learning-path">
            <el-icon><Guide /></el-icon>
            <template #title>学习路径</template>
          </el-menu-item>
          
          <el-menu-item index="/visualization">
            <el-icon><TrendCharts /></el-icon>
            <template #title>学习可视化</template>
          </el-menu-item>
          
          <el-menu-item index="/student-tasks">
            <el-icon><Document /></el-icon>
            <template #title>我的任务</template>
          </el-menu-item>
          
          <el-menu-item index="/questions">
            <el-icon><EditPen /></el-icon>
            <template #title>题库与评估</template>
          </el-menu-item>
        </template>
        
        <el-menu-item index="/topics">
            <el-icon><Message /></el-icon>
            <template #title>讨论区</template>
          </el-menu-item>
          
          <el-menu-item index="/ai-assistant/">
          <el-icon><ChatDotRound /></el-icon>
          <template #title>AI助教</template>
        </el-menu-item>
        

      </el-menu>
    </el-aside>
    
    <!-- 主内容区 -->
    <el-container>
      <!-- 顶部导航 -->
      <el-header class="header">
        <div class="header-left">
          <el-button 
            type="text" 
            @click="toggleCollapse"
            class="collapse-btn"
          >
            <el-icon><Expand v-if="isCollapse" /><Fold v-else /></el-icon>
          </el-button>
          
          <el-breadcrumb separator="/">
            <el-breadcrumb-item 
              v-for="item in breadcrumbs" 
              :key="item.path"
              :to="item.path"
            >
              {{ item.title }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <div class="user-info">
              <el-avatar :size="32" :src="userStore.user?.avatar">
                {{ userStore.user?.full_name?.charAt(0) }}
              </el-avatar>
              <span class="username">{{ userStore.user?.full_name || userStore.user?.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <!-- 主要内容 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Message, DataAnalysis, House, Folder, Share, User } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapse = ref(false)

const activeMenu = computed(() => route.path)

const breadcrumbs = computed(() => {
  const matched = route.matched.filter(item => item.meta && item.meta.title)
  return matched.map(item => ({
    title: item.meta.title,
    path: item.path
  }))
})

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

const handleCommand = async (command) => {
  if (command === 'logout') {
    try {
      await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      await userStore.logoutUser()
      ElMessage.success('退出成功')
      router.push('/login')
    } catch (error) {
      // 用户取消
    }
  }
}
</script>

<style lang="scss" scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  transition: width 0.28s;
  
  .logo {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 18px;
    font-weight: bold;
    
    img {
      height: 32px;
      margin-right: 8px;
    }
  }
  
  .sidebar-menu {
    border: none;
    background-color: #304156;
    
    :deep(.el-menu-item) {
      color: #bfcbd9;
      
      &:hover {
        background-color: #263445;
        color: #409eff;
      }
      
      &.is-active {
        background-color: #409eff;
        color: white;
      }
    }
  }
}

.header {
  background-color: white;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  
  .header-left {
    display: flex;
    align-items: center;
    
    .collapse-btn {
      margin-right: 20px;
      font-size: 18px;
    }
  }
  
  .header-right {
    .user-info {
      display: flex;
      align-items: center;
      cursor: pointer;
      padding: 8px 12px;
      border-radius: 4px;
      transition: background-color 0.3s;
      
      &:hover {
        background-color: #f5f7fa;
      }
      
      .username {
        margin: 0 8px;
        font-size: 14px;
      }
    }
  }
}

.main-content {
  background-color: #f5f7fa;
  padding: 20px;
}
</style>
