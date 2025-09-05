"use client"

import type React from "react"

import { useState } from "react"
import { StaffPool } from "./staff-pool"
import { ProjectSlots } from "./project-slots"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { RefreshCw, Save } from "lucide-react"

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
}

interface Project {
  id: string
  name: string
  requiredSkills: string[]
  priority: string
  deadline: string
  estimatedHours: number
  assignedStaff: Staff[]
  status: string
}

interface DragDropSchedulerProps {
  data: {
    availableStaff: Staff[]
    projects: Project[]
  }
  onDataChange: (data: any) => void
}

export function DragDropScheduler({ data, onDataChange }: DragDropSchedulerProps) {
  const [draggedStaff, setDraggedStaff] = useState<Staff | null>(null)
  const [dragOverProject, setDragOverProject] = useState<string | null>(null)

  const handleDragStart = (staff: Staff) => {
    setDraggedStaff(staff)
    console.log("[v0] 开始拖拽人员:", staff.name)
  }

  const handleDragEnd = () => {
    setDraggedStaff(null)
    setDragOverProject(null)
    console.log("[v0] 拖拽结束")
  }

  const handleDragOver = (e: React.DragEvent, projectId: string) => {
    e.preventDefault()
    setDragOverProject(projectId)
  }

  const handleDragLeave = () => {
    setDragOverProject(null)
  }

  const handleDrop = (e: React.DragEvent, projectId: string) => {
    e.preventDefault()

    if (!draggedStaff) return

    console.log("[v0] 将人员", draggedStaff.name, "分配到项目", projectId)

    // 检查技能匹配度
    const project = data.projects.find((p) => p.id === projectId)
    if (!project) return

    const skillMatch = calculateSkillMatch(draggedStaff.skills, project.requiredSkills)

    if (skillMatch < 0.3) {
      alert(`技能匹配度较低 (${Math.round(skillMatch * 100)}%)，建议选择其他人员`)
      return
    }

    // 检查工作负载
    if (draggedStaff.workload > 80) {
      alert(`${draggedStaff.name} 当前工作负载过高 (${draggedStaff.workload}%)，可能影响项目进度`)
    }

    // 更新项目分配
    const updatedProjects = data.projects.map((p) => {
      if (p.id === projectId) {
        const isAlreadyAssigned = p.assignedStaff.some((s) => s.id === draggedStaff.id)
        if (isAlreadyAssigned) {
          return p // 已经分配过了
        }
        return {
          ...p,
          assignedStaff: [...p.assignedStaff, draggedStaff],
          status: "已分配",
        }
      }
      return p
    })

    // 更新人员工作负载
    const updatedStaff = data.availableStaff.map((s) => {
      if (s.id === draggedStaff.id) {
        return {
          ...s,
          workload: Math.min(100, s.workload + 20), // 增加20%工作负载
        }
      }
      return s
    })

    onDataChange({
      ...data,
      projects: updatedProjects,
      availableStaff: updatedStaff,
    })

    setDragOverProject(null)
    setDraggedStaff(null)
  }

  const calculateSkillMatch = (staffSkills: string[], requiredSkills: string[]): number => {
    const matchedSkills = staffSkills.filter((skill) => requiredSkills.includes(skill))
    return matchedSkills.length / requiredSkills.length
  }

  const handleRemoveStaffFromProject = (projectId: string, staffId: string) => {
    console.log("[v0] 从项目", projectId, "移除人员", staffId)

    const updatedProjects = data.projects.map((p) => {
      if (p.id === projectId) {
        return {
          ...p,
          assignedStaff: p.assignedStaff.filter((s) => s.id !== staffId),
          status: p.assignedStaff.length <= 1 ? "待分配" : "已分配",
        }
      }
      return p
    })

    // 减少人员工作负载
    const updatedStaff = data.availableStaff.map((s) => {
      if (s.id === staffId) {
        return {
          ...s,
          workload: Math.max(0, s.workload - 20), // 减少20%工作负载
        }
      }
      return s
    })

    onDataChange({
      ...data,
      projects: updatedProjects,
      availableStaff: updatedStaff,
    })
  }

  const handleResetAssignments = () => {
    console.log("[v0] 重置所有分配")

    const resetProjects = data.projects.map((p) => ({
      ...p,
      assignedStaff: [],
      status: "待分配",
    }))

    const resetStaff = data.availableStaff.map((s) => ({
      ...s,
      workload: Math.max(0, s.workload - 40), // 重置工作负载
    }))

    onDataChange({
      ...data,
      projects: resetProjects,
      availableStaff: resetStaff,
    })
  }

  const handleSaveAssignments = () => {
    console.log("[v0] 保存当前分配方案")
    // 这里会调用API保存分配方案
    alert("分配方案已保存")
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <h3 className="text-lg font-semibold">拖拽式人员调度</h3>
          <p className="text-sm text-muted-foreground">将左侧人员拖拽到右侧项目中进行分配</p>
        </div>

        <div className="flex items-center space-x-2">
          <Button variant="outline" onClick={handleResetAssignments}>
            <RefreshCw className="w-4 h-4 mr-2" />
            重置分配
          </Button>
          <Button onClick={handleSaveAssignments} className="bg-primary hover:bg-primary/90">
            <Save className="w-4 h-4 mr-2" />
            保存方案
          </Button>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* 人员池 */}
        <Card className="border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>可用人员池</span>
              <Badge variant="outline">{data.availableStaff.length} 人</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <StaffPool staff={data.availableStaff} onDragStart={handleDragStart} onDragEnd={handleDragEnd} />
          </CardContent>
        </Card>

        {/* 项目分配区 */}
        <Card className="border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>项目分配区</span>
              <Badge variant="outline">{data.projects.length} 个项目</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ProjectSlots
              projects={data.projects}
              dragOverProject={dragOverProject}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onRemoveStaff={handleRemoveStaffFromProject}
            />
          </CardContent>
        </Card>
      </div>

      {/* 拖拽提示 */}
      {draggedStaff && (
        <div className="fixed bottom-4 right-4 bg-primary text-primary-foreground p-3 rounded-lg shadow-lg z-50">
          <p className="text-sm">正在拖拽: {draggedStaff.name}</p>
          <p className="text-xs opacity-90">拖拽到项目区域进行分配</p>
        </div>
      )}
    </div>
  )
}
