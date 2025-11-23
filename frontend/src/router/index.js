import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import QuestionsView from '@/views/Questions/index.vue'
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/Register.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      name: 'Layout',
      component: () => import('@/layout/index.vue'),
      meta: { requiresAuth: true },
      redirect: '/dashboard',
      children: [
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: () => import('@/views/Dashboard.vue'),
          meta: { title: 'HOME' }
        },
        {
          path: 'resources',
          name: 'Resources',
          component: () => import('@/views/Resources/index.vue'),
          meta: { title: '知识资源管理', roles: ['teacher', 'admin'] }
        },
        {
          path: 'knowledge-graph',
          name: 'KnowledgeGraph',
          component: () => import('@/views/KnowledgeGraph/index.vue'),
          meta: { title: '知识图谱管理', roles: ['teacher', 'admin'] }
        },

        {
          path: 'learning-path',
          name: 'LearningPath',
          component: () => import('@/views/LearningPath/index.vue'),
          meta: { title: '学习路径推荐', roles: ['student'] }
        },
        {
          path: 'user-management',
          name: 'UserManagement',
          component: () => import('@/views/UserManagement/index.vue'),
          meta: { title: '用户管理', roles: ['admin'] }
        },

        {
          path: 'visualization',
          name: 'Visualization',
          component: () => import('@/views/Visualization/index.vue'),
          meta: { title: '学习过程可视化', roles: ['student'] }
        },
        {
          path: 'ai-assistant/:conv_id?',
          name: 'AIAssistant',
          component: () => import('@/views/AIAssistant/index.vue'),
          meta: { title: 'AI助教' }
        },
        {
          path: 'teacher-tasks',
          name: 'TeacherTasks',
          component: () => import('@/views/Tasks/TeacherTasks.vue'),
          meta: { title: '任务管理', roles: ['teacher', 'admin'] } 
        },
        { 
          path: 'student-progress',
          name: 'StudentProgress',
          component: () => import('@/views/StudentProgress/index.vue'),
          meta: { title: '学生学习状况', roles: ['teacher', 'admin'] } 
        },
          
        {
          path: 'topics',
          name: 'Topics',
          component: () => import('@/views/Topics/index.vue'),
          meta: { title: '讨论区', roles: ['teacher', 'student', 'admin'] } 
        },
        { 
          path: 'topics/:id', 
          name: 'TopicDetail', 
          component: () => import('@/views/Topics/TopicDetail.vue'), 
          meta: { title: '主题详情', roles: ['teacher', 'student', 'admin'] }, 
          hidden: true 
        },
        {
          path: 'student-tasks',
          name: 'StudentTasks',
          component: () => import('@/views/Tasks/StudentTasks.vue'),
          meta: { title: '我的任务', roles: ['student'] }
        },
        {
          path: 'questions',
          name: 'Questions',
          component: QuestionsView,
          meta: {
            title: '题库与评估',
            roles: ['student']
          }
        },
        {
        path: 'question-management',
        name: 'QuestionManagement',
        component: () => import('@/views/Questions/QuestionManagement.vue'),
        meta: {
          title: '题目管理',
          roles: ['teacher', 'admin']
        }
      }
      ]
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 检查是否需要认证
  if (to.meta.requiresAuth !== false && !userStore.isLoggedIn) {
    next('/login')
    return
  }
  
  // 检查角色权限
  if (to.meta.roles && to.meta.roles.length > 0) {
    // 安全获取用户角色，处理可能的undefined情况
    const userRoles = userStore.user?.roles?.map(role => role.name) || []
    
    // 为了开发和测试方便，当用户信息未完全加载时，可以暂时允许访问
    // 注意：生产环境应该严格验证权限
    if (!userStore.user) {
      console.warn('用户信息尚未完全加载，暂时允许访问页面')
      next()
      return
    }
    
    const hasPermission = to.meta.roles.some(role => userRoles.includes(role))
    
    if (!hasPermission) {
      ElMessage.error('您没有权限访问此页面')
      next('/dashboard')
      return
    }
  }
  
  next()
})

export default router
