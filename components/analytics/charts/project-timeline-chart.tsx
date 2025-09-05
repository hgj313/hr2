"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Calendar, Clock } from "lucide-react"

// 模拟项目时间线数据
const mockTimelineData = [
  {
    id: "1",
    name: "企业官网重构",
    startDate: "2024-01-15",
    endDate: "2024-03-15",
    progress: 65,
    status: "进行中",
    team: ["张三", "李四", "王五"],
  },
  {
    id: "2",
    name: "移动应用开发",
    startDate: "2024-02-01",
    endDate: "2024-05-01",
    progress: 25,
    status: "计划中",
    team: ["赵六", "钱七"],
  },
  {
    id: "3",
    name: "数据分析平台",
    startDate: "2023-10-01",
    endDate: "2024-01-01",
    progress: 100,
    status: "已完成",
    team: ["孙八", "周九", "吴十"],
  },
  {
    id: "4",
    name: "客户关系管理系统",
    startDate: "2024-01-01",
    endDate: "2024-04-01",
    progress: 40,
    status: "暂停",
    team: ["郑十一"],
  },
]

export function ProjectTimelineChart() {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "进行中":
        return "bg-blue-100 text-blue-800"
      case "已完成":
        return "bg-green-100 text-green-800"
      case "计划中":
        return "bg-yellow-100 text-yellow-800"
      case "暂停":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const calculateDuration = (startDate: string, endDate: string) => {
    const start = new Date(startDate)
    const end = new Date(endDate)
    const diffTime = Math.abs(end.getTime() - start.getTime())
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    return Math.round(diffDays / 30) // 转换为月
  }

  return (
    <Card className="border-border/50">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Calendar className="w-5 h-5" />
          项目时间线
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {mockTimelineData.map((project) => (
            <div key={project.id} className="space-y-3 p-4 bg-muted/20 rounded-lg">
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <h4 className="font-medium">{project.name}</h4>
                  <div className="flex items-center gap-4 text-sm text-muted-foreground">
                    <div className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      <span>
                        {project.startDate} - {project.endDate}
                      </span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      <span>{calculateDuration(project.startDate, project.endDate)} 个月</span>
                    </div>
                  </div>
                </div>
                <Badge className={getStatusColor(project.status)}>{project.status}</Badge>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span>进度</span>
                  <span className="font-medium">{project.progress}%</span>
                </div>
                <div className="w-full bg-muted rounded-full h-2">
                  <div
                    className="bg-primary h-2 rounded-full transition-all"
                    style={{ width: `${project.progress}%` }}
                  />
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="text-sm text-muted-foreground">团队: {project.team.join(", ")}</div>
                <div className="text-sm text-muted-foreground">{project.team.length} 人</div>
              </div>
            </div>
          ))}

          {/* 时间线统计 */}
          <div className="pt-4 border-t border-border/50">
            <div className="grid grid-cols-4 gap-4 text-center">
              <div>
                <div className="text-lg font-bold text-blue-600">
                  {mockTimelineData.filter((p) => p.status === "进行中").length}
                </div>
                <p className="text-xs text-muted-foreground">进行中</p>
              </div>
              <div>
                <div className="text-lg font-bold text-green-600">
                  {mockTimelineData.filter((p) => p.status === "已完成").length}
                </div>
                <p className="text-xs text-muted-foreground">已完成</p>
              </div>
              <div>
                <div className="text-lg font-bold text-yellow-600">
                  {mockTimelineData.filter((p) => p.status === "计划中").length}
                </div>
                <p className="text-xs text-muted-foreground">计划中</p>
              </div>
              <div>
                <div className="text-lg font-bold text-red-600">
                  {mockTimelineData.filter((p) => p.status === "暂停").length}
                </div>
                <p className="text-xs text-muted-foreground">暂停</p>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
