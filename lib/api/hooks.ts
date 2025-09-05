/**
 * React Hooks for API calls
 * 提供统一的数据获取和状态管理
 */

import { useState, useEffect, useCallback } from 'react';
import { api } from './services';
import { ApiError } from './client';
import type {
  User,
  Project,
  UserListParams,
  ProjectListParams,
  PaginatedResponse,
  DashboardStats,
  AnalyticsParams,
  Notification,
} from './types';

// 通用API状态类型
interface ApiState<T> {
  data: T | null;
  loading: boolean;
  error: ApiError | null;
}

// 分页状态类型
interface PaginatedState<T> extends ApiState<PaginatedResponse<T>> {
  loadMore: () => void;
  hasMore: boolean;
}

/**
 * 通用API调用Hook
 */
export function useApi<T>(
  apiCall: () => Promise<{ data: T }>,
  dependencies: any[] = []
): ApiState<T> & { refetch: () => void } {
  const [state, setState] = useState<ApiState<T>>({
    data: null,
    loading: true,
    error: null,
  });

  const fetchData = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const response = await apiCall();
      setState({ data: response.data, loading: false, error: null });
    } catch (error) {
      setState({
        data: null,
        loading: false,
        error: error instanceof ApiError ? error : new ApiError('Unknown error', 500),
      });
    }
  }, dependencies);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return {
    ...state,
    refetch: fetchData,
  };
}

/**
 * 用户列表Hook
 */
export function useUsers(params?: UserListParams) {
  return useApi(
    () => api.users.getUsers(params),
    [JSON.stringify(params)]
  );
}

/**
 * 单个用户Hook
 */
export function useUser(id: number) {
  return useApi(
    () => api.users.getUser(id),
    [id]
  );
}

/**
 * 项目列表Hook
 */
export function useProjects(params?: ProjectListParams) {
  return useApi(
    () => api.projects.getProjects(params),
    [JSON.stringify(params)]
  );
}

/**
 * 单个项目Hook
 */
export function useProject(id: number) {
  return useApi(
    () => api.projects.getProject(id),
    [id]
  );
}

/**
 * 项目任务Hook
 */
export function useProjectTasks(projectId: number) {
  return useApi(
    () => api.projects.getProjectTasks(projectId),
    [projectId]
  );
}

/**
 * 仪表盘统计数据Hook
 */
export function useDashboardStats(params?: AnalyticsParams) {
  return useApi(
    () => api.analytics.getDashboardStats(params),
    [JSON.stringify(params)]
  );
}

/**
 * 通知列表Hook
 */
export function useNotifications(params?: {
  page?: number;
  size?: number;
  read?: boolean;
  type?: string;
}) {
  return useApi(
    () => api.notifications.getNotifications(params),
    [JSON.stringify(params)]
  );
}

/**
 * 系统配置Hook
 */
export function useSystemConfig() {
  return useApi(() => api.config.getSystemConfig());
}

/**
 * 当前用户信息Hook
 */
export function useProfile() {
  return useApi(() => api.auth.getProfile());
}

/**
 * AI推荐Hook
 */
export function useRecommendations(params?: {
  project_id?: number;
  user_id?: number;
  type?: string;
}) {
  return useApi(
    () => api.scheduling.getRecommendations(params),
    [JSON.stringify(params)]
  );
}

/**
 * 调度结果Hook
 */
export function useSchedulingResult(taskId: string) {
  return useApi(
    () => api.scheduling.getSchedulingResult(taskId),
    [taskId]
  );
}

/**
 * 分页数据Hook
 */
export function usePaginatedData<T>(
  apiCall: (page: number, size: number) => Promise<{ data: PaginatedResponse<T> }>,
  pageSize: number = 20
): PaginatedState<T> {
  const [state, setState] = useState<PaginatedState<T>>({
    data: null,
    loading: true,
    error: null,
    loadMore: () => {},
    hasMore: false,
  });

  const [currentPage, setCurrentPage] = useState(1);

  const fetchData = useCallback(async (page: number, append: boolean = false) => {
    if (!append) {
      setState(prev => ({ ...prev, loading: true, error: null }));
    }

    try {
      const response = await apiCall(page, pageSize);
      const newData = response.data;

      setState(prev => ({
        ...prev,
        data: append && prev.data
          ? {
              ...newData,
              items: [...prev.data.items, ...newData.items],
            }
          : newData,
        loading: false,
        error: null,
        hasMore: newData.current_page < newData.total_pages,
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof ApiError ? error : new ApiError('Unknown error', 500),
      }));
    }
  }, [apiCall, pageSize]);

  const loadMore = useCallback(() => {
    if (state.hasMore && !state.loading) {
      const nextPage = currentPage + 1;
      setCurrentPage(nextPage);
      fetchData(nextPage, true);
    }
  }, [state.hasMore, state.loading, currentPage, fetchData]);

  useEffect(() => {
    fetchData(1);
    setCurrentPage(1);
  }, [fetchData]);

  return {
    ...state,
    loadMore,
  };
}

/**
 * 表单提交Hook
 */
export function useSubmit<T, R>(
  submitFn: (data: T) => Promise<{ data: R }>
) {
  const [state, setState] = useState<{
    loading: boolean;
    error: ApiError | null;
    success: boolean;
  }>({
    loading: false,
    error: null,
    success: false,
  });

  const submit = useCallback(async (data: T) => {
    setState({ loading: true, error: null, success: false });
    try {
      await submitFn(data);
      setState({ loading: false, error: null, success: true });
      return true;
    } catch (error) {
      setState({
        loading: false,
        error: error instanceof ApiError ? error : new ApiError('Unknown error', 500),
        success: false,
      });
      return false;
    }
  }, [submitFn]);

  const reset = useCallback(() => {
    setState({ loading: false, error: null, success: false });
  }, []);

  return {
    ...state,
    submit,
    reset,
  };
}

/**
 * 删除操作Hook
 */
export function useDelete(
  deleteFn: (id: number) => Promise<{ data: void }>
) {
  return useSubmit<number, void>(deleteFn);
}

/**
 * 批量操作Hook
 */
export function useBatchOperation<T>(
  batchFn: (items: T[]) => Promise<{ data: any }>
) {
  const [selectedItems, setSelectedItems] = useState<T[]>([]);
  const { submit, loading, error, success, reset } = useSubmit(batchFn);

  const toggleItem = useCallback((item: T) => {
    setSelectedItems(prev => {
      const exists = prev.includes(item);
      return exists
        ? prev.filter(i => i !== item)
        : [...prev, item];
    });
  }, []);

  const selectAll = useCallback((items: T[]) => {
    setSelectedItems(items);
  }, []);

  const clearSelection = useCallback(() => {
    setSelectedItems([]);
  }, []);

  const executeBatch = useCallback(async () => {
    if (selectedItems.length > 0) {
      const success = await submit(selectedItems);
      if (success) {
        clearSelection();
      }
      return success;
    }
    return false;
  }, [selectedItems, submit, clearSelection]);

  return {
    selectedItems,
    toggleItem,
    selectAll,
    clearSelection,
    executeBatch,
    loading,
    error,
    success,
    reset,
  };
}