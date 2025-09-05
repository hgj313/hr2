"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Calendar, Users, Clock, DollarSign, CheckCircle, Circle, ZoomIn, ZoomOut, Filter } from "lucide-react"

interface Project {
  id: string
  name: string
  requiredSkills: string[]
  priority: string
  deadline: string
  estimatedHours: number
  assignedStaff: any[]
  status: string
  progress: number
  budget: number
  department?: string
  complexity?: string
}

interface ProjectOverviewMapProps {
  projects: Project[]
  onProjectSelect?: (project: Project) => void
}

export function ProjectOverviewMap({ projects, onProjectSelect }: ProjectOverviewMapProps) {
  const [zoomLevel, setZoomLevel] = useState(1)
  const [filterBy, setFilterBy] = useState<"all" | "priority" | "department" | "status">("all")
  const [selectedProject, setSelectedProject] = useState<string | null>(null)

  // 按不同维度分组项目
  const groupedProjects = {
    priority: {
      高: projects.filter((p) => p.priority === "高"),
      中: projects.filter((p) => p.priority === "中"),
      低: projects.filter((p) => p.priority === "低"),
    },
    status: {
      待分配: projects.filter((p) => p.status === "待分配"),
      已分配: projects.filter((p) => p.status === "已分配"),
      进行中: projects.filter((p) => p.status === "进行中"),
      已完成: projects.filter((p) => p.status === "已完成"),
    },
    department: {
      技术部: projects.filter((p) =>
        p.requiredSkills.some((skill) => ["React", "Node.js", "Python", "TypeScript"].includes(skill)),
      ),
      设计部: projects.filter((p) =>
        p.requiredSkills.some((skill) => ["UI设计", "Figma", "Photoshop"].includes(skill)),
      ),
      产品部: projects.filter((p) => p.requiredSkills.some((skill) => ["产品设计", "需求分析"].includes(skill))),
    },
  }

  const getProjectStatusIcon = (status: string) => {
    switch (status) {
      case "已完成":
        return <CheckCircle className="w-4 h-4 text-green-400" />
      case "进行中":
        return <Clock className="w-4 h-4 text-blue-400" />
      case "已分配":
        return <Users className="w-4 h-4 text-amber-400" />
      default:
        return <Circle className="w-4 h-4 text-gray-400" />
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "高":
        return "border-red-400 bg-red-400/10"
      case "中":
        return "border-amber-400 bg-amber-400/10"
      case "低":
        return "border-green-400 bg-green-400/10"
      default:
        return "border-gray-400 bg-gray-400/10"
    }
  }

  const handleProjectClick = (project: Project) => {
    setSelectedProject(project.id)
    onProjectSelect?.(project)
  }

  return (
    <div className="space-y-6">
      {/* 控制面板 */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setZoomLevel(Math.max(0.5, zoomLevel - 0.25))}
            className="luxury-button text-white border-white/30"
          >
            <ZoomOut className="w-4 h-4" />
          </Button>
          <span className="text-white/80 text-sm">缩放: {Math.round(zoomLevel * 100)}%</span>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setZoomLevel(Math.min(2, zoomLevel + 0.25))}
            className="luxury-button text-white border-white/30"
          >
            <ZoomIn className="w-4 h-4" />
          </Button>
        </div>

        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-white/60" />
          <select
            value={filterBy}
            onChange={(e) => setFilterBy(e.target.value as any)}
            className="bg-white/10 border border-white/20 rounded px-3 py-1 text-white text-sm"
          >
            <option value="all">全部项目</option>
            <option value="priority">按优先级</option>
            <option value="status">按状态</option>
            <option value="department">按部门</option>
          </select>
        </div>
      </div>

      {/* 项目全景地图 */}
      <div
        className="relative overflow-hidden rounded-xl glass-morphism p-6"
        style={{ transform: `scale(${zoomLevel})`, transformOrigin: "top left" }}
      >
        {filterBy === "all" ? (
          // 网格布局显示所有项目
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {projects.map((project, index) => (
              <div
                key={project.id}
                className={`
                  relative p-4 rounded-lg border-2 cursor-pointer transition-all duration-300
                  ${getPriorityColor(project.priority)}
                  ${selectedProject === project.id ? "glow-accent scale-105" : "hover:scale-102"}
                  floating-animation
                `}
                style={{ animationDelay: `${index * 0.1}s` }}
                onClick={() => handleProjectClick(project)}
              >
                {/* 项目状态指示器 */}
                <div className="absolute top-2 right-2">{getProjectStatusIcon(project.status)}</div>

                {/* 项目信息 */}
                <div className="space-y-3">
                  <div>
                    <h4 className="text-white font-semibold text-sm mb-1">{project.name}</h4>
                    <Badge variant="outline" className="text-xs">
                      {project.priority}优先级
                    </Badge>
                  </div>

                  {/* 进度条 */}
                  <div className="space-y-1">
                    <div className="flex justify-between text-xs text-white/70">
                      <span>进度</span>
                      <span>{project.progress}%</span>
                    </div>
                    <div className="w-full bg-white/10 rounded-full h-1.5">
                      <div
                        className="h-1.5 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-500"
                        style={{ width: `${project.progress}%` }}
                      />
                    </div>
                  </div>

                  {/* 关键指标 */}
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="flex items-center text-white/70">
                      <Users className="w-3 h-3 mr-1" />
                      {project.assignedStaff.length}人
                    </div>
                    <div className="flex items-center text-white/70">
                      <Clock className="w-3 h-3 mr-1" />
                      {project.estimatedHours}h
                    </div>
                    <div className="flex items-center text-white/70">
                      <DollarSign className="w-3 h-3 mr-1" />
                      {(project.budget / 1000).toFixed(0)}k
                    </div>
                    <div className="flex items-center text-white/70">
                      <Calendar className="w-3 h-3 mr-1" />
                      {new Date(project.deadline).toLocaleDateString("zh-CN", { month: "short", day: "numeric" })}
                    </div>
                  </div>
                </div>

                {/* 紧急程度指示 */}
                {project.priority === "高" && (
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-400 rounded-full pulse-glow" />
                )}
              </div>
            ))}
          </div>
        ) : (
          // 分组显示
          <div className="space-y-8">
            {Object.entries(groupedProjects[filterBy]).map(([groupName, groupProjects]) => (
              <div key={groupName} className="space-y-4">
                <div className="flex items-center space-x-3">
                  <h3 className="text-xl font-bold text-white">{groupName}</h3>
                  <Badge variant="outline" className="text-white/70">
                    {groupProjects.length} 个项目
                  </Badge>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {groupProjects.map((project, index) => (
                    <div
                      key={project.id}
                      className={`
                        relative p-4 rounded-lg border-2 cursor-pointer transition-all duration-300
                        ${getPriorityColor(project.priority)}
                        ${selectedProject === project.id ? "glow-accent scale-105" : "hover:scale-102"}
                        floating-animation
                      `}
                      style={{ animationDelay: `${index * 0.1}s` }}
                      onClick={() => handleProjectClick(project)}
                    >
                      <div className="absolute top-2 right-2">{getProjectStatusIcon(project.status)}</div>

                      <div className="space-y-2">
                        <h4 className="text-white font-medium text-sm">{project.name}</h4>

                        <div className="flex items-center justify-between text-xs text-white/70">
                          <span>{project.assignedStaff.length} 人员</span>
                          <span>{project.progress}% 完成</span>
                        </div>

                        <div className="w-full bg-white/10 rounded-full h-1">
                          <div
                            className="h-1 rounded-full bg-gradient-to-r from-blue-400 to-purple-400"
                            style={{ width: `${project.progress}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 选中项目详情 */}
      {selectedProject && (
        <Card className="luxury-card">
          <CardHeader>
            <CardTitle className="text-white">项目详情</CardTitle>
          </CardHeader>
          <CardContent>
            {(() => {
              const project = projects.find((p) => p.id === selectedProject)
              if (!project) return null

              return (
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-3">
                    <div>
                      <label className="text-sm text-white/70">项目名称</label>
                      <p className="text-white font-medium">{project.name}</p>
                    </div>
                    <div>
                      <label className="text-sm text-white/70">所需技能</label>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {project.requiredSkills.map((skill) => (
                          <Badge key={skill} variant="outline" className="text-xs">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    <div>
                      <label className="text-sm text-white/70">截止日期</label>
                      <p className="text-white">{project.deadline}</p>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <div>
                      <label className="text-sm text-white/70">预算</label>
                      <p className="text-white font-medium">¥{project.budget.toLocaleString()}</p>
                    </div>
                    <div>
                      <label className="text-sm text-white/70">预估工时</label>
                      <p className="text-white">{project.estimatedHours} 小时</p>
                    </div>
                    <div>
                      <label className="text-sm text-white/70">分配人员</label>
                      <p className="text-white">{project.assignedStaff.length} 人</p>
                    </div>
                  </div>
                </div>
              )
            })()}
          </CardContent>
        </Card>
      )}
    </div>
  )
}
