"use client"

import { RouteGuard } from "@/lib/auth/route-guard"
import { ProjectManagement } from "@/components/projects/project-management"

export default function ProjectsPage() {
  return (
    <RouteGuard requiredRoles={["admin", "manager"]}>
      <div className="container mx-auto py-6">
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">项目管理</h1>
            <p className="text-muted-foreground">
              管理项目信息、任务分配和进度跟踪
            </p>
          </div>
          <ProjectManagement />
        </div>
      </div>
    </RouteGuard>
  )
}