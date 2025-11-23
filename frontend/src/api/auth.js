import request from './request'

export const login = (data) => {
  // 确保数据格式与后端的OAuth2PasswordRequestForm匹配
  const formData = new FormData()
  formData.append('username', data.username)
  formData.append('password', data.password)
  
  return request({
    url: '/api/auth/login',
    method: 'post',
    data: formData
  })
}

export const register = (data) => {
  return request({
    url: '/api/auth/register',
    method: 'post',
    data
  })
}

export const logout = () => {
  return request({
    url: '/api/auth/logout',
    method: 'post'
  })
}

export const getUserInfo = () => {
  return request({
    url: '/api/auth/me',
    method: 'get'
  })
}
