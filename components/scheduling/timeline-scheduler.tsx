"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { ChevronLeft, ChevronRight, Calendar } from "lucide-react"

interface TimelineSchedulerProps {
  data: any
  onDataChange: (data: any) => void
}

export function TimelineScheduler({ data, onDataChange }: TimelineSchedulerProps) {
  const [currentWeek, setCurrentWeek] = useState(0)

  // 生成时间轴数据
  const generateTimelineData = () => {
    const weeks = []
    const startDate = new Date()

    for (let i = 0; i < 8; i++) {
      const weekStart = new Date(startDate)
      weekStart.setDate(startDate.getDate() + i * 7)

      const days = []
      for (let j = 0; j < 7; j++) {
        const day = new Date(weekStart)
        day.setDate(weekStart.getDate() + j)
        days.push({
          date: day.toISOString().split("T")[0],
          dayName: day.toLocaleDateString("zh-CN", { weekday: "short" }),
          dayNumber: day.getDate(),
        })
      }

      weeks.push({
        weekNumber: i + 1,
        days,
      })
    }

    return weeks
  }

  const timelineData = generateTimelineData()
  const currentWeekData = timelineData[currentWeek]

  // 模拟人员时间安排数据
  const staffSchedule = data.availableStaff.map((staff: any) => ({
    ...staff,
    schedule: currentWeekData.days.map((day: any) => ({
      date: day.date,
      projects:
        Math.random() > 0.7
          ? []
          : [
              {
                id: Math.random().toString(),
                name: data.projects[Math.floor(Math.random() * data.projects.length)]?.name || "项目A",
                hours: Math.floor(Math.random() * 8) + 1,
                color: ["bg-blue-100 text-blue-800", "bg-green-100 text-green-800", "bg-purple-100 text-purple-800"][
                  Math.floor(Math.random() * 3)
                ],
              },
            ],
    })),
  }))

  const handlePrevWeek = () => {
    setCurrentWeek(Math.max(0, currentWeek - 1))
  }

  const handleNextWeek = () => {
    setCurrentWeek(Math.min(timelineData.length - 1, currentWeek + 1))
  }

  const handleDragStart = (e: React.DragEvent, staffId: string, date: string) => {
    e.dataTransfer.setData("staffId", staffId)
    e.dataTransfer.setData("date", date)
    console.log("[v0] 开始拖拽时间段:", staffId, date)
  }

  const handleDrop = (e: React.DragEvent, targetStaffId: string, targetDate: string) => {
    e.preventDefault()
    const sourceStaffId = e.dataTransfer.getData("staffId")
    const sourceDate = e.dataTransfer.getData("date")

    console.log("[v0] 拖拽时间段从", sourceStaffId, sourceDate, "到", targetStaffId, targetDate)

    // 这里可以实现时间段的重新分配逻辑
    alert(`时间段调整: ${sourceDate} → ${targetDate}`)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <h3 className="text-lg font-semibold">时间轴调度</h3>
          <p className="text-sm text-muted-foreground">查看和调整人员的时间安排</p>
        </div>

        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={handlePrevWeek} disabled={currentWeek === 0}>
            <ChevronLeft className="w-4 h-4" />
          </Button>
          <div className="flex items-center gap-2 px-3 py-1 bg-muted rounded-md">
            <Calendar className="w-4 h-4" />
            <span className="text-sm font-medium">第 {currentWeek + 1} 周</span>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={handleNextWeek}
            disabled={currentWeek === timelineData.length - 1}
          >
            <ChevronRight className="w-4 h-4" />
          </Button>
        </div>
      </div>

      <Card className="border-border/50">
        <CardHeader>
          <CardTitle>人员时间安排</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <div className="min-w-[800px]">
              {/* 时间轴头部 */}
              <div className="grid grid-cols-8 gap-2 mb-4">
                <div className="font-medium text-sm text-muted-foreground">人员</div>
                {currentWeekData.days.map((day: any) => (
                  <div key={day.date} className="text-center">
                    <div className="text-xs text-muted-foreground">{day.dayName}</div>
                    <div className="text-sm font-medium">{day.dayNumber}</div>
                  </div>
                ))}
              </div>

              {/* 人员时间安排 */}
              <div className="space-y-2">
                {staffSchedule.map((staff: any) => (
                  <div key={staff.id} className="grid grid-cols-8 gap-2 items-center">
                    <div className="flex items-center space-x-2">
                      <Avatar className="w-8 h-8">
                        <AvatarImage src="/placeholder.svg?height=32&width=32" alt={staff.name} />
                        <AvatarFallback className="text-xs">{staff.name.charAt(0)}</AvatarFallback>
                      </Avatar>
                      <div>
                        <p className="text-sm font-medium">{staff.name}</p>
                        <p className="text-xs text-muted-foreground">{staff.position}</p>
                      </div>
                    </div>

                    {staff.schedule.map((daySchedule: any) => (
                      <div
                        key={daySchedule.date}
                        className="min-h-[60px] border border-border/50 rounded-md p-1 space-y-1"
                        onDragOver={(e) => e.preventDefault()}
                        onDrop={(e) => handleDrop(e, staff.id, daySchedule.date)}
                      >
                        {daySchedule.projects.map((project: any) => (
                          <div
                            key={project.id}
                            className={`text-xs p-1 rounded cursor-move ${project.color}`}
                            draggable
                            onDragStart={(e) => handleDragStart(e, staff.id, daySchedule.date)}
                          >
                            <div className="font-medium truncate">{project.name}</div>
                            <div>{project.hours}h</div>
                          </div>
                        ))}
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 图例 */}
      <Card className="border-border/50">
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div className="space-y-2">
              <h4 className="text-sm font-medium">操作说明</h4>
              <div className="text-xs text-muted-foreground space-y-1">
                <p>• 拖拽项目块可以重新安排时间</p>
                <p>• 点击空白区域可以添加新的时间安排</p>
                <p>• 不同颜色代表不同类型的项目</p>
              </div>
            </div>

            <div className="flex items-center space-x-4 text-xs">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-blue-100 rounded"></div>
                <span>开发项目</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-green-100 rounded"></div>
                <span>设计项目</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-purple-100 rounded"></div>
                <span>管理项目</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
