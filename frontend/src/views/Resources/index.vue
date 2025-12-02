<template>
  <div class="resources-container">
    <!-- 页面标题和操作 -->
    <div class="page-header">
      <div class="page-title">
        <h2>知识资源管理</h2>
      </div>
      <div class="page-actions">
        <el-button type="primary" @click="showUploadDialog = true">
          <el-icon><Upload /></el-icon>
          上传资源
        </el-button>
      </div>
    </div>
    
    <!-- 搜索和筛选 -->
    <el-card class="search-card">
      <el-form :model="searchForm" inline>
        <el-form-item label="资源名称">
          <el-input
            v-model="searchForm.title"
            placeholder="请输入资源名称"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="资源类型">
          <el-select v-model="searchForm.file_type" placeholder="请选择类型" clearable>
            <el-option label="全部" value="" />
            <el-option label="文本" value="text" />
            <el-option label="PDF" value="pdf" />
            <el-option label="PPT" value="ppt" />
            <el-option label="视频" value="video" />
            <el-option label="音频" value="audio" />
            <el-option label="图片" value="image" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 资源列表 -->
    <el-card class="resources-list-card">
      <template #header>
        <div class="card-header">
          <span>资源列表</span>
          <div class="header-actions">
            <el-button-group>
              <el-button 
                :type="viewMode === 'grid' ? 'primary' : ''" 
                @click="viewMode = 'grid'"
              >
                <el-icon><Grid /></el-icon>
              </el-button>
              <el-button 
                :type="viewMode === 'list' ? 'primary' : ''" 
                @click="viewMode = 'list'"
              >
                <el-icon><List /></el-icon>
              </el-button>
            </el-button-group>
          </div>
        </div>
      </template>
      
      <!-- 网格视图 -->
      <div v-if="viewMode === 'grid'" class="grid-view">
        <div class="resource-grid">
          <div 
            v-for="resource in resources" 
            :key="resource.id"
            class="resource-item"
          >
            <div class="resource-preview">
              <div class="preview-icon" :class="resource.file_type">
                <el-icon>
                  <component :is="getFileIcon(resource.file_type)" />
                </el-icon>
              </div>
            </div>
            <div class="resource-info">
              <h4 class="resource-title" :title="resource.title">
                {{ resource.title }}
              </h4>
              <p class="resource-meta">
                <span class="file-type">{{ getFileTypeName(resource.file_type) }}</span>
                <span class="file-size">{{ formatFileSize(resource.file_size) }}</span>
              </p>
              <p class="resource-desc" v-if="resource.description">
                {{ resource.description }}
              </p>
              <div class="resource-actions">
                <el-button size="small" @click="handlePreview(resource)">预览</el-button>
                <el-button size="small" type="primary" @click="handleDownload(resource)">下载</el-button>
                <el-dropdown @command="(command) => handleAction(command, resource)">
                  <el-button size="small">
                    更多<el-icon><ArrowDown /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="edit">编辑</el-dropdown-item>
                      <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 列表视图 -->
      <div v-else class="list-view">
        <el-table :data="resources" style="width: 100%">
          <el-table-column prop="title" label="资源名称" min-width="200">
            <template #default="{ row }">
              <div class="resource-name-cell">
                <div class="file-icon" :class="row.file_type">
                  <el-icon>
                    <component :is="getFileIcon(row.file_type)" />
                  </el-icon>
                </div>
                <span class="resource-title">{{ row.title }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="file_type" label="类型" width="100">
            <template #default="{ row }">
              <el-tag :type="getFileTypeTag(row.file_type)">
                {{ getFileTypeName(row.file_type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="file_size" label="大小" width="100">
            <template #default="{ row }">
              {{ formatFileSize(row.file_size) }}
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
          <el-table-column prop="created_at" label="上传时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="handlePreview(row)">预览</el-button>
              <el-button size="small" type="primary" @click="handleDownload(row)">下载</el-button>
              <el-dropdown @command="(command) => handleAction(command, row)">
                <el-button size="small">
                  更多<el-icon><ArrowDown /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="edit">编辑</el-dropdown-item>
                    <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 上传对话框 -->
    <el-dialog
      v-model="showUploadDialog"
      title="上传资源"
      width="600px"
      :before-close="handleCloseUploadDialog"
    >
      <el-form
        ref="uploadFormRef"
        :model="uploadForm"
        :rules="uploadRules"
        label-width="100px"
      >
        <el-form-item label="选择文件" prop="file">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :on-change="handleFileChange"
            :before-remove="handleFileRemove"
            :limit="1"
            accept=".txt,.pdf,.ppt,.pptx,.mp4,.mp3,.jpg,.jpeg,.png,.gif"
          >
            <el-button type="primary">
              <el-icon><Upload /></el-icon>
              选择文件
            </el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持格式：文本(.txt)、PDF(.pdf)、PPT(.ppt/.pptx)、视频(.mp4)、音频(.mp3)、图片(.jpg/.jpeg/.png/.gif)
              </div>
            </template>
          </el-upload>
        </el-form-item>
        
        <el-form-item label="资源标题" prop="title">
          <el-input v-model="uploadForm.title" placeholder="请输入资源标题" />
        </el-form-item>
        
        <el-form-item label="资源描述">
          <el-input
            v-model="uploadForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入资源描述（可选）"
          />
        </el-form-item>
        
        <el-form-item label="资源类型" prop="file_type">
          <el-select v-model="uploadForm.file_type" placeholder="请选择资源类型">
            <el-option label="文本" value="text" />
            <el-option label="PDF" value="pdf" />
            <el-option label="PPT" value="ppt" />
            <el-option label="视频" value="video" />
            <el-option label="音频" value="audio" />
            <el-option label="图片" value="image" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showUploadDialog = false">取消</el-button>
          <el-button type="primary" :loading="uploading" @click="handleUpload">
            上传
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 编辑对话框 -->
    <el-dialog
      v-model="showEditDialog"
      title="编辑资源"
      width="500px"
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editRules"
        label-width="100px"
      >
        <el-form-item label="资源标题" prop="title">
          <el-input v-model="editForm.title" />
        </el-form-item>
        
        <el-form-item label="资源描述">
          <el-input
            v-model="editForm.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showEditDialog = false">取消</el-button>
          <el-button type="primary" @click="handleEdit">保存</el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 预览对话框 -->
    <el-dialog
      v-model="showPreviewDialog"
      :title="currentPreviewResource?.title || '文件预览'"
      width="80%"
      :before-close="handleClosePreviewDialog"
    >
      <div v-if="previewLoading" class="preview-loading">
        <el-skeleton animated />
      </div>
      <template v-else-if="currentPreviewResource">
        <!-- 图片预览 -->
        <div v-if="currentPreviewResource.file_type === 'image'" class="preview-content image-preview">
          <img :src="currentPreviewResource.download_url" :alt="currentPreviewResource.title" style="max-width: 100%; max-height: 600px; object-fit: contain;" />
        </div>
        
        <!-- PDF预览 -->
        <div v-else-if="currentPreviewResource.file_type === 'pdf'" class="preview-content pdf-preview">
          <iframe 
            :src="currentPreviewResource.download_url" 
            frameborder="0" 
            style="width: 100%; height: 600px;"
          ></iframe>
        </div>
        
        <!-- 视频预览 -->
        <div v-else-if="currentPreviewResource.file_type === 'video'" class="preview-content video-preview">
          <video 
            :src="currentPreviewResource.download_url" 
            controls 
            autoplay 
            muted 
            style="width: 100%; max-height: 600px;"
          >
            您的浏览器不支持视频播放
          </video>
        </div>
        
        <!-- 音频预览 -->
        <div v-else-if="currentPreviewResource.file_type === 'audio'" class="preview-content audio-preview">
          <audio 
            :src="currentPreviewResource.download_url" 
            controls 
            style="width: 100%;"
          >
            您的浏览器不支持音频播放
          </audio>
        </div>
        
        <!-- 文本预览 -->
        <div v-else-if="currentPreviewResource.file_type === 'text'" class="preview-content text-preview">
          <pre style="white-space: pre-wrap; word-wrap: break-word; max-height: 600px; overflow-y: auto; padding: 16px; background: #f5f7fa; border-radius: 4px;">
            <iframe 
              :src="currentPreviewResource.download_url" 
              frameborder="0" 
              style="width: 100%; height: 600px;"
            ></iframe>
          </pre>
        </div>
        
        <!-- PPT预览 -->
        <div v-else-if="currentPreviewResource.file_type === 'ppt'" class="preview-content ppt-preview">
          <div style="text-align: center; padding: 40px;">
            <el-icon class="preview-ppt-icon"><Present /></el-icon>
            <p style="margin-top: 16px; color: #606266;">PPT文件预览</p>
            <p style="margin-top: 8px; color: #909399; font-size: 14px;">原始文件名：{{ currentPreviewResource.original_name }}</p>
            <el-button type="primary" style="margin-top: 24px;" @click="window.open(currentPreviewResource.download_url, '_blank')">
              <el-icon><Download /></el-icon> 下载查看
            </el-button>
          </div>
        </div>
        
        <!-- 其他类型文件 -->
        <div v-else class="preview-content other-preview">
          <div style="text-align: center; padding: 40px;">
            <el-icon class="preview-other-icon"><Document /></el-icon>
            <p style="margin-top: 16px; color: #606266;">{{ getFileTypeName(currentPreviewResource.file_type) }}文件</p>
            <p style="margin-top: 8px; color: #909399; font-size: 14px;">原始文件名：{{ currentPreviewResource.original_name }}</p>
            <p style="margin-top: 8px; color: #909399; font-size: 14px;">文件大小：{{ formatFileSize(currentPreviewResource.file_size) }}</p>
            <el-button type="primary" style="margin-top: 24px;" @click="window.open(currentPreviewResource.download_url, '_blank')">
              <el-icon><Link /></el-icon> 打开文件
            </el-button>
          </div>
        </div>
      </template>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleClosePreviewDialog">关闭</el-button>
          <el-button type="primary" @click="handleDownload(currentPreviewResource)">
            <el-icon><Download /></el-icon> 下载
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getResources, uploadResource, deleteResource, updateResource } from '@/api/resources'
import { Document, Download, Link, Present, Picture } from '@element-plus/icons-vue'

// 响应式数据
const viewMode = ref('grid')
const showUploadDialog = ref(false)
const showEditDialog = ref(false)
const uploading = ref(false)
const showPreviewDialog = ref(false)  // 预览对话框显示状态
const currentPreviewResource = ref(null)  // 当前预览的资源
const previewLoading = ref(false)  // 预览加载状态

const uploadFormRef = ref()
const editFormRef = ref()
const uploadRef = ref()

// 搜索表单
const searchForm = reactive({
  title: '',
  file_type: ''
})

// 上传表单
const uploadForm = reactive({
  file: null,
  title: '',
  description: '',
  file_type: ''
})

// 编辑表单
const editForm = reactive({
  id: null,
  title: '',
  description: ''
})

// 表单验证规则
const uploadRules = {
  title: [
    { required: true, message: '请输入资源标题', trigger: 'blur' }
  ],
  file_type: [
    { required: true, message: '请选择资源类型', trigger: 'change' }
  ]
}

const editRules = {
  title: [
    { required: true, message: '请输入资源标题', trigger: 'blur' }
  ]
}

// 分页数据
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 资源列表
const resources = ref([])

// 文件类型图标映射
const fileIcons = {
  text: 'Document',
  pdf: 'Document',
  ppt: 'Present',
  video: 'Video',
  audio: 'Music',
  image: 'Picture'  // 注意：在Element Plus中可能是'Picture'或'Image'，根据版本可能需要调整
}

// 获取文件图标
const getFileIcon = (fileType) => {
  return fileIcons[fileType] || 'Document'
}

// 获取文件类型名称
const getFileTypeName = (fileType) => {
  const typeNames = {
    text: '文本',
    pdf: 'PDF',
    ppt: 'PPT',
    video: '视频',
    audio: '音频',
    image: '图片'
  }
  return typeNames[fileType] || '未知'
}

// 获取文件类型标签
const getFileTypeTag = (fileType) => {
  const typeTags = {
    text: '',
    pdf: 'danger',
    ppt: 'warning',
    video: 'success',
    audio: 'info',
    image: 'primary'
  }
  return typeTags[fileType] || ''
}

// 格式化文件大小
const formatFileSize = (size) => {
  if (!size) return '0 B'
  const units = ['B', 'KB', 'MB', 'GB']
  let index = 0
  while (size >= 1024 && index < units.length - 1) {
    size /= 1024
    index++
  }
  return `${size.toFixed(1)} ${units[index]}`
}

// 格式化日期
const formatDate = (date) => {
  return new Date(date).toLocaleString('zh-CN')
}

// 加载资源列表
const loadResources = async () => {
  try {
    // 调用实际的API
    const skip = (pagination.currentPage - 1) * pagination.pageSize
    const response = await getResources({
      skip: skip,
      limit: pagination.pageSize,
      title: searchForm.title,
      file_type: searchForm.file_type
    })
    
    // 检查响应是否包含错误（来自响应拦截器的404处理）
    if (response?.error) {
      console.error('API错误响应:', response)
      resources.value = []
      pagination.total = 0
      return
    }
    
    // 处理新的响应格式，确保获取正确的数据和总数
    const resourceData = response?.data || []
    pagination.total = response?.total || 0
    
    // 转换后端数据格式以匹配前端需求
    resources.value = resourceData.map(resource => ({
      id: resource.file_id,
      title: resource.title,
      description: resource.description,
      file_type: resource.type,
      file_size: resource.size,
      created_at: resource.created_at,
      download_url: resource.download_url,
      original_name: resource.original_name
    }))
    
  } catch (error) {
    console.error('加载资源列表失败:', error)
    ElMessage.error('加载资源列表失败: ' + (error.message || '未知错误'))
    resources.value = []
    pagination.total = 0
  }
}

// 搜索
const handleSearch = () => {
  pagination.currentPage = 1
  loadResources()
}

// 重置搜索
const handleReset = () => {
  Object.assign(searchForm, {
    title: '',
    file_type: ''
  })
  handleSearch()
}

// 分页大小改变
const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.currentPage = 1
  loadResources()
}

// 当前页改变
const handleCurrentChange = (page) => {
  pagination.currentPage = page
  loadResources()
}

// 文件选择
const handleFileChange = (file) => {
  uploadForm.file = file.raw
  
  // 自动设置标题
  if (!uploadForm.title) {
    uploadForm.title = file.name.substring(0, file.name.lastIndexOf('.')) || file.name
  }
  
  // 自动设置文件类型
  const extension = file.name.split('.').pop().toLowerCase()
  const typeMap = {
    'txt': 'text',
    'pdf': 'pdf',
    'ppt': 'ppt',
    'pptx': 'ppt',
    'mp4': 'video',
    'mp3': 'audio',
    'jpg': 'image',
    'jpeg': 'image',
    'png': 'image',
    'gif': 'image'
  }
  uploadForm.file_type = typeMap[extension] || ''
}

// 文件移除
const handleFileRemove = () => {
  uploadForm.file = null
  return true
}

// 上传
const handleUpload = async () => {
  if (!uploadFormRef.value) return
  
  await uploadFormRef.value.validate(async (valid) => {
    if (valid && uploadForm.file) {
      uploading.value = true
      try {
        // 调用实际的API，确保参数名称与后端匹配
        const formData = new FormData()
        formData.append('file', uploadForm.file)
        formData.append('title', uploadForm.title)
        formData.append('description', uploadForm.description || '')
        // 注意：后端参数名是'type'，不是'file_type'
        formData.append('type', uploadForm.file_type)
        
        const response = await uploadResource(formData)
        
        // 处理响应格式，根据后端返回格式获取消息
        const successMessage = response?.message || response?.data?.message || '上传成功'
        ElMessage.success(successMessage)
        showUploadDialog.value = false
        resetUploadForm()
        loadResources()
      } catch (error) {
        console.error('资源上传失败:', error)
        ElMessage.error('资源上传失败: ' + (error.response?.data?.message || error.message))
      } finally {
        uploading.value = false
      }
    }
  })
}

// 关闭上传对话框
const handleCloseUploadDialog = () => {
  showUploadDialog.value = false
  resetUploadForm()
}

// 重置上传表单
const resetUploadForm = () => {
  Object.assign(uploadForm, {
    file: null,
    title: '',
    description: '',
    file_type: ''
  })
  uploadRef.value?.clearFiles()
  uploadFormRef.value?.resetFields()
}

// 预览
const handlePreview = async (resource) => {
  if (!resource || !resource.download_url) {
    ElMessage.warning('预览链接不可用')
    return
  }
  
  // 显示预览对话框
  currentPreviewResource.value = resource
  showPreviewDialog.value = true
}

// 下载
const handleDownload = (resource) => {
  try {
    if (resource.download_url) {
      // 直接使用后端提供的download_url
      const link = document.createElement('a')
      link.href = resource.download_url
      link.download = resource.title
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      ElMessage.success('下载开始')
    } else {
      ElMessage.warning('下载链接不可用')
    }
  } catch (error) {
    console.error('下载失败:', error)
    ElMessage.error('下载失败: ' + (error.message || '未知错误'))
  }
}

// 操作处理
const handleAction = async (command, resource) => {
  switch (command) {
    case 'edit':
      Object.assign(editForm, {
        id: resource.id,
        title: resource.title,
        description: resource.description || ''
      })
      showEditDialog.value = true
      break
    case 'delete':
      // 首先处理确认对话框
      try {
        await ElMessageBox.confirm('确定要删除这个资源吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        // 用户确认后，再调用API
        try {
          await deleteResource(resource.id)
          ElMessage.success('删除成功')
          loadResources()
        } catch (apiError) {
          // 专门处理API错误
          if (apiError.response) {
            ElMessage.error(apiError.response.data.detail || '删除失败')
          } else {
            ElMessage.error('删除失败: ' + (apiError.message || '未知错误'))
          }
        }
      } catch (error) {
        // 只处理用户取消的情况
        if (error.message !== 'cancel') {
          console.error('对话框错误:', error)
        }
        // 用户取消不需要显示消息
      }
      break
  }
}

// 编辑保存
const handleEdit = async () => {
  if (!editFormRef.value) return
  
  await editFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 调用更新资源API
        const response = await updateResource(editForm.id, {
          title: editForm.title,
          description: editForm.description
        })
        
        ElMessage.success('编辑成功')
        showEditDialog.value = false
        loadResources()  // 重新加载资源列表
      } catch (error) {
        console.error('编辑资源失败:', error)
        ElMessage.error('编辑失败: ' + (error.response?.data?.detail || error.message || '未知错误'))
      }
    }
  })
}

