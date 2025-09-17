"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Progress } from "@/components/ui/progress"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import {
  Users,
  FolderOpen,
  Search,
  Filter,
  RotateCcw,
  Save,
  Clock,
  Star,
  AlertTriangle,
  ChevronDown,
  ChevronRight,
} from "lucide-react"
import { mockUsers, mockProjects } from "@/lib/mock-data"
import { User } from "lucide-react"

interface Assignment {
  userId: string
  projectId: string
  assignedAt: Date
}

export function DragDropScheduling() {
  const [availableUsers, setAvailableUsers] = useState(mockUsers.filter((user) => user.status === "active"))
  const [projects] = useState(mockProjects)
  const [assignments, setAssignments] = useState<Assignment[]>([])
  const [draggedUser, setDraggedUser] = useState<any>(null)
  const [searchTerm, setSearchTerm] = useState("")
  const [skillFilter, setSkillFilter] = useState("")
  const [expandedProjects, setExpandedProjects] = useState<Record<string, boolean>>({})

  // Filter available users based on search and skills
  const filteredUsers = availableUsers.filter((user) => {
    const matchesSearch =
      user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.position.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesSkill =
      !skillFilter || user.skills.some((skill) => skill.toLowerCase().includes(skillFilter.toLowerCase()))
    return matchesSearch && matchesSkill
  })

  // Get assigned users for a project
  const getAssignedUsers = (projectId) => {
    const projectAssignments = assignments.filter((a) => a.projectId === projectId)
    return projectAssignments.map((a) => mockUsers.find((u) => u.id === a.userId)).filter(Boolean)
  }

  // Handle drag start
  const handleDragStart = (e, user) => {
    setDraggedUser(user)
    e.dataTransfer.effectAllowed = "move"
  }

  // Handle drag over
  const handleDragOver = (e) => {
    e.preventDefault()
    e.dataTransfer.dropEffect = "move"
  }

  // Handle drop on project
  const handleDropOnProject = (e, projectId) => {
    e.preventDefault()
    if (!draggedUser) return

    // Check if user is already assigned to this project
    const isAlreadyAssigned = assignments.some((a) => a.userId === draggedUser.id && a.projectId === projectId)

    if (isAlreadyAssigned) return

    // Add assignment
    const newAssignment = {
      userId: draggedUser.id,
      projectId,
      assignedAt: new Date(),
    }

    setAssignments((prev) => [...prev, newAssignment])

    // Remove user from available pool
    setAvailableUsers((prev) => prev.filter((u) => u.id !== draggedUser.id))

    setDraggedUser(null)
  }

  // Handle removing user from project (drag back to pool)
  const handleRemoveFromProject = (userId, projectId) => {
    // Remove assignment
    setAssignments((prev) => prev.filter((a) => !(a.userId === userId && a.projectId === projectId)))

    // Add user back to available pool
    const user = mockUsers.find((u) => u.id === userId)
    if (user && !availableUsers.find((u) => u.id === userId)) {
      setAvailableUsers((prev) => [...prev, user])
    }
  }

  // Reset all assignments
  const handleReset = () => {
    setAssignments([])
    setAvailableUsers(mockUsers.filter((user) => user.status === "active"))
  }

  // Save assignments
  const handleSave = () => {
    console.log("Saving assignments:", assignments)
    // Here you would typically send to API
    alert("调度方案已保存！")
  }

  // Get skill match percentage
  const getSkillMatch = (user, project) => {
    const userSkills = user.skills.map((s) => s.toLowerCase())
    const requiredSkills = project.requiredSkills.map((s) => s.toLowerCase())
    const matchCount = requiredSkills.filter((skill) =>
      userSkills.some((userSkill) => userSkill.includes(skill)),
    ).length
    return requiredSkills.length > 0 ? Math.round((matchCount / requiredSkills.length) * 100) : 100
  }

  const toggleProjectExpansion = (projectId: string) => {
    setExpandedProjects((prev) => ({
      ...prev,
      [projectId]: !prev[projectId],
    }))
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-balance">拖拽式调度</h1>
          <p className="text-muted-foreground mt-1">通过拖拽方式将人员分配到项目中</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleReset}>
            <RotateCcw className="w-4 h-4 mr-2" />
            重置
          </Button>
          <Button onClick={handleSave}>
            <Save className="w-4 h-4 mr-2" />
            保存方案
          </Button>
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <Users className="w-5 h-5 text-blue-600" />
              <div>
                <div className="text-2xl font-bold">{availableUsers.length}</div>
                <div className="text-sm text-muted-foreground">可用人员</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <FolderOpen className="w-5 h-5 text-green-600" />
              <div>
                <div className="text-2xl font-bold">{projects.length}</div>
                <div className="text-sm text-muted-foreground">活跃项目</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <User className="w-5 h-5 text-purple-600" />
              <div>
                <div className="text-2xl font-bold">{assignments.length}</div>
                <div className="text-sm text-muted-foreground">已分配</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <Clock className="w-5 h-5 text-orange-600" />
              <div>
                <div className="text-2xl font-bold">
                  {Math.round((assignments.length / Math.max(mockUsers.length, 1)) * 100)}%
                </div>
                <div className="text-sm text-muted-foreground">分配率</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Panel - Available Resources */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="w-5 h-5" />
              人力资源池 ({filteredUsers.length})
            </CardTitle>
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="搜索姓名或职位..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-9"
                />
              </div>
              <div className="relative">
                <Filter className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="技能筛选..."
                  value={skillFilter}
                  onChange={(e) => setSkillFilter(e.target.value)}
                  className="pl-9 w-32"
                />
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {filteredUsers.map((user) => (
                <div
                  key={user.id}
                  draggable
                  onDragStart={(e) => handleDragStart(e, user)}
                  className="flex items-center gap-3 p-3 border rounded-lg cursor-move hover:bg-muted/50 transition-colors"
                >
                  <Avatar className="w-10 h-10">
                    <AvatarImage src={user.avatar || "/placeholder.svg"} />
                    <AvatarFallback>{user.name.slice(0, 2)}</AvatarFallback>
                  </Avatar>
                  <div className="flex-1 min-w-0">
                    <div className="font-medium truncate">{user.name}</div>
                    <div className="text-sm text-muted-foreground truncate">{user.position}</div>
                    <div className="flex items-center gap-1 mt-1">
                      <div className="text-xs text-muted-foreground">负载:</div>
                      <Progress value={user.workload} className="h-1 w-16" />
                      <div className="text-xs text-muted-foreground">{user.workload}%</div>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {user.skills.slice(0, 2).map((skill) => (
                      <Badge key={skill} variant="secondary" className="text-xs">
                        {skill}
                      </Badge>
                    ))}
                    {user.skills.length > 2 && (
                      <Badge variant="outline" className="text-xs">
                        +{user.skills.length - 2}
                      </Badge>
                    )}
                  </div>
                </div>
              ))}
              {filteredUsers.length === 0 && (
                <div className="text-center py-8 text-muted-foreground">
                  <Users className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <div>暂无可用人员</div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Right Panel - Projects */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FolderOpen className="w-5 h-5" />
              项目池 ({projects.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {projects.map((project) => {
                const assignedUsers = getAssignedUsers(project.id)
                const isExpanded = expandedProjects[project.id] || false

                return (
                  <div
                    key={project.id}
                    onDragOver={handleDragOver}
                    onDrop={(e) => handleDropOnProject(e, project.id)}
                    className="border rounded-lg hover:border-primary/50 transition-colors"
                  >
                    <Collapsible open={isExpanded} onOpenChange={() => toggleProjectExpansion(project.id)}>
                      <div className="p-4">
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex-1">
                            <div className="font-medium text-balance">{project.name}</div>
                            <div className="text-sm text-muted-foreground mt-1">{project.description}</div>
                          </div>
                          <div className="flex items-center gap-2">
                            <Badge
                              variant={
                                project.priority === "high"
                                  ? "destructive"
                                  : project.priority === "medium"
                                    ? "default"
                                    : "secondary"
                              }
                            >
                              {project.priority === "high"
                                ? "高优先级"
                                : project.priority === "medium"
                                  ? "中优先级"
                                  : "低优先级"}
                            </Badge>
                            <CollapsibleTrigger asChild>
                              <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                                {isExpanded ? (
                                  <ChevronDown className="w-4 h-4" />
                                ) : (
                                  <ChevronRight className="w-4 h-4" />
                                )}
                              </Button>
                            </CollapsibleTrigger>
                          </div>
                        </div>

                        {/* Required Skills */}
                        <div className="mb-3">
                          <div className="text-xs text-muted-foreground mb-1">所需技能:</div>
                          <div className="flex flex-wrap gap-1">
                            {project.requiredSkills.map((skill) => (
                              <Badge key={skill} variant="outline" className="text-xs">
                                {skill}
                              </Badge>
                            ))}
                          </div>
                        </div>

                        <div className="flex items-center justify-between text-sm">
                          <div className="flex items-center gap-2">
                            <Users className="w-4 h-4 text-muted-foreground" />
                            <span className="text-muted-foreground">已分配: {assignedUsers.length} 人</span>
                          </div>
                          {assignedUsers.length === 0 && (
                            <div className="text-xs text-muted-foreground">拖拽人员到此处分配</div>
                          )}
                        </div>
                      </div>

                      <CollapsibleContent>
                        <div className="px-4 pb-4 border-t bg-muted/20">
                          <div className="pt-3">
                            <div className="text-xs text-muted-foreground mb-2 font-medium">分配详情:</div>
                            {assignedUsers.length > 0 ? (
                              <div className="space-y-2">
                                {assignedUsers.map((user) => {
                                  const skillMatch = getSkillMatch(user, project)
                                  return (
                                    <div
                                      key={user.id}
                                      className="flex items-center gap-3 p-3 bg-background rounded-lg border"
                                    >
                                      <Avatar className="w-8 h-8">
                                        <AvatarImage src={user.avatar || "/placeholder.svg"} />
                                        <AvatarFallback className="text-xs">{user.name.slice(0, 2)}</AvatarFallback>
                                      </Avatar>
                                      <div className="flex-1 min-w-0">
                                        <div className="font-medium text-sm truncate">{user.name}</div>
                                        <div className="text-xs text-muted-foreground truncate">{user.position}</div>
                                        <div className="flex items-center gap-1 mt-1">
                                          <div className="text-xs text-muted-foreground">负载:</div>
                                          <Progress value={user.workload} className="h-1 w-12" />
                                          <div className="text-xs text-muted-foreground">{user.workload}%</div>
                                        </div>
                                      </div>
                                      <div className="flex items-center gap-2">
                                        <div className="flex items-center gap-1">
                                          {skillMatch >= 80 ? (
                                            <Star className="w-3 h-3 text-green-600" />
                                          ) : skillMatch >= 60 ? (
                                            <Star className="w-3 h-3 text-yellow-600" />
                                          ) : (
                                            <AlertTriangle className="w-3 h-3 text-red-600" />
                                          )}
                                          <span className="text-xs font-medium">{skillMatch}%</span>
                                        </div>
                                        <Button
                                          size="sm"
                                          variant="ghost"
                                          onClick={() => handleRemoveFromProject(user.id, project.id)}
                                          className="h-6 w-6 p-0 hover:bg-destructive/10 hover:text-destructive"
                                        >
                                          ×
                                        </Button>
                                      </div>
                                    </div>
                                  )
                                })}
                              </div>
                            ) : (
                              <div className="text-center py-6 text-muted-foreground border-2 border-dashed rounded-lg">
                                <Users className="w-8 h-8 mx-auto mb-2 opacity-50" />
                                <div className="text-sm">暂无分配人员</div>
                                <div className="text-xs mt-1">从左侧拖拽人员到此项目</div>
                              </div>
                            )}
                          </div>
                        </div>
                      </CollapsibleContent>
                    </Collapsible>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
