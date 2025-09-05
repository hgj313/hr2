import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from './client'
import { Schedule } from '@/components/scheduling/scheduling-management'

// 获取所有调度任务
export function useSchedules() {
  return useQuery({
    queryKey: ['schedules'],
    queryFn: async (): Promise<Schedule[]> => {
      const response = await api.get('/schedules')
      return response.data
    },
  })
}

// 获取单个调度任务
export function useSchedule(id: string) {
  return useQuery({
    queryKey: ['schedules', id],
    queryFn: async (): Promise<Schedule> => {
      const response = await api.get(`/schedules/${id}`)
      return response.data
    },
    enabled: !!id,
  })
}

// 创建调度任务
export function useCreateSchedule() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (data: Omit<Schedule, 'id' | 'created_at' | 'updated_at'>): Promise<Schedule> => {
      const response = await api.post('/schedules', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['schedules'] })
    },
  })
}

// 更新调度任务
export function useUpdateSchedule() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: Partial<Schedule> }): Promise<Schedule> => {
      const response = await api.put(`/schedules/${id}`, data)
      return response.data
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['schedules'] })
      queryClient.invalidateQueries({ queryKey: ['schedules', data.id] })
    },
  })
}

// 删除调度任务
export function useDeleteSchedule() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (id: string): Promise<void> => {
      await api.delete(`/schedules/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['schedules'] })
    },
  })
}

// 获取调度冲突
export function useScheduleConflicts(scheduleId: string) {
  return useQuery({
    queryKey: ['schedules', scheduleId, 'conflicts'],
    queryFn: async () => {
      const response = await api.get(`/schedules/${scheduleId}/conflicts`)
      return response.data
    },
    enabled: !!scheduleId,
  })
}

// 解决调度冲突
export function useResolveScheduleConflict() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ scheduleId, conflictId, resolution }: {
      scheduleId: string
      conflictId: string
      resolution: string
    }) => {
      const response = await api.post(`/schedules/${scheduleId}/conflicts/${conflictId}/resolve`, {
        resolution,
      })
      return response.data
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['schedules'] })
      queryClient.invalidateQueries({ queryKey: ['schedules', variables.scheduleId] })
      queryClient.invalidateQueries({ queryKey: ['schedules', variables.scheduleId, 'conflicts'] })
    },
  })
}

// 批量解决调度冲突
export function useResolveAllScheduleConflicts() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (scheduleId: string) => {
      const response = await api.post(`/schedules/${scheduleId}/conflicts/resolve-all`)
      return response.data
    },
    onSuccess: (_, scheduleId) => {
      queryClient.invalidateQueries({ queryKey: ['schedules'] })
      queryClient.invalidateQueries({ queryKey: ['schedules', scheduleId] })
      queryClient.invalidateQueries({ queryKey: ['schedules', scheduleId, 'conflicts'] })
    },
  })
}

// 获取调度统计数据
export function useScheduleStats() {
  return useQuery({
    queryKey: ['schedules', 'stats'],
    queryFn: async () => {
      const response = await api.get('/schedules/stats')
      return response.data
    },
  })
}

// 获取调度建议
export function useScheduleSuggestions(params?: {
  project_id?: string
  start_date?: string
  end_date?: string
  required_skills?: string[]
}) {
  return useQuery({
    queryKey: ['schedules', 'suggestions', params],
    queryFn: async () => {
      const response = await api.get('/schedules/suggestions', { params })
      return response.data
    },
    enabled: !!params,
  })
}

// 优化调度
export function useOptimizeSchedule() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (scheduleId: string) => {
      const response = await api.post(`/schedules/${scheduleId}/optimize`)
      return response.data
    },
    onSuccess: (_, scheduleId) => {
      queryClient.invalidateQueries({ queryKey: ['schedules'] })
      queryClient.invalidateQueries({ queryKey: ['schedules', scheduleId] })
    },
  })
}