"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Activity, Zap, Clock, Cpu, HardDrive, Wifi, AlertTriangle, CheckCircle, TrendingUp } from "lucide-react"

interface PerformanceMetric {
  id: string
  name: string
  value: number
  unit: string
  status: "good" | "warning" | "critical"
  trend: "up" | "down" | "stable"
  threshold: { warning: number; critical: number }
}

interface SystemHealth {
  overall: "healthy" | "warning" | "critical"
  uptime: number
  lastUpdate: Date
  activeUsers: number
  responseTime: number
}

export function PerformanceMonitor() {
  const [metrics, setMetrics] = useState<PerformanceMetric[]>([])
  const [systemHealth, setSystemHealth] = useState<SystemHealth>({
    overall: "healthy",
    uptime: 99.8,
    lastUpdate: new Date(),
    activeUsers: 24,
    responseTime: 120,
  })
  const [isMonitoring, setIsMonitoring] = useState(true)
  const [alertCount, setAlertCount] = useState(0)

  // 生成性能指标数据
  const generateMetrics = () => {
    const newMetrics: PerformanceMetric[] = [
      {
        id: "cpu-usage",
        name: "CPU使用率",
        value: Math.random() * 40 + 30, // 30-70%
        unit: "%",
        status: "good",
        trend: Math.random() > 0.5 ? "up" : "down",
        threshold: { warning: 70, critical: 85 },
      },
      {
        id: "memory-usage",
        name: "内存使用率",
        value: Math.random() * 30 + 40, // 40-70%
        unit: "%",
        status: "good",
        trend: Math.random() > 0.5 ? "up" : "down",
        threshold: { warning: 75, critical: 90 },
      },
      {
        id: "response-time",
        name: "响应时间",
        value: Math.random() * 100 + 80, // 80-180ms
        unit: "ms",
        status: "good",
        trend: Math.random() > 0.5 ? "up" : "down",
        threshold: { warning: 200, critical: 500 },
      },
      {
        id: "throughput",
        name: "吞吐量",
        value: Math.random() * 500 + 800, // 800-1300 req/s
        unit: "req/s",
        status: "good",
        trend: "up",
        threshold: { warning: 500, critical: 300 },
      },
      {
        id: "error-rate",
        name: "错误率",
        value: Math.random() * 2, // 0-2%
        unit: "%",
        status: "good",
        trend: Math.random() > 0.7 ? "up" : "down",
        threshold: { warning: 1, critical: 5 },
      },
      {
        id: "database-connections",
        name: "数据库连接",
        value: Math.random() * 20 + 15, // 15-35
        unit: "个",
        status: "good",
        trend: "stable",
        threshold: { warning: 40, critical: 50 },
      },
    ]

    // 更新状态
    newMetrics.forEach((metric) => {
      if (metric.value >= metric.threshold.critical) {
        metric.status = "critical"
      } else if (metric.value >= metric.threshold.warning) {
        metric.status = "warning"
      }
    })

    setMetrics(newMetrics)

    // 更新系统健康状态
    const criticalCount = newMetrics.filter((m) => m.status === "critical").length
    const warningCount = newMetrics.filter((m) => m.status === "warning").length

    setSystemHealth((prev) => ({
      ...prev,
      overall: criticalCount > 0 ? "critical" : warningCount > 0 ? "warning" : "healthy",
      lastUpdate: new Date(),
      activeUsers: Math.floor(Math.random() * 10) + 20,
      responseTime: newMetrics.find((m) => m.id === "response-time")?.value || 120,
    }))

    setAlertCount(criticalCount + warningCount)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "good":
        return "text-green-400 border-green-400 bg-green-400/20"
      case "warning":
        return "text-amber-400 border-amber-400 bg-amber-400/20"
      case "critical":
        return "text-red-400 border-red-400 bg-red-400/20"
      default:
        return "text-gray-400 border-gray-400 bg-gray-400/20"
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "good":
        return <CheckCircle className="w-4 h-4" />
      case "warning":
      case "critical":
        return <AlertTriangle className="w-4 h-4" />
      default:
        return <Activity className="w-4 h-4" />
    }
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "up":
        return <TrendingUp className="w-3 h-3 text-green-400" />
      case "down":
        return <TrendingUp className="w-3 h-3 text-red-400 rotate-180" />
      default:
        return <div className="w-3 h-3 bg-blue-400 rounded-full" />
    }
  }

  const getMetricIcon = (id: string) => {
    switch (id) {
      case "cpu-usage":
        return <Cpu className="w-5 h-5" />
      case "memory-usage":
        return <HardDrive className="w-5 h-5" />
      case "response-time":
        return <Clock className="w-5 h-5" />
      case "throughput":
        return <Zap className="w-5 h-5" />
      case "error-rate":
        return <AlertTriangle className="w-5 h-5" />
      case "database-connections":
        return <Wifi className="w-5 h-5" />
      default:
        return <Activity className="w-5 h-5" />
    }
  }

  useEffect(() => {
    generateMetrics()

    if (isMonitoring) {
      const interval = setInterval(generateMetrics, 3000) // 每3秒更新
      return () => clearInterval(interval)
    }
  }, [isMonitoring])

  return (
    <div className="space-y-6">
      {/* 系统健康概览 */}
      <Card className="luxury-card">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-white flex items-center">
              <Activity className="w-5 h-5 mr-2" />
              系统性能监控
              <Badge className={`ml-3 ${getStatusColor(systemHealth.overall)}`}>
                {systemHealth.overall === "healthy" ? "健康" : systemHealth.overall === "warning" ? "警告" : "严重"}
              </Badge>
            </CardTitle>
            <div className="flex items-center space-x-4">
              {alertCount > 0 && (
                <Badge variant="destructive" className="animate-pulse">
                  {alertCount} 个警告
                </Badge>
              )}
              <Button
                onClick={() => setIsMonitoring(!isMonitoring)}
                variant={isMonitoring ? "default" : "outline"}
                className="luxury-button text-white"
                size="sm"
              >
                {isMonitoring ? "暂停监控" : "开始监控"}
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-white mb-1">{systemHealth.uptime}%</div>
              <div className="text-white/70 text-sm">系统可用性</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-white mb-1">{systemHealth.activeUsers}</div>
              <div className="text-white/70 text-sm">在线用户</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-white mb-1">{Math.round(systemHealth.responseTime)}ms</div>
              <div className="text-white/70 text-sm">平均响应时间</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-white mb-1">
                {systemHealth.lastUpdate.toLocaleTimeString("zh-CN", {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </div>
              <div className="text-white/70 text-sm">最后更新</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 性能指标网格 */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {metrics.map((metric, index) => (
          <Card
            key={metric.id}
            className={`luxury-card floating-animation ${getStatusColor(metric.status)}`}
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  {getMetricIcon(metric.id)}
                  <CardTitle className="text-sm text-white">{metric.name}</CardTitle>
                </div>
                <div className="flex items-center space-x-1">
                  {getStatusIcon(metric.status)}
                  {getTrendIcon(metric.trend)}
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="text-center">
                  <div className="text-2xl font-bold text-white">
                    {Math.round(metric.value * 10) / 10}
                    <span className="text-sm text-white/70 ml-1">{metric.unit}</span>
                  </div>
                </div>

                {/* 性能条 */}
                <div className="space-y-1">
                  <div className="flex justify-between text-xs text-white/70">
                    <span>0</span>
                    <span>警告: {metric.threshold.warning}</span>
                    <span>严重: {metric.threshold.critical}</span>
                  </div>
                  <div className="w-full bg-white/10 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-500 ${
                        metric.status === "critical"
                          ? "bg-red-400"
                          : metric.status === "warning"
                            ? "bg-amber-400"
                            : "bg-green-400"
                      }`}
                      style={{
                        width: `${Math.min(100, (metric.value / (metric.threshold.critical * 1.2)) * 100)}%`,
                      }}
                    />
                  </div>
                </div>

                {/* 状态描述 */}
                <div className="text-xs text-white/70 text-center">
                  {metric.status === "good" ? "运行正常" : metric.status === "warning" ? "需要关注" : "需要立即处理"}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* 实时性能图表 */}
      <Card className="luxury-card">
        <CardHeader>
          <CardTitle className="text-white flex items-center">
            <TrendingUp className="w-5 h-5 mr-2" />
            实时性能趋势
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2">
            {/* CPU和内存使用率 */}
            <div className="space-y-4">
              <h4 className="text-white font-medium">CPU & 内存使用率</h4>
              <div className="h-32 bg-white/5 rounded-lg flex items-end justify-between p-4">
                {Array.from({ length: 10 }, (_, i) => {
                  const cpuValue = Math.random() * 30 + 40
                  const memValue = Math.random() * 25 + 35
                  return (
                    <div key={i} className="flex flex-col items-center space-y-1">
                      <div className="flex space-x-1">
                        <div
                          className="bg-blue-400 rounded-t"
                          style={{ height: `${cpuValue}px`, width: "4px" }}
                          title={`CPU: ${Math.round(cpuValue)}%`}
                        />
                        <div
                          className="bg-purple-400 rounded-t"
                          style={{ height: `${memValue}px`, width: "4px" }}
                          title={`内存: ${Math.round(memValue)}%`}
                        />
                      </div>
                      <span className="text-white/70 text-xs">{i + 1}</span>
                    </div>
                  )
                })}
              </div>
              <div className="flex justify-center space-x-4 text-xs">
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-blue-400 rounded"></div>
                  <span className="text-white/70">CPU</span>
                </div>
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-purple-400 rounded"></div>
                  <span className="text-white/70">内存</span>
                </div>
              </div>
            </div>

            {/* 响应时间和吞吐量 */}
            <div className="space-y-4">
              <h4 className="text-white font-medium">响应时间 & 吞吐量</h4>
              <div className="h-32 bg-white/5 rounded-lg flex items-end justify-between p-4">
                {Array.from({ length: 10 }, (_, i) => {
                  const responseTime = Math.random() * 50 + 80
                  const throughput = Math.random() * 200 + 800
                  return (
                    <div key={i} className="flex flex-col items-center space-y-1">
                      <div className="flex space-x-1">
                        <div
                          className="bg-green-400 rounded-t"
                          style={{ height: `${(responseTime / 200) * 80}px`, width: "4px" }}
                          title={`响应时间: ${Math.round(responseTime)}ms`}
                        />
                        <div
                          className="bg-amber-400 rounded-t"
                          style={{ height: `${(throughput / 1200) * 80}px`, width: "4px" }}
                          title={`吞吐量: ${Math.round(throughput)} req/s`}
                        />
                      </div>
                      <span className="text-white/70 text-xs">{i + 1}</span>
                    </div>
                  )
                })}
              </div>
              <div className="flex justify-center space-x-4 text-xs">
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-green-400 rounded"></div>
                  <span className="text-white/70">响应时间</span>
                </div>
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-amber-400 rounded"></div>
                  <span className="text-white/70">吞吐量</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
