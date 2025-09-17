"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Area,
  AreaChart,
} from "recharts"
import { TrendingUp, Users, Clock, Target, AlertTriangle, Download, Award, Activity } from "lucide-react"

// Mock analytics data
const utilizationData = [
  { department: "技术开发部", utilization: 92, target: 85, members: 15 },
  { department: "产品部", utilization: 88, target: 85, members: 8 },
  { department: "设计部", utilization: 75, target: 85, members: 6 },
  { department: "人力资源部", utilization: 70, target: 85, members: 4 },
  { department: "信息技术部", utilization: 85, target: 85, members: 5 },
]

const projectProgressData = [
  { name: "企业管理系统升级", progress: 65, budget: 500000, spent: 325000 },
  { name: "移动端应用开发", progress: 15, budget: 300000, spent: 45000 },
  { name: "数据分析平台", progress: 40, budget: 400000, spent: 160000 },
]

const workloadTrendData = [
  { month: "1月", average: 78, peak: 95, low: 62 },
  { month: "2月", average: 82, peak: 98, low: 65 },
  { month: "3月", average: 85, peak: 100, low: 70 },
  { month: "4月", average: 88, peak: 105, low: 72 },
  { month: "5月", average: 86, peak: 102, low: 68 },
  { month: "6月", average: 84, peak: 99, low: 69 },
]

const skillDistributionData = [
  { name: "前端开发", value: 35, color: "#3b82f6" },
  { name: "后端开发", value: 28, color: "#10b981" },
  { name: "UI/UX设计", value: 15, color: "#f59e0b" },
  { name: "项目管理", value: 12, color: "#ef4444" },
  { name: "数据分析", value: 10, color: "#8b5cf6" },
]

const departmentEfficiencyData = [
  { department: "技术开发部", score: 95, projects: 8, completed: 6 },
  { department: "产品部", score: 88, projects: 5, completed: 4 },
  { department: "设计部", score: 82, projects: 4, completed: 3 },
  { department: "人力资源部", score: 78, projects: 3, completed: 2 },
  { department: "信息技术部", score: 85, projects: 4, completed: 3 },
]

const alerts = [
  {
    id: "1",
    type: "warning",
    title: "张三工作量超标",
    description: "当前工作负载达到150%，建议调整任务分配",
    severity: "high",
  },
  {
    id: "2",
    type: "info",
    title: "项目B进度延迟",
    description: "预计延迟3天完成，需要关注资源分配",
    severity: "medium",
  },
  {
    id: "3",
    type: "success",
    title: "李四技能不匹配",
    description: "分配的任务需要React技能，建议安排培训",
    severity: "low",
  },
]

