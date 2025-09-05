"use client"

import { useState } from "react"
import { ProjectForm } from "./project-form"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { MoreHorizontal, Edit, Trash2, Eye, Users, Calendar } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

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

interface ProjectListProps {
  projects: Project[]
  onProjectUpdate: (projects: Project[]) => void
}

export function ProjectList({ projects, onProjectUpdate }: ProjectListProps) {
  const [selectedProject, setSelectedProject] = useState<Project | null>(null)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [isDetailDialogOpen, setIsDetailDialogOpen] = useState(false)

  const handleEditProject = (project: Project) => {
    setSelectedProject(project)
    setIsEditDialogOpen(true)
  }

  const handleViewProject = (project: Project) => {
    setSelectedProject(project)
    setIsDetailDialogOpen(true)
  }

  const handleDeleteProject = (projectId: string) => {
    if (confirm("确定要删除这个项目吗？")) {
      const updatedProjects = projects.filter((project) => project.id !== projectId)
      onProjectUpdate(updatedProjects)
    }
  }

  const handleUpdateProject = (projectData: any) => {
    const updatedProjects = projects.map((project) =>
      project.id === selectedProject?.id ? { ...project, ...projectData } : project,
    )
    onProjectUpdate(updatedProjects)
    setIsEditDialogOpen(false)
    setSelectedProject(null)
  }

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
    <>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {projects.map((project) => (
          <Card key={project.id} className="border-border/50 hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <div className="space-y-2">
                  <CardTitle className="text-lg line-clamp-1">{project.name}</CardTitle>
                  <p className="text-sm text-muted-foreground line-clamp-2">{project.description}</p>
                </div>

                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="sm">
                      <MoreHorizontal className="w-4 h-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={() => handleViewProject(project)}>
                      <Eye className="w-4 h-4 mr-2" />
                      查看详情
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handleEditProject(project)}>
                      <Edit className="w-4 h-4 mr-2" />
                      编辑
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handleDeleteProject(project.id)} className="text-red-600">
                      <Trash2 className="w-4 h-4 mr-2" />
                      删除
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>

              <div className="flex items-center gap-2">
                <Badge className={getStatusColor(project.status)}>{project.status}</Badge>
                <Badge className={getPriorityColor(project.priority)}>{project.priority}优先级</Badge>
              </div>
            </CardHeader>

            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">进度</span>
                  <span className="font-medium">{project.progress}%</span>
                </div>
                <Progress value={project.progress} className="h-2" />
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-muted-foreground" />
                  <span className="text-muted-foreground">开始:</span>
                </div>
                <span className="text-right">{project.startDate}</span>

                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-muted-foreground" />
                  <span className="text-muted-foreground">结束:</span>
                </div>
                <span className="text-right">{project.endDate}</span>
              </div>

              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Users className="w-4 h-4" />
                  <span>团队成员 ({project.team.length})</span>
                </div>
                <div className="flex -space-x-2">
                  {project.team.slice(0, 4).map((member) => (
                    <Avatar key={member.id} className="w-8 h-8 border-2 border-background">
                      <AvatarImage src={member.avatar || "/placeholder.svg"} alt={member.name} />
                      <AvatarFallback className="text-xs">{member.name.charAt(0)}</AvatarFallback>
                    </Avatar>
                  ))}
                  {project.team.length > 4 && (
                    <div className="w-8 h-8 rounded-full bg-muted border-2 border-background flex items-center justify-center">
                      <span className="text-xs text-muted-foreground">+{project.team.length - 4}</span>
                    </div>
                  )}
                </div>
              </div>

              <div className="space-y-2">
                <span className="text-sm text-muted-foreground">标签</span>
                <div className="flex flex-wrap gap-1">
                  {project.tags.slice(0, 3).map((tag) => (
                    <Badge key={tag} variant="outline" className="text-xs">
                      {tag}
                    </Badge>
                  ))}
                  {project.tags.length > 3 && (
                    <Badge variant="outline" className="text-xs">
                      +{project.tags.length - 3}
                    </Badge>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>编辑项目</DialogTitle>
          </DialogHeader>
          {selectedProject && <ProjectForm initialData={selectedProject} onSubmit={handleUpdateProject} />}
        </DialogContent>
      </Dialog>

      <Dialog open={isDetailDialogOpen} onOpenChange={setIsDetailDialogOpen}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>项目详情</DialogTitle>
          </DialogHeader>
          {selectedProject && (
            <div className="space-y-6">
              <div className="grid gap-6 md:grid-cols-2">
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold mb-2">{selectedProject.name}</h3>
                    <p className="text-muted-foreground">{selectedProject.description}</p>
                  </div>

                  <div className="grid gap-3">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">状态:</span>
                      <Badge className={getStatusColor(selectedProject.status)}>{selectedProject.status}</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">优先级:</span>
                      <Badge className={getPriorityColor(selectedProject.priority)}>
                        {selectedProject.priority}优先级
                      </Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">项目经理:</span>
                      <span>{selectedProject.manager}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">预算:</span>
                      <span>¥{selectedProject.budget.toLocaleString()}</span>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium mb-2">项目进度</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>完成度</span>
                        <span>{selectedProject.progress}%</span>
                      </div>
                      <Progress value={selectedProject.progress} className="h-2" />
                    </div>
                  </div>

                  <div>
                    <h4 className="font-medium mb-2">时间安排</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">开始日期:</span>
                        <span>{selectedProject.startDate}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">结束日期:</span>
                        <span>{selectedProject.endDate}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="font-medium">团队成员</h4>
                <div className="grid gap-3 md:grid-cols-2">
                  {selectedProject.team.map((member) => (
                    <div key={member.id} className="flex items-center space-x-3 p-3 bg-muted/50 rounded-lg">
                      <Avatar className="w-10 h-10">
                        <AvatarImage src={member.avatar || "/placeholder.svg"} alt={member.name} />
                        <AvatarFallback>{member.name.charAt(0)}</AvatarFallback>
                      </Avatar>
                      <div>
                        <p className="font-medium">{member.name}</p>
                        <p className="text-sm text-muted-foreground">{member.role}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="font-medium">任务列表</h4>
                <div className="space-y-2">
                  {selectedProject.tasks.map((task) => (
                    <div key={task.id} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                      <div>
                        <p className="font-medium">{task.title}</p>
                        <p className="text-sm text-muted-foreground">负责人: {task.assignee}</p>
                      </div>
                      <Badge className={getStatusColor(task.status)}>{task.status}</Badge>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </>
  )
}
