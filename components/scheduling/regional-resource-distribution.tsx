"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { MapPin, Users, Wrench, TreePine, Flower, Eye } from "lucide-react"

// 园林景观施工行业的区域资源数据
const regionalData = {
  华中: {
    id: "central",
    name: "华中区域",
    color: "bg-emerald-500",
    totalStaff: 45,
    availableStaff: 32,
    activeProjects: 8,
    specialties: ["园林设计", "绿化施工", "景观维护"],
    staff: [
      {
        id: "c1",
        name: "李园林",
        position: "高级园林设计师",
        specialty: "古典园林",
        status: "可用",
        experience: "8年",
      },
      { id: "c2", name: "王绿化", position: "绿化工程师", specialty: "植物配置", status: "项目中", experience: "5年" },
      { id: "c3", name: "张景观", position: "景观施工员", specialty: "硬质景观", status: "可用", experience: "6年" },
      { id: "c4", name: "陈维护", position: "养护技师", specialty: "植物养护", status: "可用", experience: "4年" },
    ],
    currentProjects: ["武汉东湖公园改造", "长沙橘子洲景观", "郑州绿博园扩建"],
  },
  华南: {
    id: "south",
    name: "华南区域",
    color: "bg-orange-500",
    totalStaff: 38,
    availableStaff: 28,
    activeProjects: 6,
    specialties: ["热带植物", "滨海景观", "度假村园林"],
    staff: [
      { id: "s1", name: "林热带", position: "热带植物专家", specialty: "热带园林", status: "可用", experience: "10年" },
      { id: "s2", name: "黄滨海", position: "滨海景观师", specialty: "海岸景观", status: "可用", experience: "7年" },
      {
        id: "s3",
        name: "吴度假",
        position: "度假村设计师",
        specialty: "休闲景观",
        status: "项目中",
        experience: "6年",
      },
      { id: "s4", name: "刘棕榈", position: "棕榈养护师", specialty: "棕榈科植物", status: "可用", experience: "5年" },
    ],
    currentProjects: ["深圳湾公园", "三亚度假村", "广州花城广场"],
  },
  华东: {
    id: "east",
    name: "华东区域",
    color: "bg-blue-500",
    totalStaff: 52,
    availableStaff: 41,
    activeProjects: 10,
    specialties: ["江南园林", "城市绿化", "屋顶花园"],
    staff: [
      { id: "e1", name: "沈江南", position: "江南园林大师", specialty: "苏式园林", status: "可用", experience: "15年" },
      { id: "e2", name: "徐城市", position: "城市绿化师", specialty: "立体绿化", status: "可用", experience: "8年" },
      { id: "e3", name: "朱屋顶", position: "屋顶花园师", specialty: "空中花园", status: "项目中", experience: "6年" },
      { id: "e4", name: "马水景", position: "水景工程师", specialty: "水系景观", status: "可用", experience: "9年" },
    ],
    currentProjects: ["上海外滩绿化", "杭州西湖景区", "南京中山陵", "苏州园林修复"],
  },
  西南: {
    id: "southwest",
    name: "西南区域",
    color: "bg-purple-500",
    totalStaff: 35,
    availableStaff: 26,
    activeProjects: 7,
    specialties: ["山地景观", "民族园林", "生态修复"],
    staff: [
      { id: "w1", name: "杨山地", position: "山地景观师", specialty: "坡地设计", status: "可用", experience: "7年" },
      { id: "w2", name: "罗民族", position: "民族园林师", specialty: "民族风情", status: "可用", experience: "6年" },
      { id: "w3", name: "唐生态", position: "生态修复师", specialty: "植被恢复", status: "项目中", experience: "8年" },
      { id: "w4", name: "何高原", position: "高原植物师", specialty: "高原适应", status: "可用", experience: "5年" },
    ],
    currentProjects: ["成都天府公园", "重庆山城步道", "昆明滇池治理"],
  },
}

interface RegionalResourceDistributionProps {
  onRegionSelect?: (regionId: string) => void
}

