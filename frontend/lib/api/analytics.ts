import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { toast } from '@/components/ui/use-toast'

// 分析数据类型定义
export interface AnalyticsOverview {
  totalUsers: number
  userGrowth: number
  activeProjects: number
  projectGrowth: number
  totalSchedules: number
  completedSchedules: number
  systemEfficiency: number
  efficiencyChange: number
}

export interface TrendDataPoint {
  date: string
  completed: number
  inProgress: number
  planned: number
}

export interface UserActivityData {
  time: string
  activeUsers: number
  newUsers: number
}

export interface ProjectStatusDistribution {
  name: string
  value: number
}

export interface ScheduleEfficiencyData {
  category: string
  efficiency: number
  target: number
}

export interface ResourceUtilizationData {
  resource: string
  utilization: number
  capacity: number
}

export interface PerformanceAlert {
  severity: 'high' | 'medium' | 'low'
  title: string
  description: string
  suggestion?: string
}

export interface AnalyticsData {
  overview: AnalyticsOverview
  trendData: TrendDataPoint[]
  userStats: {
    activityData: UserActivityData[]
  }
  distributionData: {
    projectStatus: ProjectStatusDistribution[]
  }
  scheduleStats: {
    efficiencyData: ScheduleEfficiencyData[]
  }
  performanceMetrics: {
    resourceUtilization: ResourceUtilizationData[]
    alerts: PerformanceAlert[]
  }
}

// 模拟API数据
const mockAnalyticsData: AnalyticsData = {
  overview: {
    totalUsers: 156,
    userGrowth: 12.5,
    activeProjects: 24,
    projectGrowth: 8.3,
    totalSchedules: 89,
    completedSchedules: 67,
    systemEfficiency: 87,
    efficiencyChange: 5.2,
  },
  trendData: [
    { date: '2024-01', completed: 12, inProgress: 8, planned: 15 },
    { date: '2024-02', completed: 15, inProgress: 10, planned: 12 },
    { date: '2024-03', completed: 18, inProgress: 12, planned: 18 },
    { date: '2024-04', completed: 22, inProgress: 15, planned: 20 },
    { date: '2024-05', completed: 25, inProgress: 18, planned: 22 },
    { date: '2024-06', completed: 28, inProgress: 20, planned: 25 },
  ],
  userStats: {
    activityData: [
      { time: '00:00', activeUsers: 12, newUsers: 2 },
      { time: '04:00', activeUsers: 8, newUsers: 1 },
      { time: '08:00', activeUsers: 45, newUsers: 8 },
      { time: '12:00', activeUsers: 67, newUsers: 12 },
      { time: '16:00', activeUsers: 89, newUsers: 15 },
      { time: '20:00', activeUsers: 34, newUsers: 5 },
    ],
  },
  distributionData: {
    projectStatus: [
      { name: '计划中', value: 8 },
      { name: '进行中', value: 12 },
      { name: '已完成', value: 24 },
      { name: '已暂停', value: 3 },
      { name: '已取消', value: 2 },
    ],
  },
  scheduleStats: {
    efficiencyData: [
      { category: '任务分配', efficiency: 85, target: 90 },
      { category: '资源利用', efficiency: 78, target: 80 },
      { category: '时间管理', efficiency: 92, target: 85 },
      { category: '冲突解决', efficiency: 88, target: 90 },
    ],
  },
  performanceMetrics: {
    resourceUtilization: [
      { resource: '开发团队', utilization: 85, capacity: 100 },
      { resource: '设计团队', utilization: 72, capacity: 100 },
      { resource: '测试团队', utilization: 90, capacity: 100 },
      { resource: '运维团队', utilization: 68, capacity: 100 },
    ],
    alerts: [
      {
        severity: 'high',
        title: '资源利用率过高',
        description: '测试团队的资源利用率已达到90%，可能影响项目进度',
        suggestion: '考虑增加测试人员或重新分配任务',
      },
      {
        severity: 'medium',
        title: '项目延期风险',
        description: '有3个项目存在延期风险，需要关注进度',
        suggestion: '优化任务分配，增加关键路径监控',
      },
      {
        severity: 'low',
        title: '系统性能优化',
        description: '系统响应时间可以进一步优化',
        suggestion: '考虑升级服务器配置或优化数据库查询',
      },
    ],
  },
}

// API函数
const fetchAnalyticsData = async (timeRange: string): Promise<AnalyticsData> => {
  // 模拟API调用延迟
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  // 根据时间范围调整数据（这里简化处理）
  return mockAnalyticsData
}

const exportAnalyticsData = async (timeRange: string, format: string) => {
  await new Promise(resolve => setTimeout(resolve, 500))
  return { success: true, downloadUrl: `/api/analytics/export?range=${timeRange}&format=${format}` }
}

// React Query Hooks
export const useAnalyticsData = (timeRange: string) => {
  return useQuery({
    queryKey: ['analytics', timeRange],
    queryFn: () => fetchAnalyticsData(timeRange),
    staleTime: 5 * 60 * 1000, // 5分钟
    cacheTime: 10 * 60 * 1000, // 10分钟
  })
}

export const useExportAnalytics = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ timeRange, format }: { timeRange: string; format: string }) =>
      exportAnalyticsData(timeRange, format),
    onSuccess: () => {
      toast({
        title: '导出成功',
        description: '分析报告已生成，请检查下载文件夹',
      })
    },
    onError: () => {
      toast({
        title: '导出失败',
        description: '导出分析报告时发生错误，请重试',
        variant: 'destructive',
      })
    },
  })
}

// 实时数据更新Hook
export const useRealTimeAnalytics = (timeRange: string, enabled: boolean = true) => {
  return useQuery({
    queryKey: ['analytics', 'realtime', timeRange],
    queryFn: () => fetchAnalyticsData(timeRange),
    refetchInterval: enabled ? 30000 : false, // 30秒刷新一次
    enabled,
  })
}

// 获取特定指标数据
export const useMetricData = (metric: string, timeRange: string) => {
  return useQuery({
    queryKey: ['analytics', 'metric', metric, timeRange],
    queryFn: async () => {
      const data = await fetchAnalyticsData(timeRange)
      // 根据指标类型返回相应数据
      switch (metric) {
        case 'overview':
          return data.overview
        case 'trends':
          return data.trendData
        case 'users':
          return data.userStats
        case 'projects':
          return data.distributionData
        case 'schedules':
          return data.scheduleStats
        case 'performance':
          return data.performanceMetrics
        default:
          return null
      }
    },
  })
}