// interceptors.js - 使用 fetch-intercept 模拟 request.js 的拦截器行为

import fetchIntercept from 'fetch-intercept';
import { ElMessage } from 'element-plus';
import router from '@/router';
import Cookies from 'js-cookie';

// 用于在 response 拦截器中判断是否为登录请求
// 因为 fetch-intercept 的 response 钩子无法直接访问原始的 request config
// 我们通过 URL 来判断
const LOGIN_URL = '/auth/login';

// --- 注册 fetch 拦截器 ---
const unregister = fetchIntercept.register({
  // --- 请求拦截 (request) ---
  request: function (url, config) {
    console.log('请求URL:', url);
    console.log('请求方法:', config?.method || 'GET');

    // 1. 获取 Token
    const token = Cookies.get('token');
    console.log('Token存在:', !!token);
    if (token) {
      console.log('Token值:', token.substring(0, 10) + '...');
    } else {
      console.warn('未找到Token，无法添加Authorization头');
    }

    // 2. 创建新的配置对象
    const newConfig = { ...config };

    // 3. 添加 Authorization 头
    if (token) {
      newConfig.headers = {
        ...newConfig.headers,
        Authorization: `Bearer ${token}`,
      };
      console.log('已添加Authorization头:', `Bearer ${token.substring(0, 10)}...`);
    }

    return [url, newConfig]; // 返回修改后的参数
  },

  // --- 请求错误拦截 (requestError) ---
  requestError: function (error) {
    console.error('请求拦截器错误:', error);
    // 这里可以处理请求配置阶段的错误
    return Promise.reject(error);
  },

  // --- 响应拦截 (response) ---
  // 注意：fetch-intercept 的 response 钩子在 fetch resolve 时调用
  // 它不能阻止 fetch resolve，但可以修改 response 或抛出错误
  response: function (response) {
    // 注意：这里不能直接访问发起请求时的 config
    // 所以我们需要通过 response.url 来判断是否是登录请求
    const isLoginRequest = response.url.includes(LOGIN_URL);

    console.log('响应状态:', response.status);
    console.log('响应URL:', response.url);

    // 4. 根据状态码处理响应 (核心逻辑)
    switch (response.status) {
      case 401:
        if (isLoginRequest) {
          // 登录请求的 401：只显示错误信息，不 reject
          // 我们需要读取响应体来获取 detail
          response
            .clone() // 克隆响应，因为响应体只能读取一次
            .json()
            .then(data => {
              ElMessage.error(data?.detail || '用户名或密码错误');
            })
            .catch(() => {
              ElMessage.error('用户名或密码错误');
            });
          // 返回原始的 response，让调用者可以继续处理 (但通常是错误的)
          return response;
        } else {
          // 其他请求的 401：显示过期信息，登出，跳转
          ElMessage.error('登录已过期，请重新登录');
          Cookies.remove('token');
          router.push('/login');
          // 返回原始的 response
          return response;
        }

      case 403:
        // 403 错误：只 reject 不显示消息，让调用方处理
        // 这里我们返回一个被 reject 的 Promise
        return Promise.reject(new Error('Forbidden', { cause: response }));

      case 404:
        ElMessage.error('请求的资源不存在');
        // 返回一个包含错误信息的对象的 Promise，而不是原始 response
        // 这样调用者 await 会得到这个对象，而不是 response
        return Promise.resolve({
          error: 'not_found',
          message: '请求的资源不存在',
          ok: false,
          status: 404,
        });

      case 500:
        ElMessage.error('服务器内部错误');
        // 返回原始的 response
        return response;

      default:
        if (!response.ok) {
          // 处理其他非 2xx 的错误
          response
            .clone()
            .json()
            .then(data => {
              ElMessage.error(data?.detail || '请求失败');
            })
            .catch(() => {
              ElMessage.error(`请求失败: ${response.status} ${response.statusText}`);
            });
        }
        // 对于 2xx 或已处理的非 2xx，返回原始 response
        return response;
    }
  },

  // --- 响应错误拦截 (responseError) ---
  // 注意：fetch-intercept 的 responseError 钩子在 fetch reject 时调用
  // 通常是网络错误 (如 Failed to fetch)
  responseError: function (error) {
    console.error('响应拦截器错误:', error);
    // 处理网络连接失败
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      ElMessage.error('网络连接失败');
    } else {
      ElMessage.error('请求失败');
    }
    return Promise.reject(error);
  },
});

// 可以选择导出 unregister 函数，以便在需要时注销拦截器
export { unregister };