// 关闭预览对话框
const handleClosePreviewDialog = () => {
  showPreviewDialog.value = false
  currentPreviewResource.value = null
  previewLoading.value = false
}

onMounted(() => {
  loadResources()
})
</script>

<style lang="scss" scoped>
.resources-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  
  .page-title {
    h2 {
      margin: 0 0 8px 0;
      color: #333;
    }
    
    p {
      margin: 0;
      color: #666;
      font-size: 14px;
    }
  }
}

.search-card {
  margin-bottom: 20px;
}

.resources-list-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}

.grid-view {
  .resource-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    
    .resource-item {
      border: 1px solid #e4e7ed;
      border-radius: 8px;
      padding: 16px;
      transition: all 0.3s;
      
      &:hover {
        border-color: #409eff;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
      }
      
      .resource-preview {
        margin-bottom: 12px;
        
        .preview-icon {
          width: 60px;
          height: 60px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 24px;
          color: white;
          
          &.text, &.pdf {
            background: #f56c6c;
          }
          
          &.ppt {
            background: #e6a23c;
          }
          
          &.video {
            background: #67c23a;
          }
          
          &.audio {
            background: #909399;
          }
          
          &.image {
            background: #409eff;
          }
        }
      }
      
      .resource-info {
        .resource-title {
          margin: 0 0 8px 0;
          font-size: 16px;
          color: #333;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        
        .resource-meta {
          margin: 0 0 8px 0;
          font-size: 12px;
          color: #666;
          
          .file-type {
            margin-right: 8px;
          }
        }
        
        .resource-desc {
          margin: 0 0 12px 0;
          font-size: 14px;
          color: #666;
          line-height: 1.4;
          overflow: hidden;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
        }
        
        .resource-actions {
          display: flex;
          gap: 8px;
        }
      }
    }
  }
}

.list-view {
  .resource-name-cell {
    display: flex;
    align-items: center;
    
    .file-icon {
      width: 32px;
      height: 32px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 12px;
      font-size: 16px;
      color: white;
      
      &.text, &.pdf {
        background: #f56c6c;
      }
      
      &.ppt {
        background: #e6a23c;
      }
      
      &.video {
        background: #67c23a;
      }
      
      &.audio {
        background: #909399;
      }
      
      &.image {
        background: #409eff;
      }
    }
    
    .resource-title {
      font-weight: 500;
    }
  }
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 预览对话框样式 */
.preview-loading {
  min-height: 400px;
}

.preview-content {
  min-height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px;
}

.image-preview,
.pdf-preview,
.video-preview,
.audio-preview,
.text-preview {
  width: 100%;
}

.preview-ppt-icon,
.preview-other-icon {
  font-size: 64px;
  color: #409eff;
}
</style>
