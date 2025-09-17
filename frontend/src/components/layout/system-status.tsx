"use client"

import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"
import { CheckCircle, Clock, Users, FolderKanban } from "lucide-react"

export function SystemStatus() {
  const systemStats = {
    totalUsers: 183,
    activeProjects: 24,
    schedulingTasks: 156,
    systemHealth: "正常",
  }

  return (
    <Card className="mb-6">
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <span className="text-sm font-medium">系统状态</span>
              <Badge variant="default" className="bg-green-100 text-green-800">
                {systemStats.systemHealth}
              </Badge>
            </div>
          </div>
          <div className="flex items-center gap-6 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <Users className="w-4 h-4" />
              <span>{systemStats.totalUsers} 用户</span>
            </div>
            <div className="flex items-center gap-1">
              <FolderKanban className="w-4 h-4" />
              <span>{systemStats.activeProjects} 项目</span>
            </div>
            <div className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              <span>{systemStats.schedulingTasks} 调度任务</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
