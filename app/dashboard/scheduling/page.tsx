import { EnhancedSchedulingDashboard } from "@/components/scheduling/enhanced-scheduling-dashboard"

export default function SchedulingPage() {
  return (
    <div className="scheduling-command-center">
      <div className="relative z-10 flex-1 space-y-8 p-8">
        <div className="space-y-4">
          <div className="luxury-card p-6">
            <h1 className="text-4xl font-bold text-white mb-2 text-balance">智能调度指挥中心</h1>
            <p className="text-white/80 text-lg">基于AI算法的企业级人力资源智能调度与全景管理平台</p>
          </div>
        </div>
        <EnhancedSchedulingDashboard />
      </div>
    </div>
  )
}
