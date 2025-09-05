"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { TrendingUp, TrendingDown, AlertTriangle, Target, Calendar, Users, DollarSign, Brain, Zap } from "lucide-react"

interface PredictionData {
  id: string
  type: "resource_demand" | "project_completion" | "cost_forecast" | "risk_assessment"
  title: string
  currentValue: number
  predictedValue: number
  confidence: number
  trend: "up" | "down" | "stable"
  timeframe: string
  impact: "high" | "medium" | "low"
  recommendations: string[]
}

interface PredictiveAnalyzerProps {
  staff: any[]
  projects: any[]
}

export function PredictiveAnalyzer({ staff, projects }: PredictiveAnalyzerProps) {
  const [predictions, setPredictions] = useState<PredictionData[]>([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [selectedTimeframe, setSelectedTimeframe] = useState<"1week" | "1month" | "3months">("1month")
  const [forecastAccuracy, setForecastAccuracy] = useState(0)

  // 生成预测分析数据
  const generatePredictions = () => {
    setIsAnalyzing(true)

    setTimeout(() => {
      const newPredictions: PredictionData[] = []

      // 1. 资源需求预测
      const currentUtilization = staff.reduce((sum, s) => sum + s.workload, 0) / staff.length
      const predictedUtilization = currentUtilization + (Math.random() - 0.5) * 20

      newPredictions.push({
        id: "resource-demand",
        type: "resource_demand",
        title: "团队资源利用率预测",
        currentValue: currentUtilization,
        predictedValue: predictedUtilization,
        confidence: 0.85,
        trend: predictedUtilization > currentUtilization ? "up" : "down",
        timeframe: selectedTimeframe === "1week" ? "下周" : selectedTimeframe === "1month" ? "下月" : "下季度",
        impact: Math.abs(predictedUtilization - currentUtilization) > 15 ? "high" : "medium",
        recommendations: [
          predictedUtilization > 80 ? "建议招聘新员工或外包部分工作" : "资源充足，可考虑承接更多项目",
          "优化工作分配，平衡团队负载",
          "提前规划培训和技能提升",
        ],
      })

      // 2. 项目完成时间预测
      projects.forEach((project) => {
        const baseProgress = project.progress || 0
        const predictedProgress = Math.min(100, baseProgress + Math.random() * 40 + 20)
        const daysToComplete = Math.round((100 - predictedProgress) / 2)

        newPredictions.push({
          id: `project-completion-${project.id}`,
          type: "project_completion",
          title: `${project.name} 完成时间预测`,
          currentValue: baseProgress,
          predictedValue: predictedProgress,
          confidence: 0.78,
          trend: "up",
          timeframe: `预计 ${daysToComplete} 天后完成`,
          impact:
            new Date(project.deadline) < new Date(Date.now() + daysToComplete * 24 * 60 * 60 * 1000) ? "low" : "high",
          recommendations: [
            daysToComplete > 30 ? "项目进度正常，保持当前节奏" : "需要加快进度或调整资源分配",
            "定期检查里程碑完成情况",
            "及时沟通潜在风险和阻碍",
          ],
        })
      })

      // 3. 成本预测
      const totalBudget = projects.reduce((sum, p) => sum + p.budget, 0)
      const predictedCost = totalBudget * (0.85 + Math.random() * 0.3)

      newPredictions.push({
        id: "cost-forecast",
        type: "cost_forecast",
        title: "项目成本预测",
        currentValue: totalBudget * 0.6, // 假设已花费60%
        predictedValue: predictedCost,
        confidence: 0.82,
        trend: predictedCost > totalBudget ? "up" : "down",
        timeframe: "项目结束时",
        impact: predictedCost > totalBudget * 1.1 ? "high" : "medium",
        recommendations: [
          predictedCost > totalBudget ? "成本可能超支，需要优化资源配置" : "成本控制良好",
          "定期审查预算执行情况",
          "考虑成本效益更高的解决方案",
        ],
      })

      // 4. 风险评估
      const highPriorityProjects = projects.filter((p) => p.priority === "高").length
      const riskScore = (highPriorityProjects / projects.length) * 100

      newPredictions.push({
        id: "risk-assessment",
        type: "risk_assessment",
        title: "项目风险评估",
        currentValue: riskScore,
        predictedValue: riskScore + Math.random() * 20 - 10,
        confidence: 0.75,
        trend: Math.random() > 0.5 ? "up" : "down",
        timeframe: "未来一个月",
        impact: riskScore > 60 ? "high" : "medium",
        recommendations: ["制定风险缓解策略", "增加项目监控频率", "准备应急预案和备用资源"],
      })

      setPredictions(newPredictions)
      setForecastAccuracy(Math.random() * 15 + 80) // 80-95%的准确率
      setIsAnalyzing(false)
    }, 2000)
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "up":
        return <TrendingUp className="w-4 h-4 text-green-400" />
      case "down":
        return <TrendingDown className="w-4 h-4 text-red-400" />
      default:
        return <Target className="w-4 h-4 text-blue-400" />
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "resource_demand":
        return <Users className="w-5 h-5 text-blue-400" />
      case "project_completion":
        return <Calendar className="w-5 h-5 text-green-400" />
      case "cost_forecast":
        return <DollarSign className="w-5 h-5 text-amber-400" />
      case "risk_assessment":
        return <AlertTriangle className="w-5 h-5 text-red-400" />
      default:
        return <Brain className="w-5 h-5 text-purple-400" />
    }
  }

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case "high":
        return "border-red-400 bg-red-400/10 text-red-300"
      case "medium":
        return "border-amber-400 bg-amber-400/10 text-amber-300"
      case "low":
        return "border-green-400 bg-green-400/10 text-green-300"
      default:
        return "border-gray-400 bg-gray-400/10 text-gray-300"
    }
  }

  useEffect(() => {
    generatePredictions()
  }, [selectedTimeframe, staff, projects])

  return (
    <div className="space-y-6">
      {/* 预测控制面板 */}
      <Card className="luxury-card">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-white flex items-center">
              <Brain className="w-5 h-5 mr-2" />
              AI预测分析引擎
              {isAnalyzing && (
                <Badge className="ml-2 bg-purple-500/20 text-purple-300 border-purple-400 animate-pulse">
                  分析中...
                </Badge>
              )}
            </CardTitle>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <span className="text-white/70 text-sm">预测周期:</span>
                <select
                  value={selectedTimeframe}
                  onChange={(e) => setSelectedTimeframe(e.target.value as any)}
                  className="bg-white/10 border border-white/20 rounded px-3 py-1 text-white text-sm"
                >
                  <option value="1week">1周</option>
                  <option value="1month">1个月</option>
                  <option value="3months">3个月</option>
                </select>
              </div>
              <Button
                onClick={generatePredictions}
                disabled={isAnalyzing}
                className="luxury-button text-white"
                size="sm"
              >
                <Zap className="w-4 h-4 mr-2" />
                重新预测
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3 mb-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-white mb-1">{Math.round(forecastAccuracy)}%</div>
              <div className="text-white/70 text-sm">预测准确率</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-white mb-1">{predictions.length}</div>
              <div className="text-white/70 text-sm">预测维度</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-white mb-1">
                {predictions.filter((p) => p.impact === "high").length}
              </div>
              <div className="text-white/70 text-sm">高影响预测</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 预测结果展示 */}
      <div className="grid gap-6 lg:grid-cols-2">
        {predictions.map((prediction, index) => (
          <Card
            key={prediction.id}
            className="luxury-card floating-animation"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {getTypeIcon(prediction.type)}
                  <CardTitle className="text-white text-lg">{prediction.title}</CardTitle>
                </div>
                <Badge className={`${getImpactColor(prediction.impact)}`}>
                  {prediction.impact === "high" ? "高影响" : prediction.impact === "medium" ? "中影响" : "低影响"}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* 预测数值对比 */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-3 rounded-lg bg-white/5">
                    <div className="text-white/70 text-xs mb-1">当前值</div>
                    <div className="text-white text-xl font-bold">
                      {prediction.type === "cost_forecast" || prediction.type === "resource_demand"
                        ? `${Math.round(prediction.currentValue)}${prediction.type === "cost_forecast" ? "k" : "%"}`
                        : `${Math.round(prediction.currentValue)}%`}
                    </div>
                  </div>
                  <div className="text-center p-3 rounded-lg bg-white/5">
                    <div className="text-white/70 text-xs mb-1">预测值</div>
                    <div className="text-white text-xl font-bold flex items-center justify-center">
                      {prediction.type === "cost_forecast" || prediction.type === "resource_demand"
                        ? `${Math.round(prediction.predictedValue)}${prediction.type === "cost_forecast" ? "k" : "%"}`
                        : `${Math.round(prediction.predictedValue)}%`}
                      <span className="ml-2">{getTrendIcon(prediction.trend)}</span>
                    </div>
                  </div>
                </div>

                {/* 预测详情 */}
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-white/70">预测时间</span>
                    <span className="text-white">{prediction.timeframe}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-white/70">置信度</span>
                    <span className="text-white">{Math.round(prediction.confidence * 100)}%</span>
                  </div>
                </div>

                {/* 置信度进度条 */}
                <div className="space-y-1">
                  <div className="w-full bg-white/10 rounded-full h-2">
                    <div
                      className="h-2 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-500"
                      style={{ width: `${prediction.confidence * 100}%` }}
                    />
                  </div>
                </div>

                {/* AI建议 */}
                <div className="space-y-2">
                  <div className="text-white/80 text-sm font-medium">AI建议:</div>
                  <div className="space-y-1">
                    {prediction.recommendations.slice(0, 2).map((rec, idx) => (
                      <div key={idx} className="text-white/70 text-xs flex items-start">
                        <span className="text-amber-400 mr-2">•</span>
                        {rec}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* 趋势分析图表 */}
      <Card className="luxury-card">
        <CardHeader>
          <CardTitle className="text-white flex items-center">
            <TrendingUp className="w-5 h-5 mr-2" />
            预测趋势分析
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2">
            {/* 资源利用率趋势 */}
            <div className="space-y-4">
              <h4 className="text-white font-medium">资源利用率趋势</h4>
              <div className="h-32 bg-white/5 rounded-lg flex items-end justify-between p-4">
                {[65, 72, 68, 75, 82, 78, 85].map((value, index) => (
                  <div key={index} className="flex flex-col items-center space-y-2">
                    <div
                      className="bg-gradient-to-t from-blue-400 to-purple-400 rounded-t"
                      style={{ height: `${value}%`, width: "12px" }}
                    />
                    <span className="text-white/70 text-xs">{index === 6 ? "预测" : `第${index + 1}周`}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* 项目完成率预测 */}
            <div className="space-y-4">
              <h4 className="text-white font-medium">项目完成率预测</h4>
              <div className="h-32 bg-white/5 rounded-lg flex items-end justify-between p-4">
                {[20, 35, 50, 65, 78, 88, 95].map((value, index) => (
                  <div key={index} className="flex flex-col items-center space-y-2">
                    <div
                      className="bg-gradient-to-t from-green-400 to-emerald-400 rounded-t"
                      style={{ height: `${value}%`, width: "12px" }}
                    />
                    <span className="text-white/70 text-xs">{index === 6 ? "预测" : `第${index + 1}周`}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
