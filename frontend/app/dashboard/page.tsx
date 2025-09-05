import { DashboardHeader } from "@/components/dashboard/dashboard-header"
import { DashboardStats } from "@/components/dashboard/dashboard-stats"
import { DashboardCharts } from "@/components/dashboard/dashboard-charts"
import { RecentActivities } from "@/components/dashboard/recent-activities"
import { RouteGuard } from "@/lib/auth/route-guard"

export default function DashboardPage() {
  return (
    <RouteGuard>
      <div className="flex-1 space-y-4 lg:space-y-6 spacing-responsive">
        <DashboardHeader />
        <DashboardStats />
        <div className="grid gap-4 lg:gap-6 grid-cols-1 lg:grid-cols-7">
          <div className="lg:col-span-4 order-2 lg:order-1">
            <DashboardCharts />
          </div>
          <div className="lg:col-span-3 order-1 lg:order-2">
            <RecentActivities />
          </div>
        </div>
      </div>
    </RouteGuard>
  )
}
