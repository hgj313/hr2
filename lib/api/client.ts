/**
 * API客户端配置
 * 基于后端API集成手册规范实现
 */

// API响应基础类型
export interface ApiResponse<T = any> {
  success: boolean;
  code: number;
  message: string;
  data?: T;
  error?: {
    type: string;
    details?: any;
  };
}

// 分页响应类型
export interface PaginatedResponse<T> {
  items: T[];
  pagination: {
    page: number;
    size: number;
    total: number;
    pages: number;
  };
}

// API错误类
export class ApiError extends Error {
  constructor(
    public code: number,
    public type: string,
    message: string,
    public details?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// 环境配置
const getApiConfig = () => {
  const env = process.env.NODE_ENV || 'development';
  
  const configs = {
    development: {
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      timeout: 10000,
    },
    production: {
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'https://api.example.com',
      timeout: 15000,
    },
  };
  
  return configs[env as keyof typeof configs] || configs.development;
};

// Token管理
class TokenManager {
  private static readonly ACCESS_TOKEN_KEY = 'access_token';
  private static readonly REFRESH_TOKEN_KEY = 'refresh_token';
  
  static getAccessToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem(this.ACCESS_TOKEN_KEY);
  }
  
  static setAccessToken(token: string): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem(this.ACCESS_TOKEN_KEY, token);
  }
  
  static getRefreshToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }
  
  static setRefreshToken(token: string): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem(this.REFRESH_TOKEN_KEY, token);
  }
  
  static clearTokens(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem(this.ACCESS_TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
  }
}

// HTTP客户端类
class HttpClient {
  private config = getApiConfig();
  private isRefreshing = false;
  private failedQueue: Array<{
    resolve: (value: any) => void;
    reject: (error: any) => void;
  }> = [];
  
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.config.baseURL}${endpoint}`;
    const token = TokenManager.getAccessToken();
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };
    
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
    
    try {
      const response = await fetch(url, {
        ...options,
        headers,
        signal: AbortSignal.timeout(this.config.timeout),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        // 处理401未授权错误
        if (response.status === 401 && token) {
          return this.handleTokenRefresh(endpoint, options);
        }
        
        throw new ApiError(
          data.code || response.status,
          data.error?.type || 'HTTP_ERROR',
          data.message || response.statusText,
          data.error?.details
        );
      }
      
      return data;
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      
      // 网络错误或其他错误
      throw new ApiError(
        0,
        'NETWORK_ERROR',
        error instanceof Error ? error.message : '网络请求失败'
      );
    }
  }
  
  private async handleTokenRefresh<T>(
    endpoint: string,
    options: RequestInit
  ): Promise<ApiResponse<T>> {
    if (this.isRefreshing) {
      // 如果正在刷新token，将请求加入队列
      return new Promise((resolve, reject) => {
        this.failedQueue.push({ resolve, reject });
      });
    }
    
    this.isRefreshing = true;
    
    try {
      const refreshToken = TokenManager.getRefreshToken();
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }
      
      const refreshResponse = await fetch(`${this.config.baseURL}/api/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });
      
      if (!refreshResponse.ok) {
        throw new Error('Token refresh failed');
      }
      
      const refreshData = await refreshResponse.json();
      TokenManager.setAccessToken(refreshData.data.access_token);
      
      // 处理队列中的请求
      this.failedQueue.forEach(({ resolve }) => {
        resolve(this.request(endpoint, options));
      });
      this.failedQueue = [];
      
      // 重新执行原始请求
      return this.request(endpoint, options);
    } catch (error) {
      // 刷新失败，清除token并跳转登录
      TokenManager.clearTokens();
      this.failedQueue.forEach(({ reject }) => {
        reject(error);
      });
      this.failedQueue = [];
      
      // 跳转到登录页面
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
      
      throw new ApiError(2001, 'TOKEN_EXPIRED', '登录已过期，请重新登录');
    } finally {
      this.isRefreshing = false;
    }
  }
  
  async get<T>(endpoint: string, params?: Record<string, any>): Promise<ApiResponse<T>> {
    const url = params ? `${endpoint}?${new URLSearchParams(params)}` : endpoint;
    return this.request<T>(url, { method: 'GET' });
  }
  
  async post<T>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }
  
  async put<T>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }
  
  async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

// 导出单例实例
export const apiClient = new HttpClient();
export { TokenManager };