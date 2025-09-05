import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export function DashboardCharts() {
  return (
    <Card className="border-border/50">
      <CardHeader>
        <CardTitle>项目进度趋势</CardTitle>
        <CardDescription>过去6个月的项目完成情况</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[300px] flex items-center justify-center bg-muted/20 rounded-lg">
          <p className="text-muted-foreground">图表组件将在后续实现</p>
        </div>
      </CardContent>
    </Card>
  )
}
