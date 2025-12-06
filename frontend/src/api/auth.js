import request from './request'

export const login = (data) => {
  // 确保数据格式与后端的OAuth2PasswordRequestForm匹配
  const formData = new FormData()
  formData.append('username', data.username)
  formData.append('password', data.password)
  
  return request.post('/auth/login', formData)
}

export const register = (data) => {
  return request.post('/auth/register', data)
}

export const logout = () => {
  return request.post('/auth/logout')
}

export const getUserInfo = () => {
  return request.get('/auth/me')
}