export function RegionalResourceDistribution({ onRegionSelect }: RegionalResourceDistributionProps) {
  const [selectedRegion, setSelectedRegion] = useState<string | null>(null)
  const [showStaffDetail, setShowStaffDetail] = useState(false)

  const handleRegionClick = (regionId: string) => {
    setSelectedRegion(regionId)
    setShowStaffDetail(true)
    onRegionSelect?.(regionId)
  }

  const closeDetail = () => {
    setSelectedRegion(null)
    setShowStaffDetail(false)
  }

  const selectedRegionData = selectedRegion ? regionalData[selectedRegion as keyof typeof regionalData] : null

  return (
    <div className="space-y-6">
      {/* 区域概览卡片 */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {Object.entries(regionalData).map(([key, region], index) => (
          <Card
            key={region.id}
            className="luxury-card floating-animation cursor-pointer hover:scale-105 transition-all duration-300"
            style={{ animationDelay: `${index * 0.2}s` }}
            onClick={() => handleRegionClick(key)}
          >
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg text-white flex items-center">
                  <MapPin className="w-5 h-5 mr-2 text-amber-400" />
                  {region.name}
                </CardTitle>
                <div className={`w-3 h-3 rounded-full ${region.color} pulse-glow`} />
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-white/70 text-sm">总人数</span>
                <span className="text-white font-semibold">{region.totalStaff}人</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-white/70 text-sm">可用人员</span>
                <span className="text-emerald-400 font-semibold">{region.availableStaff}人</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-white/70 text-sm">进行项目</span>
                <span className="text-blue-400 font-semibold">{region.activeProjects}个</span>
              </div>

              {/* 利用率进度条 */}
              <div className="space-y-1">
                <div className="flex justify-between text-xs">
                  <span className="text-white/60">资源利用率</span>
                  <span className="text-white/80">
                    {Math.round(((region.totalStaff - region.availableStaff) / region.totalStaff) * 100)}%
                  </span>
                </div>
                <div className="w-full bg-white/10 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-500 ${region.color.replace("bg-", "bg-gradient-to-r from-")} to-transparent`}
                    style={{ width: `${((region.totalStaff - region.availableStaff) / region.totalStaff) * 100}%` }}
                  />
                </div>
              </div>

              {/* 专业领域标签 */}
              <div className="flex flex-wrap gap-1 mt-3">
                {region.specialties.slice(0, 2).map((specialty) => (
                  <Badge key={specialty} variant="secondary" className="text-xs bg-white/10 text-white/80">
                    {specialty}
                  </Badge>
                ))}
                {region.specialties.length > 2 && (
                  <Badge variant="secondary" className="text-xs bg-white/10 text-white/80">
                    +{region.specialties.length - 2}
                  </Badge>
                )}
              </div>

              <Button
                variant="outline"
                size="sm"
                className="w-full mt-3 luxury-button text-white border-white/30 bg-transparent hover:bg-white/10"
              >
                <Eye className="w-4 h-4 mr-2" />
                查看详情
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* 人员详情弹窗 */}
      {showStaffDetail && selectedRegionData && (
        <Card className="luxury-card">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-xl text-white flex items-center">
                <TreePine className="w-6 h-6 mr-3 text-emerald-400" />
                {selectedRegionData.name} - 人员配置详情
              </CardTitle>
              <Button
                variant="ghost"
                size="sm"
                onClick={closeDetail}
                className="text-white/70 hover:text-white hover:bg-white/10"
              >
                ✕
              </Button>
            </div>
            <p className="text-white/70">园林景观施工专业团队分布</p>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* 区域统计 */}
            <div className="grid gap-4 md:grid-cols-3">
              <div className="glass-morphism p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <Users className="w-8 h-8 text-blue-400" />
                  <div className="text-right">
                    <div className="text-2xl font-bold text-white">{selectedRegionData.totalStaff}</div>
                    <div className="text-sm text-white/70">总人数</div>
                  </div>
                </div>
              </div>
              <div className="glass-morphism p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <Wrench className="w-8 h-8 text-emerald-400" />
                  <div className="text-right">
                    <div className="text-2xl font-bold text-white">{selectedRegionData.availableStaff}</div>
                    <div className="text-sm text-white/70">可调配</div>
                  </div>
                </div>
              </div>
              <div className="glass-morphism p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <Flower className="w-8 h-8 text-purple-400" />
                  <div className="text-right">
                    <div className="text-2xl font-bold text-white">{selectedRegionData.activeProjects}</div>
                    <div className="text-sm text-white/70">在建项目</div>
                  </div>
                </div>
              </div>
            </div>

            {/* 专业团队列表 */}
            <div>
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                <Users className="w-5 h-5 mr-2 text-amber-400" />
                专业团队成员
              </h3>
              <div className="grid gap-3 md:grid-cols-2">
                {selectedRegionData.staff.map((member) => (
                  <div
                    key={member.id}
                    className="glass-morphism p-4 rounded-lg hover:bg-white/10 transition-all duration-300"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-semibold text-white">{member.name}</h4>
                      <Badge
                        variant={member.status === "可用" ? "default" : "secondary"}
                        className={
                          member.status === "可用"
                            ? "bg-emerald-500/20 text-emerald-400"
                            : "bg-amber-500/20 text-amber-400"
                        }
                      >
                        {member.status}
                      </Badge>
                    </div>
                    <div className="space-y-1 text-sm">
                      <div className="text-white/80">{member.position}</div>
                      <div className="text-white/60">专长: {member.specialty}</div>
                      <div className="text-white/60">经验: {member.experience}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* 当前项目 */}
            <div>
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                <TreePine className="w-5 h-5 mr-2 text-emerald-400" />
                在建园林项目
              </h3>
              <div className="space-y-2">
                {selectedRegionData.currentProjects.map((project, index) => (
                  <div key={index} className="flex items-center p-3 glass-morphism rounded-lg">
                    <div className="w-2 h-2 bg-emerald-400 rounded-full mr-3 pulse-glow" />
                    <span className="text-white">{project}</span>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
