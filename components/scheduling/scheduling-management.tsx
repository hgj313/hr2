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
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
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
import { Avatar } from "@/components/ui/avatar"
import { Progress } from "@/components/ui/progress"
import {
  Search,
  Filter,
  Plus,
  MoreHorizontal,
  Edit,
  Trash2,
  Calendar,
  Users,
  Clock,
  AlertTriangle,
  CheckCircle,
  Play,
  Pause,
  RotateCcw,
} from "lucide-react"
import { useSchedules, useDeleteSchedule, useUpdateSchedule } from "@/lib/api/schedules"
import { useToast } from "@/hooks/use-toast"
import { ScheduleCreateDialog } from "./schedule-create-dialog"
import { ScheduleEditDialog } from "./schedule-edit-dialog"
import { ConflictResolutionDialog } from "./conflict-resolution-dialog"

// 调度状态类型
export type ScheduleStatus = "draft" | "active" | "paused" | "completed" | "cancelled"

// 调度优先级类型
export type SchedulePriority = "low" | "medium" | "high" | "urgent"

// 调度类型
export interface Schedule {
  id: string
  name: string
  description?: string
  status: ScheduleStatus
  priority: SchedulePriority
  start_date: string
  end_date: string
  project_id?: string
  project_name?: string
  assigned_users: string[]
  assigned_user_names?: string[]
  conflicts?: ScheduleConflict[]
  progress?: number
  created_at: string
  updated_at: string
}

// 调度冲突类型
export interface ScheduleConflict {
  id: string
  type: "resource" | "time" | "skill"
  severity: "low" | "medium" | "high"
  description: string
  affected_users: string[]
  suggested_resolution?: string
}

// 状态标签映射
const statusLabels: Record<ScheduleStatus, string> = {
  draft: "草稿",
  active: "进行中",
  paused: "暂停",
  completed: "已完成",
  cancelled: "已取消",
}

// 优先级标签映射
const priorityLabels: Record<SchedulePriority, string> = {
  low: "低",
  medium: "中",
  high: "高",
  urgent: "紧急",
}

// 获取状态徽章样式
const getStatusBadgeVariant = (status: ScheduleStatus) => {
  switch (status) {
    case "draft":
      return "secondary"
    case "active":
      return "default"
    case "paused":
      return "outline"
    case "completed":
      return "default"
    case "cancelled":
      return "destructive"
    default:
      return "secondary"
  }
}

// 获取优先级徽章样式
const getPriorityBadgeVariant = (priority: SchedulePriority) => {
  switch (priority) {
    case "low":
      return "secondary"
    case "medium":
      return "outline"
    case "high":
      return "default"
    case "urgent":
      return "destructive"
    default:
      return "secondary"
  }
}

