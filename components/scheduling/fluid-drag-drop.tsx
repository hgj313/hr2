"use client"

import type React from "react"

import { useState, useRef } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Users, Zap, Target, TrendingUp, AlertTriangle, CheckCircle } from "lucide-react"

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

interface Project {
  id: string
  name: string
  requiredSkills: string[]
  priority: string
  deadline: string
  estimatedHours: number
  assignedStaff: Staff[]
  status: string
  progress: number
  budget: number
}

interface FluidDragDropProps {
  staff: Staff[]
  projects: Project[]
  onAssignment: (staffId: string, projectId: string) => void
}

export function FluidDragDrop({ staff, projects, onAssignment }: FluidDragDropProps) {
  const [draggedStaff, setDraggedStaff] = useState<Staff | null>(null)
  const [dragPosition, setDragPosition] = useState({ x: 0, y: 0 })
  const [hoveredProject, setHoveredProject] = useState<string | null>(null)
  const [matchScores, setMatchScores] = useState<Record<string, number>>({})
  const [aiRecommendations, setAiRecommendations] = useState<string[]>([])
  const [connectionPaths, setConnectionPaths] = useState<any[]>([])
  const dragRef = useRef<HTMLDivElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  // 计算技能匹配度
  const calculateSkillMatch = (staffSkills: string[], requiredSkills: string[]): number => {
    const matchedSkills = staffSkills.filter((skill) => requiredSkills.includes(skill))
    const matchScore = matchedSkills.length / requiredSkills.length
    const bonusScore = matchedSkills.length > requiredSkills.length ? 0.1 : 0
    return Math.min(1, matchScore + bonusScore)
  }

  // 计算综合匹配度（技能 + 工作负载 + 效率）
  const calculateOverallMatch = (staff: Staff, project: Project): number => {
    const skillMatch = calculateSkillMatch(staff.skills, project.requiredSkills)
    const workloadScore = (100 - staff.workload) / 100 // 工作负载越低分数越高
    const efficiencyScore = staff.efficiency / 100
    const availabilityScore = staff.availability === "可用" ? 1 : 0.3

    return skillMatch * 0.4 + workloadScore * 0.2 + efficiencyScore * 0.3 + availabilityScore * 0.1
  }

  // AI推荐算法
  const generateAIRecommendations = (staff: Staff) => {
    const recommendations = projects
      .map((project) => ({
        projectId: project.id,
        score: calculateOverallMatch(staff, project),
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, 3)
      .filter((rec) => rec.score > 0.6)
      .map((rec) => rec.projectId)

    setAiRecommendations(recommendations)
  }

  // 生成连接路径动画
  const generateConnectionPaths = (staffElement: HTMLElement, projectElements: HTMLElement[]) => {
    const staffRect = staffElement.getBoundingClientRect()
    const containerRect = containerRef.current?.getBoundingClientRect()

    if (!containerRect) return

    const paths = projectElements.map((projectElement, index) => {
      const projectRect = projectElement.getBoundingClientRect()

      const startX = staffRect.left + staffRect.width / 2 - containerRect.left
      const startY = staffRect.top + staffRect.height / 2 - containerRect.top
      const endX = projectRect.left + projectRect.width / 2 - containerRect.left
      const endY = projectRect.top + projectRect.height / 2 - containerRect.top

      // 创建贝塞尔曲线路径
      const controlX1 = startX + (endX - startX) * 0.3
      const controlY1 = startY - 50
      const controlX2 = startX + (endX - startX) * 0.7
      const controlY2 = endY - 50

      return {
        id: `path-${index}`,
        d: `M ${startX} ${startY} C ${controlX1} ${controlY1}, ${controlX2} ${controlY2}, ${endX} ${endY}`,
        opacity: 0.8 - index * 0.2,
        delay: index * 0.1,
      }
    })

    setConnectionPaths(paths)
  }

  const handleDragStart = (e: React.DragEvent, staff: Staff) => {
    setDraggedStaff(staff)

    // 计算所有项目的匹配度
    const scores: Record<string, number> = {}
    projects.forEach((project) => {
      scores[project.id] = calculateOverallMatch(staff, project)
    })
    setMatchScores(scores)

    // 生成AI推荐
    generateAIRecommendations(staff)

    // 设置拖拽数据
    e.dataTransfer.setData("text/plain", staff.id)
    e.dataTransfer.effectAllowed = "move"
  }

  const handleDrag = (e: React.DragEvent) => {
    if (e.clientX !== 0 && e.clientY !== 0) {
      setDragPosition({ x: e.clientX, y: e.clientY })
    }
  }

  const handleDragEnd = () => {
    setDraggedStaff(null)
    setMatchScores({})
    setAiRecommendations([])
    setConnectionPaths([])
    setHoveredProject(null)
  }

  const handleDragOver = (e: React.DragEvent, projectId: string) => {
    e.preventDefault()
    setHoveredProject(projectId)
  }

  const handleDragLeave = () => {
    setHoveredProject(null)
  }

  const handleDrop = (e: React.DragEvent, projectId: string) => {
    e.preventDefault()
    const staffId = e.dataTransfer.getData("text/plain")

    if (staffId && draggedStaff) {
      const matchScore = matchScores[projectId] || 0

      // 显示匹配度反馈
      if (matchScore < 0.3) {
        // 低匹配度警告
        return
      }

      onAssignment(staffId, projectId)
    }

    handleDragEnd()
  }

  const getMatchColor = (score: number) => {
    if (score >= 0.8) return "text-green-400 border-green-400 bg-green-400/20"
    if (score >= 0.6) return "text-amber-400 border-amber-400 bg-amber-400/20"
    if (score >= 0.4) return "text-orange-400 border-orange-400 bg-orange-400/20"
    return "text-red-400 border-red-400 bg-red-400/20"
  }

  const getMatchIcon = (score: number) => {
    if (score >= 0.8) return <CheckCircle className="w-4 h-4" />
    if (score >= 0.6) return <Target className="w-4 h-4" />
    if (score >= 0.4) return <TrendingUp className="w-4 h-4" />
    return <AlertTriangle className="w-4 h-4" />
  }

  return (
    <div ref={containerRef} className="relative space-y-6">
      {/* AI推荐连线动画 */}
      {draggedStaff && connectionPaths.length > 0 && (
        <svg className="absolute inset-0 pointer-events-none z-10" style={{ width: "100%", height: "100%" }}>
          {connectionPaths.map((path, index) => (
            <g key={path.id}>
              <path
                d={path.d}
                stroke="url(#aiGradient)"
                strokeWidth="2"
                fill="none"
                opacity={path.opacity}
                className="animate-pulse"
                style={{
                  animation: `drawPath 1s ease-out ${path.delay}s forwards`,
                  strokeDasharray: "5,5",
                  strokeDashoffset: "10",
                }}
              />
              <circle
                r="3"
                fill="#fbbf24"
                className="animate-ping"
                style={{
                  animation: `moveAlongPath 2s ease-in-out ${path.delay}s infinite`,
                }}
              >
                <animateMotion dur="2s" repeatCount="indefinite" begin={`${path.delay}s`}>
                  <mpath href={`#${path.id}`} />
                </animateMotion>
              </circle>
            </g>
          ))}
          <defs>
            <linearGradient id="aiGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#fbbf24" stopOpacity="0.8" />
              <stop offset="50%" stopColor="#a855f7" stopOpacity="0.6" />
              <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.4" />
            </linearGradient>
          </defs>
        </svg>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        {/* 人员池 */}
        <Card className="luxury-card">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <Users className="w-5 h-5 mr-2" />
              智能人员池
              {draggedStaff && (
                <Badge className="ml-2 bg-purple-500/20 text-purple-300 border-purple-400">AI分析中</Badge>
              )}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-3">
              {staff.map((person, index) => (
                <div
                  key={person.id}
                  draggable
                  onDragStart={(e) => handleDragStart(e, person)}
                  onDrag={handleDrag}
                  onDragEnd={handleDragEnd}
                  className={`
                    relative p-4 rounded-lg border-2 cursor-move transition-all duration-300
                    ${
                      draggedStaff?.id === person.id
                        ? "border-purple-400 bg-purple-400/20 scale-105 glow-accent"
                        : "border-white/20 bg-white/5 hover:border-white/40 hover:bg-white/10"
                    }
                    floating-animation
                  `}
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  {/* 拖拽指示器 */}
                  <div className="absolute top-2 right-2">
                    <div className="w-2 h-2 bg-white/40 rounded-full"></div>
                    <div className="w-2 h-2 bg-white/40 rounded-full mt-1"></div>
                    <div className="w-2 h-2 bg-white/40 rounded-full mt-1"></div>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <h4 className="text-white font-semibold">{person.name}</h4>
                      <Badge variant="outline" className="text-xs">
                        {person.level}
                      </Badge>
                    </div>

                    <p className="text-white/70 text-sm">{person.position}</p>

                    <div className="flex flex-wrap gap-1">
                      {person.skills.slice(0, 3).map((skill) => (
                        <Badge key={skill} variant="secondary" className="text-xs">
                          {skill}
                        </Badge>
                      ))}
                    </div>

                    <div className="flex items-center justify-between text-xs text-white/70">
                      <span>负载: {person.workload}%</span>
                      <span>效率: {person.efficiency}%</span>
                    </div>
                  </div>

                  {/* 流体效果 */}
                  {draggedStaff?.id === person.id && (
                    <div className="absolute inset-0 rounded-lg overflow-hidden">
                      <div className="absolute inset-0 bg-gradient-to-r from-purple-400/20 via-blue-400/20 to-purple-400/20 animate-pulse"></div>
                      <div className="absolute inset-0 bg-gradient-to-br from-transparent via-white/5 to-transparent animate-ping"></div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* 项目分配区 */}
        <Card className="luxury-card">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <Target className="w-5 h-5 mr-2" />
              智能项目匹配
              {draggedStaff && <Badge className="ml-2 bg-blue-500/20 text-blue-300 border-blue-400">显示匹配度</Badge>}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {projects.map((project, index) => {
                const matchScore = matchScores[project.id] || 0
                const isRecommended = aiRecommendations.includes(project.id)
                const isHovered = hoveredProject === project.id

                return (
                  <div
                    key={project.id}
                    onDragOver={(e) => handleDragOver(e, project.id)}
                    onDragLeave={handleDragLeave}
                    onDrop={(e) => handleDrop(e, project.id)}
                    className={`
                      relative p-4 rounded-lg border-2 transition-all duration-300
                      ${
                        draggedStaff
                          ? `${getMatchColor(matchScore)} ${isHovered ? "scale-105 glow-accent" : ""}`
                          : "border-white/20 bg-white/5"
                      }
                      ${isRecommended ? "ring-2 ring-amber-400/50" : ""}
                      floating-animation
                    `}
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    {/* AI推荐标识 */}
                    {isRecommended && (
                      <div className="absolute -top-2 -right-2">
                        <div className="bg-amber-400 text-black rounded-full p-1">
                          <Zap className="w-3 h-3" />
                        </div>
                      </div>
                    )}

                    {/* 匹配度指示器 */}
                    {draggedStaff && (
                      <div className="absolute top-2 right-2 flex items-center space-x-1">
                        {getMatchIcon(matchScore)}
                        <span className="text-xs font-bold">{Math.round(matchScore * 100)}%</span>
                      </div>
                    )}

                    <div className="space-y-3">
                      <div>
                        <h4 className="text-white font-semibold mb-1">{project.name}</h4>
                        <Badge variant={project.priority === "高" ? "destructive" : "secondary"}>
                          {project.priority}优先级
                        </Badge>
                      </div>

                      <div className="flex flex-wrap gap-1">
                        {project.requiredSkills.map((skill) => (
                          <Badge
                            key={skill}
                            variant="outline"
                            className={`text-xs ${
                              draggedStaff?.skills.includes(skill) ? "border-green-400 text-green-400" : ""
                            }`}
                          >
                            {skill}
                          </Badge>
                        ))}
                      </div>

                      <div className="flex items-center justify-between text-xs text-white/70">
                        <span>预算: ¥{(project.budget / 1000).toFixed(0)}k</span>
                        <span>工时: {project.estimatedHours}h</span>
                      </div>

                      {/* 已分配人员 */}
                      {project.assignedStaff.length > 0 && (
                        <div className="flex items-center space-x-2">
                          <Users className="w-3 h-3 text-white/70" />
                          <span className="text-xs text-white/70">已分配 {project.assignedStaff.length} 人</span>
                        </div>
                      )}
                    </div>

                    {/* 匹配度进度条 */}
                    {draggedStaff && (
                      <div className="mt-3 space-y-1">
                        <div className="flex justify-between text-xs">
                          <span className="text-white/70">匹配度</span>
                          <span className="text-white">{Math.round(matchScore * 100)}%</span>
                        </div>
                        <div className="w-full bg-white/10 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full transition-all duration-500 ${
                              matchScore >= 0.8
                                ? "bg-green-400"
                                : matchScore >= 0.6
                                  ? "bg-amber-400"
                                  : matchScore >= 0.4
                                    ? "bg-orange-400"
                                    : "bg-red-400"
                            }`}
                            style={{ width: `${matchScore * 100}%` }}
                          />
                        </div>
                      </div>
                    )}

                    {/* 流体拖拽效果 */}
                    {isHovered && draggedStaff && (
                      <div className="absolute inset-0 rounded-lg overflow-hidden pointer-events-none">
                        <div className="absolute inset-0 bg-gradient-to-r from-blue-400/10 via-purple-400/10 to-blue-400/10 animate-pulse"></div>
                        <div className="absolute inset-0 border-2 border-blue-400/50 rounded-lg animate-ping"></div>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 拖拽跟随指示器 */}
      {draggedStaff && (
        <div
          className="fixed pointer-events-none z-50 transform -translate-x-1/2 -translate-y-1/2"
          style={{ left: dragPosition.x, top: dragPosition.y }}
        >
          <div className="bg-purple-500/90 text-white px-3 py-2 rounded-lg shadow-lg backdrop-blur-sm">
            <div className="text-sm font-medium">{draggedStaff.name}</div>
            <div className="text-xs opacity-80">{draggedStaff.position}</div>
          </div>
        </div>
      )}
    </div>
  )
}
