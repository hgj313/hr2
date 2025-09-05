"use client"

import { useState } from "react"
import { UserForm } from "./user-form"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { MoreHorizontal, Edit, Trash2, Eye, MapPin, Award } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"

interface User {
  id: string
  name: string
  email: string
  department: string
  position: string
  skills: string[]
  level: string
  status: string
  avatar: string
  phone: string
  joinDate: string
  workload: number
  region: string
  specialization: string
  certifications: string[]
  experience: number
}

interface UserListProps {
  users: User[]
  onUserUpdate: (users: User[]) => void
}

export function UserList({ users, onUserUpdate }: UserListProps) {
  const [selectedUser, setSelectedUser] = useState<User | null>(null)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [isDetailDialogOpen, setIsDetailDialogOpen] = useState(false)

  const handleEditUser = (user: User) => {
    setSelectedUser(user)
    setIsEditDialogOpen(true)
  }

  const handleViewUser = (user: User) => {
    setSelectedUser(user)
    setIsDetailDialogOpen(true)
  }

  const handleDeleteUser = (userId: string) => {
    if (confirm("确定要删除这个员工吗？")) {
      const updatedUsers = users.filter((user) => user.id !== userId)
      onUserUpdate(updatedUsers)
    }
  }

  const handleUpdateUser = (userData: any) => {
    const updatedUsers = users.map((user) => (user.id === selectedUser?.id ? { ...user, ...userData } : user))
    onUserUpdate(updatedUsers)
    setIsEditDialogOpen(false)
    setSelectedUser(null)
  }

  const getWorkloadColor = (workload: number) => {
    if (workload >= 90) return "bg-red-500"
    if (workload >= 70) return "bg-yellow-500"
    return "bg-green-500"
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "在职":
        return "bg-green-100 text-green-800"
      case "离职":
        return "bg-red-100 text-red-800"
      case "休假":
        return "bg-yellow-100 text-yellow-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getRegionColor = (region: string) => {
    switch (region) {
      case "华中":
        return "bg-blue-100 text-blue-800"
      case "华南":
        return "bg-green-100 text-green-800"
      case "华东":
        return "bg-purple-100 text-purple-800"
      case "西南":
        return "bg-orange-100 text-orange-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  return (
    <>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {users.map((user) => (
          <Card key={user.id} className="border-border/50 hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                    <span className="text-sm font-medium text-green-700">{user.name.charAt(0)}</span>
                  </div>
                  <div>
                    <CardTitle className="text-base">{user.name}</CardTitle>
                    <p className="text-sm text-muted-foreground">{user.position}</p>
                  </div>
                </div>

                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="sm">
                      <MoreHorizontal className="w-4 h-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={() => handleViewUser(user)}>
                      <Eye className="w-4 h-4 mr-2" />
                      查看详情
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handleEditUser(user)}>
                      <Edit className="w-4 h-4 mr-2" />
                      编辑
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handleDeleteUser(user.id)} className="text-red-600">
                      <Trash2 className="w-4 h-4 mr-2" />
                      删除
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </CardHeader>

            <CardContent className="space-y-3">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">部门:</span>
                <span>{user.department}</span>
              </div>

              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">区域:</span>
                <Badge className={getRegionColor(user.region)}>
                  <MapPin className="w-3 h-3 mr-1" />
                  {user.region}
                </Badge>
              </div>

              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">专业:</span>
                <span className="text-xs bg-emerald-100 text-emerald-700 px-2 py-1 rounded">{user.specialization}</span>
              </div>

              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">经验:</span>
                <span className="font-medium">{user.experience}年</span>
              </div>

              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">级别:</span>
                <Badge variant="outline">{user.level}</Badge>
              </div>

              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">状态:</span>
                <Badge className={getStatusColor(user.status)}>{user.status}</Badge>
              </div>

              <div className="space-y-2">
                <span className="text-sm text-muted-foreground">工作负载:</span>
                <span>{user.workload}%</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div
                  className={`h-2 rounded-full ${getWorkloadColor(user.workload)}`}
                  style={{ width: `${user.workload}%` }}
                />
              </div>

              <div className="space-y-2">
                <span className="text-sm text-muted-foreground">技能标签:</span>
                <div className="flex flex-wrap gap-1">
                  {user.skills.slice(0, 3).map((skill) => (
                    <Badge key={skill} variant="secondary" className="text-xs bg-green-100 text-green-800">
                      {skill}
                    </Badge>
                  ))}
                  {user.skills.length > 3 && (
                    <Badge variant="secondary" className="text-xs">
                      +{user.skills.length - 3}
                    </Badge>
                  )}
                </div>
              </div>

              {user.certifications && user.certifications.length > 0 && (
                <div className="space-y-2">
                  <span className="text-sm text-muted-foreground">资质证书:</span>
                  <div className="flex flex-wrap gap-1">
                    {user.certifications.slice(0, 2).map((cert) => (
                      <Badge key={cert} variant="secondary" className="text-xs bg-blue-100 text-blue-800">
                        <Award className="w-3 h-3 mr-1" />
                        {cert}
                      </Badge>
                    ))}
                    {user.certifications.length > 2 && (
                      <Badge variant="secondary" className="text-xs">
                        +{user.certifications.length - 2}
                      </Badge>
                    )}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>编辑员工信息</DialogTitle>
          </DialogHeader>
          {selectedUser && <UserForm initialData={selectedUser} onSubmit={handleUpdateUser} />}
        </DialogContent>
      </Dialog>

      <Dialog open={isDetailDialogOpen} onOpenChange={setIsDetailDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>园林专业人员详细信息</DialogTitle>
          </DialogHeader>
          {selectedUser && (
            <div className="space-y-6">
              <div className="flex items-center space-x-4">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="text-xl font-medium text-green-700">{selectedUser.name.charAt(0)}</span>
                </div>
                <div>
                  <h3 className="text-xl font-semibold">{selectedUser.name}</h3>
                  <p className="text-muted-foreground">{selectedUser.position}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <Badge className={getRegionColor(selectedUser.region)} variant="secondary">
                      <MapPin className="w-3 h-3 mr-1" />
                      {selectedUser.region}
                    </Badge>
                    <span className="text-sm text-emerald-600">{selectedUser.specialization}</span>
                  </div>
                </div>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <label className="text-sm font-medium text-muted-foreground">邮箱</label>
                  <p className="mt-1">{selectedUser.email}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">电话</label>
                  <p className="mt-1">{selectedUser.phone}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">部门</label>
                  <p className="mt-1">{selectedUser.department}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">入职日期</label>
                  <p className="mt-1">{selectedUser.joinDate}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">工作经验</label>
                  <p className="mt-1">{selectedUser.experience} 年</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">专业领域</label>
                  <p className="mt-1">{selectedUser.specialization}</p>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-muted-foreground">专业技能</label>
                <div className="flex flex-wrap gap-2 mt-2">
                  {selectedUser.skills.map((skill) => (
                    <Badge key={skill} variant="secondary" className="bg-green-100 text-green-800">
                      {skill}
                    </Badge>
                  ))}
                </div>
              </div>

              {selectedUser.certifications && selectedUser.certifications.length > 0 && (
                <div>
                  <label className="text-sm font-medium text-muted-foreground">资质证书</label>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {selectedUser.certifications.map((cert) => (
                      <Badge key={cert} variant="secondary" className="bg-blue-100 text-blue-800">
                        <Award className="w-3 h-3 mr-1" />
                        {cert}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>
    </>
  )
}
