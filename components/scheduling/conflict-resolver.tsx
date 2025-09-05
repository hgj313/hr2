"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { AlertTriangle, CheckCircle, Clock, Users, Lightbulb } from "lucide-react"

interface Conflict {
  id: string
  type: string
  description: string
  severity: string
  affectedProjects: string[]
  suggestions: string[]
}

interface ConflictResolverProps {
  conflicts: Conflict[]
  onResolve: (data: any) => void
}

export function ConflictResolver({ conflicts, onResolve }: ConflictResolverProps) {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "高":
        return "bg-red-100 text-red-800 border-red-200"
      case "中":
        return "bg-yellow-100 text-yellow-800 border-yellow-200"
      case "低":
        return "bg-green-100 text-green-800 border-green-200"
      default:
        return "bg-gray-100 text-gray-800 border-gray-200"
    }
  }

  const getConflictIcon = (type: string) => {
    switch (type) {
      case "时间冲突":
        return <Clock className="w-4 h-4" />
      case "技能不匹配":
        return <Users className="w-4 h-4" />
      default:
        return <AlertTriangle className="w-4 h-4" />
    }
  }

  const handleResolveConflict = (conflictId: string, suggestionIndex: number) => {
    console.log("[v0] 解决冲突:", conflictId, "使用建议:", suggestionIndex)

    // 这里会调用相应的解决方案
    const conflict = conflicts.find((c) => c.id === conflictId)
    if (conflict) {
      alert(`正在应用解决方案: ${conflict.suggestions[suggestionIndex]}`)

      // 模拟解决冲突后更新数据
      onResolve((prevData: any) => ({
        ...prevData,
        conflicts: prevData.conflicts.filter((c: any) => c.id !== conflictId),
      }))
    }
  }

  const handleIgnoreConflict = (conflictId: string) => {
    console.log("[v0] 忽略冲突:", conflictId)

    onResolve((prevData: any) => ({
      ...prevData,
      conflicts: prevData.conflicts.filter((c: any) => c.id !== conflictId),
    }))
  }

  if (conflicts.length === 0) {
    return (
      <Card className="border-border/50">
        <CardContent className="pt-6">
          <div className="text-center space-y-4">
            <CheckCircle className="w-12 h-12 text-green-500 mx-auto" />
            <div>
              <h3 className="text-lg font-semibold text-foreground">没有检测到冲突</h3>
              <p className="text-muted-foreground">当前的人员分配方案运行良好</p>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      <div className="space-y-1">
        <h3 className="text-lg font-semibold">冲突解决中心</h3>
        <p className="text-sm text-muted-foreground">检测到 {conflicts.length} 个调度冲突，请选择合适的解决方案</p>
      </div>

      <div className="space-y-4">
        {conflicts.map((conflict) => (
          <Card key={conflict.id} className="border-border/50">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-3">
                  <div className="flex items-center justify-center w-10 h-10 bg-muted rounded-lg">
                    {getConflictIcon(conflict.type)}
                  </div>
                  <div>
                    <CardTitle className="text-base">{conflict.type}</CardTitle>
                    <p className="text-sm text-muted-foreground">{conflict.description}</p>
                  </div>
                </div>
                <Badge className={getSeverityColor(conflict.severity)} variant="outline">
                  {conflict.severity}优先级
                </Badge>
              </div>
            </CardHeader>

            <CardContent className="space-y-4">
              <div>
                <h5 className="text-sm font-medium mb-2">影响的项目</h5>
                <div className="flex flex-wrap gap-2">
                  {conflict.affectedProjects.map((project) => (
                    <Badge key={project} variant="secondary">
                      {project}
                    </Badge>
                  ))}
                </div>
              </div>

              <Alert>
                <Lightbulb className="h-4 w-4" />
                <AlertDescription>
                  <div className="space-y-3">
                    <p className="font-medium">建议的解决方案:</p>
                    <div className="space-y-2">
                      {conflict.suggestions.map((suggestion, index) => (
                        <div key={index} className="flex items-center justify-between p-2 bg-muted/50 rounded-md">
                          <span className="text-sm">{suggestion}</span>
                          <Button
                            size="sm"
                            onClick={() => handleResolveConflict(conflict.id, index)}
                            className="bg-primary hover:bg-primary/90"
                          >
                            应用
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                </AlertDescription>
              </Alert>

              <div className="flex justify-end space-x-2">
                <Button variant="outline" size="sm" onClick={() => handleIgnoreConflict(conflict.id)}>
                  暂时忽略
                </Button>
                <Button
                  size="sm"
                  onClick={() => handleResolveConflict(conflict.id, 0)}
                  className="bg-primary hover:bg-primary/90"
                >
                  自动解决
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="border-border/50 bg-muted/20">
        <CardContent className="pt-6">
          <div className="space-y-2">
            <h4 className="text-sm font-medium">冲突预防建议</h4>
            <div className="text-xs text-muted-foreground space-y-1">
              <p>• 定期检查人员工作负载，避免过度分配</p>
              <p>• 在项目开始前确认所需技能和人员可用性</p>
              <p>• 使用AI智能调度功能获得最优分配建议</p>
              <p>• 为项目预留适当的缓冲时间</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
