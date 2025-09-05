"use client"

import { useState } from "react"
import { PerformanceChart } from "./charts/performance-chart"
import { WorkloadChart } from "./charts/workload-chart"
import { ProjectTimelineChart } from "./charts/project-timeline-chart"
import { SummaryReport } from "./reports/summary-report"
import { ExportDialog } from "./reports/export-dialog"
import { RealTimeMetrics } from "./metrics/real-time-metrics"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Download, RefreshCw, TrendingUp, Trees, Sprout, Leaf, MapPin } from "lucide-react"

const mockAnalyticsData = {
  overview: {
    totalProjects: 24,
    activeProjects: 8,
    completedProjects: 16,
    totalEmployees: 48,
    averageUtilization: 76,
    onTimeDelivery: 89,
    totalArea: 580000, // 总施工面积（平方米）
    plantSurvivalRate: 94, // 植物成活率
    ecoEfficiency: 87, // 生态效益指数
    seasonalOptimization: 91, // 季节优化率
  },
  trends: {
    projectCompletion: [
      { month: "1月", completed: 2, started: 3, area: 45000 },
      { month: "2月", completed: 1, started: 2, area: 28000 },
      { month: "3月", completed: 4, started: 6, area: 85000 },
      { month: "4月", completed: 6, started: 5, area: 120000 },
      { month: "5月", completed: 5, started: 4, area: 95000 },
      { month: "6月", completed: 3, started: 2, area: 67000 },
    ],
    resourceUtilization: [
      { department: "设计部", utilization: 85, capacity: 100, projects: 8 },
      { department: "施工部", utilization: 92, capacity: 100, projects: 12 },
      { department: "绿化部", utilization: 78, capacity: 100, projects: 15 },
      { department: "古建部", utilization: 68, capacity: 100, projects: 3 },
    ],
    performanceMetrics: [
      { metric: "项目按时完成率", value: 89, target: 90, trend: "up" },
      { metric: "植物成活率", value: 94, target: 92, trend: "up" },
      { metric: "生态效益指数", value: 87, target: 85, trend: "up" },
      { metric: "成本控制率", value: 91, target: 90, trend: "stable" },
    ],
    regionalData: [
      { region: "华东", projects: 8, area: 180000, completion: 92 },
      { region: "华中", projects: 6, area: 150000, completion: 88 },
      { region: "华南", projects: 5, area: 120000, completion: 94 },
      { region: "西南", projects: 5, area: 130000, completion: 86 },
    ],
    seasonalAnalysis: [
      { season: "春季", projects: 12, plantingSuccess: 96, weatherImpact: 15 },
      { season: "夏季", projects: 8, plantingSuccess: 88, weatherImpact: 35 },
      { season: "秋季", projects: 10, plantingSuccess: 94, weatherImpact: 20 },
      { season: "冬季", projects: 4, plantingSuccess: 85, weatherImpact: 45 },
    ],
  },
}

