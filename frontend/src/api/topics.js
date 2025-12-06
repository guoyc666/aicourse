import request from './request'

// 获取主题列表（支持搜索） - 确保路径以斜杠结尾，与后端保持一致
export const getTopics = (params = {}) => {
  return request.get('/topics/', { params })
}

// 获取单个主题详情 - 确保路径以斜杠结尾，与后端保持一致
export const getTopicDetail = (topicId) => {
  return request.get(`/topics/${topicId}/`)
}

// 创建新主题 - 确保路径以斜杠结尾，与后端保持一致
export const createTopic = (topicData) => {
  return request.post('/topics/', topicData)
}

// 更新主题 - 确保路径以斜杠结尾，与后端保持一致
export const updateTopic = (topicId, topicData) => {
  return request.put(`/topics/${topicId}/`, topicData)
}

// 删除主题 - 确保路径以斜杠结尾，与后端保持一致
export const deleteTopic = (topicId) => {
  return request.delete(`/topics/${topicId}/`)
}

// 获取主题的所有回复 - 确保路径以斜杠结尾，与后端保持一致
export const getTopicReplies = (topicId, params = {}) => {
  return request.get(`/topics/${topicId}/replies/`, { params })
}

// 创建回复 - 确保路径以斜杠结尾，与后端保持一致
export const createReply = (topicId, replyData) => {
  return request.post(`/topics/${topicId}/replies/`, replyData)
}

// 更新回复 - 确保路径以斜杠结尾，与后端保持一致
export const updateReply = (replyId, replyData) => {
  return request.put(`/topics/replies/${replyId}/`, replyData)
}

// 删除回复 - 确保路径以斜杠结尾，与后端保持一致
export const deleteReply = (replyId) => {
  return request.delete(`/topics/replies/${replyId}/`)
}