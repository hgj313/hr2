"use client"

import { useState } from "react"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Bell,
  Search,
  Filter,
  MoreHorizontal,
  Check,
  CheckCheck,
  Trash2,
  Settings,
  AlertCircle,
  Info,
  CheckCircle,
  AlertTriangle,
  Calendar,
  User,
  FolderOpen,
  Clock,
} from "lucide-react"
import { formatDistanceToNow } from "date-fns"
import { zhCN } from "date-fns/locale"
import {
  useNotifications,
  useMarkNotificationAsRead,
  useMarkAllNotificationsAsRead,
  useDeleteNotification,
  useNotificationSettings,
  type Notification,
  type NotificationType,
  type NotificationPriority,
} from "@/lib/api/notifications"
import { NotificationSettings } from "./notification-settings"
import { useToast } from "@/components/ui/use-toast"

// 通知类型标签映射
const notificationTypeLabels: Record<NotificationType, string> = {
  system: "系统",
  project: "项目",
  schedule: "调度",
  user: "用户",
  reminder: "提醒",
}

// 通知优先级标签映射
const notificationPriorityLabels: Record<NotificationPriority, string> = {
  low: "低",
  medium: "中",
  high: "高",
  urgent: "紧急",
}

// 获取通知类型图标
const getNotificationTypeIcon = (type: NotificationType) => {
  switch (type) {
    case "system":
      return <Settings className="h-4 w-4" />
    case "project":
      return <FolderOpen className="h-4 w-4" />
    case "schedule":
      return <Calendar className="h-4 w-4" />
    case "user":
      return <User className="h-4 w-4" />
    case "reminder":
      return <Clock className="h-4 w-4" />
    default:
      return <Bell className="h-4 w-4" />
  }
}

// 获取通知优先级徽章样式
const getNotificationPriorityBadge = (priority: NotificationPriority) => {
  switch (priority) {
    case "urgent":
      return "destructive"
    case "high":
      return "destructive"
    case "medium":
      return "default"
    case "low":
      return "secondary"
    default:
      return "default"
  }
}

// 获取通知状态图标
const getNotificationStatusIcon = (priority: NotificationPriority) => {
  switch (priority) {
    case "urgent":
      return <AlertTriangle className="h-4 w-4 text-red-500" />
    case "high":
      return <AlertCircle className="h-4 w-4 text-orange-500" />
    case "medium":
      return <Info className="h-4 w-4 text-blue-500" />
    case "low":
      return <CheckCircle className="h-4 w-4 text-green-500" />
    default:
      return <Info className="h-4 w-4 text-gray-500" />
  }
}

