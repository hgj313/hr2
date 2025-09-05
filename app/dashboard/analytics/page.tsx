```tsx file="app/dashboard/analytics/page.tsx"
import { AnalyticsDashboard } from "@/components/analytics/analytics-dashboard"

export default function AnalyticsPage() {
  return (
    <div className="flex-1 space-y-6 p-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-foreground">园林业务数据分析</h1>
        <p className="text-muted-foreground">深入洞察园林施工数据，优化项目效率和生态效益</p>
      </div>
      <AnalyticsDashboard />
    </div>
  )
}
