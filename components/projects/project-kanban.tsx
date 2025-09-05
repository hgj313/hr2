"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { MoreHorizontal, Users, Calendar } from "lucide-react"

interface Project {
  id: string
  name: string
  description: string
  status: string
  priority: string
  startDate: string
  endDate: string
  progress: number
  budget: number
  manager: string
  team: Array<{ id: string; name: string; role: string; avatar: string }>
  tags: string[]
  tasks: Array<{ id: string; title: string; status: string; assignee: string }>
}

interface ProjectKanbanProps {
  projects: Project[]
  onProjectUpdate: (projects: Project[]) => void
}

const statusColumns = [
  { id: "计划中", title: "计划中", color: "bg-yellow-50 border-yellow-200" },
  { id: "进行中", title: "进行中", color: "bg-blue-50 border-blue-200" },
  { id: "已完成", title: "已完成", color: "bg-green-50 border-green-200" },
  { id: "暂停", title: "暂停", color: "bg-red-50 border-red-200" },
]

export function ProjectKanban({ projects, onProjectUpdate }: ProjectKanbanProps) {
  const [draggedProject, setDraggedProject] = useState<Project | null>(null)

  const handleDragStart = (e: React.DragEvent, project: Project) => {
    setDraggedProject(project)
    e.dataTransfer.effectAllowed = "move"
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = "move"
  }

  const handleDrop = (e: React.DragEvent, newStatus: string) => {
    e.preventDefault()
    if (draggedProject && draggedProject.status !== newStatus) {
      const updatedProjects = projects.map((project) =>
        project.id === draggedProject.id ? { ...project, status: newStatus } : project,
      )
      onProjectUpdate(updatedProjects)
    }
    setDraggedProject(null)
  }

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

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
      {statusColumns.map((column) => {
        const columnProjects = projects.filter((project) => project.status === column.id)

        return (
          <div
            key={column.id}
            className={`space-y-4 p-4 rounded-lg border-2 border-dashed ${column.color} min-h-[600px]`}
            onDragOver={handleDragOver}
            onDrop={(e) => handleDrop(e, column.id)}
          >
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-lg">{column.title}</h3>
              <Badge variant="outline">{columnProjects.length}</Badge>
            </div>

            <div className="space-y-3">
              {columnProjects.map((project) => (
                <Card
                  key={project.id}
                  className="cursor-move hover:shadow-md transition-shadow border-border/50"
                  draggable
                  onDragStart={(e) => handleDragStart(e, project)}
                >
                  <CardHeader className="pb-3">
                    <div className="flex items-start justify-between">
                      <div className="space-y-1">
                        <CardTitle className="text-base line-clamp-2">{project.name}</CardTitle>
                        <p className="text-sm text-muted-foreground line-clamp-2">{project.description}</p>
                      </div>
                      <Button variant="ghost" size="sm">
                        <MoreHorizontal className="w-4 h-4" />
                      </Button>
                    </div>

                    <div className="flex items-center gap-2">
                      <Badge className={getPriorityColor(project.priority)}>{project.priority}</Badge>
                    </div>
                  </CardHeader>

                  <CardContent className="space-y-3">
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">进度</span>
                        <span className="font-medium">{project.progress}%</span>
                      </div>
                      <Progress value={project.progress} className="h-1.5" />
                    </div>

                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-1">
                        <Calendar className="w-3 h-3 text-muted-foreground" />
                        <span className="text-muted-foreground">截止</span>
                      </div>
                      <span>{project.endDate}</span>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-1 text-sm text-muted-foreground">
                        <Users className="w-3 h-3" />
                        <span>{project.team.length}</span>
                      </div>
                      <div className="flex -space-x-1">
                        {project.team.slice(0, 3).map((member) => (
                          <Avatar key={member.id} className="w-6 h-6 border border-background">
                            <AvatarImage src={member.avatar || "/placeholder.svg"} alt={member.name} />
                            <AvatarFallback className="text-xs">{member.name.charAt(0)}</AvatarFallback>
                          </Avatar>
                        ))}
                        {project.team.length > 3 && (
                          <div className="w-6 h-6 rounded-full bg-muted border border-background flex items-center justify-center">
                            <span className="text-xs text-muted-foreground">+{project.team.length - 3}</span>
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="flex flex-wrap gap-1">
                      {project.tags.slice(0, 2).map((tag) => (
                        <Badge key={tag} variant="outline" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                      {project.tags.length > 2 && (
                        <Badge variant="outline" className="text-xs">
                          +{project.tags.length - 2}
                        </Badge>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )
      })}
    </div>
  )
}
