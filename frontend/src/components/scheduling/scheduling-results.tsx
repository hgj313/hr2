"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Alert, AlertDescription } from "@/components/ui/alert"
import {
  ArrowLeft,
  CheckCircle,
  AlertTriangle,
  Clock,
  TrendingUp,
  DollarSign,
  Users,
  RefreshCw,
  Download,
  Calendar,
} from "lucide-react"
import type { SchedulingResult, SchedulingConfig } from "@/lib/mock-data"
import { getUserById, mockProjects, getSchedulingAssignments, getSchedulingConflicts } from "@/lib/mock-data"

interface SchedulingResultsProps {
  result: SchedulingResult
  config: SchedulingConfig
  onBack: () => void
  onRerun: () => void
  onConfirm: () => void
}

export function SchedulingResults({ result, config, onBack, onRerun, onConfirm }: SchedulingResultsProps) {
  const [activeTab, setActiveTab] = useState("overview")
  const assignments = getSchedulingAssignments(result.id)
  const conflicts = getSchedulingConflicts(result.id)

  const getStatusBadge = (status: SchedulingResult["status"]) => {
    const variants = {
      running: "outline",
      completed: "default",
      failed: "destructive",
    } as const

    const labels = {
      running: "运行中",
      completed: "已完成",
      failed: "失败",
    }

    const icons = {
      running: Clock,
      completed: CheckCircle,
      failed: AlertTriangle,
    }

    const Icon = icons[status]

    return (
      <Badge variant={variants[status]} className="gap-1">
        <Icon className="w-3 h-3" />
        {labels[status]}
      </Badge>
    )
  }

  const getConflictSeverityBadge = (severity: "low" | "medium" | "high") => {
    const variants = {
      low: "outline",
      medium: "secondary",
      high: "destructive",
    } as const

    const labels = {
      low: "低",
      medium: "中",
      high: "高",
    }

    return (
      <Badge variant={variants[severity]} className="text-xs">
        {labels[severity]}
      </Badge>
    )
  }

  const getConflictTypeLabel = (type: string) => {
    const labels = {
      time_overlap: "时间冲突",
      skill_mismatch: "技能不匹配",
      overload: "工作过载",
      unavailable: "不可用",
    }
    return labels[type as keyof typeof labels] || type
  }

  const formatDuration = (startTime: string, endTime?: string) => {
    if (!endTime) return "运行中..."
    const start = new Date(startTime)
    const end = new Date(endTime)
    const duration = Math.round((end.getTime() - start.getTime()) / 1000)
    return `${duration}秒`
  }

  const getScoreColor = (score: number) => {
    if (score >= 90) return "text-green-600"
    if (score >= 70) return "text-blue-600"
    if (score >= 50) return "text-yellow-600"
    return "text-red-600"
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={onBack} className="gap-2">
            <ArrowLeft className="w-4 h-4" />
            返回配置
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-balance">调度结果</h1>
            <p className="text-muted-foreground mt-1">{config.name}</p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={onRerun} className="gap-2 bg-transparent">
            <RefreshCw className="w-4 h-4" />
            重新调度
          </Button>
          {result.status === "completed" && (
            <Button onClick={onConfirm} className="gap-2">
              <CheckCircle className="w-4 h-4" />
              确认方案
            </Button>
          )}
        </div>
      </div>

      {/* Status and Progress */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="text-lg font-semibold">调度状态</div>
              {getStatusBadge(result.status)}
            </div>
            <div className="text-sm text-muted-foreground">
              执行时间: {formatDuration(result.startTime, result.endTime)}
            </div>
          </div>
          {result.status === "running" && (
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>进度</span>
                <span>{result.progress}%</span>
              </div>
              <Progress value={result.progress} className="h-2" />
            </div>
          )}
        </CardContent>
      </Card>

      {result.status === "completed" && (
        <>
          {/* Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                    <TrendingUp className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <div className={`text-2xl font-bold ${getScoreColor(result.metrics.efficiencyScore)}`}>
                      {result.metrics.efficiencyScore}
                    </div>
                    <div className="text-sm text-muted-foreground">效率评分</div>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                    <DollarSign className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <div className={`text-2xl font-bold ${getScoreColor(result.metrics.costScore)}`}>
                      {result.metrics.costScore}
                    </div>
                    <div className="text-sm text-muted-foreground">成本评分</div>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                    <Users className="w-5 h-5 text-yellow-600" />
                  </div>
                  <div>
                    <div className={`text-2xl font-bold ${getScoreColor(result.metrics.satisfactionScore)}`}>
                      {result.metrics.satisfactionScore}
                    </div>
                    <div className="text-sm text-muted-foreground">满意度</div>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                    <AlertTriangle className="w-5 h-5 text-red-600" />
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-red-600">{result.metrics.conflictCount}</div>
                    <div className="text-sm text-muted-foreground">冲突数量</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Results Tabs */}
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="overview">调度概览</TabsTrigger>
              <TabsTrigger value="assignments">人员分配</TabsTrigger>
              <TabsTrigger value="conflicts">冲突分析</TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>调度配置</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <div className="text-muted-foreground">调度周期</div>
                        <div className="font-medium">
                          {config.startDate} 至 {config.endDate}
                        </div>
                      </div>
                      <div>
                        <div className="text-muted-foreground">项目数量</div>
                        <div className="font-medium">{config.projectIds.length}个</div>
                      </div>
                      <div>
                        <div className="text-muted-foreground">最大负载</div>
                        <div className="font-medium">{config.maxWorkloadPercentage}%</div>
                      </div>
                      <div>
                        <div className="text-muted-foreground">团队规模</div>
                        <div className="font-medium">{config.preferredTeamSize}人</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>优化目标</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-wrap gap-2">
                      {config.objectives.efficiency && <Badge variant="secondary">效率优先</Badge>}
                      {config.objectives.costControl && <Badge variant="secondary">成本控制</Badge>}
                      {config.objectives.loadBalancing && <Badge variant="secondary">负载均衡</Badge>}
                      {config.objectives.skillMatching && <Badge variant="secondary">技能匹配</Badge>}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="assignments" className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">人员分配结果</h3>
                <Button variant="outline" className="gap-2 bg-transparent">
                  <Download className="w-4 h-4" />
                  导出分配表
                </Button>
              </div>
              <Card>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>员工</TableHead>
                      <TableHead>项目</TableHead>
                      <TableHead>日期</TableHead>
                      <TableHead>时间</TableHead>
                      <TableHead>工作量</TableHead>
                      <TableHead>置信度</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {assignments.map((assignment) => {
                      const user = getUserById(assignment.userId)
                      const project = mockProjects.find((p) => p.id === assignment.projectId)

                      return (
                        <TableRow key={assignment.id}>
                          <TableCell>
                            {user && (
                              <div className="flex items-center gap-2">
                                <Avatar className="w-6 h-6">
                                  <AvatarFallback className="text-xs">{user.name.slice(0, 2)}</AvatarFallback>
                                </Avatar>
                                <span className="font-medium">{user.name}</span>
                              </div>
                            )}
                          </TableCell>
                          <TableCell>
                            {project && (
                              <div>
                                <div className="font-medium">{project.name}</div>
                                <div className="text-sm text-muted-foreground">
                                  {assignment.taskId ? `任务 #${assignment.taskId}` : "项目总体"}
                                </div>
                              </div>
                            )}
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-1">
                              <Calendar className="w-4 h-4 text-muted-foreground" />
                              {assignment.date}
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-1">
                              <Clock className="w-4 h-4 text-muted-foreground" />
                              {assignment.startTime} - {assignment.endTime}
                            </div>
                          </TableCell>
                          <TableCell>
                            <Badge variant="outline">{assignment.workload}小时</Badge>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-2">
                              <Progress value={assignment.confidence} className="w-16 h-2" />
                              <span className="text-sm text-muted-foreground">{assignment.confidence}%</span>
                            </div>
                          </TableCell>
                        </TableRow>
                      )
                    })}
                  </TableBody>
                </Table>
              </Card>
            </TabsContent>

            <TabsContent value="conflicts" className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">冲突分析</h3>
                <div className="text-sm text-muted-foreground">发现 {conflicts.length} 个潜在冲突</div>
              </div>

              {conflicts.length > 0 ? (
                <div className="space-y-4">
                  {conflicts.map((conflict) => (
                    <Alert key={conflict.id}>
                      <AlertTriangle className="h-4 w-4" />
                      <AlertDescription>
                        <div className="space-y-3">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <span className="font-medium">{getConflictTypeLabel(conflict.type)}</span>
                              {getConflictSeverityBadge(conflict.severity)}
                            </div>
                          </div>
                          <p className="text-sm">{conflict.description}</p>
                          <div className="space-y-2">
                            <div className="text-sm">
                              <span className="font-medium">影响人员: </span>
                              {conflict.affectedUsers
                                .map((userId) => {
                                  const user = getUserById(userId)
                                  return user?.name
                                })
                                .join(", ")}
                            </div>
                            <div className="text-sm">
                              <span className="font-medium">建议解决方案: </span>
                              <ul className="list-disc list-inside mt-1">
                                {conflict.suggestions.map((suggestion, index) => (
                                  <li key={index}>{suggestion}</li>
                                ))}
                              </ul>
                            </div>
                          </div>
                        </div>
                      </AlertDescription>
                    </Alert>
                  ))}
                </div>
              ) : (
                <Card>
                  <CardContent className="pt-6">
                    <div className="text-center py-8">
                      <CheckCircle className="w-12 h-12 text-green-600 mx-auto mb-4" />
                      <h3 className="text-lg font-medium mb-2">无冲突检测</h3>
                      <p className="text-muted-foreground">调度方案未发现任何冲突，可以直接执行</p>
                    </div>
                  </CardContent>
                </Card>
              )}
            </TabsContent>
          </Tabs>
        </>
      )}
    </div>
  )
}
