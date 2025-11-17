import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { login, logout, getUserInfo } from '@/api/auth'
import Cookies from 'js-cookie'
export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(Cookies.get('token') || '')
  
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  
  const userRoles = computed(() => {
    if (!user.value?.roles) return []
    return user.value.roles.map(role => role.name)
  })
  
  const hasRole = (roleName) => {
    return userRoles.value.includes(roleName)
  }
  
  const hasPermission = (permission) => {
    if (!user.value?.roles) return false
    return user.value.roles.some(role => 
      role.permissions?.some(perm => perm.name === permission)
    )
  }
  
  const loginUser = async (credentials) => {
    try {
      const response = await login(credentials)
      console.log('登录响应:', response)
      token.value = response.access_token
      user.value = response.user
      
      // 保存token到cookie
      Cookies.set('token', token.value, { expires: 7 })
      console.log('Token已保存到Cookie:', token.value)
      
      return response
    } catch (error) {
      console.error('登录失败:', error)
      throw error
    }
  }
  
  const logoutUser = async () => {
    try {
      await logout()
    } catch (error) {
      console.error('登出失败:', error)
    } finally {
      token.value = ''
      user.value = null
      Cookies.remove('token')
    }
  }
  
  const initUser = async () => {
    if (token.value) {
      try {
        const userInfo = await getUserInfo()
        user.value = userInfo
      } catch (error) {
        console.error('获取用户信息失败:', error)
        logoutUser()
      }
    }
  }
  
  const updateUser = (userData) => {
    user.value = { ...user.value, ...userData }
  }
  
  return {
    user,
    token,
    isLoggedIn,
    userRoles,
    hasRole,
    hasPermission,
    loginUser,
    logoutUser,
    initUser,
    updateUser
  }
})
