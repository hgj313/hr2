"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { getTasksByProject, getUserById } from "@/lib/mock-data"

interface GanttChartProps {
  projectId: string
}

export function GanttChart({ projectId }: GanttChartProps) {
  const tasks = getTasksByProject(projectId)

  // Calculate date range for the chart
  const allDates = tasks.flatMap((task) => [new Date(task.startDate), new Date(task.endDate)])
  const minDate = new Date(Math.min(...allDates.map((d) => d.getTime())))
  const maxDate = new Date(Math.max(...allDates.map((d) => d.getTime())))

  // Generate month headers
  const months: Date[] = []
  const current = new Date(minDate.getFullYear(), minDate.getMonth(), 1)
  while (current <= maxDate) {
    months.push(new Date(current))
    current.setMonth(current.getMonth() + 1)
  }

  const getDaysBetween = (start: Date, end: Date) => {
    return Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24))
  }

  const getTaskPosition = (taskStart: Date, taskEnd: Date) => {
    const totalDays = getDaysBetween(minDate, maxDate)
    const startOffset = getDaysBetween(minDate, taskStart)
    const duration = getDaysBetween(taskStart, taskEnd)

    return {
      left: `${(startOffset / totalDays) * 100}%`,
      width: `${(duration / totalDays) * 100}%`,
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "bg-green-500"
      case "in_progress":
        return "bg-blue-500"
      case "review":
        return "bg-yellow-500"
      default:
        return "bg-gray-300"
    }
  }

  const getStatusLabel = (status: string) => {
    const labels = {
      todo: "待开始",
      in_progress: "进行中",
      review: "待审核",
      completed: "已完成",
    }
    return labels[status as keyof typeof labels] || status
  }

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold">项目时间线</h3>
        <p className="text-sm text-muted-foreground">甘特图显示项目任务的时间安排和进度</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>甘特图</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Timeline Header */}
            <div className="relative">
              <div className="flex border-b pb-2 mb-4">
                <div className="w-64 font-medium text-sm">任务名称</div>
                <div className="flex-1 relative">
                  <div className="flex">
                    {months.map((month, index) => (
                      <div key={index} className="flex-1 text-center text-sm font-medium text-muted-foreground">
                        {month.toLocaleDateString("zh-CN", { year: "numeric", month: "short" })}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Tasks */}
            <div className="space-y-3">
              {tasks.map((task) => {
                const assignee = getUserById(task.assignee)
                const position = getTaskPosition(new Date(task.startDate), new Date(task.endDate))

                return (
                  <div key={task.id} className="flex items-center">
                    <div className="w-64 pr-4">
                      <div className="font-medium text-sm">{task.name}</div>
                      <div className="text-xs text-muted-foreground">
                        {assignee?.name} • {task.startDate} - {task.endDate}
                      </div>
                    </div>
                    <div className="flex-1 relative h-8 bg-muted/30 rounded">
                      <div
                        className={`absolute top-1 bottom-1 rounded ${getStatusColor(task.status)} flex items-center justify-center`}
                        style={position}
                      >
                        <Badge variant="secondary" className="text-xs">
                          {getStatusLabel(task.status)}
                        </Badge>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>

            {/* Legend */}
            <div className="flex items-center gap-6 pt-4 border-t">
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-gray-300 rounded"></div>
                <span className="text-sm">待开始</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-blue-500 rounded"></div>
                <span className="text-sm">进行中</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-yellow-500 rounded"></div>
                <span className="text-sm">待审核</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-green-500 rounded"></div>
                <span className="text-sm">已完成</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
