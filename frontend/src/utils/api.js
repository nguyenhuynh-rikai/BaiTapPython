const API_BASE_URL = typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://localhost:8000/api'
  : 'https://baitappython-web.onrender.com/api';

/**
 * Helper chung để gửi HTTP request kèm Token tự động
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  // Tự động đọc token từ localStorage
  const token = localStorage.getItem('token');
  
  // Thiết lập Headers mặc định
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    ...options.headers,
  };
  
  // Nếu có Token, tự động đính kèm dạng 'Token <key>' chuẩn Django REST TokenAuthentication
  if (token) {
    headers['Authorization'] = `Token ${token}`;
  }
  
  const response = await fetch(url, {
    ...options,
    headers,
  });
  
  // Nếu gặp lỗi Unauthorized (401), tự động xóa token hỏng và điều hướng đăng nhập
  if (response.status === 401) {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    
    // Quét tìm lỗi cụ thể từ các trường (như username, password)
    let errorMsg = errorData.detail || errorData.non_field_errors?.[0];
    
    if (!errorMsg) {
      // Lấy lỗi đầu tiên từ bất kỳ trường nào có lỗi
      const errors = Object.entries(errorData);
      if (errors.length > 0) {
        const [field, messages] = errors[0];
        if (Array.isArray(messages) && messages.length > 0) {
          errorMsg = `${messages[0]}`;
        } else {
          errorMsg = `${messages}`;
        }
      }
    }
    
    errorMsg = errorMsg || 'Có lỗi xảy ra!';
    throw new Error(errorMsg);
  }
  
  // Trả về JSON nếu có body phản hồi
  return response.status === 204 ? null : response.json();
}

export const api = {
  get: (endpoint, headers = {}) => apiRequest(endpoint, { method: 'GET', headers }),
  post: (endpoint, body, headers = {}) => apiRequest(endpoint, { 
    method: 'POST', 
    body: JSON.stringify(body), 
    headers 
  }),
  put: (endpoint, body, headers = {}) => apiRequest(endpoint, { 
    method: 'PUT', 
    body: JSON.stringify(body), 
    headers 
  }),
  patch: (endpoint, body, headers = {}) => apiRequest(endpoint, { 
    method: 'PATCH', 
    body: JSON.stringify(body), 
    headers 
  }),
  delete: (endpoint, headers = {}) => apiRequest(endpoint, { method: 'DELETE', headers }),
};
