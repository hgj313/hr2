/**
 * API服务模块
 * 封装所有后端API调用
 */

import { apiClient, ApiResponse, PaginatedResponse } from './client';
import {
  User,
  CreateUserRequest,
  UpdateUserRequest,
  UserListParams,
  LoginRequest,
  LoginResponse,
  RefreshTokenRequest,
  Project,
  CreateProjectRequest,
  UpdateProjectRequest,
  ProjectListParams,
  Task,
  SchedulingTask,
  SchedulingResult,
  AIRecommendation,
  DashboardStats,
  AnalyticsParams,
  SystemConfig,
  Notification,
  ExportRequest,
  ExportResult,
} from './types';

// 认证服务
export const authService = {
  /**
   * 用户登录
   */
  async login(credentials: LoginRequest): Promise<ApiResponse<LoginResponse>> {
    return apiClient.post<LoginResponse>('/api/auth/login', credentials);
  },

  /**
   * 刷新Token
   */
  async refreshToken(data: RefreshTokenRequest): Promise<ApiResponse<LoginResponse>> {
    return apiClient.post<LoginResponse>('/api/auth/refresh', data);
  },

  /**
   * 用户登出
   */
  async logout(): Promise<ApiResponse<void>> {
    return apiClient.post<void>('/api/auth/logout');
  },

  /**
   * 获取当前用户信息
   */
  async getProfile(): Promise<ApiResponse<User>> {
    return apiClient.get<User>('/api/auth/profile');
  },
};

// 用户管理服务
export const userService = {
  /**
   * 获取用户列表
   */
  async getUsers(params?: UserListParams): Promise<ApiResponse<PaginatedResponse<User>>> {
    return apiClient.get<PaginatedResponse<User>>('/api/users', params);
  },

  /**
   * 获取用户详情
   */
  async getUser(id: number): Promise<ApiResponse<User>> {
    return apiClient.get<User>(`/api/users/${id}`);
  },

  /**
   * 创建用户
   */
  async createUser(data: CreateUserRequest): Promise<ApiResponse<User>> {
    return apiClient.post<User>('/api/users', data);
  },

  /**
   * 更新用户
   */
  async updateUser(id: number, data: UpdateUserRequest): Promise<ApiResponse<User>> {
    return apiClient.put<User>(`/api/users/${id}`, data);
  },

  /**
   * 删除用户
   */
  async deleteUser(id: number): Promise<ApiResponse<void>> {
    return apiClient.delete<void>(`/api/users/${id}`);
  },

  /**
   * 更新用户状态
   */
  async updateUserStatus(id: number, status: 'active' | 'inactive'): Promise<ApiResponse<User>> {
    return apiClient.put<User>(`/api/users/${id}/status`, { status });
  },
};

// 项目管理服务
export const projectService = {
  /**
   * 获取项目列表
   */
  async getProjects(params?: ProjectListParams): Promise<ApiResponse<PaginatedResponse<Project>>> {
    return apiClient.get<PaginatedResponse<Project>>('/api/projects', params);
  },

  /**
   * 获取项目详情
   */
  async getProject(id: number): Promise<ApiResponse<Project>> {
    return apiClient.get<Project>(`/api/projects/${id}`);
  },

  /**
   * 创建项目
   */
  async createProject(data: CreateProjectRequest): Promise<ApiResponse<Project>> {
    return apiClient.post<Project>('/api/projects', data);
  },

  /**
   * 更新项目
   */
  async updateProject(id: number, data: UpdateProjectRequest): Promise<ApiResponse<Project>> {
    return apiClient.put<Project>(`/api/projects/${id}`, data);
  },

  /**
   * 删除项目
   */
  async deleteProject(id: number): Promise<ApiResponse<void>> {
    return apiClient.delete<void>(`/api/projects/${id}`);
  },

  /**
   * 获取项目任务
   */
  async getProjectTasks(id: number): Promise<ApiResponse<Task[]>> {
    return apiClient.get<Task[]>(`/api/projects/${id}/tasks`);
  },
};

