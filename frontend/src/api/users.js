import request from './request'

// 获取用户列表
export const getUsers = (params = {}) => {
  return request.get('/users/', { params })
}

export const getStudents = (params = {}) => {
  return request.get('/users/students/', { params })
}

// 获取特定用户信息
export const getUser = (userId) => {
  return request.get(`/users/${userId}`)
}

// 更新用户信息
export const updateUser = (userId, data) => {
  return request.put(`/users/${userId}`, data)
}

// 删除用户
export const deleteUser = (userId) => {
  return request.delete(`/users/${userId}`)
}

// 获取角色列表
export const getRoles = () => {
  return request.get('/users/roles/')
}

// 为用户分配角色
export const assignRoleToUser = (userId, roleId) => {
  return request.post(`/users/${userId}/roles/${roleId}`)
}

// 移除用户角色
export const removeRoleFromUser = (userId, roleId) => {
  return request.delete(`/users/${userId}/roles/${roleId}`)
}