export function AnalyticsDashboard() {
  const [activeTab, setActiveTab] = useState("overview")
  const [timeRange, setTimeRange] = useState("last30days")
  const [isExportOpen, setIsExportOpen] = useState(false)
  const [isRefreshing, setIsRefreshing] = useState(false)

  const handleRefresh = async () => {
    setIsRefreshing(true)
    console.log("[v0] 刷新园林业务数据...")

    // 模拟数据刷新
    await new Promise((resolve) => setTimeout(resolve, 1000))

    setIsRefreshing(false)
    console.log("[v0] 园林数据刷新完成")
  }

  const handleExport = () => {
    setIsExportOpen(true)
  }

  return (
    <div className="space-y-6">
      {/* 控制栏 */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-40">
              <SelectValue placeholder="选择时间范围" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="last7days">最近7天</SelectItem>
              <SelectItem value="last30days">最近30天</SelectItem>
              <SelectItem value="last90days">最近90天</SelectItem>
              <SelectItem value="lastyear">最近一年</SelectItem>
              <SelectItem value="season">按季节</SelectItem>
            </SelectContent>
          </Select>

          <Button variant="outline" onClick={handleRefresh} disabled={isRefreshing}>
            <RefreshCw className={`w-4 h-4 mr-2 ${isRefreshing ? "animate-spin" : ""}`} />
            {isRefreshing ? "刷新中..." : "刷新数据"}
          </Button>
        </div>

        <Button onClick={handleExport} className="bg-green-600 hover:bg-green-700 text-white">
          <Download className="w-4 h-4 mr-2" />
          导出园林报告
        </Button>
      </div>

      {/* 实时指标 */}
      <RealTimeMetrics data={mockAnalyticsData.overview} />

      {/* 分析内容 */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5 max-w-3xl">
          <TabsTrigger value="overview">施工概览</TabsTrigger>
          <TabsTrigger value="performance">质量分析</TabsTrigger>
          <TabsTrigger value="resources">资源分析</TabsTrigger>
          <TabsTrigger value="regional">区域分析</TabsTrigger>
          <TabsTrigger value="reports">报告中心</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="mt-6 space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            <PerformanceChart data={mockAnalyticsData.trends.projectCompletion} />
            <WorkloadChart data={mockAnalyticsData.trends.resourceUtilization} />
          </div>

          <Card className="border-border/50">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Leaf className="w-5 h-5 mr-2 text-green-600" />
                季节性施工分析
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-4">
                {mockAnalyticsData.trends.seasonalAnalysis.map((season) => (
                  <div key={season.season} className="text-center p-4 rounded-lg bg-green-50">
                    <h4 className="font-medium text-green-800 mb-2">{season.season}</h4>
                    <div className="space-y-2 text-sm">
                      <div>
                        <span className="text-gray-600">项目数: </span>
                        <span className="font-medium">{season.projects}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">成活率: </span>
                        <span className="font-medium text-green-600">{season.plantingSuccess}%</span>
                      </div>
                      <div>
                        <span className="text-gray-600">天气影响: </span>
                        <span className="font-medium text-amber-600">{season.weatherImpact}%</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <ProjectTimelineChart />
        </TabsContent>

        <TabsContent value="performance" className="mt-6 space-y-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {mockAnalyticsData.trends.performanceMetrics.map((metric) => (
              <Card key={metric.metric} className="border-border/50">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-muted-foreground flex items-center">
                    {metric.metric.includes("植物") && <Sprout className="w-4 h-4 mr-1 text-green-600" />}
                    {metric.metric.includes("生态") && <Trees className="w-4 h-4 mr-1 text-emerald-600" />}
                    {metric.metric}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <div className="text-2xl font-bold text-green-700">{metric.value}%</div>
                    <div
                      className={`flex items-center text-sm ${
                        metric.trend === "up"
                          ? "text-green-600"
                          : metric.trend === "down"
                            ? "text-red-600"
                            : "text-gray-600"
                      }`}
                    >
                      <TrendingUp className="w-4 h-4 mr-1" />
                      {metric.trend === "up" ? "↗" : metric.trend === "down" ? "↘" : "→"}
                    </div>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">目标: {metric.target}%</p>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            <Card className="border-border/50">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Trees className="w-5 h-5 mr-2 text-green-600" />
                  专业团队绩效排名
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { name: "施工部", score: 92, projects: 12, specialty: "土建施工" },
                    { name: "设计部", score: 88, projects: 8, specialty: "景观设计" },
                    { name: "绿化部", score: 85, projects: 15, specialty: "植物配置" },
                    { name: "古建部", score: 82, projects: 3, specialty: "古建修复" },
                  ].map((team, index) => (
                    <div key={team.name} className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                          <span className="text-sm font-medium text-green-700">#{index + 1}</span>
                        </div>
                        <div>
                          <p className="font-medium">{team.name}</p>
                          <p className="text-sm text-muted-foreground">
                            {team.projects} 个项目 · {team.specialty}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="font-medium text-green-700">{team.score}分</p>
                        <div className="w-20 bg-green-100 rounded-full h-2 mt-1">
                          <div className="bg-green-600 h-2 rounded-full" style={{ width: `${team.score}%` }} />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="border-border/50">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Sprout className="w-5 h-5 mr-2 text-emerald-600" />
                  植物成活率分析
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { category: "乔木类", value: 96, color: "bg-green-600", count: "1,250株" },
                    { category: "灌木类", value: 94, color: "bg-emerald-500", count: "3,680株" },
                    { category: "草本类", value: 92, color: "bg-lime-500", count: "15,200㎡" },
                    { category: "水生植物", value: 88, color: "bg-teal-500", count: "850株" },
                  ].map((item) => (
                    <div key={item.category} className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span>{item.category}</span>
                        <div className="text-right">
                          <span className="font-medium">{item.value}%</span>
                          <p className="text-xs text-muted-foreground">{item.count}</p>
                        </div>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div className={`${item.color} h-2 rounded-full`} style={{ width: `${item.value}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="resources" className="mt-6 space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="border-border/50">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Trees className="w-5 h-5 mr-2 text-green-600" />
                  专业技能分布
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { skill: "景观设计", count: 12, percentage: 75 },
                    { skill: "植物配置", count: 15, percentage: 94 },
                    { skill: "土建施工", count: 18, percentage: 100 },
                    { skill: "古建修复", count: 6, percentage: 37 },
                    { skill: "生态修复", count: 8, percentage: 50 },
                  ].map((skill) => (
                    <div key={skill.skill} className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span>{skill.skill}</span>
                        <span className="font-medium">{skill.count} 人</span>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div className="bg-green-600 h-2 rounded-full" style={{ width: `${skill.percentage}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="border-border/50">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Leaf className="w-5 h-5 mr-2 text-emerald-600" />
                  成本效益分析
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-700">¥18,475,000</div>
                    <p className="text-sm text-muted-foreground">本月总投资</p>
                  </div>

                  <div className="space-y-3">
                    {[
                      { category: "人工成本", amount: 8500000, percentage: 46, color: "bg-green-500" },
                      { category: "材料成本", amount: 6200000, percentage: 34, color: "bg-emerald-500" },
                      { category: "设备租赁", amount: 2100000, percentage: 11, color: "bg-lime-500" },
                      { category: "其他费用", amount: 1675000, percentage: 9, color: "bg-teal-500" },
                    ].map((item) => (
                      <div key={item.category} className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <div className={`w-3 h-3 ${item.color} rounded-full`}></div>
                          <span className="text-sm">{item.category}</span>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-medium">¥{item.amount.toLocaleString()}</p>
                          <p className="text-xs text-muted-foreground">{item.percentage}%</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <WorkloadChart data={mockAnalyticsData.trends.resourceUtilization} />
        </TabsContent>

        <TabsContent value="regional" className="mt-6 space-y-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {mockAnalyticsData.trends.regionalData.map((region) => (
              <Card key={region.region} className="border-border/50">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-medium text-muted-foreground flex items-center">
                    <MapPin className="w-4 h-4 mr-1 text-blue-600" />
                    {region.region}区域
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">项目数量</span>
                      <span className="font-medium">{region.projects}个</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">施工面积</span>
                      <span className="font-medium">{(region.area / 10000).toFixed(1)}万㎡</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">完成率</span>
                      <span className="font-medium text-green-600">{region.completion}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                      <div className="bg-green-600 h-2 rounded-full" style={{ width: `${region.completion}%` }} />
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          <Card className="border-border/50">
            <CardHeader>
              <CardTitle className="flex items-center">
                <MapPin className="w-5 h-5 mr-2 text-blue-600" />
                区域项目分布与效率对比
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {mockAnalyticsData.trends.regionalData.map((region) => (
                  <div key={region.region} className="flex items-center justify-between p-3 rounded-lg bg-gray-50">
                    <div className="flex items-center space-x-4">
                      <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                        <span className="text-sm font-medium text-blue-700">{region.region}</span>
                      </div>
                      <div>
                        <p className="font-medium">{region.region}区域</p>
                        <p className="text-sm text-gray-600">
                          {region.projects}个项目 · {(region.area / 10000).toFixed(1)}万㎡
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-medium text-green-700">{region.completion}%</p>
                      <p className="text-xs text-gray-500">完成率</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="reports" className="mt-6">
          <SummaryReport data={mockAnalyticsData} />
        </TabsContent>
      </Tabs>

      {/* 导出对话框 */}
      <ExportDialog isOpen={isExportOpen} onClose={() => setIsExportOpen(false)} data={mockAnalyticsData} />
    </div>
  )
}
