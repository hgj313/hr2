"use client"

import { useState, useEffect } from "react"
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
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { useUpdateProject } from "@/lib/api/projects"
import { useToast } from "@/hooks/use-toast"
import type { Project, ProjectStatus, ProjectPriority } from "@/lib/api/projects"

const projectSchema = z.object({
  name: z.string().min(1, "项目名称不能为空"),
  description: z.string().optional(),
  status: z.enum(["planning", "active", "on_hold", "completed", "cancelled"] as const),
  priority: z.enum(["low", "medium", "high", "urgent"] as const),
  start_date: z.string().min(1, "开始日期不能为空"),
  end_date: z.string().min(1, "结束日期不能为空"),
  budget: z.string().optional(),
  manager_id: z.string().optional(),
})

type ProjectFormData = z.infer<typeof projectSchema>

interface ProjectEditDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  project: Project | null
}

export function ProjectEditDialog({ open, onOpenChange, project }: ProjectEditDialogProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { toast } = useToast()
  const updateProjectMutation = useUpdateProject()

  const form = useForm<ProjectFormData>({
    resolver: zodResolver(projectSchema),
    defaultValues: {
      name: "",
      description: "",
      status: "planning",
      priority: "medium",
      start_date: "",
      end_date: "",
      budget: "",
      manager_id: "",
    },
  })

  // 当项目数据变化时更新表单
  useEffect(() => {
    if (project) {
      form.reset({
        name: project.name || "",
        description: project.description || "",
        status: project.status,
        priority: project.priority,
        start_date: project.start_date ? new Date(project.start_date).toISOString().split('T')[0] : "",
        end_date: project.end_date ? new Date(project.end_date).toISOString().split('T')[0] : "",
        budget: project.budget ? project.budget.toString() : "",
        manager_id: project.manager_id || "",
      })
    }
  }, [project, form])

  const onSubmit = async (data: ProjectFormData) => {
    if (!project) return
    
    setIsSubmitting(true)
    try {
      const projectData = {
        ...data,
        budget: data.budget ? parseFloat(data.budget) : undefined,
      }
      
      await updateProjectMutation.mutateAsync({
        id: project.id,
        data: projectData,
      })
      
      toast({
        title: "更新成功",
        description: "项目信息已成功更新",
      })
      
      onOpenChange(false)
    } catch (error) {
      toast({
        title: "更新失败",
        description: "更新项目信息时发生错误，请重试",
        variant: "destructive",
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>编辑项目</DialogTitle>
          <DialogDescription>
            修改项目信息
          </DialogDescription>
        </DialogHeader>
        
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>项目名称 *</FormLabel>
                    <FormControl>
                      <Input placeholder="输入项目名称" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              
              <FormField
                control={form.control}
                name="budget"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>预算金额</FormLabel>
                    <FormControl>
                      <Input 
                        type="number" 
                        placeholder="输入预算金额" 
                        {...field} 
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>项目描述</FormLabel>
                  <FormControl>
                    <Textarea 
                      placeholder="输入项目描述" 
                      className="resize-none" 
                      rows={3}
                      {...field} 
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="status"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>项目状态 *</FormLabel>
                    <Select onValueChange={field.onChange} value={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="选择项目状态" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="planning">规划中</SelectItem>
                        <SelectItem value="active">进行中</SelectItem>
                        <SelectItem value="on_hold">暂停</SelectItem>
                        <SelectItem value="completed">已完成</SelectItem>
                        <SelectItem value="cancelled">已取消</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              
              <FormField
                control={form.control}
                name="priority"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>优先级 *</FormLabel>
                    <Select onValueChange={field.onChange} value={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="选择优先级" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="low">低</SelectItem>
                        <SelectItem value="medium">中</SelectItem>
                        <SelectItem value="high">高</SelectItem>
                        <SelectItem value="urgent">紧急</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="start_date"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>开始日期 *</FormLabel>
                    <FormControl>
                      <Input type="date" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              
              <FormField
                control={form.control}
                name="end_date"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>结束日期 *</FormLabel>
                    <FormControl>
                      <Input type="date" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <DialogFooter>
              <Button 
                type="button" 
                variant="outline" 
                onClick={() => onOpenChange(false)}
                disabled={isSubmitting}
              >
                取消
              </Button>
              <Button type="submit" disabled={isSubmitting}>
                {isSubmitting ? "更新中..." : "更新项目"}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}