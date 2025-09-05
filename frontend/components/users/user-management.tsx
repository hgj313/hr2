"use client"

import { useState } from "react"
import { Plus, Search, Filter, MoreHorizontal, Edit, Trash2, UserCheck, UserX } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useUsers, useDeleteUser, useUpdateUser } from "@/lib/api/hooks"
import { UserCreateDialog } from "./user-create-dialog"
import { UserEditDialog } from "./user-edit-dialog"
import { User, UserRole, UserStatus } from "@/lib/api/types"
import { useToast } from "@/hooks/use-toast"

const roleLabels: Record<UserRole, string> = {
  admin: "管理员",
  manager: "经理",
  employee: "员工",
  viewer: "查看者"
}

const statusLabels: Record<UserStatus, string> = {
  active: "活跃",
  inactive: "停用",
  pending: "待激活"
}

const getRoleBadgeVariant = (role: UserRole) => {
  switch (role) {
    case "admin": return "destructive"
    case "manager": return "default"
    case "employee": return "secondary"
    case "viewer": return "outline"
    default: return "secondary"
  }
}

const getStatusBadgeVariant = (status: UserStatus) => {
  switch (status) {
    case "active": return "default"
    case "inactive": return "secondary"
    case "pending": return "outline"
    default: return "secondary"
  }
}