// 智能调度服务
export const schedulingService = {
  /**
   * 创建调度任务
   */
  async createSchedulingTask(data: SchedulingTask): Promise<ApiResponse<{ task_id: string }>> {
    return apiClient.post<{ task_id: string }>('/api/scheduling/tasks', data);
  },

  /**
   * 获取调度结果
   */
  async getSchedulingResult(taskId: string): Promise<ApiResponse<SchedulingResult>> {
    return apiClient.get<SchedulingResult>(`/api/scheduling/results/${taskId}`);
  },

  /**
   * 解决调度冲突
   */
  async resolveConflicts(data: {
    result_id: string;
    resolution_strategy: 'auto' | 'manual';
    manual_assignments?: any[];
  }): Promise<ApiResponse<SchedulingResult>> {
    return apiClient.post<SchedulingResult>('/api/scheduling/conflicts/resolve', data);
  },

  /**
   * 获取AI推荐
   */
  async getRecommendations(params?: {
    project_id?: number;
    user_id?: number;
    type?: string;
  }): Promise<ApiResponse<AIRecommendation[]>> {
    return apiClient.get<AIRecommendation[]>('/api/scheduling/recommendations', params);
  },
};

// 数据分析服务
export const analyticsService = {
  /**
   * 获取仪表盘统计数据
   */
  async getDashboardStats(params?: AnalyticsParams): Promise<ApiResponse<DashboardStats>> {
    return apiClient.get<DashboardStats>('/api/analytics/dashboard', params);
  },

  /**
   * 生成分析报告
   */
  async generateReport(params: AnalyticsParams & {
    report_type: 'performance' | 'utilization' | 'efficiency';
  }): Promise<ApiResponse<any>> {
    return apiClient.post<any>('/api/analytics/reports', params);
  },

  /**
   * 导出数据
   */
  async exportData(data: ExportRequest): Promise<ApiResponse<ExportResult>> {
    return apiClient.post<ExportResult>('/api/analytics/export', data);
  },
};

// 系统配置服务
export const configService = {
  /**
   * 获取系统配置
   */
  async getSystemConfig(): Promise<ApiResponse<SystemConfig>> {
    return apiClient.get<SystemConfig>('/api/config/system');
  },

  /**
   * 更新系统配置
   */
  async updateSystemConfig(data: Partial<SystemConfig>): Promise<ApiResponse<SystemConfig>> {
    return apiClient.put<SystemConfig>('/api/config/system', data);
  },

  /**
   * 获取通知设置
   */
  async getNotificationConfig(): Promise<ApiResponse<SystemConfig['notifications']>> {
    return apiClient.get<SystemConfig['notifications']>('/api/config/notifications');
  },

  /**
   * 更新通知设置
   */
  async updateNotificationConfig(
    data: Partial<SystemConfig['notifications']>
  ): Promise<ApiResponse<SystemConfig['notifications']>> {
    return apiClient.put<SystemConfig['notifications']>('/api/config/notifications', data);
  },
};

// 通知服务
export const notificationService = {
  /**
   * 获取通知列表
   */
  async getNotifications(params?: {
    page?: number;
    size?: number;
    read?: boolean;
    type?: string;
  }): Promise<ApiResponse<PaginatedResponse<Notification>>> {
    return apiClient.get<PaginatedResponse<Notification>>('/api/notifications', params);
  },

  /**
   * 标记通知为已读
   */
  async markAsRead(id: number): Promise<ApiResponse<void>> {
    return apiClient.put<void>(`/api/notifications/${id}/read`);
  },

  /**
   * 标记所有通知为已读
   */
  async markAllAsRead(): Promise<ApiResponse<void>> {
    return apiClient.put<void>('/api/notifications/read-all');
  },

  /**
   * 删除通知
   */
  async deleteNotification(id: number): Promise<ApiResponse<void>> {
    return apiClient.delete<void>(`/api/notifications/${id}`);
  },
};

// 导出所有服务
export const api = {
  auth: authService,
  users: userService,
  projects: projectService,
  scheduling: schedulingService,
  analytics: analyticsService,
  config: configService,
  notifications: notificationService,
};

export default api;