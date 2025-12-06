import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import Cookies from 'js-cookie'

// 创建axios实例
const request = axios.create({
  baseURL: '/api',  // 将/api前缀移到这里，所有接口请求不用再带 /api
  timeout: 10000,
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 直接从cookie中获取token，避免在组件外部使用useUserStore
    const token = Cookies.get('token')
    console.log('请求URL:', config.url)
    console.log('请求方法:', config.method)
    console.log('Token存在:', !!token)
    console.log('Token值:', token ? token.substring(0, 10) + '...' : '无')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('已添加Authorization头:', config.headers.Authorization.substring(0, 20) + '...')
    } else {
      console.warn('未找到Token，无法添加Authorization头')
    }
    return config
  },
  (error) => {
    console.error('请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const { response } = error
    
    if (response) {
      switch (response.status) {
        case 401:
          // 区分登录错误和令牌过期错误
          if (response.config.url === '/auth/login') {
            // 登录请求的401，只显示错误信息，不向上传递错误
            ElMessage.error(response.data?.detail || '用户名或密码错误')
            return Promise.resolve(null) // 不向上传递错误，避免重复显示错误提示
          } else {
            // 其他请求的401，显示"登录已过期"
            ElMessage.error('登录已过期，请重新登录')
            // 移除token并跳转到登录页
            Cookies.remove('token')
            router.push('/login')
          }
          break
        case 403:
          // 对于403错误，只reject不显示消息，让调用方处理显示逻辑
          return Promise.reject(error)
        case 404:
          ElMessage.error('请求的资源不存在')
          return Promise.reject(error)
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(response.data?.detail || '请求失败')
      }
    } else {
      ElMessage.error('网络连接失败')
    }
    
    return Promise.reject(error)
  }
)

export default request
