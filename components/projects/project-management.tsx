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
  DropdownMenuLabel,
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
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Progress } from "@/components/ui/progress"
import {
  Search,
  Filter,
  Plus,
  MoreHorizontal,
  Edit,
  Trash2,
  Users,
  Calendar,
  Target,
  Clock,
} from "lucide-react"
import { useProjects, useDeleteProject, useUpdateProject } from "@/lib/api/projects"
import { useToast } from "@/hooks/use-toast"
import { ProjectCreateDialog } from "./project-create-dialog"
import { ProjectEditDialog } from "./project-edit-dialog"
import type { Project, ProjectStatus, ProjectPriority } from "@/lib/api/projects"

// 状态和优先级标签映射
const statusLabels: Record<ProjectStatus, string> = {
  planning: "规划中",
  active: "进行中",
  on_hold: "暂停",
  completed: "已完成",
  cancelled: "已取消",
}

const priorityLabels: Record<ProjectPriority, string> = {
  low: "低",
  medium: "中",
  high: "高",
  urgent: "紧急",
}

// 获取状态徽章样式
const getStatusBadgeVariant = (status: ProjectStatus) => {
  switch (status) {
    case "planning":
      return "secondary"
    case "active":
      return "default"
    case "on_hold":
      return "outline"
    case "completed":
      return "success" as any
    case "cancelled":
      return "destructive"
    default:
      return "secondary"
  }
}

// 获取优先级徽章样式
const getPriorityBadgeVariant = (priority: ProjectPriority) => {
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

export function ProjectManagement() {
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState<ProjectStatus | "all">("all")
  const [priorityFilter, setPriorityFilter] = useState<ProjectPriority | "all">("all")
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [selectedProject, setSelectedProject] = useState<Project | null>(null)

  const { toast } = useToast()
  const { data: projects = [], isLoading } = useProjects()
  const deleteProjectMutation = useDeleteProject()
  const updateProjectMutation = useUpdateProject()

  const handleDeleteProject = async (id: string) => {
    try {
      await deleteProjectMutation.mutateAsync(id)
      toast({
        title: "删除成功",
        description: "项目已成功删除",
      })
    } catch (error) {
      toast({
        title: "删除失败",
        description: "删除项目时发生错误，请重试",
        variant: "destructive",
      })
    }
  }

  const handleEditProject = (project: Project) => {
    setSelectedProject(project)
    setIsEditDialogOpen(true)
  }

  // 过滤项目
  const filteredProjects = projects.filter(project => {
    const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (project.description && project.description.toLowerCase().includes(searchTerm.toLowerCase()))
    const matchesStatus = statusFilter === "all" || project.status === statusFilter
    const matchesPriority = priorityFilter === "all" || project.priority === priorityFilter
    
    return matchesSearch && matchesStatus && matchesPriority
  })

  // 计算统计数据
  const totalProjects = filteredProjects.length
  const planningProjects = filteredProjects.filter(p => p.status === "planning").length
  const activeProjects = filteredProjects.filter(p => p.status === "active").length
  const completedProjects = filteredProjects.filter(p => p.status === "completed").length

  return (
    <div className="space-y-6">
      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">总项目数</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalProjects}</div>
            <p className="text-xs text-muted-foreground">
              项目总数
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">规划中</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{planningProjects}</div>
            <p className="text-xs text-muted-foreground">
              规划阶段项目
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">进行中</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{activeProjects}</div>
            <p className="text-xs text-muted-foreground">
              正在进行的项目
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">已完成</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{completedProjects}</div>
            <p className="text-xs text-muted-foreground">
              已完成的项目
            </p>
          </CardContent>
        </Card>
      </div>

      {/* 搜索和筛选 */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>项目管理</CardTitle>
            <Button onClick={() => setIsCreateDialogOpen(true)}>
              <Plus className="mr-2 h-4 w-4" />
              新建项目
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="搜索项目名称或描述..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8"
              />
            </div>
            <Select value={statusFilter} onValueChange={(value) => setStatusFilter(value as ProjectStatus | "all")}>
              <SelectTrigger className="w-[180px]">
                <Filter className="mr-2 h-4 w-4" />
                <SelectValue placeholder="状态筛选" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">全部状态</SelectItem>
                <SelectItem value="planning">规划中</SelectItem>
                <SelectItem value="active">进行中</SelectItem>
                <SelectItem value="on_hold">暂停</SelectItem>
                <SelectItem value="completed">已完成</SelectItem>
                <SelectItem value="cancelled">已取消</SelectItem>
              </SelectContent>
            </Select>
            <Select value={priorityFilter} onValueChange={(value) => setPriorityFilter(value as ProjectPriority | "all")}>
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

          {/* 项目列表 */}
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <div className="text-muted-foreground">加载中...</div>
            </div>
          ) : filteredProjects.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <Target className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">暂无项目</h3>
              <p className="text-muted-foreground mb-4">
                {searchTerm || statusFilter !== "all" || priorityFilter !== "all" 
                  ? "没有找到符合条件的项目" 
                  : "还没有创建任何项目"}
              </p>
              {!searchTerm && statusFilter === "all" && priorityFilter === "all" && (
                <Button onClick={() => setIsCreateDialogOpen(true)}>
                  <Plus className="mr-2 h-4 w-4" />
                  创建第一个项目
                </Button>
              )}
            </div>
          ) : (
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>项目名称</TableHead>
                    <TableHead>状态</TableHead>
                    <TableHead>优先级</TableHead>
                    <TableHead>进度</TableHead>
                    <TableHead>负责人</TableHead>
                    <TableHead>截止日期</TableHead>
                    <TableHead className="text-right">操作</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredProjects.map((project) => (
                    <TableRow key={project.id}>
                      <TableCell>
                        <div>
                          <div className="font-medium">{project.name}</div>
                          {project.description && (
                            <div className="text-sm text-muted-foreground truncate max-w-[200px]">
                              {project.description}
                            </div>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant={getStatusBadgeVariant(project.status)}>
                          {statusLabels[project.status]}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Badge variant={getPriorityBadgeVariant(project.priority)}>
                          {priorityLabels[project.priority]}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          <Progress value={project.progress || 0} className="w-[60px]" />
                          <span className="text-sm text-muted-foreground">
                            {project.progress || 0}%
                          </span>
                        </div>
                      </TableCell>
                      <TableCell>
                        {project.manager_name ? (
                          <div className="flex items-center space-x-2">
                            <Avatar className="h-6 w-6">
                              <div className="bg-primary/10 text-primary text-xs font-medium flex items-center justify-center h-full">
                                {project.manager_name.charAt(0)}
                              </div>
                            </Avatar>
                            <span className="text-sm">{project.manager_name}</span>
                          </div>
                        ) : (
                          <span className="text-sm text-muted-foreground">未分配</span>
                        )}
                      </TableCell>
                      <TableCell>
                        {project.end_date ? (
                          <span className="text-sm">
                            {new Date(project.end_date).toLocaleDateString()}
                          </span>
                        ) : (
                          <span className="text-sm text-muted-foreground">未设置</span>
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
                            <DropdownMenuItem onClick={() => handleEditProject(project)}>
                              <Edit className="mr-2 h-4 w-4" />
                              编辑
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem 
                              onClick={() => handleDeleteProject(project.id)}
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

      {/* 创建项目对话框 */}
      <ProjectCreateDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
      />

      {/* 编辑项目对话框 */}
      <ProjectEditDialog
        open={isEditDialogOpen}
        onOpenChange={setIsEditDialogOpen}
        project={selectedProject}
      />
    </div>
  )
}
