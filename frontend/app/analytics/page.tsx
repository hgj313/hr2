import { RouteGuard } from "@/components/auth/route-guard"
import { AnalyticsDashboard } from "@/components/analytics/analytics-dashboard"

export default function AnalyticsPage() {
  return (
    <RouteGuard requiredRoles={["admin", "manager"]}>
      <div className="container mx-auto py-6">
        <div className="mb-6">
          <h1 className="text-3xl font-bold tracking-tight">数据分析</h1>
          <p className="text-muted-foreground">
            查看系统性能指标、统计数据和分析报告
          </p>
        </div>
        <AnalyticsDashboard />
      </div>
    </RouteGuard>
  )
}