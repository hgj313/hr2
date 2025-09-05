import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Users, FolderKanban, Calendar, TrendingUp } from "lucide-react"

const stats = [
  {
    title: "总员工数",
    value: "248",
    change: "+12%",
    changeType: "positive" as const,
    icon: Users,
  },
  {
    title: "活跃项目",
    value: "32",
    change: "+8%",
    changeType: "positive" as const,
    icon: FolderKanban,
  },
  {
    title: "本月调度",
    value: "156",
    change: "+23%",
    changeType: "positive" as const,
    icon: Calendar,
  },
  {
    title: "资源利用率",
    value: "87%",
    change: "+5%",
    changeType: "positive" as const,
    icon: TrendingUp,
  },
]

export function DashboardStats() {
  return (
    <div className="grid gap-3 lg:gap-4 grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => (
        <Card key={stat.title} className="border-border/50 card-responsive touch-feedback">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 spacing-responsive-sm">
            <CardTitle className="text-xs lg:text-sm font-medium text-muted-foreground text-responsive">
              {stat.title}
            </CardTitle>
            <stat.icon className="h-3 w-3 lg:h-4 lg:w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent className="spacing-responsive-sm">
            <div className="text-lg lg:text-2xl font-bold text-foreground">{stat.value}</div>
            <p className="text-xs text-muted-foreground mobile-hidden lg:block">
              <span className={stat.changeType === "positive" ? "text-green-600" : "text-red-600"}>{stat.change}</span>{" "}
              较上月
            </p>
            <p className="text-xs text-muted-foreground mobile-only">
              <span className={stat.changeType === "positive" ? "text-green-600" : "text-red-600"}>{stat.change}</span>
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
