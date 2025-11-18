import '@/api/interceptors';
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

import App from './App.vue'
import router from './router'
import './styles/index.scss'
import { useUserStore } from './stores/user'

const app = createApp(App)

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(ElementPlus, {
  locale: zhCn,
})

// 应用挂载
app.mount('#app')

// 挂载后初始化用户信息（避免阻塞应用启动）
const initAppData = async () => {
  const userStore = useUserStore()
  try {
    await userStore.initUser()
    // 用户信息初始化完成后，如果需要可以进行额外处理
  } catch (error) {
    console.error('用户信息初始化失败:', error)
  }
}

// 延迟初始化，确保应用已经挂载
setTimeout(() => {
  initAppData()
}, 100)