export function SchedulingManagement() {
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState<ScheduleStatus | "all">("all")
  const [priorityFilter, setPriorityFilter] = useState<SchedulePriority | "all">("all")
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [isConflictDialogOpen, setIsConflictDialogOpen] = useState(false)
  const [selectedSchedule, setSelectedSchedule] = useState<Schedule | null>(null)

  const { toast } = useToast()
  const { data: schedules = [], isLoading } = useSchedules()
  const deleteScheduleMutation = useDeleteSchedule()
  const updateScheduleMutation = useUpdateSchedule()

  const handleDeleteSchedule = async (id: string) => {
    try {
      await deleteScheduleMutation.mutateAsync(id)
      toast({
        title: "删除成功",
        description: "调度任务已成功删除",
      })
    } catch (error) {
      toast({
        title: "删除失败",
        description: "删除调度任务时发生错误，请重试",
        variant: "destructive",
      })
    }
  }

  const handleEditSchedule = (schedule: Schedule) => {
    setSelectedSchedule(schedule)
    setIsEditDialogOpen(true)
  }

  const handleResolveConflicts = (schedule: Schedule) => {
    setSelectedSchedule(schedule)
    setIsConflictDialogOpen(true)
  }

  const handleToggleScheduleStatus = async (schedule: Schedule) => {
    try {
      const newStatus = schedule.status === "active" ? "paused" : "active"
      await updateScheduleMutation.mutateAsync({
        id: schedule.id,
        data: { status: newStatus },
      })
      toast({
        title: "状态更新成功",
        description: `调度任务已${newStatus === "active" ? "启动" : "暂停"}\`,
      })
    } catch (error) {
      toast({
        title: "状态更新失败",
        description: "更新调度任务状态时发生错误，请重试",
        variant: "destructive",
      })
    }
  }

  // 过滤调度任务
  const filteredSchedules = schedules.filter(schedule => {
    const matchesSearch = schedule.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (schedule.description && schedule.description.toLowerCase().includes(searchTerm.toLowerCase()))
    const matchesStatus = statusFilter === "all" || schedule.status === statusFilter
    const matchesPriority = priorityFilter === "all" || schedule.priority === priorityFilter
    
    return matchesSearch && matchesStatus && matchesPriority
  })

  // 统计数据
  const totalSchedules = schedules.length
  const activeSchedules = schedules.filter(s => s.status === "active").length
  const completedSchedules = schedules.filter(s => s.status === "completed").length
  const conflictSchedules = schedules.filter(s => s.conflicts && s.conflicts.length > 0).length

  return (
    <div className="space-y-6">
      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">总调度数</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalSchedules}</div>
            <p className="text-xs text-muted-foreground">
              调度任务总数
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">进行中</CardTitle>
            <Play className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{activeSchedules}</div>
            <p className="text-xs text-muted-foreground">
              正在执行的调度
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">已完成</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{completedSchedules}</div>
            <p className="text-xs text-muted-foreground">
              已完成的调度
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">冲突待解决</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{conflictSchedules}</div>
            <p className="text-xs text-muted-foreground">
              存在冲突的调度
            </p>
          </CardContent>
        </Card>
      </div>

      {/* 搜索和筛选 */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>调度管理</CardTitle>
            <Button onClick={() => setIsCreateDialogOpen(true)}>
              <Plus className="mr-2 h-4 w-4" />
              新建调度
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="搜索调度名称或描述..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8"
              />
            </div>
            <Select value={statusFilter} onValueChange={(value) => setStatusFilter(value as ScheduleStatus | "all")}>
              <SelectTrigger className="w-[180px]">
                <Filter className="mr-2 h-4 w-4" />
                <SelectValue placeholder="状态筛选" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">全部状态</SelectItem>
                <SelectItem value="draft">草稿</SelectItem>
                <SelectItem value="active">进行中</SelectItem>
                <SelectItem value="paused">暂停</SelectItem>
                <SelectItem value="completed">已完成</SelectItem>
                <SelectItem value="cancelled">已取消</SelectItem>
              </SelectContent>
            </Select>
            <Select value={priorityFilter} onValueChange={(value) => setPriorityFilter(value as SchedulePriority | "all")}>
              <SelectTrigger className="w-[180px]">
                <Filter className="mr-2 h-4 w-4" />
                <SelectValue placeholder="优先级筛选" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">全部优先级</SelectItem>
                <SelectItem value="low">低</SelectItem>
                <SelectItem value="medium">中</SelectItem>
                <SelectItem value="high">高</SelectItem>
                <SelectItem value="urgent">紧急</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* 调度列表 */}
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <div className="text-muted-foreground">加载中...</div>
            </div>
          ) : filteredSchedules.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <Calendar className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">暂无调度任务</h3>
              <p className="text-muted-foreground mb-4">
                {searchTerm || statusFilter !== "all" || priorityFilter !== "all" 
                  ? "没有找到符合条件的调度任务" 
                  : "还没有创建任何调度任务"}
              </p>
              {!searchTerm && statusFilter === "all" && priorityFilter === "all" && (
                <Button onClick={() => setIsCreateDialogOpen(true)}>
                  <Plus className="mr-2 h-4 w-4" />
                  创建第一个调度任务
                </Button>
              )}
            </div>
          ) : (
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>调度名称</TableHead>
                    <TableHead>状态</TableHead>
                    <TableHead>优先级</TableHead>
                    <TableHead>进度</TableHead>
                    <TableHead>分配人员</TableHead>
                    <TableHead>项目</TableHead>
                    <TableHead>冲突</TableHead>
                    <TableHead className="text-right">操作</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredSchedules.map((schedule) => (
                    <TableRow key={schedule.id}>
                      <TableCell>
                        <div>
                          <div className="font-medium">{schedule.name}</div>
                          {schedule.description && (
                            <div className="text-sm text-muted-foreground truncate max-w-[200px]">
                              {schedule.description}
                            </div>
                          )}
                          <div className="text-xs text-muted-foreground mt-1">
                            {new Date(schedule.start_date).toLocaleDateString()} - {new Date(schedule.end_date).toLocaleDateString()}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant={getStatusBadgeVariant(schedule.status)}>
                          {statusLabels[schedule.status]}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Badge variant={getPriorityBadgeVariant(schedule.priority)}>
                          {priorityLabels[schedule.priority]}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          <Progress value={schedule.progress || 0} className="w-[60px]" />
                          <span className="text-sm text-muted-foreground">
                            {schedule.progress || 0}%
                          </span>
                        </div>
                      </TableCell>
                      <TableCell>
                        {schedule.assigned_user_names && schedule.assigned_user_names.length > 0 ? (
                          <div className="flex items-center space-x-1">
                            <Users className="h-4 w-4 text-muted-foreground" />
                            <span className="text-sm">{schedule.assigned_user_names.length}人</span>
                          </div>
                        ) : (
                          <span className="text-sm text-muted-foreground">未分配</span>
                        )}
                      </TableCell>
                      <TableCell>
                        {schedule.project_name ? (
                          <span className="text-sm">{schedule.project_name}</span>
                        ) : (
                          <span className="text-sm text-muted-foreground">无关联项目</span>
                        )}
                      </TableCell>
                      <TableCell>
                        {schedule.conflicts && schedule.conflicts.length > 0 ? (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleResolveConflicts(schedule)}
                            className="text-destructive border-destructive hover:bg-destructive hover:text-destructive-foreground"
                          >
                            <AlertTriangle className="mr-1 h-3 w-3" />
                            {schedule.conflicts.length}个冲突
                          </Button>
                        ) : (
                          <span className="text-sm text-muted-foreground">无冲突</span>
                        )}
                      </TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                              <span className="sr-only">打开菜单</span>
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem onClick={() => handleEditSchedule(schedule)}>
                              <Edit className="mr-2 h-4 w-4" />
                              编辑
                            </DropdownMenuItem>
                            {schedule.status === "active" || schedule.status === "paused" ? (
                              <DropdownMenuItem onClick={() => handleToggleScheduleStatus(schedule)}>
                                {schedule.status === "active" ? (
                                  <>
                                    <Pause className="mr-2 h-4 w-4" />
                                    暂停
                                  </>
                                ) : (
                                  <>
                                    <Play className="mr-2 h-4 w-4" />
                                    启动
                                  </>
                                )}
                              </DropdownMenuItem>
                            ) : null}
                            {schedule.conflicts && schedule.conflicts.length > 0 && (
                              <DropdownMenuItem onClick={() => handleResolveConflicts(schedule)}>
                                <RotateCcw className="mr-2 h-4 w-4" />
                                解决冲突
                              </DropdownMenuItem>
                            )}
                            <DropdownMenuSeparator />
                            <DropdownMenuItem 
                              onClick={() => handleDeleteSchedule(schedule.id)}
                              className="text-destructive"
                            >
                              <Trash2 className="mr-2 h-4 w-4" />
                              删除
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* 创建调度对话框 */}
      <ScheduleCreateDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
      />

      {/* 编辑调度对话框 */}
      <ScheduleEditDialog
        open={isEditDialogOpen}
        onOpenChange={setIsEditDialogOpen}
        schedule={selectedSchedule}
      />

      {/* 冲突解决对话框 */}
      <ConflictResolutionDialog
        open={isConflictDialogOpen}
        onOpenChange={setIsConflictDialogOpen}
        schedule={selectedSchedule}
      />
    </div>
  )
}