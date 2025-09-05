"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Users, TrendingUp, AlertTriangle, CheckCircle, Clock } from "lucide-react"

interface Staff {
  id: string
  name: string
  department: string
  position: string
  skills: string[]
  level: string
  workload: number
  availability: string
  hourlyRate: number
  efficiency: number
}

interface ResourceHeatmapProps {
  staff: Staff[]
  onStaffSelect?: (staff: Staff) => void
}

export function ResourceHeatmap({ staff, onStaffSelect }: ResourceHeatmapProps) {
  const [selectedDepartment, setSelectedDepartment] = useState<string>("all")
  const [heatmapData, setHeatmapData] = useState<any[]>([])

  // 按部门分组人员
  const departments = ["all", ...Array.from(new Set(staff.map((s) => s.department)))]

  const filteredStaff = selectedDepartment === "all" ? staff : staff.filter((s) => s.department === selectedDepartment)

  // 生成热力图数据
  useEffect(() => {
    const generateHeatmapData = () => {
      const days = ["周一", "周二", "周三", "周四", "周五"]
      const timeSlots = ["09:00", "11:00", "14:00", "16:00", "18:00"]

      const data = []

      filteredStaff.forEach((person, personIndex) => {
        days.forEach((day, dayIndex) => {
          timeSlots.forEach((time, timeIndex) => {
            // 模拟工作负载数据
            const baseLoad = person.workload
            const randomVariation = (Math.random() - 0.5) * 20
            const workload = Math.max(0, Math.min(100, baseLoad + randomVariation))

            data.push({
              person: person.name,
              day,
              time,
              workload,
              efficiency: person.efficiency,
              x: dayIndex,
              y: personIndex * timeSlots.length + timeIndex,
              personData: person,
            })
          })
        })
      })

      setHeatmapData(data)
    }

    generateHeatmapData()
    const interval = setInterval(generateHeatmapData, 5000) // 每5秒更新一次

    return () => clearInterval(interval)
  }, [filteredStaff])

  const getWorkloadColor = (workload: number) => {
    if (workload >= 90) return "bg-red-500"
    if (workload >= 75) return "bg-orange-500"
    if (workload >= 50) return "bg-yellow-500"
    if (workload >= 25) return "bg-green-500"
    return "bg-blue-500"
  }

  const getWorkloadIntensity = (workload: number) => {
    return Math.max(0.1, workload / 100)
  }

  const getAvailabilityIcon = (availability: string) => {
    switch (availability) {
      case "可用":
        return <CheckCircle className="w-4 h-4 text-green-400" />
      case "忙碌":
        return <AlertTriangle className="w-4 h-4 text-orange-400" />
      case "离线":
        return <Clock className="w-4 h-4 text-gray-400" />
      default:
        return <Users className="w-4 h-4 text-blue-400" />
    }
  }

  return (
    <div className="space-y-6">
      {/* 部门筛选 */}
      <div className="flex items-center space-x-4">
        <span className="text-white/80 text-sm">部门筛选:</span>
        <div className="flex flex-wrap gap-2">
          {departments.map((dept) => (
            <Button
              key={dept}
              variant={selectedDepartment === dept ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedDepartment(dept)}
              className="luxury-button text-white border-white/30"
            >
              {dept === "all" ? "全部" : dept}
            </Button>
          ))}
        </div>
      </div>

      {/* 人员概览卡片 */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {filteredStaff.map((person, index) => (
          <Card
            key={person.id}
            className="luxury-card cursor-pointer floating-animation"
            style={{ animationDelay: `${index * 0.1}s` }}
            onClick={() => onStaffSelect?.(person)}
          >
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm text-white">{person.name}</CardTitle>
                {getAvailabilityIcon(person.availability)}
              </div>
              <p className="text-xs text-white/70">{person.position}</p>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {/* 工作负载 */}
                <div>
                  <div className="flex justify-between text-xs text-white/70 mb-1">
                    <span>工作负载</span>
                    <span>{person.workload}%</span>
                  </div>
                  <div className="w-full bg-white/10 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-500 ${getWorkloadColor(person.workload)}`}
                      style={{
                        width: `${person.workload}%`,
                        opacity: getWorkloadIntensity(person.workload),
                      }}
                    />
                  </div>
                </div>

                {/* 效率指标 */}
                <div className="flex items-center justify-between text-xs">
                  <span className="text-white/70">效率</span>
                  <div className="flex items-center text-white">
                    <TrendingUp className="w-3 h-3 mr-1" />
                    {person.efficiency}%
                  </div>
                </div>

                {/* 技能标签 */}
                <div className="flex flex-wrap gap-1">
                  {person.skills.slice(0, 2).map((skill) => (
                    <Badge key={skill} variant="outline" className="text-xs">
                      {skill}
                    </Badge>
                  ))}
                  {person.skills.length > 2 && (
                    <Badge variant="outline" className="text-xs">
                      +{person.skills.length - 2}
                    </Badge>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* 实时工作负载热力图 */}
      <Card className="luxury-card">
        <CardHeader>
          <CardTitle className="text-white flex items-center">
            <Users className="w-5 h-5 mr-2" />
            实时工作负载热力图
          </CardTitle>
          <p className="text-white/70 text-sm">显示团队成员在不同时间段的工作负载分布</p>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* 时间轴标题 */}
            <div className="grid grid-cols-6 gap-2 text-xs text-white/70">
              <div></div>
              <div className="text-center">周一</div>
              <div className="text-center">周二</div>
              <div className="text-center">周三</div>
              <div className="text-center">周四</div>
              <div className="text-center">周五</div>
            </div>

            {/* 热力图网格 */}
            <div className="space-y-2">
              {filteredStaff.map((person, personIndex) => (
                <div key={person.id} className="grid grid-cols-6 gap-2 items-center">
                  <div className="text-xs text-white/80 truncate">{person.name}</div>
                  {[0, 1, 2, 3, 4].map((dayIndex) => {
                    const dayData = heatmapData.filter((d) => d.person === person.name && d.x === dayIndex)
                    const avgWorkload =
                      dayData.length > 0 ? dayData.reduce((sum, d) => sum + d.workload, 0) / dayData.length : 0

                    return (
                      <div
                        key={dayIndex}
                        className={`
                          h-8 rounded transition-all duration-500 flex items-center justify-center
                          ${getWorkloadColor(avgWorkload)} cursor-pointer hover:scale-110
                        `}
                        style={{
                          opacity: getWorkloadIntensity(avgWorkload),
                        }}
                        title={`${person.name} - ${Math.round(avgWorkload)}% 负载`}
                      >
                        <span className="text-xs text-white font-medium">{Math.round(avgWorkload)}%</span>
                      </div>
                    )
                  })}
                </div>
              ))}
            </div>

            {/* 图例 */}
            <div className="flex items-center justify-center space-x-6 pt-4 border-t border-white/10">
              <div className="flex items-center space-x-2 text-xs text-white/70">
                <div className="w-3 h-3 bg-blue-500 rounded"></div>
                <span>轻松 (0-25%)</span>
              </div>
              <div className="flex items-center space-x-2 text-xs text-white/70">
                <div className="w-3 h-3 bg-green-500 rounded"></div>
                <span>适中 (25-50%)</span>
              </div>
              <div className="flex items-center space-x-2 text-xs text-white/70">
                <div className="w-3 h-3 bg-yellow-500 rounded"></div>
                <span>繁忙 (50-75%)</span>
              </div>
              <div className="flex items-center space-x-2 text-xs text-white/70">
                <div className="w-3 h-3 bg-orange-500 rounded"></div>
                <span>紧张 (75-90%)</span>
              </div>
              <div className="flex items-center space-x-2 text-xs text-white/70">
                <div className="w-3 h-3 bg-red-500 rounded"></div>
                <span>超负荷 (90%+)</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