export function UserManagement() {
  const [searchTerm, setSearchTerm] = useState("")
  const [roleFilter, setRoleFilter] = useState<UserRole | "all">("all")
  const [statusFilter, setStatusFilter] = useState<UserStatus | "all">("all")
  const [createDialogOpen, setCreateDialogOpen] = useState(false)
  const [editDialogOpen, setEditDialogOpen] = useState(false)
  const [selectedUser, setSelectedUser] = useState<User | null>(null)

  const { toast } = useToast()
  const { data: users, isLoading, error } = useUsers()
  const deleteUserMutation = useDeleteUser()
  const updateUserMutation = useUpdateUser()

  // 过滤用户列表
  const filteredUsers = users?.filter((user) => {
    const matchesSearch = user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.full_name?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesRole = roleFilter === "all" || user.role === roleFilter
    const matchesStatus = statusFilter === "all" || user.status === statusFilter
    return matchesSearch && matchesRole && matchesStatus
  }) || []

  const handleDeleteUser = async (userId: string) => {
    if (window.confirm("确定要删除这个用户吗？此操作不可撤销。")) {
      try {
        await deleteUserMutation.mutateAsync(userId)
        toast({
          title: "删除成功",
          description: "用户已成功删除",
        })
      } catch (error) {
        toast({
          title: "删除失败",
          description: "删除用户时发生错误，请重试",
          variant: "destructive",
        })
      }
    }
  }

  const handleToggleUserStatus = async (user: User) => {
    const newStatus: UserStatus = user.status === "active" ? "inactive" : "active"
    try {
      await updateUserMutation.mutateAsync({
        id: user.id,
        data: { status: newStatus }
      })
      toast({
        title: "状态更新成功",
        description: `用户状态已更新为${statusLabels[newStatus]}`,
      })
    } catch (error) {
      toast({
        title: "状态更新失败",
        description: "更新用户状态时发生错误，请重试",
        variant: "destructive",
      })
    }
  }

  const handleEditUser = (user: User) => {
    setSelectedUser(user)
    setEditDialogOpen(true)
  }

  if (error) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center h-64">
          <div className="text-center">
            <p className="text-muted-foreground">加载用户数据时发生错误</p>
            <Button variant="outline" className="mt-2" onClick={() => window.location.reload()}>
              重试
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {/* 操作栏 */}
      <Card>
        <CardHeader>
          <CardTitle>用户列表</CardTitle>
          <CardDescription>
            管理系统中的所有用户账号
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
                <Input
                  placeholder="搜索用户名、邮箱或姓名..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <Select value={roleFilter} onValueChange={(value) => setRoleFilter(value as UserRole | "all")}>
              <SelectTrigger className="w-[140px]">
                <Filter className="h-4 w-4 mr-2" />
                <SelectValue placeholder="角色筛选" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">所有角色</SelectItem>
                <SelectItem value="admin">管理员</SelectItem>
                <SelectItem value="manager">经理</SelectItem>
                <SelectItem value="employee">员工</SelectItem>
                <SelectItem value="viewer">查看者</SelectItem>
              </SelectContent>
            </Select>
            <Select value={statusFilter} onValueChange={(value) => setStatusFilter(value as UserStatus | "all")}>
              <SelectTrigger className="w-[140px]">
                <SelectValue placeholder="状态筛选" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">所有状态</SelectItem>
                <SelectItem value="active">活跃</SelectItem>
                <SelectItem value="inactive">停用</SelectItem>
                <SelectItem value="pending">待激活</SelectItem>
              </SelectContent>
            </Select>
            <Button onClick={() => setCreateDialogOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              新建用户
            </Button>
          </div>

          {/* 用户表格 */}
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>用户</TableHead>
                  <TableHead>角色</TableHead>
                  <TableHead>状态</TableHead>
                  <TableHead>部门</TableHead>
                  <TableHead>创建时间</TableHead>
                  <TableHead className="text-right">操作</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {isLoading ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center py-8">
                      <div className="flex items-center justify-center">
                        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
                        <span className="ml-2">加载中...</span>
                      </div>
                    </TableCell>
                  </TableRow>
                ) : filteredUsers.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center py-8">
                      <div className="text-muted-foreground">
                        {searchTerm || roleFilter !== "all" || statusFilter !== "all" 
                          ? "没有找到匹配的用户" 
                          : "暂无用户数据"}
                      </div>
                    </TableCell>
                  </TableRow>
                ) : (
                  filteredUsers.map((user) => (
                    <TableRow key={user.id}>
                      <TableCell>
                        <div className="flex items-center space-x-3">
                          <Avatar className="h-8 w-8">
                            <AvatarImage src={user.avatar_url} alt={user.full_name || user.username} />
                            <AvatarFallback>
                              {(user.full_name || user.username).charAt(0).toUpperCase()}
                            </AvatarFallback>
                          </Avatar>
                          <div>
                            <div className="font-medium">{user.full_name || user.username}</div>
                            <div className="text-sm text-muted-foreground">{user.email}</div>
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant={getRoleBadgeVariant(user.role)}>
                          {roleLabels[user.role]}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Badge variant={getStatusBadgeVariant(user.status)}>
                          {statusLabels[user.status]}
                        </Badge>
                      </TableCell>
                      <TableCell>{user.department || "-"}</TableCell>
                      <TableCell>
                        {new Date(user.created_at).toLocaleDateString('zh-CN')}
                      </TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuLabel>操作</DropdownMenuLabel>
                            <DropdownMenuItem onClick={() => handleEditUser(user)}>
                              <Edit className="h-4 w-4 mr-2" />
                              编辑
                            </DropdownMenuItem>
                            <DropdownMenuItem onClick={() => handleToggleUserStatus(user)}>
                              {user.status === "active" ? (
                                <><UserX className="h-4 w-4 mr-2" />停用</>
                              ) : (
                                <><UserCheck className="h-4 w-4 mr-2" />启用</>
                              )}
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            <DropdownMenuItem 
                              onClick={() => handleDeleteUser(user.id)}
                              className="text-destructive"
                            >
                              <Trash2 className="h-4 w-4 mr-2" />
                              删除
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {/* 对话框 */}
      <UserCreateDialog 
        open={createDialogOpen} 
        onOpenChange={setCreateDialogOpen}
      />
      
      {selectedUser && (
        <UserEditDialog 
          open={editDialogOpen} 
          onOpenChange={setEditDialogOpen}
          user={selectedUser}
        />
      )}
    </div>
  )
}
