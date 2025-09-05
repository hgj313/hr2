"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { X } from "lucide-react"

interface ProjectFormProps {
  initialData?: any
  onSubmit: (data: any) => void
}

export function ProjectForm({ initialData, onSubmit }: ProjectFormProps) {
  const [formData, setFormData] = useState({
    name: initialData?.name || "",
    description: initialData?.description || "",
    status: initialData?.status || "计划中",
    priority: initialData?.priority || "中",
    startDate: initialData?.startDate || "",
    endDate: initialData?.endDate || "",
    budget: initialData?.budget || 0,
    manager: initialData?.manager || "",
    tags: initialData?.tags || [],
    projectType: initialData?.projectType || "",
    location: initialData?.location || "",
    area: initialData?.area || "",
    season: initialData?.season || "",
    weather: initialData?.weather || "",
    plantTypes: initialData?.plantTypes || [],
    constructionPhase: initialData?.constructionPhase || "设计阶段",
  })

  const [newTag, setNewTag] = useState("")
  const [newPlantType, setNewPlantType] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  const handleAddTag = () => {
    if (newTag.trim() && !formData.tags.includes(newTag.trim())) {
      setFormData((prev) => ({
        ...prev,
        tags: [...prev.tags, newTag.trim()],
      }))
      setNewTag("")
    }
  }

  const handleAddPlantType = () => {
    if (newPlantType.trim() && !formData.plantTypes.includes(newPlantType.trim())) {
      setFormData((prev) => ({
        ...prev,
        plantTypes: [...prev.plantTypes, newPlantType.trim()],
      }))
      setNewPlantType("")
    }
  }

  const handleRemoveTag = (tagToRemove: string) => {
    setFormData((prev) => ({
      ...prev,
      tags: prev.tags.filter((tag) => tag !== tagToRemove),
    }))
  }

  const handleRemovePlantType = (plantToRemove: string) => {
    setFormData((prev) => ({
      ...prev,
      plantTypes: prev.plantTypes.filter((plant) => plant !== plantToRemove),
    }))
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault()
      handleAddTag()
    }
  }

  const handlePlantKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault()
      handleAddPlantType()
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <Label htmlFor="name">项目名称 *</Label>
          <Input
            id="name"
            value={formData.name}
            onChange={(e) => setFormData((prev) => ({ ...prev, name: e.target.value }))}
            placeholder="如：绿城·桂花园住宅景观"
            required
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="manager">项目经理 *</Label>
          <Input
            id="manager"
            value={formData.manager}
            onChange={(e) => setFormData((prev) => ({ ...prev, manager: e.target.value }))}
            required
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">项目描述</Label>
        <Textarea
          id="description"
          value={formData.description}
          onChange={(e) => setFormData((prev) => ({ ...prev, description: e.target.value }))}
          placeholder="详细描述园林景观项目的设计理念、施工内容和预期效果..."
          rows={3}
        />
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <div className="space-y-2">
          <Label htmlFor="projectType">项目类型 *</Label>
          <Select
            value={formData.projectType}
            onValueChange={(value) => setFormData((prev) => ({ ...prev, projectType: value }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="选择项目类型" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="住宅景观">住宅景观</SelectItem>
              <SelectItem value="市政园林">市政园林</SelectItem>
              <SelectItem value="生态修复">生态修复</SelectItem>
              <SelectItem value="古建园林">古建园林</SelectItem>
              <SelectItem value="屋顶花园">屋顶花园</SelectItem>
              <SelectItem value="商业景观">商业景观</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="location">项目位置 *</Label>
          <Select
            value={formData.location}
            onValueChange={(value) => setFormData((prev) => ({ ...prev, location: value }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="选择区域·城市" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="华中·武汉">华中·武汉</SelectItem>
              <SelectItem value="华中·长沙">华中·长沙</SelectItem>
              <SelectItem value="华南·深圳">华南·深圳</SelectItem>
              <SelectItem value="华南·广州">华南·广州</SelectItem>
              <SelectItem value="华东·上海">华东·上海</SelectItem>
              <SelectItem value="华东·杭州">华东·杭州</SelectItem>
              <SelectItem value="华东·苏州">华东·苏州</SelectItem>
              <SelectItem value="西南·成都">西南·成都</SelectItem>
              <SelectItem value="西南·重庆">西南·重庆</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="area">施工面积</Label>
          <Input
            id="area"
            value={formData.area}
            onChange={(e) => setFormData((prev) => ({ ...prev, area: e.target.value }))}
            placeholder="如：15000㎡"
          />
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <div className="space-y-2">
          <Label htmlFor="season">施工季节</Label>
          <Select
            value={formData.season}
            onValueChange={(value) => setFormData((prev) => ({ ...prev, season: value }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="选择施工季节" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="春季">春季</SelectItem>
              <SelectItem value="夏季">夏季</SelectItem>
              <SelectItem value="秋季">秋季</SelectItem>
              <SelectItem value="冬季">冬季</SelectItem>
              <SelectItem value="春夏">春夏</SelectItem>
              <SelectItem value="秋冬">秋冬</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="weather">天气条件</Label>
          <Select
            value={formData.weather}
            onValueChange={(value) => setFormData((prev) => ({ ...prev, weather: value }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="选择天气条件" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="适宜">适宜</SelectItem>
              <SelectItem value="多雨">多雨</SelectItem>
              <SelectItem value="干燥">干燥</SelectItem>
              <SelectItem value="温和">温和</SelectItem>
              <SelectItem value="炎热">炎热</SelectItem>
              <SelectItem value="寒冷">寒冷</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="constructionPhase">施工阶段</Label>
          <Select
            value={formData.constructionPhase}
            onValueChange={(value) => setFormData((prev) => ({ ...prev, constructionPhase: value }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="选择施工阶段" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="设计阶段">设计阶段</SelectItem>
              <SelectItem value="土建阶段">土建阶段</SelectItem>
              <SelectItem value="绿化阶段">绿化阶段</SelectItem>
              <SelectItem value="景观阶段">景观阶段</SelectItem>
              <SelectItem value="养护阶段">养护阶段</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <div className="space-y-2">
          <Label htmlFor="status">项目状态</Label>
          <Select
            value={formData.status}
            onValueChange={(value) => setFormData((prev) => ({ ...prev, status: value }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="选择状态" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="计划中">计划中</SelectItem>
              <SelectItem value="进行中">进行中</SelectItem>
              <SelectItem value="已完成">已完成</SelectItem>
              <SelectItem value="暂停">暂停</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="priority">优先级</Label>
          <Select
            value={formData.priority}
            onValueChange={(value) => setFormData((prev) => ({ ...prev, priority: value }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="选择优先级" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="低">低</SelectItem>
              <SelectItem value="中">中</SelectItem>
              <SelectItem value="高">高</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="budget">预算 (元)</Label>
          <Input
            id="budget"
            type="number"
            value={formData.budget}
            onChange={(e) => setFormData((prev) => ({ ...prev, budget: Number.parseInt(e.target.value) || 0 }))}
            placeholder="如：2800000"
          />
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <Label htmlFor="startDate">开始日期</Label>
          <Input
            id="startDate"
            type="date"
            value={formData.startDate}
            onChange={(e) => setFormData((prev) => ({ ...prev, startDate: e.target.value }))}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="endDate">结束日期</Label>
          <Input
            id="endDate"
            type="date"
            value={formData.endDate}
            onChange={(e) => setFormData((prev) => ({ ...prev, endDate: e.target.value }))}
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label>植物类型</Label>
        <div className="flex items-center space-x-2">
          <Input
            placeholder="输入植物类型后按回车添加"
            value={newPlantType}
            onChange={(e) => setNewPlantType(e.target.value)}
            onKeyPress={handlePlantKeyPress}
          />
          <Button type="button" onClick={handleAddPlantType} variant="outline">
            添加
          </Button>
        </div>
        <div className="flex flex-wrap gap-2 mt-2">
          {formData.plantTypes.map((plant) => (
            <Badge key={plant} variant="secondary" className="flex items-center gap-1 bg-green-100 text-green-800">
              {plant}
              <X className="w-3 h-3 cursor-pointer" onClick={() => handleRemovePlantType(plant)} />
            </Badge>
          ))}
        </div>
      </div>

      <div className="space-y-2">
        <Label>项目标签</Label>
        <div className="flex items-center space-x-2">
          <Input
            placeholder="输入标签后按回车添加"
            value={newTag}
            onChange={(e) => setNewTag(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <Button type="button" onClick={handleAddTag} variant="outline">
            添加
          </Button>
        </div>
        <div className="flex flex-wrap gap-2 mt-2">
          {formData.tags.map((tag) => (
            <Badge key={tag} variant="secondary" className="flex items-center gap-1 bg-blue-100 text-blue-800">
              {tag}
              <X className="w-3 h-3 cursor-pointer" onClick={() => handleRemoveTag(tag)} />
            </Badge>
          ))}
        </div>
      </div>

      <div className="flex justify-end space-x-2">
        <Button type="submit" className="bg-green-600 hover:bg-green-700 text-white">
          {initialData ? "更新项目" : "创建园林项目"}
        </Button>
      </div>
    </form>
  )
}
