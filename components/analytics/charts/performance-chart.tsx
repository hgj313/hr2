"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp } from "lucide-react"

interface PerformanceChartProps {
  data: Array<{
    month: string
    completed: number
    started: number
  }>
}

export function PerformanceChart({ data }: PerformanceChartProps) {
  const maxValue = Math.max(...data.map((d) => Math.max(d.completed, d.started)))

  return (
    <Card className="border-border/50">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <TrendingUp className="w-5 h-5" />
          项目完成趋势
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* 图例 */}
          <div className="flex items-center gap-4 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-primary rounded-full"></div>
              <span>已完成</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-secondary rounded-full"></div>
              <span>新启动</span>
            </div>
          </div>

          {/* 图表 */}
          <div className="space-y-3">
            {data.map((item) => (
              <div key={item.month} className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium">{item.month}</span>
                  <span className="text-muted-foreground">
                    完成 {item.completed} | 启动 {item.started}
                  </span>
                </div>

                <div className="flex gap-1 h-6">
                  <div
                    className="bg-primary rounded-sm flex items-center justify-center text-xs text-primary-foreground font-medium"
                    style={{
                      width: `${(item.completed / maxValue) * 100}%`,
                      minWidth: item.completed > 0 ? "20px" : "0",
                    }}
                  >
                    {item.completed > 0 && item.completed}
                  </div>
                  <div
                    className="bg-secondary rounded-sm flex items-center justify-center text-xs text-secondary-foreground font-medium"
                    style={{ width: `${(item.started / maxValue) * 100}%`, minWidth: item.started > 0 ? "20px" : "0" }}
                  >
                    {item.started > 0 && item.started}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* 统计摘要 */}
          <div className="pt-4 border-t border-border/50">
            <div className="grid grid-cols-2 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-primary">
                  {data.reduce((sum, item) => sum + item.completed, 0)}
                </div>
                <p className="text-xs text-muted-foreground">总完成项目</p>
              </div>
              <div>
                <div className="text-2xl font-bold text-secondary">
                  {data.reduce((sum, item) => sum + item.started, 0)}
                </div>
                <p className="text-xs text-muted-foreground">总启动项目</p>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
