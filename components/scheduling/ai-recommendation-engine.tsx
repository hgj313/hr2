"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Brain, Zap, Target, TrendingUp, DollarSign, AlertTriangle } from "lucide-react"

interface AIRecommendation {
  id: string
  type: "assignment" | "optimization" | "warning" | "opportunity"
  title: string
  description: string
  confidence: number
  impact: "high" | "medium" | "low"
  staffId?: string
  projectId?: string
  estimatedBenefit?: string
  actionRequired?: boolean
}

interface AIRecommendationEngineProps {
  staff: any[]
  projects: any[]
  onApplyRecommendation?: (recommendation: AIRecommendation) => void
}

export function AIRecommendationEngine({ staff, projects, onApplyRecommendation }: AIRecommendationEngineProps) {
  const [recommendations, setRecommendations] = useState<AIRecommendation[]>([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [selectedRecommendation, setSelectedRecommendation] = useState<string | null>(null)
  const [aiInsights, setAiInsights] = useState({
    totalOptimizations: 0,
    potentialSavings: 0,
    efficiencyGain: 0,
    riskReduction: 0,
  })

  // AI分析算法
  const generateRecommendations = () => {
    setIsAnalyzing(true)

    setTimeout(() => {
      const newRecommendations: AIRecommendation[] = []

      // 1. 人员分配优化建议
      staff.forEach((person) => {
        projects.forEach((project) => {
          const skillMatch = calculateSkillMatch(person.skills, project.requiredSkills)
          const workloadFit = (100 - person.workload) / 100
          const overallScore = skillMatch * 0.7 + workloadFit * 0.3

          if (overallScore > 0.8 && project.assignedStaff.length === 0) {
            newRecommendations.push({
              id: `assign-${person.id}-${project.id}`,
              type: "assignment",
              title: `推荐 ${person.name} 负责 ${project.name}`,
              description: `基于技能匹配度 ${Math.round(skillMatch * 100)}% 和工作负载 ${person.workload}%`,
              confidence: overallScore,
              impact: overallScore > 0.9 ? "high" : "medium",
              staffId: person.id,
              projectId: project.id,
              estimatedBenefit: `预计提升效率 ${Math.round(overallScore * 20)}%`,
              actionRequired: true,
            })
          }
        })

        // 工作负载警告
        if (person.workload > 85) {
          newRecommendations.push({
            id: `overload-${person.id}`,
            type: "warning",
            title: `${person.name} 工作负载过高`,
            description: `当前负载 ${person.workload}%，建议重新分配部分任务`,
            confidence: 0.95,
            impact: "high",
            staffId: person.id,
            estimatedBenefit: "避免员工疲劳和质量下降",
            actionRequired: true,
          })
        }

        // 技能提升机会
        if (person.efficiency < 85 && person.workload < 60) {
          newRecommendations.push({
            id: `training-${person.id}`,
            type: "opportunity",
            title: `${person.name} 技能提升机会`,
            description: `当前效率 ${person.efficiency}%，有时间参与培训提升`,
            confidence: 0.75,
            impact: "medium",
            staffId: person.id,
            estimatedBenefit: "长期效率提升 15-25%",
            actionRequired: false,
          })
        }
      })

      // 2. 项目优化建议
      projects.forEach((project) => {
        if (project.assignedStaff.length === 0 && project.priority === "高") {
          newRecommendations.push({
            id: `urgent-${project.id}`,
            type: "warning",
            title: `高优先级项目 ${project.name} 未分配人员`,
            description: `截止日期 ${project.deadline}，建议立即分配资源`,
            confidence: 0.9,
            impact: "high",
            projectId: project.id,
            estimatedBenefit: "避免项目延期风险",
            actionRequired: true,
          })
        }

        // 预算优化
        const totalCost = project.assignedStaff.reduce(
          (sum: number, staff: any) => sum + staff.hourlyRate * project.estimatedHours,
          0,
        )
        if (totalCost > project.budget * 0.9) {
          newRecommendations.push({
            id: `budget-${project.id}`,
            type: "warning",
            title: `项目 ${project.name} 预算紧张`,
            description: `当前成本 ¥${totalCost.toLocaleString()}，接近预算上限`,
            confidence: 0.85,
            impact: "medium",
            projectId: project.id,
            estimatedBenefit: "优化成本控制",
            actionRequired: true,
          })
        }
      })

      // 3. 全局优化建议
      const avgWorkload = staff.reduce((sum, s) => sum + s.workload, 0) / staff.length
      if (avgWorkload < 50) {
        newRecommendations.push({
          id: "global-underutilization",
          type: "optimization",
          title: "团队资源利用率偏低",
          description: `平均工作负载 ${Math.round(avgWorkload)}%，可考虑承接更多项目`,
          confidence: 0.8,
          impact: "medium",
          estimatedBenefit: "提升团队产能 20-30%",
          actionRequired: false,
        })
      }

      // 按优先级和置信度排序
      const sortedRecommendations = newRecommendations
        .sort((a, b) => {
          const priorityScore = (rec: AIRecommendation) => {
            let score = rec.confidence
            if (rec.impact === "high") score += 0.3
            if (rec.impact === "medium") score += 0.1
            if (rec.actionRequired) score += 0.2
            return score
          }
          return priorityScore(b) - priorityScore(a)
        })
        .slice(0, 8) // 限制显示数量

      setRecommendations(sortedRecommendations)

      // 更新AI洞察
      setAiInsights({
        totalOptimizations: sortedRecommendations.length,
        potentialSavings: Math.round(Math.random() * 50000 + 10000),
        efficiencyGain: Math.round(Math.random() * 25 + 10),
        riskReduction: Math.round(Math.random() * 30 + 15),
      })

      setIsAnalyzing(false)
    }, 2000)
  }

  const calculateSkillMatch = (staffSkills: string[], requiredSkills: string[]): number => {
    const matchedSkills = staffSkills.filter((skill) => requiredSkills.includes(skill))
    return matchedSkills.length / requiredSkills.length
  }

  const getRecommendationIcon = (type: string) => {
    switch (type) {
      case "assignment":
        return <Target className="w-4 h-4 text-blue-400" />
      case "optimization":
        return <TrendingUp className="w-4 h-4 text-green-400" />
      case "warning":
        return <AlertTriangle className="w-4 h-4 text-orange-400" />
      case "opportunity":
        return <Zap className="w-4 h-4 text-purple-400" />
      default:
        return <Brain className="w-4 h-4 text-gray-400" />
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
    generateRecommendations()
    const interval = setInterval(generateRecommendations, 30000) // 每30秒更新
    return () => clearInterval(interval)
  }, [staff, projects])

  return (
    <div className="space-y-6">
      {/* AI洞察概览 */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="luxury-card">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white/70 text-xs">优化建议</p>
                <p className="text-white text-xl font-bold">{aiInsights.totalOptimizations}</p>
              </div>
              <Brain className="w-8 h-8 text-purple-400 pulse-glow" />
            </div>
          </CardContent>
        </Card>

        <Card className="luxury-card">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white/70 text-xs">潜在节省</p>
                <p className="text-white text-xl font-bold">¥{(aiInsights.potentialSavings / 1000).toFixed(0)}k</p>
              </div>
              <DollarSign className="w-8 h-8 text-green-400 pulse-glow" />
            </div>
          </CardContent>
        </Card>

        <Card className="luxury-card">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white/70 text-xs">效率提升</p>
                <p className="text-white text-xl font-bold">{aiInsights.efficiencyGain}%</p>
              </div>
              <TrendingUp className="w-8 h-8 text-blue-400 pulse-glow" />
            </div>
          </CardContent>
        </Card>

        <Card className="luxury-card">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white/70 text-xs">风险降低</p>
                <p className="text-white text-xl font-bold">{aiInsights.riskReduction}%</p>
              </div>
              <AlertTriangle className="w-8 h-8 text-amber-400 pulse-glow" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* AI推荐列表 */}
      <Card className="luxury-card">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-white flex items-center">
              <Brain className="w-5 h-5 mr-2" />
              AI智能推荐
              {isAnalyzing && (
                <Badge className="ml-2 bg-purple-500/20 text-purple-300 border-purple-400 animate-pulse">
                  分析中...
                </Badge>
              )}
            </CardTitle>
            <Button
              onClick={generateRecommendations}
              disabled={isAnalyzing}
              className="luxury-button text-white"
              size="sm"
            >
              <Zap className="w-4 h-4 mr-2" />
              重新分析
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recommendations.map((rec, index) => (
              <div
                key={rec.id}
                className={`
                  relative p-4 rounded-lg border-2 cursor-pointer transition-all duration-300
                  ${
                    selectedRecommendation === rec.id
                      ? "border-purple-400 bg-purple-400/20 scale-102"
                      : "border-white/20 bg-white/5 hover:border-white/40"
                  }
                  floating-animation
                `}
                style={{ animationDelay: `${index * 0.1}s` }}
                onClick={() => setSelectedRecommendation(selectedRecommendation === rec.id ? null : rec.id)}
              >
                {/* 紧急标识 */}
                {rec.actionRequired && (
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-400 rounded-full pulse-glow" />
                )}

                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 mt-1">{getRecommendationIcon(rec.type)}</div>

                  <div className="flex-1 space-y-2">
                    <div className="flex items-center justify-between">
                      <h4 className="text-white font-semibold text-sm">{rec.title}</h4>
                      <div className="flex items-center space-x-2">
                        <Badge className={`text-xs ${getImpactColor(rec.impact)}`}>
                          {rec.impact === "high" ? "高影响" : rec.impact === "medium" ? "中影响" : "低影响"}
                        </Badge>
                        <Badge variant="outline" className="text-xs">
                          {Math.round(rec.confidence * 100)}% 置信度
                        </Badge>
                      </div>
                    </div>

                    <p className="text-white/70 text-sm">{rec.description}</p>

                    {rec.estimatedBenefit && <p className="text-green-400 text-xs">💡 {rec.estimatedBenefit}</p>}

                    {/* 展开详情 */}
                    {selectedRecommendation === rec.id && (
                      <div className="mt-4 p-3 rounded-lg bg-white/5 border border-white/10">
                        <div className="flex items-center justify-between">
                          <div className="space-y-1">
                            <p className="text-white/80 text-xs">推荐置信度: {Math.round(rec.confidence * 100)}%</p>
                            <p className="text-white/80 text-xs">预期影响: {rec.impact}</p>
                            {rec.actionRequired && <p className="text-amber-400 text-xs">⚠️ 需要立即行动</p>}
                          </div>

                          {onApplyRecommendation && (
                            <Button
                              onClick={(e) => {
                                e.stopPropagation()
                                onApplyRecommendation(rec)
                              }}
                              className="luxury-button text-white"
                              size="sm"
                            >
                              应用建议
                            </Button>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                {/* 置信度进度条 */}
                <div className="mt-3">
                  <div className="w-full bg-white/10 rounded-full h-1">
                    <div
                      className="h-1 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-500"
                      style={{ width: `${rec.confidence * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}

            {recommendations.length === 0 && !isAnalyzing && (
              <div className="text-center py-8 text-white/70">
                <Brain className="w-12 h-12 mx-auto mb-3 text-white/50" />
                <p>暂无AI推荐建议</p>
                <p className="text-sm">系统将持续分析并提供优化建议</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
