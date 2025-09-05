"use client"

import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import {
  AlertTriangle,
  Clock,
  Users,
  Wrench,
  CheckCircle,
  XCircle,
  Loader2,
} from "lucide-react"
import { useUpdateSchedule } from "@/lib/api/schedules"
import { useToast } from "@/hooks/use-toast"
import { Schedule, ScheduleConflict } from "./scheduling-management"

interface ConflictResolutionDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  schedule: Schedule | null
}

// 冲突类型图标映射
const conflictIcons = {
  resource: Users,
  time: Clock,
  skill: Wrench,
}

// 冲突类型标签映射
const conflictTypeLabels = {
  resource: "资源冲突",
  time: "时间冲突",
  skill: "技能冲突",
}

// 冲突严重程度标签映射
const severityLabels = {
  low: "低",
  medium: "中",
  high: "高",
}

// 获取严重程度徽章样式
const getSeverityBadgeVariant = (severity: "low" | "medium" | "high") => {
  switch (severity) {
    case "low":
      return "secondary"
    case "medium":
      return "outline"
    case "high":
      return "destructive"
    default:
      return "secondary"
  }
}

export function ConflictResolutionDialog({ open, onOpenChange, schedule }: ConflictResolutionDialogProps) {
  const [resolvingConflicts, setResolvingConflicts] = useState<string[]>([])
  const [resolvedConflicts, setResolvedConflicts] = useState<string[]>([])
  const { toast } = useToast()
  const updateScheduleMutation = useUpdateSchedule()

  if (!schedule || !schedule.conflicts || schedule.conflicts.length === 0) {
    return null
  }

  const handleResolveConflict = async (conflict: ScheduleConflict) => {
    setResolvingConflicts(prev => [...prev, conflict.id])
    
    try {
      // 模拟解决冲突的API调用
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // 更新已解决的冲突列表
      setResolvedConflicts(prev => [...prev, conflict.id])
      
      toast({
        title: "冲突已解决",
        description: `${conflictTypeLabels[conflict.type]}已成功解决`,
      })
    } catch (error) {
      toast({
        title: "解决失败",
        description: "解决冲突时发生错误，请重试",
        variant: "destructive",
      })
    } finally {
      setResolvingConflicts(prev => prev.filter(id => id !== conflict.id))
    }
  }

  const handleResolveAllConflicts = async () => {
    const unresolvedConflicts = schedule.conflicts!.filter(
      conflict => !resolvedConflicts.includes(conflict.id)
    )
    
    setResolvingConflicts(unresolvedConflicts.map(c => c.id))
    
    try {
      // 模拟批量解决冲突的API调用
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // 更新调度状态，移除所有冲突
      await updateScheduleMutation.mutateAsync({
        id: schedule.id,
        data: {
          conflicts: [],
        },
      })
      
      setResolvedConflicts(prev => [...prev, ...unresolvedConflicts.map(c => c.id)])
      
      toast({
        title: "所有冲突已解决",
        description: "调度任务的所有冲突都已成功解决",
      })
      
      // 延迟关闭对话框
      setTimeout(() => {
        onOpenChange(false)
        setResolvedConflicts([])
      }, 1000)
    } catch (error) {
      toast({
        title: "批量解决失败",
        description: "批量解决冲突时发生错误，请重试",
        variant: "destructive",
      })
    } finally {
      setResolvingConflicts([])
    }
  }

  const unresolvedConflicts = schedule.conflicts.filter(
    conflict => !resolvedConflicts.includes(conflict.id)
  )

  const allResolved = unresolvedConflicts.length === 0

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-destructive" />
            冲突解决 - {schedule.name}
          </DialogTitle>
          <DialogDescription>
            解决调度任务中的资源、时间和技能冲突，确保任务能够顺利执行。
          </DialogDescription>
        </DialogHeader>
        
        <div className="space-y-4">
          {/* 冲突概览 */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">冲突概览</CardTitle>
              <CardDescription>
                当前调度任务存在 {schedule.conflicts.length} 个冲突，其中 {resolvedConflicts.length} 个已解决。
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-destructive rounded-full"></div>
                  <span className="text-sm">未解决: {unresolvedConflicts.length}</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="text-sm">已解决: {resolvedConflicts.length}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* 冲突列表 */}
          <div className="space-y-3">
            {schedule.conflicts.map((conflict, index) => {
              const Icon = conflictIcons[conflict.type]
              const isResolving = resolvingConflicts.includes(conflict.id)
              const isResolved = resolvedConflicts.includes(conflict.id)
              
              return (
                <Card key={conflict.id} className={isResolved ? "bg-green-50 border-green-200" : ""}>
                  <CardContent className="pt-4">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start gap-3 flex-1">
                        <div className={`p-2 rounded-lg ${
                          isResolved ? "bg-green-100" : "bg-destructive/10"
                        }`}>
                          {isResolved ? (
                            <CheckCircle className="h-4 w-4 text-green-600" />
                          ) : (
                            <Icon className="h-4 w-4 text-destructive" />
                          )}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <h4 className="font-medium">
                              {conflictTypeLabels[conflict.type]}
                            </h4>
                            <Badge variant={getSeverityBadgeVariant(conflict.severity)}>
                              {severityLabels[conflict.severity]}
                            </Badge>
                            {isResolved && (
                              <Badge variant="outline" className="text-green-600 border-green-600">
                                已解决
                              </Badge>
                            )}
                          </div>
                          <p className="text-sm text-muted-foreground mb-3">
                            {conflict.description}
                          </p>
                          {conflict.affected_users.length > 0 && (
                            <div className="mb-3">
                              <p className="text-xs text-muted-foreground mb-1">影响人员:</p>
                              <div className="flex flex-wrap gap-1">
                                {conflict.affected_users.map((userId, userIndex) => (
                                  <Badge key={userIndex} variant="outline" className="text-xs">
                                    用户 {userId}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          )}
                          {conflict.suggested_resolution && (
                            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                              <p className="text-xs font-medium text-blue-800 mb-1">建议解决方案:</p>
                              <p className="text-xs text-blue-700">
                                {conflict.suggested_resolution}
                              </p>
                            </div>
                          )}
                        </div>
                      </div>
                      <div className="ml-4">
                        {!isResolved && (
                          <Button
                            size="sm"
                            onClick={() => handleResolveConflict(conflict)}
                            disabled={isResolving}
                          >
                            {isResolving ? (
                              <>
                                <Loader2 className="mr-2 h-3 w-3 animate-spin" />
                                解决中...
                              </>
                            ) : (
                              "解决冲突"
                            )}
                          </Button>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>

          {/* 批量操作 */}
          {!allResolved && (
            <>
              <Separator />
              <Card>
                <CardContent className="pt-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium mb-1">批量解决</h4>
                      <p className="text-sm text-muted-foreground">
                        一键解决所有未解决的冲突
                      </p>
                    </div>
                    <Button
                      onClick={handleResolveAllConflicts}
                      disabled={resolvingConflicts.length > 0}
                      className="bg-green-600 hover:bg-green-700"
                    >
                      {resolvingConflicts.length > 0 ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          解决中...
                        </>
                      ) : (
                        <>
                          <CheckCircle className="mr-2 h-4 w-4" />
                          解决所有冲突
                        </>
                      )}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </>
          )}

          {/* 全部解决提示 */}
          {allResolved && (
            <Card className="bg-green-50 border-green-200">
              <CardContent className="pt-4">
                <div className="flex items-center gap-3">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <div>
                    <h4 className="font-medium text-green-800">所有冲突已解决</h4>
                    <p className="text-sm text-green-700">
                      调度任务的所有冲突都已成功解决，可以正常执行。
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        <DialogFooter>
          <Button
            variant="outline"
            onClick={() => {
              onOpenChange(false)
              setResolvedConflicts([])
            }}
          >
            {allResolved ? "完成" : "稍后处理"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}