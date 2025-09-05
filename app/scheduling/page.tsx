"use client"

import { RouteGuard } from "@/components/auth/route-guard"
import { SchedulingManagement } from "@/components/scheduling/scheduling-management"

export default function SchedulingPage() {
  return (
    <RouteGuard allowedRoles={["admin", "manager"]}>
      <div className="container mx-auto py-6">
        <div className="mb-6">
          <h1 className="text-3xl font-bold tracking-tight">智能调度</h1>
          <p className="text-muted-foreground">
            管理人员调度任务，优化资源配置，解决调度冲突
          </p>
        </div>
        <SchedulingManagement />
      </div>
    </RouteGuard>
  )
}