"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { TrendingUp, TrendingDown, Minus, Users, FolderKanban, Clock, Target } from "lucide-react"

interface RealTimeMetricsProps {
  data: {
    totalProjects: number
    activeProjects: number
    completedProjects: number
    totalEmployees: number
    averageUtilization: number
    onTimeDelivery: number
  }
}

export function RealTimeMetrics({ data }: RealTimeMetricsProps) {
  const metrics = [
    {
      title: "活跃项目",
      value: data.activeProjects,
      total: data.totalProjects,
      change: "+2",
      trend: "up",
      icon: FolderKanban,
      color: "text-blue-600",
    },
    {
      title: "团队人员",
      value: data.totalEmployees,
      change: "+3",
      trend: "up",
      icon: Users,
      color: "text-green-600",
    },
    {
      title: "资源利用率",
      value: `${data.averageUtilization}%`,
      change: "+5%",
      trend: "up",
      icon: Target,
      color: "text-orange-600",
    },
    {
      title: "按时交付率",
      value: `${data.onTimeDelivery}%`,
      change: "-2%",
      trend: "down",
      icon: Clock,
      color: "text-purple-600",
    },
  ]

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "up":
        return <TrendingUp className="w-3 h-3 text-green-600" />
      case "down":
        return <TrendingDown className="w-3 h-3 text-red-600" />
      default:
        return <Minus className="w-3 h-3 text-gray-600" />
    }
  }

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case "up":
        return "text-green-600"
      case "down":
        return "text-red-600"
      default:
        return "text-gray-600"
    }
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {metrics.map((metric) => (
        <Card key={metric.title} className="border-border/50 relative overflow-hidden">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center justify-between">
              <span>{metric.title}</span>
              <metric.icon className={`w-4 h-4 ${metric.color}`} />
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-baseline justify-between">
                <div className="text-2xl font-bold text-foreground">
                  {metric.value}
                  {metric.total && <span className="text-sm text-muted-foreground ml-1">/ {metric.total}</span>}
                </div>
                <div className={`flex items-center text-xs ${getTrendColor(metric.trend)}`}>
                  {getTrendIcon(metric.trend)}
                  <span className="ml-1">{metric.change}</span>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <p className="text-xs text-muted-foreground">较上周</p>
                <Badge
                  variant="outline"
                  className={`text-xs ${
                    metric.trend === "up"
                      ? "border-green-200 text-green-700"
                      : metric.trend === "down"
                        ? "border-red-200 text-red-700"
                        : "border-gray-200 text-gray-700"
                  }`}
                >
                  实时更新
                </Badge>
              </div>
            </div>

            {/* 进度条 (仅对有百分比的指标) */}
            {metric.title.includes("率") && (
              <div className="mt-3">
                <div className="w-full bg-muted rounded-full h-1.5">
                  <div
                    className={`h-1.5 rounded-full transition-all ${
                      metric.trend === "up" ? "bg-green-500" : metric.trend === "down" ? "bg-red-500" : "bg-gray-500"
                    }`}
                    style={{
                      width: `${Number.parseInt(metric.value.replace("%", ""))}%`,
                    }}
                  />
                </div>
              </div>
            )}
          </CardContent>

          {/* 装饰性背景 */}
          <div className={`absolute top-0 right-0 w-20 h-20 ${metric.color} opacity-5 rounded-full -mr-10 -mt-10`} />
        </Card>
      ))}
    </div>
  )
}
