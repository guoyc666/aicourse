import request from './request'

// 获取资源列表
export const getResources = (params) => {
  return request({
    url: '/api/resources',
    method: 'get',
    params
  })
}

// 上传资源文件
export const uploadResource = (formData) => {
  return request({
    url: '/api/resource/upload',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 删除资源文件
export const deleteResource = (fileId) => {
  return request({
    url: `/api/resources/${fileId}`,
    method: 'delete'
  })
}

// 编辑资源信息
export const updateResource = (fileId, data) => {
  return request({
    url: `/api/resources/${fileId}`,
    method: 'put',
    data
  })
}

// 注意：下载功能直接使用后端提供的download_url，不需要单独的API调用

// 资源下载辅助函数
export const downloadResource = (resource) => {
  if (!resource || !resource.download_url) {
    throw new Error('下载链接不可用')
  }
  
  const link = document.createElement('a')
  link.href = resource.download_url
  link.download = resource.title || resource.original_name || '资源文件'
  document.body.appendChild(link)
  link.click()
  setTimeout(() => {
    document.body.removeChild(link)
  }, 100)
}