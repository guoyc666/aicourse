import request from './request'

/**
 * 创建新任务（教师权限）
 * @param {Object} taskData - 任务数据
 * @param {string} taskData.title - 任务标题
 * @param {string} [taskData.description] - 任务描述
 * @param {Date} [taskData.due_date] - 截止日期
 * @param {Array<number>} taskData.student_ids - 要分配任务的学生ID列表
 * @returns {Promise<Object>} 创建的任务
 */
export const createTask = (taskData) => {
  return request({ 
    url: '/api/tasks/', 
    method: 'post', 
    data: taskData 
  })
}

/**
 * 获取任务列表
 * - 教师：获取自己创建的所有任务
 * - 学生：获取分配给自己的所有任务
 * @param {Object} [params] - 查询参数
 * @param {number} [params.skip=0] - 跳过的条数
 * @param {number} [params.limit=100] - 返回的最大条数
 * @returns {Promise<Array>} 任务列表
 */
export const getTasks = (params = {}) => {
  return request({ 
    url: '/api/tasks/', 
    method: 'get', 
    params 
  })
}

/**
 * 获取分配给当前用户的任务详情列表（学生功能）
 * @returns {Promise<Array>} 分配任务列表
 */
export const getAssignedTasks = () => {
  return request({ 
    url: '/api/tasks/assigned/', 
    method: 'get' 
  })
}

/**
 * 获取任务详情
 * @param {number} taskId - 任务ID
 * @returns {Promise<Object>} 任务详情
 */
export const getTask = (taskId) => {
  return request({ 
    url: `/api/tasks/${taskId}/`, 
    method: 'get' 
  })
}

/**
 * 更新任务（教师权限）
 * @param {number} taskId - 任务ID
 * @param {Object} taskData - 更新的任务数据
 * @param {string} [taskData.title] - 任务标题
 * @param {string} [taskData.description] - 任务描述
 * @param {Date} [taskData.due_date] - 截止日期
 * @returns {Promise<Object>} 更新后的任务
 */
export const updateTask = (taskId, taskData) => {
  return request({ 
    url: `/api/tasks/${taskId}/`, 
    method: 'put', 
    data: taskData 
  })
}

/**
 * 删除任务（教师权限）
 * @param {number} taskId - 任务ID
 * @returns {Promise<Object>} 删除结果
 */
export const deleteTask = (taskId) => {
  return request({ 
    url: `/api/tasks/${taskId}/`, 
    method: 'delete' 
  })
}

/**
 * 确认任务完成（学生功能）
 * @param {number} assignedTaskId - 分配任务ID
 * @returns {Promise<Object>} 操作结果
 */
export const confirmTaskCompleted = (assignedTaskId) => {
  return request({
    url: `/api/tasks/assigned/${assignedTaskId}/complete/`,
    method: 'post'
  })
}

/**
 * 提交任务（学生功能）
 * @param {number} taskId - 任务ID
 * @param {Object} submissionData - 提交数据
 * @param {string} [submissionData.content] - 提交内容
 * @param {string} [submissionData.file_path] - 文件路径
 * @returns {Promise<Object>} 提交结果
 */
export const submitTask = (taskId, submissionData) => {
  return request({
    url: `/api/tasks/${taskId}/submit/`,
    method: 'post', 
    data: submissionData 
  })
}