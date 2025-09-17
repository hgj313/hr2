"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Users, ChevronDown, ChevronRight } from "lucide-react"
import { mockDepartments, mockUsers, getUserById, type Department } from "@/lib/mock-data"
import { useState } from "react"

interface OrganizationChartProps {
  onUserSelect: (userId: string) => void
}

export function OrganizationChart({ onUserSelect }: OrganizationChartProps) {
  const [expandedDepts, setExpandedDepts] = useState<string[]>(["1", "2"])

  const toggleDepartment = (deptId: string) => {
    setExpandedDepts((prev) => (prev.includes(deptId) ? prev.filter((id) => id !== deptId) : [...prev, deptId]))
  }

  const getDepartmentMembers = (deptName: string) => {
    return mockUsers.filter((user) => user.department === deptName)
  }

  const renderDepartment = (dept: Department, level = 0) => {
    const manager = getUserById(dept.managerId)
    const members = getDepartmentMembers(dept.name)
    const isExpanded = expandedDepts.includes(dept.id)

    return (
      <div key={dept.id} className={`${level > 0 ? "ml-6 border-l border-border pl-4" : ""}`}>
        <Card className="mb-4">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Button variant="ghost" size="sm" onClick={() => toggleDepartment(dept.id)} className="p-1 h-6 w-6">
                  {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                </Button>
                <div>
                  <CardTitle className="text-lg">{dept.name}</CardTitle>
                  <p className="text-sm text-muted-foreground mt-1">{dept.description}</p>
                </div>
              </div>
              <Badge variant="secondary" className="gap-1">
                <Users className="w-3 h-3" />
                {dept.memberCount}人
              </Badge>
            </div>
          </CardHeader>

          {isExpanded && (
            <CardContent className="pt-0">
              {/* Department Manager */}
              {manager && (
                <div className="mb-4">
                  <h4 className="text-sm font-medium text-muted-foreground mb-2">部门负责人</h4>
                  <div
                    className="flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:bg-muted/50 transition-colors"
                    onClick={() => onUserSelect(manager.id)}
                  >
                    <Avatar className="w-8 h-8">
                      <AvatarFallback className="text-xs">{manager.name.slice(0, 2)}</AvatarFallback>
                    </Avatar>
                    <div>
                      <div className="font-medium text-sm">{manager.name}</div>
                      <div className="text-xs text-muted-foreground">{manager.position}</div>
                    </div>
                    <Badge variant="outline" className="ml-auto text-xs">
                      {manager.role === "admin"
                        ? "管理员"
                        : manager.role === "manager"
                          ? "经理"
                          : manager.role === "hr"
                            ? "HR"
                            : "员工"}
                    </Badge>
                  </div>
                </div>
              )}

              {/* Department Members */}
              {members.length > 1 && (
                <div>
                  <h4 className="text-sm font-medium text-muted-foreground mb-2">部门成员</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {members
                      .filter((member) => member.id !== dept.managerId)
                      .map((member) => (
                        <div
                          key={member.id}
                          className="flex items-center gap-3 p-2 border rounded cursor-pointer hover:bg-muted/50 transition-colors"
                          onClick={() => onUserSelect(member.id)}
                        >
                          <Avatar className="w-6 h-6">
                            <AvatarFallback className="text-xs">{member.name.slice(0, 2)}</AvatarFallback>
                          </Avatar>
                          <div className="flex-1 min-w-0">
                            <div className="font-medium text-sm truncate">{member.name}</div>
                            <div className="text-xs text-muted-foreground truncate">{member.position}</div>
                          </div>
                          <Badge variant={member.status === "active" ? "default" : "secondary"} className="text-xs">
                            {member.status === "active" ? "在职" : member.status === "on_leave" ? "请假" : "离职"}
                          </Badge>
                        </div>
                      ))}
                  </div>
                </div>
              )}
            </CardContent>
          )}
        </Card>

        {/* Render child departments if any */}
        {mockDepartments
          .filter((childDept) => childDept.parentId === dept.id)
          .map((childDept) => renderDepartment(childDept, level + 1))}
      </div>
    )
  }

  const rootDepartments = mockDepartments.filter((dept) => !dept.parentId)

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-balance">组织架构</h1>
        <p className="text-muted-foreground mt-1">查看企业组织结构和人员分布</p>
      </div>

      <div className="space-y-4">{rootDepartments.map((dept) => renderDepartment(dept))}</div>
    </div>
  )
}
