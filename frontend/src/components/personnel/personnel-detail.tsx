"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Separator } from "@/components/ui/separator"
import { Progress } from "@/components/ui/progress"
import { ArrowLeft, Mail, Phone, Calendar, MapPin, Edit, MoreHorizontal, Award, Clock, TrendingUp } from "lucide-react"
import type { User } from "@/lib/mock-data"
import { getProjectsByUser } from "@/lib/mock-data"

interface PersonnelDetailProps {
  user: User
  onBack: () => void
  onEdit: (user: User) => void
}

export function PersonnelDetail({ user, onBack, onEdit }: PersonnelDetailProps) {
  const userProjects = getProjectsByUser(user.id)

  const getStatusBadge = (status: User["status"]) => {
    const variants = {
      active: "default",
      inactive: "secondary",
      on_leave: "outline",
    } as const

    const labels = {
      active: "在职",
      inactive: "离职",
      on_leave: "请假",
    }

    return (
      <Badge variant={variants[status]} className="text-xs">
        {labels[status]}
      </Badge>
    )
  }

  const getRoleBadge = (role: User["role"]) => {
    const variants = {
      admin: "destructive",
      hr: "default",
      manager: "secondary",
      employee: "outline",
    } as const

    const labels = {
      admin: "管理员",
      hr: "HR",
      manager: "经理",
      employee: "员工",
    }

    return (
      <Badge variant={variants[role]} className="text-xs">
        {labels[role]}
      </Badge>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="sm" onClick={onBack} className="gap-2">
            <ArrowLeft className="w-4 h-4" />
            返回列表
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-balance">员工详情</h1>
            <p className="text-muted-foreground mt-1">查看和管理员工详细信息</p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => onEdit(user)} className="gap-2">
            <Edit className="w-4 h-4" />
            编辑信息
          </Button>
          <Button variant="ghost" size="sm">
            <MoreHorizontal className="w-4 h-4" />
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Basic Info */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader className="text-center pb-4">
              <Avatar className="w-24 h-24 mx-auto mb-4">
                <AvatarFallback className="text-2xl">{user.name.slice(0, 2)}</AvatarFallback>
              </Avatar>
              <CardTitle className="text-xl">{user.name}</CardTitle>
              <div className="flex items-center justify-center gap-2 mt-2">
                {getRoleBadge(user.role)}
                {getStatusBadge(user.status)}
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-center gap-3 text-sm">
                  <Mail className="w-4 h-4 text-muted-foreground" />
                  <span>{user.email}</span>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <Phone className="w-4 h-4 text-muted-foreground" />
                  <span>{user.phone}</span>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <MapPin className="w-4 h-4 text-muted-foreground" />
                  <span>{user.department}</span>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <Calendar className="w-4 h-4 text-muted-foreground" />
                  <span>入职时间：{user.hireDate}</span>
                </div>
              </div>

              <Separator />

              <div>
                <h4 className="font-medium mb-3 flex items-center gap-2">
                  <TrendingUp className="w-4 h-4" />
                  工作负载
                </h4>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>当前负载</span>
                    <span>{user.workload}%</span>
                  </div>
                  <Progress value={user.workload} className="h-2" />
                  <p className="text-xs text-muted-foreground">
                    {user.workload > 90 ? "工作负载较重" : user.workload > 70 ? "工作负载适中" : "工作负载较轻"}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Detailed Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Skills */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Award className="w-5 h-5" />
                技能标签
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {user.skills.map((skill, index) => (
                  <Badge key={index} variant="secondary" className="text-sm">
                    {skill}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Projects */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Clock className="w-5 h-5" />
                参与项目
              </CardTitle>
            </CardHeader>
            <CardContent>
              {userProjects.length > 0 ? (
                <div className="space-y-4">
                  {userProjects.map((project) => (
                    <div key={project.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div>
                        <h4 className="font-medium">{project.name}</h4>
                        <p className="text-sm text-muted-foreground mt-1">{project.description}</p>
                        <div className="flex items-center gap-4 mt-2">
                          <Badge
                            variant={
                              project.status === "active"
                                ? "default"
                                : project.status === "completed"
                                  ? "secondary"
                                  : "outline"
                            }
                          >
                            {project.status === "active"
                              ? "进行中"
                              : project.status === "completed"
                                ? "已完成"
                                : project.status === "planning"
                                  ? "规划中"
                                  : "暂停"}
                          </Badge>
                          <span className="text-sm text-muted-foreground">
                            {project.startDate} - {project.endDate}
                          </span>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium">{project.progress}%</div>
                        <Progress value={project.progress} className="w-20 h-2 mt-1" />
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  <Clock className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>暂无参与的项目</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Work History */}
          <Card>
            <CardHeader>
              <CardTitle>工作履历</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-start gap-4">
                  <div className="w-2 h-2 bg-primary rounded-full mt-2"></div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h4 className="font-medium">{user.position}</h4>
                      <span className="text-sm text-muted-foreground">{user.hireDate} - 至今</span>
                    </div>
                    <p className="text-sm text-muted-foreground mt-1">{user.department}</p>
                    <p className="text-sm mt-2">
                      负责{user.department}的日常工作，具备{user.skills.join("、")}等专业技能。
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
