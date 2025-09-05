"use client"

import type React from "react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Calendar, Target, X, Users } from "lucide-react"

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

interface ProjectSlotsProps {
  projects: Project[]
  dragOverProject: string | null
  onDragOver: (e: React.DragEvent, projectId: string) => void
  onDragLeave: () => void
  onDrop: (e: React.DragEvent, projectId: string) => void
  onRemoveStaff: (projectId: string, staffId: string) => void
}

export function ProjectSlots({
  projects,
  dragOverProject,
  onDragOver,
  onDragLeave,
  onDrop,
  onRemoveStaff,
}: ProjectSlotsProps) {
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "高":
        return "bg-red-100 text-red-800"
      case "中":
        return "bg-yellow-100 text-yellow-800"
      case "低":
        return "bg-green-100 text-green-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "已分配":
        return "bg-green-100 text-green-800"
      case "待分配":
        return "bg-yellow-100 text-yellow-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const calculateSkillMatch = (staffSkills: string[], requiredSkills: string[]): number => {
    const matchedSkills = staffSkills.filter((skill) => requiredSkills.includes(skill))
    return matchedSkills.length / requiredSkills.length
  }

  return (
    <div className="space-y-4 max-h-[600px] overflow-y-auto">
      {projects.map((project) => (
        <Card
          key={project.id}
          className={`border-2 border-dashed transition-all ${
            dragOverProject === project.id
              ? "border-primary bg-primary/5 shadow-md"
              : "border-border/50 hover:border-border"
          }`}
          onDragOver={(e) => onDragOver(e, project.id)}
          onDragLeave={onDragLeave}
          onDrop={(e) => onDrop(e, project.id)}
        >
          <CardHeader className="pb-3">
            <div className="flex items-start justify-between">
              <div className="space-y-2">
                <CardTitle className="text-base">{project.name}</CardTitle>
                <div className="flex items-center gap-2">
                  <Badge className={getPriorityColor(project.priority)}>{project.priority}优先级</Badge>
                  <Badge className={getStatusColor(project.status)}>{project.status}</Badge>
                </div>
              </div>
              <div className="text-right text-sm text-muted-foreground">
                <div className="flex items-center gap-1">
                  <Calendar className="w-3 h-3" />
                  <span>{project.deadline}</span>
                </div>
                <div className="flex items-center gap-1 mt-1">
                  <Target className="w-3 h-3" />
                  <span>{project.estimatedHours}h</span>
                </div>
              </div>
            </div>
          </CardHeader>

          <CardContent className="space-y-4">
            <div className="space-y-2">
              <h5 className="text-sm font-medium text-muted-foreground">所需技能</h5>
              <div className="flex flex-wrap gap-1">
                {project.requiredSkills.map((skill) => (
                  <Badge key={skill} variant="outline" className="text-xs">
                    {skill}
                  </Badge>
                ))}
              </div>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <h5 className="text-sm font-medium text-muted-foreground">分配人员</h5>
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <Users className="w-3 h-3" />
                  <span>{project.assignedStaff.length} 人</span>
                </div>
              </div>

              {project.assignedStaff.length === 0 ? (
                <div className="flex items-center justify-center h-20 border-2 border-dashed border-muted-foreground/20 rounded-lg">
                  <p className="text-sm text-muted-foreground">拖拽人员到此处进行分配</p>
                </div>
              ) : (
                <div className="space-y-2">
                  {project.assignedStaff.map((staff) => {
                    const skillMatch = calculateSkillMatch(staff.skills, project.requiredSkills)
                    return (
                      <div key={staff.id} className="flex items-center justify-between p-2 bg-muted/50 rounded-lg">
                        <div className="flex items-center space-x-2">
                          <Avatar className="w-6 h-6">
                            <AvatarImage src="/placeholder.svg?height=24&width=24" alt={staff.name} />
                            <AvatarFallback className="text-xs">{staff.name.charAt(0)}</AvatarFallback>
                          </Avatar>
                          <div>
                            <p className="text-sm font-medium">{staff.name}</p>
                            <p className="text-xs text-muted-foreground">{staff.position}</p>
                          </div>
                        </div>

                        <div className="flex items-center space-x-2">
                          <Badge
                            variant="outline"
                            className={`text-xs ${
                              skillMatch >= 0.7
                                ? "bg-green-50 text-green-700"
                                : skillMatch >= 0.4
                                  ? "bg-yellow-50 text-yellow-700"
                                  : "bg-red-50 text-red-700"
                            }`}
                          >
                            {Math.round(skillMatch * 100)}% 匹配
                          </Badge>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => onRemoveStaff(project.id, staff.id)}
                            className="h-6 w-6 p-0"
                          >
                            <X className="w-3 h-3" />
                          </Button>
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