export function AnalyticsDashboard() {
  const [timeRange, setTimeRange] = useState("month")
  const [selectedDepartment, setSelectedDepartment] = useState("all")
  const [activeTab, setActiveTab] = useState("overview")

  const getSeverityBadge = (severity: string) => {
    const variants = {
      high: "destructive",
      medium: "secondary",
      low: "outline",
    } as const

    return (
      <Badge variant={variants[severity as keyof typeof variants]} className="text-xs">
        {severity === "high" ? "高" : severity === "medium" ? "中" : "低"}
      </Badge>
    )
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("zh-CN", {
      style: "currency",
      currency: "CNY",
      minimumFractionDigits: 0,
    }).format(amount)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-balance">数据分析</h1>
          <p className="text-muted-foreground mt-1">多维度数据分析和可视化报表</p>
        </div>
        <div className="flex gap-2">
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="week">本周</SelectItem>
              <SelectItem value="month">本月</SelectItem>
              <SelectItem value="quarter">本季度</SelectItem>
              <SelectItem value="year">本年</SelectItem>
            </SelectContent>
          </Select>
          <Select value={selectedDepartment} onValueChange={setSelectedDepartment}>
            <SelectTrigger className="w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">全部部门</SelectItem>
              <SelectItem value="tech">技术开发部</SelectItem>
              <SelectItem value="product">产品部</SelectItem>
              <SelectItem value="design">设计部</SelectItem>
              <SelectItem value="hr">人力资源部</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" className="gap-2 bg-transparent">
            <Download className="w-4 h-4" />
            导出报表
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <Users className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">85%</div>
                <div className="text-sm text-muted-foreground">平均利用率</div>
              </div>
            </div>
            <div className="mt-4 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-green-600" />
              <span className="text-sm text-green-600">+5.2% 较上月</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <Target className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">12/15</div>
                <div className="text-sm text-muted-foreground">项目完成</div>
              </div>
            </div>
            <div className="mt-4 flex items-center gap-2">
              <Activity className="w-4 h-4 text-blue-600" />
              <span className="text-sm text-blue-600">80% 完成率</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                <Clock className="w-5 h-5 text-yellow-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">2.3天</div>
                <div className="text-sm text-muted-foreground">平均延期</div>
              </div>
            </div>
            <div className="mt-4 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-red-600 rotate-180" />
              <span className="text-sm text-red-600">-1.2天 较上月</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                <Award className="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <div className="text-2xl font-bold">88分</div>
                <div className="text-sm text-muted-foreground">满意度评分</div>
              </div>
            </div>
            <div className="mt-4 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-green-600" />
              <span className="text-sm text-green-600">+3.5分 较上月</span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Analytics Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">总览</TabsTrigger>
          <TabsTrigger value="utilization">人员利用率</TabsTrigger>
          <TabsTrigger value="projects">项目分析</TabsTrigger>
          <TabsTrigger value="trends">趋势分析</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Department Efficiency */}
            <Card>
              <CardHeader>
                <CardTitle>部门效率排行</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {departmentEfficiencyData.map((dept, index) => (
                    <div key={dept.department} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center text-sm font-medium">
                          {index + 1}
                        </div>
                        <div>
                          <div className="font-medium">{dept.department}</div>
                          <div className="text-sm text-muted-foreground">
                            {dept.completed}/{dept.projects} 项目完成
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-lg">{dept.score}分</div>
                        <Progress value={dept.score} className="w-20 h-2 mt-1" />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Skill Distribution */}
            <Card>
              <CardHeader>
                <CardTitle>技能分布</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={skillDistributionData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={100}
                        paddingAngle={5}
                        dataKey="value"
                      >
                        {skillDistributionData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(value) => [`${value}%`, "占比"]} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div className="grid grid-cols-2 gap-2 mt-4">
                  {skillDistributionData.map((skill) => (
                    <div key={skill.name} className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full" style={{ backgroundColor: skill.color }}></div>
                      <span className="text-sm">{skill.name}</span>
                      <span className="text-sm text-muted-foreground ml-auto">{skill.value}%</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Alerts */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" />
                异常告警
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {alerts.map((alert) => (
                  <div key={alert.id} className="flex items-start gap-3 p-3 border rounded-lg">
                    <div className="w-2 h-2 rounded-full bg-yellow-500 mt-2"></div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-medium">{alert.title}</span>
                        {getSeverityBadge(alert.severity)}
                      </div>
                      <p className="text-sm text-muted-foreground">{alert.description}</p>
                    </div>
                    <Button variant="ghost" size="sm">
                      处理
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="utilization" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>部门人员利用率</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={utilizationData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="department" />
                    <YAxis />
                    <Tooltip
                      formatter={(value, name) => [`${value}%`, name === "utilization" ? "实际利用率" : "目标利用率"]}
                    />
                    <Bar dataKey="utilization" fill="#3b82f6" name="utilization" />
                    <Bar dataKey="target" fill="#e5e7eb" name="target" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>利用率详情</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {utilizationData.map((dept) => (
                    <div key={dept.department}>
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium">{dept.department}</span>
                        <span className="text-sm text-muted-foreground">{dept.members}人</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Progress value={dept.utilization} className="flex-1 h-2" />
                        <span className="text-sm font-medium w-12">{dept.utilization}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>利用率统计</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">最高利用率</span>
                    <span className="font-medium">92% (技术开发部)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">最低利用率</span>
                    <span className="font-medium">70% (人力资源部)</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">平均利用率</span>
                    <span className="font-medium">82%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">达标部门</span>
                    <span className="font-medium">3/5 (60%)</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="projects" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>项目进度统计</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {projectProgressData.map((project) => (
                  <div key={project.name} className="space-y-3">
                    <div className="flex justify-between items-center">
                      <h4 className="font-medium">{project.name}</h4>
                      <span className="text-sm text-muted-foreground">{project.progress}%</span>
                    </div>
                    <Progress value={project.progress} className="h-3" />
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="text-muted-foreground">预算: </span>
                        <span className="font-medium">{formatCurrency(project.budget)}</span>
                      </div>
                      <div>
                        <span className="text-muted-foreground">已用: </span>
                        <span className="font-medium">{formatCurrency(project.spent)}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>项目状态分布</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span>进行中</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-muted rounded-full h-2">
                        <div className="bg-blue-500 h-2 rounded-full" style={{ width: "60%" }}></div>
                      </div>
                      <span className="text-sm">60%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>规划中</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-muted rounded-full h-2">
                        <div className="bg-yellow-500 h-2 rounded-full" style={{ width: "25%" }}></div>
                      </div>
                      <span className="text-sm">25%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>已完成</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-muted rounded-full h-2">
                        <div className="bg-green-500 h-2 rounded-full" style={{ width: "15%" }}></div>
                      </div>
                      <span className="text-sm">15%</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>预算使用情况</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold">65%</div>
                    <div className="text-sm text-muted-foreground">总预算使用率</div>
                  </div>
                  <Progress value={65} className="h-3" />
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <div className="text-muted-foreground">总预算</div>
                      <div className="font-medium">{formatCurrency(1200000)}</div>
                    </div>
                    <div>
                      <div className="text-muted-foreground">已使用</div>
                      <div className="font-medium">{formatCurrency(780000)}</div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="trends" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>工作负载趋势</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={workloadTrendData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip
                      formatter={(value, name) => [
                        `${value}%`,
                        name === "average" ? "平均负载" : name === "peak" ? "峰值负载" : "最低负载",
                      ]}
                    />
                    <Area
                      type="monotone"
                      dataKey="peak"
                      stackId="1"
                      stroke="#ef4444"
                      fill="#ef4444"
                      fillOpacity={0.3}
                    />
                    <Area
                      type="monotone"
                      dataKey="average"
                      stackId="2"
                      stroke="#3b82f6"
                      fill="#3b82f6"
                      fillOpacity={0.6}
                    />
                    <Area type="monotone" dataKey="low" stackId="3" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>趋势分析</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center gap-3">
                    <TrendingUp className="w-5 h-5 text-green-600" />
                    <div>
                      <div className="font-medium">工作负载稳步上升</div>
                      <div className="text-sm text-muted-foreground">过去6个月平均增长12%</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <Activity className="w-5 h-5 text-blue-600" />
                    <div>
                      <div className="font-medium">项目完成率提升</div>
                      <div className="text-sm text-muted-foreground">较去年同期提升15%</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <Users className="w-5 h-5 text-purple-600" />
                    <div>
                      <div className="font-medium">团队效率优化</div>
                      <div className="text-sm text-muted-foreground">人均产出提升8%</div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>预测分析</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-muted-foreground">下月预计负载</span>
                      <span className="font-medium">89%</span>
                    </div>
                    <Progress value={89} className="h-2" />
                  </div>
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-muted-foreground">季度目标达成</span>
                      <span className="font-medium">92%</span>
                    </div>
                    <Progress value={92} className="h-2" />
                  </div>
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-muted-foreground">资源需求增长</span>
                      <span className="font-medium">+15%</span>
                    </div>
                    <Progress value={115} className="h-2" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
