"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  Calendar,
  Users,
  Zap,
  Settings,
  Brain,
  Target,
  TrendingUp,
  Activity,
  Trees,
  Sprout,
  CloudRain,
  Sun,
} from "lucide-react"
import { ProjectOverviewMap } from "./project-overview-map"
import { ResourceHeatmap } from "./resource-heatmap"
import { FluidDragDrop } from "./fluid-drag-drop"
import { PredictiveAnalyzer } from "./predictive-analyzer"
import { PerformanceMonitor } from "./performance-monitor"
import { RegionalResourceDistribution } from "./regional-resource-distribution"

const mockEnhancedData = {
  availableStaff: [
    {
      id: "1",
      name: "李园林",
      department: "设计部",
      position: "景观设计师",
      skills: ["景观设计", "CAD制图", "植物配置"],
      level: "高级",
      workload: 60,
      availability: "可用",
      hourlyRate: 280,
      efficiency: 92,
      region: "华东",
      specialization: "住宅景观",
      certifications: ["注册景观设计师", "高级园林工程师"],
      experience: 8,
      seasonalPreference: "春秋",
      weatherSuitability: ["晴天", "阴天"],
    },
    {
      id: "2",
      name: "王施工",
      department: "施工部",
      position: "施工队长",
      skills: ["土建施工", "设备操作", "安全管理"],
      level: "高级",
      workload: 45,
      availability: "可用",
      hourlyRate: 220,
      efficiency: 88,
      region: "华中",
      specialization: "市政园林",
      certifications: ["建造师", "安全工程师"],
      experience: 12,
      seasonalPreference: "春夏秋",
      weatherSuitability: ["晴天"],
    },
    {
      id: "3",
      name: "陈绿化",
      department: "绿化部",
      position: "绿化工程师",
      skills: ["植物种植", "养护管理", "病虫害防治"],
      level: "中级",
      workload: 80,
      availability: "忙碌",
      hourlyRate: 180,
      efficiency: 95,
      region: "华南",
      specialization: "生态修复",
      certifications: ["园艺师", "植保员"],
      experience: 6,
      seasonalPreference: "春秋",
      weatherSuitability: ["晴天", "阴天", "小雨"],
    },
    {
      id: "4",
      name: "赵古建",
      department: "古建部",
      position: "古建工艺师",
      skills: ["古建修复", "传统工艺", "文物保护"],
      level: "专家",
      workload: 70,
      availability: "可用",
      hourlyRate: 350,
      efficiency: 90,
      region: "华东",
      specialization: "古建园林",
      certifications: ["文物保护工程师", "古建筑修缮师"],
      experience: 15,
      seasonalPreference: "秋冬",
      weatherSuitability: ["晴天", "阴天"],
    },
    {
      id: "5",
      name: "孙水景",
      department: "景观部",
      position: "水景工程师",
      skills: ["水景设计", "喷泉施工", "水质管理"],
      level: "高级",
      workload: 55,
      availability: "可用",
      hourlyRate: 260,
      efficiency: 94,
      region: "西南",
      specialization: "住宅景观",
      certifications: ["给排水工程师", "景观设计师"],
      experience: 10,
      seasonalPreference: "春夏",
      weatherSuitability: ["晴天"],
    },
    {
      id: "6",
      name: "刘生态",
      department: "生态部",
      position: "生态修复专家",
      skills: ["土壤改良", "生态评估", "环境监测"],
      level: "专家",
      workload: 40,
      availability: "可用",
      hourlyRate: 320,
      efficiency: 87,
      region: "华中",
      specialization: "生态修复",
      certifications: ["环境工程师", "土壤修复师"],
      experience: 12,
      seasonalPreference: "全年",
      weatherSuitability: ["晴天", "阴天", "小雨"],
    },
  ],
  projects: [
    {
      id: "1",
      name: "绿城·桂花园住宅景观",
      requiredSkills: ["景观设计", "植物配置", "水景设计"],
      priority: "高",
      deadline: "2024-08-15",
      estimatedHours: 480,
      assignedStaff: [],
      status: "待分配",
      progress: 0,
      budget: 2800000,
      projectType: "住宅景观",
      location: "华东·杭州",
      area: "15000㎡",
      season: "春季",
      weather: "适宜",
      constructionPhase: "绿化阶段",
      plantTypes: ["桂花", "樱花", "竹子"],
      weatherDependency: "中等",
      seasonalConstraints: ["春季种植", "秋季养护"],
    },
    {
      id: "2",
      name: "市政公园生态修复工程",
      requiredSkills: ["生态评估", "土壤改良", "植被恢复"],
      priority: "高",
      deadline: "2024-10-30",
      estimatedHours: 720,
      assignedStaff: [],
      status: "待分配",
      progress: 0,
      budget: 4500000,
      projectType: "生态修复",
      location: "华中·武汉",
      area: "35000㎡",
      season: "春季",
      weather: "多雨",
      constructionPhase: "土建阶段",
      plantTypes: ["本土植物", "湿地植物"],
      weatherDependency: "高",
      seasonalConstraints: ["避开梅雨季", "春秋施工"],
    },
    {
      id: "3",
      name: "古典园林修缮工程",
      requiredSkills: ["古建修复", "传统工艺", "文物保护"],
      priority: "高",
      deadline: "2024-06-30",
      estimatedHours: 600,
      assignedStaff: [],
      status: "待分配",
      progress: 0,
      budget: 6200000,
      projectType: "古建园林",
      location: "华东·苏州",
      area: "8000㎡",
      season: "秋冬",
      weather: "干燥",
      constructionPhase: "景观阶段",
      plantTypes: ["传统花木", "古树名木"],
      weatherDependency: "低",
      seasonalConstraints: ["避开雨季", "冬季施工"],
    },
    {
      id: "4",
      name: "商业综合体屋顶花园",
      requiredSkills: ["屋顶绿化", "结构设计", "防水处理"],
      priority: "中",
      deadline: "2024-07-01",
      estimatedHours: 400,
      assignedStaff: [],
      status: "待分配",
      progress: 0,
      budget: 3200000,
      projectType: "屋顶花园",
      location: "华南·深圳",
      area: "12000㎡",
      season: "冬春",
      weather: "温和",
      constructionPhase: "设计阶段",
      plantTypes: ["耐旱植物", "轻质植物"],
      weatherDependency: "中等",
      seasonalConstraints: ["避开台风季", "春季种植"],
    },
    {
      id: "5",
      name: "湿地公园景观提升",
      requiredSkills: ["湿地设计", "水生植物", "生态保护"],
      priority: "中",
      deadline: "2024-09-15",
      estimatedHours: 520,
      assignedStaff: [],
      status: "待分配",
      progress: 0,
      budget: 3800000,
      projectType: "生态修复",
      location: "西南·成都",
      area: "25000㎡",
      season: "春夏",
      weather: "湿润",
      constructionPhase: "绿化阶段",
      plantTypes: ["水生植物", "湿地植物"],
      weatherDependency: "高",
      seasonalConstraints: ["春季种植", "夏季养护"],
    },
  ],
  realTimeMetrics: {
    totalProjects: 5,
    activeProjects: 3,
    completedToday: 2,
    resourceUtilization: 67,
    aiAccuracy: 94,
    costEfficiency: 89,
    weatherImpact: 15,
    seasonalOptimization: 88,
    plantSurvivalRate: 92,
  },
}

