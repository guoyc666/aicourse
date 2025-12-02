import request from './request'

// 获取用户列表
export const getUsers = (params = {}) => {
  return request({
    url: '/api/users/',
    method: 'get',
    params
  })
}

export const getStudents = (params = {}) => {
  return request({
    url: '/api/users/students/',
    method: 'get',
    params
  })
}

// 获取特定用户信息
export const getUser = (userId) => {
  return request({
    url: `/api/users/${userId}`,
    method: 'get'
  })
}

// 更新用户信息
export const updateUser = (userId, data) => {
  return request({
    url: `/api/users/${userId}`,
    method: 'put',
    data
  })
}

// 删除用户
export const deleteUser = (userId) => {
  return request({
    url: `/api/users/${userId}`,
    method: 'delete'
  })
}

// 获取角色列表
export const getRoles = () => {
  return request({
    url: '/api/users/roles/',
    method: 'get'
  })
}

// 为用户分配角色
export const assignRoleToUser = (userId, roleId) => {
  return request({
    url: `/api/users/${userId}/roles/${roleId}`,
    method: 'post'
  })
}

// 移除用户角色
export const removeRoleFromUser = (userId, roleId) => {
  return request({
    url: `/api/users/${userId}/roles/${roleId}`,
    method: 'delete'
  })
}