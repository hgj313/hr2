"use client"

import { useEffect } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Loader2 } from "lucide-react"
import { useUpdateUser } from "@/lib/api/users"
import { useToast } from "@/hooks/use-toast"
import type { User, UserRole } from "@/lib/api/users"

const editUserSchema = z.object({
  username: z.string().min(3, "用户名至少3个字符").max(50, "用户名不能超过50个字符"),
  email: z.string().email("请输入有效的邮箱地址"),
  full_name: z.string().optional(),
  role: z.enum(["admin", "manager", "employee", "viewer"] as const),
  department: z.string().optional(),
  password: z.string().optional(),
})

type EditUserFormData = z.infer<typeof editUserSchema>

interface UserEditDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  user: User
}

export function UserEditDialog({ open, onOpenChange, user }: UserEditDialogProps) {
  const { toast } = useToast()
  const updateUserMutation = useUpdateUser()

  const form = useForm<EditUserFormData>({
    resolver: zodResolver(editUserSchema),
    defaultValues: {
      username: "",
      email: "",
      full_name: "",
      role: "employee",
      department: "",
      password: "",
    },
  })

  // 当用户数据变化时更新表单
  useEffect(() => {
    if (user && open) {
      form.reset({
        username: user.username,
        email: user.email,
        full_name: user.full_name || "",
        role: user.role,
        department: user.department || "",
        password: "", // 密码字段保持空白
      })
    }
  }, [user, open, form])

  const onSubmit = async (data: EditUserFormData) => {
    try {
      // 如果密码为空，则不更新密码
      const updateData = { ...data }
      if (!updateData.password) {
        delete updateData.password
      }
      
      await updateUserMutation.mutateAsync({
        id: user.id,
        data: updateData,
      })
      
      toast({
        title: "更新成功",
        description: "用户信息已成功更新",
      })
      
      onOpenChange(false)
    } catch (error: any) {
      toast({
        title: "更新失败",
        description: error.message || "更新用户信息时发生错误，请重试",
        variant: "destructive",
      })
    }
  }

  const handleOpenChange = (newOpen: boolean) => {
    if (!newOpen) {
      form.reset()
    }
    onOpenChange(newOpen)
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>编辑用户</DialogTitle>
          <DialogDescription>
            修改用户信息和权限设置
          </DialogDescription>
        </DialogHeader>
        
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="username"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>用户名 *</FormLabel>
                  <FormControl>
                    <Input placeholder="请输入用户名" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>邮箱 *</FormLabel>
                  <FormControl>
                    <Input type="email" placeholder="请输入邮箱地址" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <FormField
              control={form.control}
              name="full_name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>姓名</FormLabel>
                  <FormControl>
                    <Input placeholder="请输入真实姓名" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <FormField
              control={form.control}
              name="role"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>角色 *</FormLabel>
                  <Select onValueChange={field.onChange} value={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="选择用户角色" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      <SelectItem value="admin">管理员</SelectItem>
                      <SelectItem value="manager">经理</SelectItem>
                      <SelectItem value="employee">员工</SelectItem>
                      <SelectItem value="viewer">查看者</SelectItem>
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <FormField
              control={form.control}
              name="department"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>部门</FormLabel>
                  <FormControl>
                    <Input placeholder="请输入部门名称" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>新密码</FormLabel>
                  <FormControl>
                    <Input 
                      type="password" 
                      placeholder="留空则不修改密码" 
                      {...field} 
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => handleOpenChange(false)}
                disabled={updateUserMutation.isPending}
              >
                取消
              </Button>
              <Button type="submit" disabled={updateUserMutation.isPending}>
                {updateUserMutation.isPending && (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                )}
                保存更改
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}