export function EnhancedSchedulingDashboard() {
  const [activeTab, setActiveTab] = useState("overview")
  const [schedulingData, setSchedulingData] = useState(mockEnhancedData)
  const [isAIRunning, setIsAIRunning] = useState(false)
  const [realTimeData, setRealTimeData] = useState(mockEnhancedData.realTimeMetrics)
  const [currentWeather, setCurrentWeather] = useState("晴天")
  const [currentSeason, setCurrentSeason] = useState("春季")

  // 模拟实时数据更新
  useEffect(() => {
    const interval = setInterval(() => {
      setRealTimeData((prev) => ({
        ...prev,
        resourceUtilization: Math.max(50, Math.min(95, prev.resourceUtilization + (Math.random() - 0.5) * 4)),
        aiAccuracy: Math.max(85, Math.min(98, prev.aiAccuracy + (Math.random() - 0.5) * 2)),
        costEfficiency: Math.max(80, Math.min(95, prev.costEfficiency + (Math.random() - 0.5) * 3)),
        plantSurvivalRate: Math.max(85, Math.min(98, prev.plantSurvivalRate + (Math.random() - 0.5) * 2)),
        seasonalOptimization: Math.max(80, Math.min(95, prev.seasonalOptimization + (Math.random() - 0.5) * 3)),
      }))
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  const handleRunAIScheduling = async () => {
    setIsAIRunning(true)

    // 模拟AI处理时间
    await new Promise((resolve) => setTimeout(resolve, 2000))

    // 园林施工AI智能分配逻辑
    const updatedProjects = schedulingData.projects.map((project) => {
      const suitableStaff = schedulingData.availableStaff
        .filter((staff) => {
          // 基础可用性检查
          if (staff.availability !== "可用" || staff.workload >= 80) return false

          // 技能匹配检查
          const hasRequiredSkills = project.requiredSkills.some((skill) => staff.skills.includes(skill))
          if (!hasRequiredSkills) return false

          // 专业领域匹配
          const specializationMatch = staff.specialization === project.projectType

          // 区域匹配（优先同区域）
          const regionMatch = staff.region === project.location.split("·")[0]

          // 季节适应性检查
          const seasonMatch = staff.seasonalPreference.includes(project.season) || staff.seasonalPreference === "全年"

          // 天气适应性检查
          const weatherMatch = staff.weatherSuitability.includes(currentWeather)

          // 综合评分
          let score = 0
          if (hasRequiredSkills) score += 40
          if (specializationMatch) score += 30
          if (regionMatch) score += 15
          if (seasonMatch) score += 10
          if (weatherMatch) score += 5

          return score >= 50 // 至少50分才能被分配
        })
        .sort((a, b) => {
          // 按综合评分排序
          const scoreA = a.efficiency + a.experience * 2 + (a.level === "专家" ? 20 : a.level === "高级" ? 10 : 0)
          const scoreB = b.efficiency + b.experience * 2 + (b.level === "专家" ? 20 : b.level === "高级" ? 10 : 0)
          return scoreB - scoreA
        })

      return {
        ...project,
        assignedStaff: suitableStaff.slice(0, Math.min(3, suitableStaff.length)),
        status: suitableStaff.length > 0 ? "已分配" : "待分配",
        progress: suitableStaff.length > 0 ? Math.floor(Math.random() * 30) + 10 : 0,
        aiRecommendations:
          suitableStaff.length > 0
            ? [
                `推荐${suitableStaff[0].name}作为项目负责人`,
                `当前${currentSeason}${currentWeather}，适合${project.constructionPhase}`,
                `预计植物成活率：${Math.floor(Math.random() * 10) + 90}%`,
              ]
            : ["暂无合适人员", "建议调整项目时间或要求"],
      }
    })

    setSchedulingData((prev) => ({
      ...prev,
      projects: updatedProjects,
    }))

    setIsAIRunning(false)
  }

  const handleStaffAssignment = (staffId: string, projectId: string) => {
    const staff = schedulingData.availableStaff.find((s) => s.id === staffId)
    const project = schedulingData.projects.find((p) => p.id === projectId)

    if (!staff || !project) return

    // 更新项目分配
    const updatedProjects = schedulingData.projects.map((p) => {
      if (p.id === projectId) {
        const isAlreadyAssigned = p.assignedStaff.some((s) => s.id === staffId)
        if (isAlreadyAssigned) return p

        return {
          ...p,
          assignedStaff: [...p.assignedStaff, staff],
          status: "已分配",
        }
      }
      return p
    })

    // 更新人员工作负载
    const updatedStaff = schedulingData.availableStaff.map((s) => {
      if (s.id === staffId) {
        return {
          ...s,
          workload: Math.min(100, s.workload + 20),
        }
      }
      return s
    })

    setSchedulingData((prev) => ({
      ...prev,
      projects: updatedProjects,
      availableStaff: updatedStaff,
    }))
  }

  const handleApplyRecommendation = (recommendation: any) => {
    if (recommendation.type === "assignment" && recommendation.staffId && recommendation.projectId) {
      handleStaffAssignment(recommendation.staffId, recommendation.projectId)
    }
    // 可以添加其他类型推荐的处理逻辑
  }

  const stats = {
    totalStaff: schedulingData.availableStaff.length,
    availableStaff: schedulingData.availableStaff.filter((s) => s.availability === "可用").length,
    activeProjects: schedulingData.projects.length,
    assignedProjects: schedulingData.projects.filter((p) => p.status === "已分配").length,
    avgEfficiency: Math.round(
      schedulingData.availableStaff.reduce((acc, s) => acc + s.efficiency, 0) / schedulingData.availableStaff.length,
    ),
    totalArea: schedulingData.projects.reduce((sum, p) => sum + Number.parseInt(p.area?.replace("㎡", "") || "0"), 0),
  }

  return (
    <div className="space-y-8">
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-5">
        <Card className="luxury-card floating-animation">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-white/80">施工面积</CardTitle>
            <Trees className="h-5 w-5 text-green-400 pulse-glow" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-white mb-1">{(stats.totalArea / 10000).toFixed(1)}万㎡</div>
            <div className="flex items-center text-xs text-green-400">
              <TrendingUp className="w-3 h-3 mr-1" />
              总施工面积
            </div>
          </CardContent>
        </Card>

        <Card className="luxury-card floating-animation" style={{ animationDelay: "0.3s" }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-white/80">植物成活率</CardTitle>
            <Sprout className="h-5 w-5 text-emerald-400 pulse-glow" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-white mb-1">{Math.round(realTimeData.plantSurvivalRate)}%</div>
            <div className="flex items-center text-xs text-emerald-400">
              <Target className="w-3 h-3 mr-1" />
              种植成活率
            </div>
          </CardContent>
        </Card>

        <Card className="luxury-card floating-animation" style={{ animationDelay: "0.6s" }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-white/80">季节优化</CardTitle>
            <Sun className="h-5 w-5 text-amber-400 pulse-glow" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-white mb-1">{Math.round(realTimeData.seasonalOptimization)}%</div>
            <div className="flex items-center text-xs text-amber-400">
              <Calendar className="w-3 h-3 mr-1" />
              {currentSeason}施工
            </div>
          </CardContent>
        </Card>

        <Card className="luxury-card floating-animation" style={{ animationDelay: "0.9s" }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-white/80">天气适应</CardTitle>
            <CloudRain className="h-5 w-5 text-blue-400 pulse-glow" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-white mb-1">{currentWeather}</div>
            <div className="flex items-center text-xs text-blue-400">
              <Activity className="w-3 h-3 mr-1" />
              当前天气
            </div>
          </CardContent>
        </Card>

        <Card className="luxury-card floating-animation" style={{ animationDelay: "1.2s" }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-white/80">AI匹配度</CardTitle>
            <Brain className="h-5 w-5 text-purple-400 pulse-glow" />
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-white mb-1">{Math.round(realTimeData.aiAccuracy)}%</div>
            <div className="flex items-center text-xs text-purple-400">
              <Target className="w-3 h-3 mr-1" />
              智能推荐
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 区域资源分布组件 */}
      <Card className="luxury-card">
        <CardHeader>
          <CardTitle className="text-xl text-white flex items-center">
            <Users className="w-6 h-6 mr-3 text-emerald-400" />
            区域资源分布 - 园林景观施工团队
          </CardTitle>
          <p className="text-white/70">按地理区域查看专业施工团队配置与项目分布</p>
        </CardHeader>
        <CardContent>
          <RegionalResourceDistribution onRegionSelect={(regionId) => console.log("选中区域:", regionId)} />
        </CardContent>
      </Card>

      {/* 主控制面板 */}
      <Card className="luxury-card">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl text-white mb-2">园林景观智能调度控制台</CardTitle>
              <p className="text-white/70">AI驱动的季节性施工资源优化与天气适应性调度</p>
              <div className="flex items-center gap-4 mt-2 text-sm text-white/60">
                <span>当前季节: {currentSeason}</span>
                <span>天气状况: {currentWeather}</span>
                <span>适宜施工项目: {schedulingData.projects.filter((p) => p.weather === "适宜").length}个</span>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Button
                onClick={handleRunAIScheduling}
                disabled={isAIRunning}
                className="luxury-button text-white px-6 py-3"
              >
                <Zap className="w-5 h-5 mr-2" />
                {isAIRunning ? "AI分析中..." : "启动园林AI调度"}
              </Button>
              <Button variant="outline" className="luxury-button text-white border-white/30 bg-transparent">
                <Settings className="w-5 h-5 mr-2" />
                季节配置
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-7 max-w-5xl glass-morphism">
              <TabsTrigger value="overview" className="text-white">
                施工概览
              </TabsTrigger>
              <TabsTrigger value="regional" className="text-white">
                区域分布
              </TabsTrigger>
              <TabsTrigger value="projects" className="text-white">
                项目矩阵
              </TabsTrigger>
              <TabsTrigger value="resources" className="text-white">
                人员资源
              </TabsTrigger>
              <TabsTrigger value="intelligent" className="text-white">
                智能调度
              </TabsTrigger>
              <TabsTrigger value="analytics" className="text-white">
                AI分析
              </TabsTrigger>
              <TabsTrigger value="performance" className="text-white">
                性能监控
              </TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="mt-8">
              <div className="grid gap-6 lg:grid-cols-2">
                <Card className="luxury-card">
                  <CardHeader>
                    <CardTitle className="text-white">园林项目状态分布</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {schedulingData.projects.map((project, index) => (
                        <div
                          key={project.id}
                          className="flex items-center justify-between p-3 rounded-lg glass-morphism"
                        >
                          <div className="flex items-center space-x-3">
                            <div
                              className={`w-3 h-3 rounded-full ${
                                project.status === "已分配" ? "bg-green-400 glow-accent" : "bg-amber-400"
                              }`}
                            />
                            <div>
                              <span className="text-white font-medium">{project.name}</span>
                              <div className="text-xs text-white/60 mt-1">
                                {project.projectType} · {project.location} · {project.area}
                              </div>
                            </div>
                          </div>
                          <div className="flex flex-col items-end gap-1">
                            <Badge variant={project.priority === "高" ? "destructive" : "secondary"}>
                              {project.priority}优先级
                            </Badge>
                            <span className="text-xs text-white/60">{project.constructionPhase}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                <Card className="luxury-card">
                  <CardHeader>
                    <CardTitle className="text-white">专业人员工作负载</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {schedulingData.availableStaff.map((staff) => (
                        <div key={staff.id} className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <div>
                              <span className="text-white">{staff.name}</span>
                              <span className="text-white/60 ml-2">({staff.position})</span>
                            </div>
                            <span className="text-white/70">{staff.workload}%</span>
                          </div>
                          <div className="flex items-center gap-2 text-xs text-white/60">
                            <span>{staff.region}</span>
                            <span>•</span>
                            <span>{staff.specialization}</span>
                            <span>•</span>
                            <span>{staff.experience}年经验</span>
                          </div>
                          <div className="w-full bg-white/10 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full transition-all duration-500 ${
                                staff.workload > 80
                                  ? "bg-red-400"
                                  : staff.workload > 60
                                    ? "bg-amber-400"
                                    : "bg-green-400"
                              }`}
                              style={{ width: `${staff.workload}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="regional" className="mt-8">
              <RegionalResourceDistribution
                onRegionSelect={(regionId) => {
                  console.log("切换到区域:", regionId)
                }}
              />
            </TabsContent>

            <TabsContent value="projects" className="mt-8">
              <ProjectOverviewMap
                projects={schedulingData.projects}
                onProjectSelect={(project) => console.log("选中项目:", project)}
              />
            </TabsContent>

            <TabsContent value="resources" className="mt-8">
              <ResourceHeatmap
                staff={schedulingData.availableStaff}
                onStaffSelect={(staff) => console.log("选中人员:", staff)}
              />
            </TabsContent>

            <TabsContent value="intelligent" className="mt-8">
              <FluidDragDrop
                staff={schedulingData.availableStaff}
                projects={schedulingData.projects}
                onAssignment={handleStaffAssignment}
              />
            </TabsContent>

            <TabsContent value="analytics" className="mt-8">
              <PredictiveAnalyzer staff={schedulingData.availableStaff} projects={schedulingData.projects} />
            </TabsContent>

            <TabsContent value="performance" className="mt-8">
              <PerformanceMonitor />
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}
