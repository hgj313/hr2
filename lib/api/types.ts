/**
 * API类型定义
 * 基于后端API集成手册定义的数据结构
 */

// 用户相关类型
export interface User {
  id: number;
  username: string;
  name: string;
  email: string;
  phone?: string;
  role: 'admin' | 'manager' | 'employee';
  department?: string;
  position?: string;
  skills?: string[];
  status: 'active' | 'inactive';
  created_at: string;
  updated_at: string;
  last_login?: string;
}

export interface CreateUserRequest {
  username: string;
  name: string;
  email: string;
  phone?: string;
  password: string;
  role: 'admin' | 'manager' | 'employee';
  department?: string;
  position?: string;
  skills?: string[];
}

export interface UpdateUserRequest {
  name?: string;
  email?: string;
  phone?: string;
  role?: 'admin' | 'manager' | 'employee';
  department?: string;
  position?: string;
  skills?: string[];
  status?: 'active' | 'inactive';
}

export interface UserListParams {
  page?: number;
  size?: number;
  search?: string;
  role?: string;
  department?: string;
  status?: string;
}

// 认证相关类型
export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

// 项目相关类型
export interface Project {
  id: number;
  name: string;
  description?: string;
  status: 'planning' | 'active' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  start_date: string;
  end_date: string;
  budget?: number;
  manager_id: number;
  manager?: User;
  team_members?: User[];
  location?: string;
  area?: number;
  season?: string;
  weather_requirements?: string;
  plant_types?: string[];
  construction_phase?: string;
  tags?: string[];
  created_at: string;
  updated_at: string;
}

export interface CreateProjectRequest {
  name: string;
  description?: string;
  status: 'planning' | 'active' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  start_date: string;
  end_date: string;
  budget?: number;
  manager_id: number;
  team_member_ids?: number[];
  location?: string;
  area?: number;
  season?: string;
  weather_requirements?: string;
  plant_types?: string[];
  construction_phase?: string;
  tags?: string[];
}

export interface UpdateProjectRequest {
  name?: string;
  description?: string;
  status?: 'planning' | 'active' | 'completed' | 'cancelled';
  priority?: 'low' | 'medium' | 'high' | 'urgent';
  start_date?: string;
  end_date?: string;
  budget?: number;
  manager_id?: number;
  team_member_ids?: number[];
  location?: string;
  area?: number;
  season?: string;
  weather_requirements?: string;
  plant_types?: string[];
  construction_phase?: string;
  tags?: string[];
}

export interface ProjectListParams {
  page?: number;
  size?: number;
  search?: string;
  status?: string;
  priority?: string;
  manager_id?: number;
  start_date?: string;
  end_date?: string;
}

// 任务相关类型
export interface Task {
  id: number;
  project_id: number;
  name: string;
  description?: string;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  start_date: string;
  end_date: string;
  assigned_user_id?: number;
  assigned_user?: User;
  estimated_hours?: number;
  actual_hours?: number;
  dependencies?: number[];
  created_at: string;
  updated_at: string;
}

// 调度相关类型
export interface SchedulingTask {
  project_id: number;
  requirements: {
    skills: string[];
    team_size: number;
    duration: number;
    priority: 'low' | 'medium' | 'high' | 'urgent';
    start_date: string;
    end_date: string;
  };
  constraints?: {
    required_users?: number[];
    excluded_users?: number[];
    max_workload?: number;
    weather_dependent?: boolean;
  };
}

export interface SchedulingResult {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  assignments?: {
    user_id: number;
    user: User;
    tasks: {
      task_id: number;
      start_time: string;
      end_time: string;
      workload: number;
    }[];
    total_workload: number;
  }[];
  conflicts?: {
    type: 'time_conflict' | 'skill_mismatch' | 'overload';
    description: string;
    affected_users: number[];
    suggestions: string[];
  }[];
  optimization_score?: number;
  created_at: string;
  completed_at?: string;
}

export interface AIRecommendation {
  type: 'optimization' | 'warning' | 'suggestion';
  title: string;
  description: string;
  impact: 'low' | 'medium' | 'high';
  actions?: {
    label: string;
    action: string;
    params?: any;
  }[];
}

// 数据分析相关类型
export interface DashboardStats {
  users: {
    total: number;
    active: number;
    by_role: Record<string, number>;
  };
  projects: {
    total: number;
    active: number;
    completed: number;
    by_status: Record<string, number>;
  };
  scheduling: {
    total_tasks: number;
    completed_tasks: number;
    efficiency_rate: number;
    average_workload: number;
  };
  performance: {
    on_time_completion: number;
    resource_utilization: number;
    cost_efficiency: number;
  };
}

export interface AnalyticsParams {
  start_date?: string;
  end_date?: string;
  project_ids?: number[];
  user_ids?: number[];
  metrics?: string[];
}

// 系统配置相关类型
export interface SystemConfig {
  scheduling: {
    max_workload_per_user: number;
    default_task_duration: number;
    conflict_resolution_strategy: 'auto' | 'manual';
    optimization_algorithm: 'greedy' | 'genetic' | 'simulated_annealing';
  };
  notifications: {
    email_enabled: boolean;
    sms_enabled: boolean;
    push_enabled: boolean;
    reminder_hours: number[];
  };
  security: {
    session_timeout: number;
    password_policy: {
      min_length: number;
      require_uppercase: boolean;
      require_lowercase: boolean;
      require_numbers: boolean;
      require_symbols: boolean;
    };
  };
}

// 通知相关类型
export interface Notification {
  id: number;
  user_id: number;
  type: 'info' | 'warning' | 'error' | 'success';
  title: string;
  message: string;
  read: boolean;
  created_at: string;
  expires_at?: string;
}

// 导出相关类型
export interface ExportRequest {
  type: 'users' | 'projects' | 'schedules' | 'analytics';
  format: 'csv' | 'excel' | 'pdf';
  filters?: Record<string, any>;
  date_range?: {
    start_date: string;
    end_date: string;
  };
}

export interface ExportResult {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  download_url?: string;
  file_size?: number;
  created_at: string;
  expires_at: string;
}