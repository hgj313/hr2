"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Loader2, CheckCircle, Cpu, Database, Users, Target } from "lucide-react"
import type { SchedulingConfig, SchedulingResult } from "@/lib/mock-data"
import { executeScheduling } from "@/lib/mock-data"

interface SchedulingExecutionProps {
  config: SchedulingConfig
  onComplete: (result: SchedulingResult) => void
  onCancel: () => void
}

export function SchedulingExecution({ config, onComplete, onCancel }: SchedulingExecutionProps) {
  const [progress, setProgress] = useState(0)
  const [currentStep, setCurrentStep] = useState("")
  const [isExecuting, setIsExecuting] = useState(true)
  const [logs, setLogs] = useState<string[]>([])

  const steps = [
    { id: "init", label: "初始化调度引擎", icon: Cpu },
    { id: "data", label: "加载项目和人员数据", icon: Database },
    { id: "analyze", label: "分析技能和可用性", icon: Users },
    { id: "optimize", label: "执行优化算法", icon: Target },
    { id: "validate", label: "验证调度结果", icon: CheckCircle },
  ]

  useEffect(() => {
    const simulateExecution = async () => {
      const totalSteps = steps.length

      for (let i = 0; i < totalSteps; i++) {
        const step = steps[i]
        setCurrentStep(step.label)
        setLogs((prev) => [...prev, `[${new Date().toLocaleTimeString()}] 开始 ${step.label}...`])

        // Simulate step execution time
        const stepDuration = 800 + Math.random() * 400
        const stepProgress = ((i + 1) / totalSteps) * 100

        await new Promise((resolve) => {
          const interval = setInterval(() => {
            setProgress((prev) => {
              const newProgress = Math.min(prev + 2, stepProgress)
              if (newProgress >= stepProgress) {
                clearInterval(interval)
                resolve(undefined)
              }
              return newProgress
            })
          }, stepDuration / 50)
        })

        setLogs((prev) => [...prev, `[${new Date().toLocaleTimeString()}] 完成 ${step.label}`])
      }

      setLogs((prev) => [...prev, `[${new Date().toLocaleTimeString()}] 调度执行完成，生成结果报告...`])

      // Execute the actual scheduling
      try {
        const result = await executeScheduling(config)
        setIsExecuting(false)
        onComplete(result)
      } catch (error) {
        setLogs((prev) => [...prev, `[${new Date().toLocaleTimeString()}] 错误: 调度执行失败`])
        setIsExecuting(false)
      }
    }

    simulateExecution()
  }, [config, onComplete])

  const getCurrentStepIndex = () => {
    return steps.findIndex((step) => step.label === currentStep)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-balance">执行调度</h1>
          <p className="text-muted-foreground mt-1">正在执行智能调度算法，请稍候...</p>
        </div>
        <Button variant="outline" onClick={onCancel} disabled={!isExecuting}>
          取消执行
        </Button>
      </div>

      {/* Progress Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Loader2 className="w-5 h-5 animate-spin" />
            调度进度
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">总体进度</span>
            <span className="text-sm text-muted-foreground">{Math.round(progress)}%</span>
          </div>
          <Progress value={progress} className="h-3" />
          <div className="text-sm text-muted-foreground">当前步骤: {currentStep}</div>
        </CardContent>
      </Card>

      {/* Step Progress */}
      <Card>
        <CardHeader>
          <CardTitle>执行步骤</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {steps.map((step, index) => {
              const Icon = step.icon
              const currentIndex = getCurrentStepIndex()
              const isCompleted = index < currentIndex
              const isCurrent = index === currentIndex
              const isPending = index > currentIndex

              return (
                <div key={step.id} className="flex items-center gap-3">
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center ${
                      isCompleted
                        ? "bg-green-100 text-green-600"
                        : isCurrent
                          ? "bg-blue-100 text-blue-600"
                          : "bg-gray-100 text-gray-400"
                    }`}
                  >
                    {isCompleted ? (
                      <CheckCircle className="w-4 h-4" />
                    ) : isCurrent ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Icon className="w-4 h-4" />
                    )}
                  </div>
                  <div className="flex-1">
                    <div
                      className={`font-medium ${isCurrent ? "text-blue-600" : isCompleted ? "text-green-600" : "text-gray-500"}`}
                    >
                      {step.label}
                    </div>
                  </div>
                  <Badge variant={isCompleted ? "default" : isCurrent ? "secondary" : "outline"}>
                    {isCompleted ? "已完成" : isCurrent ? "进行中" : "等待中"}
                  </Badge>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Configuration Summary */}
      <Card>
        <CardHeader>
          <CardTitle>调度配置</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <div className="text-muted-foreground">方案名称</div>
              <div className="font-medium">{config.name}</div>
            </div>
            <div>
              <div className="text-muted-foreground">调度周期</div>
              <div className="font-medium">
                {config.startDate} 至 {config.endDate}
              </div>
            </div>
            <div>
              <div className="text-muted-foreground">项目数量</div>
              <div className="font-medium">{config.projectIds.length}个</div>
            </div>
            <div>
              <div className="text-muted-foreground">最大负载</div>
              <div className="font-medium">{config.maxWorkloadPercentage}%</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Execution Logs */}
      <Card>
        <CardHeader>
          <CardTitle>执行日志</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-muted/30 rounded-lg p-4 max-h-48 overflow-y-auto">
            <div className="space-y-1 font-mono text-sm">
              {logs.map((log, index) => (
                <div key={index} className="text-muted-foreground">
                  {log}
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
