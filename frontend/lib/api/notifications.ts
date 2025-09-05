import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"

// 通知类型定义
export type NotificationType = "system" | "project" | "schedule" | "user" | "reminder"
export type NotificationPriority = "urgent" | "high" | "medium" | "low"
export type NotificationStatus = "unread" | "read"

export interface Notification {
  id: string
  title: string
  message: string
  type: NotificationType
  priority: NotificationPriority
  status: NotificationStatus
  createdAt: string
  readAt?: string
  userId: string
  metadata?: {
    projectId?: string
    scheduleId?: string
    actionUrl?: string
    [key: string]: any
  }
}

export interface NotificationSettings {
  emailNotifications: boolean
  pushNotifications: boolean
  smsNotifications: boolean
  soundEnabled: boolean
  notificationFrequency: "immediate" | "hourly" | "daily" | "weekly"
  quietHours: {
    enabled: boolean
    startTime: string
    endTime: string
  }
  categories: {
    system: boolean
    project: boolean
    schedule: boolean
    user: boolean
    reminder: boolean
  }
  priorities: {
    urgent: boolean
    high: boolean
    medium: boolean
    low: boolean
  }
}

export interface NotificationStats {
  total: number
  unread: number
  urgent: number
  today: number
}

// 模拟通知数据
const mockNotifications: Notification[] = [
  {
    id: "1",
    title: "新项目分配",
    message: "您已被分配到项目 '智能办公系统开发'",
    type: "project",
    priority: "high",
    status: "unread",
    createdAt: new Date().toISOString(),
    userId: "user1",
    metadata: {
      projectId: "proj1",
      actionUrl: "/projects/proj1"
    }
  },
  {
    id: "2",
    title: "调度冲突提醒",
    message: "检测到资源调度冲突，需要您的处理",
    type: "schedule",
    priority: "urgent",
    status: "unread",
    createdAt: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
    userId: "user1",
    metadata: {
      scheduleId: "sched1",
      actionUrl: "/scheduling"
    }
  },
  {
    id: "3",
    title: "系统维护通知",
    message: "系统将于今晚22:00-24:00进行维护升级",
    type: "system",
    priority: "medium",
    status: "read",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
    readAt: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
    userId: "user1"
  },
  {
    id: "4",
    title: "任务截止提醒",
    message: "项目 'HR系统优化' 的任务将于明天截止",
    type: "reminder",
    priority: "high",
    status: "unread",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 4).toISOString(),
    userId: "user1",
    metadata: {
      projectId: "proj2",
      actionUrl: "/projects/proj2"
    }
  },
  {
    id: "5",
    title: "用户权限更新",
    message: "您的账户权限已更新，新增项目管理权限",
    type: "user",
    priority: "medium",
    status: "read",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 6).toISOString(),
    readAt: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(),
    userId: "user1"
  },
  {
    id: "6",
    title: "团队会议提醒",
    message: "明天上午10:00有团队周会，请准时参加",
    type: "reminder",
    priority: "medium",
    status: "unread",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 8).toISOString(),
    userId: "user1"
  },
  {
    id: "7",
    title: "项目进度更新",
    message: "项目 '移动端应用开发' 进度已更新至75%",
    type: "project",
    priority: "low",
    status: "read",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 12).toISOString(),
    readAt: new Date(Date.now() - 1000 * 60 * 60 * 10).toISOString(),
    userId: "user1",
    metadata: {
      projectId: "proj3",
      actionUrl: "/projects/proj3"
    }
  },
  {
    id: "8",
    title: "系统性能报告",
    message: "本周系统性能报告已生成，请查看",
    type: "system",
    priority: "low",
    status: "unread",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
    userId: "user1",
    metadata: {
      actionUrl: "/analytics"
    }
  }
]

const mockNotificationSettings: NotificationSettings = {
  emailNotifications: true,
  pushNotifications: true,
  smsNotifications: false,
  soundEnabled: true,
  notificationFrequency: "immediate",
  quietHours: {
    enabled: false,
    startTime: "22:00",
    endTime: "08:00"
  },
  categories: {
    system: true,
    project: true,
    schedule: true,
    user: true,
    reminder: true
  },
  priorities: {
    urgent: true,
    high: true,
    medium: true,
    low: false
  }
}

// API函数模拟
const fetchNotifications = async (): Promise<Notification[]> => {
  // 模拟API延迟
  await new Promise(resolve => setTimeout(resolve, 500))
  return mockNotifications
}

const markNotificationAsRead = async (id: string): Promise<void> => {
  await new Promise(resolve => setTimeout(resolve, 300))
  const notification = mockNotifications.find(n => n.id === id)
  if (notification) {
    notification.status = "read"
    notification.readAt = new Date().toISOString()
  }
}

const markAllNotificationsAsRead = async (): Promise<void> => {
  await new Promise(resolve => setTimeout(resolve, 500))
  const now = new Date().toISOString()
  mockNotifications.forEach(notification => {
    if (notification.status === "unread") {
      notification.status = "read"
      notification.readAt = now
    }
  })
}

const deleteNotification = async (id: string): Promise<void> => {
  await new Promise(resolve => setTimeout(resolve, 300))
  const index = mockNotifications.findIndex(n => n.id === id)
  if (index > -1) {
    mockNotifications.splice(index, 1)
  }
}

const fetchNotificationSettings = async (): Promise<NotificationSettings> => {
  await new Promise(resolve => setTimeout(resolve, 300))
  return mockNotificationSettings
}

const updateNotificationSettings = async (settings: NotificationSettings): Promise<NotificationSettings> => {
  await new Promise(resolve => setTimeout(resolve, 500))
  Object.assign(mockNotificationSettings, settings)
  return mockNotificationSettings
}

// React Query Hooks
export const useNotifications = () => {
  return useQuery({
    queryKey: ["notifications"],
    queryFn: fetchNotifications,
    staleTime: 1000 * 60 * 5, // 5分钟
  })
}

export const useMarkNotificationAsRead = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: markNotificationAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notifications"] })
    },
  })
}

export const useMarkAllNotificationsAsRead = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: markAllNotificationsAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notifications"] })
    },
  })
}

export const useDeleteNotification = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: deleteNotification,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notifications"] })
    },
  })
}

export const useNotificationSettings = () => {
  return useQuery({
    queryKey: ["notification-settings"],
    queryFn: fetchNotificationSettings,
    staleTime: 1000 * 60 * 10, // 10分钟
  })
}

export const useUpdateNotificationSettings = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: updateNotificationSettings,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notification-settings"] })
    },
  })
}

// 计算通知统计
export const useNotificationStats = () => {
  return useQuery({
    queryKey: ["notification-stats"],
    queryFn: async (): Promise<NotificationStats> => {
      const notifications = await fetchNotifications()
      const now = new Date()
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      
      return {
        total: notifications.length,
        unread: notifications.filter(n => n.status === "unread").length,
        urgent: notifications.filter(n => n.priority === "urgent" && n.status === "unread").length,
        today: notifications.filter(n => new Date(n.createdAt) >= today).length,
      }
    },
    staleTime: 1000 * 60 * 2, // 2分钟
  })
}