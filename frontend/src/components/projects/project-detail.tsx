"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import {
  ArrowLeft,
  Users,
  DollarSign,
  Edit,
  MoreHorizontal,
  Plus,
  Clock,
  CheckCircle,
  AlertCircle,
  Circle,
  Target,
  TrendingUp,
  FileText,
} from "lucide-react"
import type { Project } from "@/lib/mock-data"
import { getUserById, getTasksByProject } from "@/lib/mock-data"
import { GanttChart } from "@/components/projects/gantt-chart"

interface ProjectDetailProps {
  project: Project
  onBack: () => void
  onEdit: (project: Project) => void
}

export function ProjectDetail({ project, onBack, onEdit }: ProjectDetailProps) {
  const [activeTab, setActiveTab] = useState("overview")
  const manager = getUserById(project.manager)
  const projectTasks = getTasksByProject(project.id)

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

  const getTaskStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle className="w-4 h-4 text-green-600" />
      case "in_progress":
        return <Clock className="w-4 h-4 text-blue-600" />
      case "review":
        return <AlertCircle className="w-4 h-4 text-yellow-600" />
      default:
        return <Circle className="w-4 h-4 text-gray-400" />
    }
  }

  const getTaskStatusLabel = (status: string) => {
    const labels = {
      todo: "待开始",
      in_progress: "进行中",
      review: "待审核",
      completed: "已完成",
    }
    return labels[status as keyof typeof labels] || status
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("zh-CN", {
      style: "currency",
      currency: "CNY",
      minimumFractionDigits: 0,
    }).format(amount)
  }

  const completedTasks = projectTasks.filter((task) => task.status === "completed").length
  const totalTasks = projectTasks.length
  const taskCompletionRate = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={onBack} className="gap-2">
            <ArrowLeft className="w-4 h-4" />
            返回列表
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-balance">{project.name}</h1>
            <p className="text-muted-foreground mt-1">{project.description}</p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => onEdit(project)} className="gap-2">
            <Edit className="w-4 h-4" />
            编辑项目
          </Button>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm">
                <MoreHorizontal className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem>
                <FileText className="w-4 h-4 mr-2" />
                导出报告
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Target className="w-4 h-4 mr-2" />
                设置里程碑
              </DropdownMenuItem>
              <DropdownMenuItem className="text-destructive">
                <AlertCircle className="w-4 h-4 mr-2" />
                归档项目
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      {/* Project Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-primary" />
              </div>
              <div>
                <div className="text-2xl font-bold">{project.progress}%</div>
                <div className="text-sm text-muted-foreground">项目进度</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <CheckCircle className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">
                  {completedTasks}/{totalTasks}
                </div>
                <div className="text-sm text-muted-foreground">任务完成</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <Users className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">{project.members.length + 1}</div>
                <div className="text-sm text-muted-foreground">团队成员</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                <DollarSign className="w-5 h-5 text-yellow-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">{formatCurrency(project.budget)}</div>
                <div className="text-sm text-muted-foreground">项目预算</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Project Details Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">项目概览</TabsTrigger>
          <TabsTrigger value="tasks">任务管理</TabsTrigger>
          <TabsTrigger value="timeline">时间线</TabsTrigger>
          <TabsTrigger value="team">团队成员</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>项目信息</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="text-sm text-muted-foreground">项目状态</div>
                      <div className="mt-1">{getStatusBadge(project.status)}</div>
                    </div>
                    <div>
                      <div className="text-sm text-muted-foreground">优先级</div>
                      <div className="mt-1">{getPriorityBadge(project.priority)}</div>
                    </div>
                    <div>
                      <div className="text-sm text-muted-foreground">开始时间</div>
                      <div className="mt-1 font-medium">{project.startDate}</div>
                    </div>
                    <div>
                      <div className="text-sm text-muted-foreground">结束时间</div>
                      <div className="mt-1 font-medium">{project.endDate}</div>
                    </div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground mb-2">项目进度</div>
                    <Progress value={project.progress} className="h-3" />
                    <div className="flex justify-between text-sm text-muted-foreground mt-1">
                      <span>0%</span>
                      <span>{project.progress}%</span>
                      <span>100%</span>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>所需技能</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {project.requiredSkills.map((skill, index) => (
                      <Badge key={index} variant="secondary">
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>项目经理</CardTitle>
                </CardHeader>
                <CardContent>
                  {manager && (
                    <div className="flex items-center gap-3">
                      <Avatar className="w-12 h-12">
                        <AvatarFallback>{manager.name.slice(0, 2)}</AvatarFallback>
                      </Avatar>
                      <div>
                        <div className="font-medium">{manager.name}</div>
                        <div className="text-sm text-muted-foreground">{manager.position}</div>
                        <div className="text-sm text-muted-foreground">{manager.email}</div>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>快速统计</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">任务完成率</span>
                    <span className="font-medium">{taskCompletionRate}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">预算使用</span>
                    <span className="font-medium">65%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">剩余天数</span>
                    <span className="font-medium">45天</span>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="tasks" className="space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">项目任务</h3>
            <Button className="gap-2">
              <Plus className="w-4 h-4" />
              新建任务
            </Button>
          </div>
          <Card>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>任务名称</TableHead>
                  <TableHead>负责人</TableHead>
                  <TableHead>状态</TableHead>
                  <TableHead>优先级</TableHead>
                  <TableHead>进度</TableHead>
                  <TableHead>截止时间</TableHead>
                  <TableHead className="text-right">操作</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {projectTasks.map((task) => {
                  const assignee = getUserById(task.assignee)
                  const progress =
                    task.status === "completed"
                      ? 100
                      : task.status === "in_progress"
                        ? Math.round((task.actualHours / task.estimatedHours) * 100)
                        : 0

                  return (
                    <TableRow key={task.id}>
                      <TableCell>
                        <div>
                          <div className="font-medium">{task.name}</div>
                          <div className="text-sm text-muted-foreground">{task.description}</div>
                        </div>
                      </TableCell>
                      <TableCell>
                        {assignee && (
                          <div className="flex items-center gap-2">
                            <Avatar className="w-6 h-6">
                              <AvatarFallback className="text-xs">{assignee.name.slice(0, 2)}</AvatarFallback>
                            </Avatar>
                            <span className="text-sm">{assignee.name}</span>
                          </div>
                        )}
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          {getTaskStatusIcon(task.status)}
                          <span className="text-sm">{getTaskStatusLabel(task.status)}</span>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge
                          variant={
                            task.priority === "high"
                              ? "destructive"
                              : task.priority === "medium"
                                ? "default"
                                : "outline"
                          }
                        >
                          {task.priority === "high" ? "高" : task.priority === "medium" ? "中" : "低"}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Progress value={progress} className="w-16 h-2" />
                          <span className="text-sm text-muted-foreground">{progress}%</span>
                        </div>
                      </TableCell>
                      <TableCell>{task.endDate}</TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm">
                              <MoreHorizontal className="w-4 h-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem>编辑任务</DropdownMenuItem>
                            <DropdownMenuItem>查看详情</DropdownMenuItem>
                            <DropdownMenuItem className="text-destructive">删除任务</DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  )
                })}
              </TableBody>
            </Table>
          </Card>
        </TabsContent>

        <TabsContent value="timeline" className="space-y-6">
          <GanttChart projectId={project.id} />
        </TabsContent>

        <TabsContent value="team" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Project Manager */}
            {manager && (
              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center gap-3">
                    <Avatar className="w-12 h-12">
                      <AvatarFallback>{manager.name.slice(0, 2)}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <div className="font-medium">{manager.name}</div>
                      <div className="text-sm text-muted-foreground">{manager.position}</div>
                      <Badge variant="destructive" className="text-xs mt-1">
                        项目经理
                      </Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Team Members */}
            {project.members.map((memberId) => {
              const member = getUserById(memberId)
              if (!member) return null

              return (
                <Card key={memberId}>
                  <CardContent className="pt-6">
                    <div className="flex items-center gap-3">
                      <Avatar className="w-12 h-12">
                        <AvatarFallback>{member.name.slice(0, 2)}</AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <div className="font-medium">{member.name}</div>
                        <div className="text-sm text-muted-foreground">{member.position}</div>
                        <Badge variant="outline" className="text-xs mt-1">
                          团队成员
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
