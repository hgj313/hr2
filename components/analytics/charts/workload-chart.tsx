"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Users } from "lucide-react"

interface WorkloadChartProps {
  data: Array<{
    department: string
    utilization: number
    capacity: number
  }>
}

export function WorkloadChart({ data }: WorkloadChartProps) {
  const getUtilizationColor = (utilization: number) => {
    if (utilization >= 90) return "bg-red-500"
    if (utilization >= 80) return "bg-yellow-500"
    if (utilization >= 70) return "bg-blue-500"
    return "bg-green-500"
  }

  const getUtilizationStatus = (utilization: number) => {
    if (utilization >= 90) return { text: "过载", color: "text-red-600" }
    if (utilization >= 80) return { text: "繁忙", color: "text-yellow-600" }
    if (utilization >= 70) return { text: "正常", color: "text-blue-600" }
    return { text: "空闲", color: "text-green-600" }
  }

  return (
    <Card className="border-border/50">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Users className="w-5 h-5" />
          部门工作负载
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {data.map((dept) => {
            const status = getUtilizationStatus(dept.utilization)
            return (
              <div key={dept.department} className="space-y-3">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium">{dept.department}</h4>
                    <p className="text-sm text-muted-foreground">
                      利用率 {dept.utilization}% / {dept.capacity}%
                    </p>
                  </div>
                  <div className="text-right">
                    <span className={`text-sm font-medium ${status.color}`}>{status.text}</span>
                  </div>
                </div>

                <div className="space-y-2">
                  <Progress value={dept.utilization} className="h-3" />
                  <div className="flex justify-between text-xs text-muted-foreground">
                    <span>0%</span>
                    <span>50%</span>
                    <span>100%</span>
                  </div>
                </div>
              </div>
            )
          })}

          {/* 总体统计 */}
          <div className="pt-4 border-t border-border/50">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-lg font-bold text-foreground">
                  {Math.round(data.reduce((sum, d) => sum + d.utilization, 0) / data.length)}%
                </div>
                <p className="text-xs text-muted-foreground">平均利用率</p>
              </div>
              <div>
                <div className="text-lg font-bold text-green-600">{data.filter((d) => d.utilization < 80).length}</div>
                <p className="text-xs text-muted-foreground">正常部门</p>
              </div>
              <div>
                <div className="text-lg font-bold text-red-600">{data.filter((d) => d.utilization >= 90).length}</div>
                <p className="text-xs text-muted-foreground">过载部门</p>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