export function NotificationCenter() {
  const [searchTerm, setSearchTerm] = useState("")
  const [typeFilter, setTypeFilter] = useState<NotificationType | "all">("all")
  const [priorityFilter, setPriorityFilter] = useState<NotificationPriority | "all">("all")
  const [statusFilter, setStatusFilter] = useState<"all" | "read" | "unread">("all")
  const [showSettings, setShowSettings] = useState(false)
  
  const { toast } = useToast()
  const { data: notifications, isLoading } = useNotifications()
  const { data: settings } = useNotificationSettings()
  const markAsReadMutation = useMarkNotificationAsRead()
  const markAllAsReadMutation = useMarkAllNotificationsAsRead()
  const deleteNotificationMutation = useDeleteNotification()

  // 过滤通知
  const filteredNotifications = notifications?.filter((notification) => {
    const matchesSearch = notification.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         notification.message.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesType = typeFilter === "all" || notification.type === typeFilter
    const matchesPriority = priorityFilter === "all" || notification.priority === priorityFilter
    const matchesStatus = statusFilter === "all" || 
                         (statusFilter === "read" && notification.isRead) ||
                         (statusFilter === "unread" && !notification.isRead)
    
    return matchesSearch && matchesType && matchesPriority && matchesStatus
  }) || []

  // 统计数据
  const unreadCount = notifications?.filter(n => !n.isRead).length || 0
  const urgentCount = notifications?.filter(n => n.priority === "urgent" && !n.isRead).length || 0

  const handleMarkAsRead = async (notificationId: string) => {
    try {
      await markAsReadMutation.mutateAsync(notificationId)
      toast({
        title: "标记成功",
        description: "通知已标记为已读",
      })
    } catch (error) {
      toast({
        title: "操作失败",
        description: "标记通知时发生错误",
        variant: "destructive",
      })
    }
  }

  const handleMarkAllAsRead = async () => {
    try {
      await markAllAsReadMutation.mutateAsync()
      toast({
        title: "标记成功",
        description: "所有通知已标记为已读",
      })
    } catch (error) {
      toast({
        title: "操作失败",
        description: "批量标记通知时发生错误",
        variant: "destructive",
      })
    }
  }

  const handleDeleteNotification = async (notificationId: string) => {
    try {
      await deleteNotificationMutation.mutateAsync(notificationId)
      toast({
        title: "删除成功",
        description: "通知已删除",
      })
    } catch (error) {
      toast({
        title: "删除失败",
        description: "删除通知时发生错误",
        variant: "destructive",
      })
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <Bell className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
          <p className="text-muted-foreground">加载通知中...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">未读通知</CardTitle>
            <Bell className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{unreadCount}</div>
            <p className="text-xs text-muted-foreground">
              共 {notifications?.length || 0} 条通知
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">紧急通知</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-500">{urgentCount}</div>
            <p className="text-xs text-muted-foreground">
              需要立即处理
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">今日通知</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {notifications?.filter(n => {
                const today = new Date()
                const notificationDate = new Date(n.createdAt)
                return notificationDate.toDateString() === today.toDateString()
              }).length || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              今天收到的通知
            </p>
          </CardContent>
        </Card>
      </div>

      {/* 控制栏 */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <div className="relative">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="搜索通知..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-8"
            />
          </div>
        </div>
        
        <div className="flex gap-2">
          <Select value={typeFilter} onValueChange={(value) => setTypeFilter(value as NotificationType | "all")}>
            <SelectTrigger className="w-[120px]">
              <SelectValue placeholder="类型" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">所有类型</SelectItem>
              {Object.entries(notificationTypeLabels).map(([value, label]) => (
                <SelectItem key={value} value={value}>
                  {label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          
          <Select value={priorityFilter} onValueChange={(value) => setPriorityFilter(value as NotificationPriority | "all")}>
            <SelectTrigger className="w-[120px]">
              <SelectValue placeholder="优先级" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">所有优先级</SelectItem>
              {Object.entries(notificationPriorityLabels).map(([value, label]) => (
                <SelectItem key={value} value={value}>
                  {label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          
          <Select value={statusFilter} onValueChange={(value) => setStatusFilter(value as "all" | "read" | "unread")}>
            <SelectTrigger className="w-[120px]">
              <SelectValue placeholder="状态" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">所有状态</SelectItem>
              <SelectItem value="unread">未读</SelectItem>
              <SelectItem value="read">已读</SelectItem>
            </SelectContent>
          </Select>
          
          <Button
            variant="outline"
            onClick={handleMarkAllAsRead}
            disabled={unreadCount === 0 || markAllAsReadMutation.isPending}
          >
            <CheckCheck className="mr-2 h-4 w-4" />
            全部已读
          </Button>
          
          <Button
            variant="outline"
            onClick={() => setShowSettings(true)}
          >
            <Settings className="mr-2 h-4 w-4" />
            设置
          </Button>
        </div>
      </div>

      {/* 通知列表 */}
      <Card>
        <CardHeader>
          <CardTitle>通知列表</CardTitle>
          <CardDescription>
            显示 {filteredNotifications.length} 条通知
          </CardDescription>
        </CardHeader>
        <CardContent>
          {filteredNotifications.length === 0 ? (
            <div className="text-center py-12">
              <Bell className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-medium mb-2">暂无通知</h3>
              <p className="text-muted-foreground">
                {searchTerm || typeFilter !== "all" || priorityFilter !== "all" || statusFilter !== "all"
                  ? "没有符合筛选条件的通知"
                  : "您目前没有任何通知"}
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredNotifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`flex items-start gap-4 p-4 rounded-lg border transition-colors ${
                    notification.isRead
                      ? "bg-background"
                      : "bg-muted/50 border-primary/20"
                  }`}
                >
                  <div className="flex-shrink-0">
                    {getNotificationStatusIcon(notification.priority)}
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h4 className={`font-medium ${
                            notification.isRead ? "text-muted-foreground" : "text-foreground"
                          }`}>
                            {notification.title}
                          </h4>
                          {!notification.isRead && (
                            <div className="w-2 h-2 bg-primary rounded-full" />
                          )}
                        </div>
                        
                        <p className={`text-sm mb-2 ${
                          notification.isRead ? "text-muted-foreground" : "text-foreground"
                        }`}>
                          {notification.message}
                        </p>
                        
                        <div className="flex items-center gap-2 text-xs text-muted-foreground">
                          <div className="flex items-center gap-1">
                            {getNotificationTypeIcon(notification.type)}
                            <span>{notificationTypeLabels[notification.type]}</span>
                          </div>
                          
                          <Badge variant={getNotificationPriorityBadge(notification.priority)} className="text-xs">
                            {notificationPriorityLabels[notification.priority]}
                          </Badge>
                          
                          <span>
                            {formatDistanceToNow(new Date(notification.createdAt), {
                              addSuffix: true,
                              locale: zhCN,
                            })}
                          </span>
                        </div>
                      </div>
                      
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="sm">
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          {!notification.isRead && (
                            <DropdownMenuItem
                              onClick={() => handleMarkAsRead(notification.id)}
                              disabled={markAsReadMutation.isPending}
                            >
                              <Check className="mr-2 h-4 w-4" />
                              标记为已读
                            </DropdownMenuItem>
                          )}
                          <DropdownMenuSeparator />
                          <DropdownMenuItem
                            onClick={() => handleDeleteNotification(notification.id)}
                            disabled={deleteNotificationMutation.isPending}
                            className="text-destructive"
                          >
                            <Trash2 className="mr-2 h-4 w-4" />
                            删除通知
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* 通知设置对话框 */}
      <NotificationSettings
        open={showSettings}
        onOpenChange={setShowSettings}
        settings={settings}
      />
    </div>
  )
}