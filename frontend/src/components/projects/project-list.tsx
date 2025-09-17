"use client"

import { useState, useMemo } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Progress } from "@/components/ui/progress"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import {
  Search,
  Plus,
  Calendar,
  Users,
  DollarSign,
  MoreHorizontal,
  Eye,
  Edit,
  Archive,
  TrendingUp,
  Clock,
  AlertTriangle,
} from "lucide-react"
import { mockProjects, getUserById, type Project } from "@/lib/mock-data"

interface ProjectListProps {
  onProjectSelect: (project: Project) => void
  onProjectEdit: (project: Project) => void
}

export function ProjectList({ onProjectSelect, onProjectEdit }: ProjectListProps) {
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [priorityFilter, setPriorityFilter] = useState("all")
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid")

  const filteredProjects = useMemo(() => {
    return mockProjects.filter((project) => {
      const matchesSearch =
        project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        project.description.toLowerCase().includes(searchTerm.toLowerCase())
      const matchesStatus = statusFilter === "all" || project.status === statusFilter
      const matchesPriority = priorityFilter === "all" || project.priority === priorityFilter
      return matchesSearch && matchesStatus && matchesPriority
    })
  }, [searchTerm, statusFilter, priorityFilter])

  const getStatusBadge = (status: Project["status"]) => {
    const variants = {
      planning: "outline",
      active: "default",
      completed: "secondary",
      on_hold: "destructive",
    } as const

    const labels = {
      planning: "规划中",
      active: "进行中",
      completed: "已完成",
      on_hold: "暂停",
    }

    return (
      <Badge variant={variants[status]} className="text-xs">
        {labels[status]}
      </Badge>
    )
  }

  const getPriorityBadge = (priority: Project["priority"]) => {
    const variants = {
      low: "outline",
      medium: "secondary",
      high: "default",
      urgent: "destructive",
    } as const

    const labels = {
      low: "低",
      medium: "中",
      high: "高",
      urgent: "紧急",
    }

    return (
      <Badge variant={variants[priority]} className="text-xs">
        {labels[priority]}
      </Badge>
    )
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("zh-CN", {
      style: "currency",
      currency: "CNY",
      minimumFractionDigits: 0,
    }).format(amount)
  }

  const getProjectHealth = (project: Project) => {
    if (project.progress >= 90) return { status: "excellent", color: "text-green-600", icon: TrendingUp }
    if (project.progress >= 70) return { status: "good", color: "text-blue-600", icon: TrendingUp }
    if (project.progress >= 50) return { status: "warning", color: "text-yellow-600", icon: Clock }
    return { status: "danger", color: "text-red-600", icon: AlertTriangle }
  }

  const ProjectCard = ({ project }: { project: Project }) => {
    const manager = getUserById(project.manager)
    const health = getProjectHealth(project)
    const HealthIcon = health.icon

    return (
      <Card className="hover:shadow-md transition-shadow cursor-pointer" onClick={() => onProjectSelect(project)}>
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <CardTitle className="text-lg line-clamp-1">{project.name}</CardTitle>
              <p className="text-sm text-muted-foreground mt-1 line-clamp-2">{project.description}</p>
            </div>
            <DropdownMenu>
              <DropdownMenuTrigger asChild onClick={(e) => e.stopPropagation()}>
                <Button variant="ghost" size="sm">
                  <MoreHorizontal className="w-4 h-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem
                  onClick={(e) => {
                    e.stopPropagation()
                    onProjectSelect(project)
                  }}
                >
                  <Eye className="w-4 h-4 mr-2" />
                  查看详情
                </DropdownMenuItem>
                <DropdownMenuItem
                  onClick={(e) => {
                    e.stopPropagation()
                    onProjectEdit(project)
                  }}
                >
                  <Edit className="w-4 h-4 mr-2" />
                  编辑项目
                </DropdownMenuItem>
                <DropdownMenuItem className="text-destructive">
                  <Archive className="w-4 h-4 mr-2" />
                  归档项目
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          <div className="flex items-center gap-2 mt-3">
            {getStatusBadge(project.status)}
            {getPriorityBadge(project.priority)}
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">进度</span>
              <div className="flex items-center gap-2">
                <HealthIcon className={`w-4 h-4 ${health.color}`} />
                <span className="font-medium">{project.progress}%</span>
              </div>
            </div>
            <Progress value={project.progress} className="h-2" />
          </div>

          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-muted-foreground" />
              <div>
                <div className="text-muted-foreground">开始时间</div>
                <div className="font-medium">{project.startDate}</div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <DollarSign className="w-4 h-4 text-muted-foreground" />
              <div>
                <div className="text-muted-foreground">预算</div>
                <div className="font-medium">{formatCurrency(project.budget)}</div>
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Users className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">{project.members.length + 1}人团队</span>
            </div>
            {manager && (
              <div className="flex items-center gap-2">
                <Avatar className="w-6 h-6">
                  <AvatarFallback className="text-xs">{manager.name.slice(0, 2)}</AvatarFallback>
                </Avatar>
                <span className="text-sm font-medium">{manager.name}</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-balance">项目管理</h1>
          <p className="text-muted-foreground mt-1">管理项目全生命周期和任务分配</p>
        </div>
        <Button className="gap-2">
          <Plus className="w-4 h-4" />
          新建项目
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                <Input
                  placeholder="搜索项目名称或描述..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-full sm:w-32">
                <SelectValue placeholder="状态" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">全部状态</SelectItem>
                <SelectItem value="planning">规划中</SelectItem>
                <SelectItem value="active">进行中</SelectItem>
                <SelectItem value="completed">已完成</SelectItem>
                <SelectItem value="on_hold">暂停</SelectItem>
              </SelectContent>
            </Select>
            <Select value={priorityFilter} onValueChange={setPriorityFilter}>
              <SelectTrigger className="w-full sm:w-32">
                <SelectValue placeholder="优先级" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">全部优先级</SelectItem>
                <SelectItem value="urgent">紧急</SelectItem>
                <SelectItem value="high">高</SelectItem>
                <SelectItem value="medium">中</SelectItem>
                <SelectItem value="low">低</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Results Summary */}
      <div className="flex items-center justify-between text-sm text-muted-foreground">
        <div>共找到 {filteredProjects.length} 个项目</div>
        <div className="flex gap-2">
          <Button variant={viewMode === "grid" ? "default" : "outline"} size="sm" onClick={() => setViewMode("grid")}>
            网格视图
          </Button>
          <Button variant={viewMode === "list" ? "default" : "outline"} size="sm" onClick={() => setViewMode("list")}>
            列表视图
          </Button>
        </div>
      </div>

      {/* Projects Grid */}
      <div className={viewMode === "grid" ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" : "space-y-4"}>
        {filteredProjects.map((project) => (
          <ProjectCard key={project.id} project={project} />
        ))}
      </div>

      {filteredProjects.length === 0 && (
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-4">
            <Search className="w-8 h-8 text-muted-foreground" />
          </div>
          <h3 className="text-lg font-medium mb-2">未找到匹配的项目</h3>
          <p className="text-muted-foreground">尝试调整搜索条件或创建新项目</p>
        </div>
      )}
    </div>
  )
}
