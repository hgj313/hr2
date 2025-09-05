"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { X } from "lucide-react"
import { GARDEN_DEPARTMENTS, GARDEN_POSITIONS, GARDEN_SKILLS, REGIONS } from "@/lib/constants/garden-constants"

interface UserFormProps {
  initialData?: any
  onSubmit: (data: any) => void
}

export function UserForm({ initialData, onSubmit }: UserFormProps) {
  const [formData, setFormData] = useState({
    name: initialData?.name || "",
    email: initialData?.email || "",
    phone: initialData?.phone || "",
    department: initialData?.department || "",
    position: initialData?.position || "",
    level: initialData?.level || "",
    status: initialData?.status || "在职",
    joinDate: initialData?.joinDate || "",
    skills: initialData?.skills || [],
    workload: initialData?.workload || 0,
    region: initialData?.region || "",
    specialization: initialData?.specialization || "",
    certifications: initialData?.certifications || [],
    experience: initialData?.experience || 0,
  })

  const [newSkill, setNewSkill] = useState("")
  const [newCertification, setNewCertification] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  const handleAddSkill = () => {
    if (newSkill.trim() && !formData.skills.includes(newSkill.trim())) {
      setFormData((prev) => ({
        ...prev,
        skills: [...prev.skills, newSkill.trim()],
      }))
      setNewSkill("")
    }
  }

  const handleAddCertification = () => {
    if (newCertification.trim() && !formData.certifications.includes(newCertification.trim())) {
      setFormData((prev) => ({
        ...prev,
        certifications: [...prev.certifications, newCertification.trim()],
      }))
      setNewCertification("")
    }
  }

  const handleRemoveSkill = (skillToRemove: string) => {
    setFormData((prev) => ({
      ...prev,
      skills: prev.skills.filter((skill) => skill !== skillToRemove),
    }))
  }

  const handleRemoveCertification = (certToRemove: string) => {
    setFormData((prev) => ({
      ...prev,
      certifications: prev.certifications.filter((cert) => cert !== certToRemove),
    }))
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault()
      handleAddSkill()
    }
  }

  const handleCertKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault()
      handleAddCertification()
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <Label htmlFor="name">姓名 *</Label>
          <Input
            id="name"
            value={formData.name}
            onChange={(e) => setFormData((prev) => ({ ...prev, name: e.target.value }))}
            required
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="email">邮箱 *</Label>
          <Input
            id="email"
            type="email"
            value={formData.email}
            onChange={(e) => setFormData((prev) => ({ ...prev, email: e.target.value }))}
            required
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="phone">电话</Label>
          <Input
            id="phone"
            value={formData.phone}
            onChange={(e) => setFormData((prev) => ({ ...prev, phone: e.target.value }))}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="joinDate">入职日期</Label>
          <Input
            id="joinDate"
            type="date"
            value={formData.joinDate}
            onChange={(e) => setFormData((prev) => ({ ...prev, joinDate: e.target.value }))}
          />
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <Label htmlFor="department">部门 *</Label>
          <Select
            value={formData.department}
            onValueChange={(value) => setFormData((prev) => ({ ...prev, department: value }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="选择部门" />
            </SelectTrigger>
            <SelectContent>
              {GARDEN_DEPARTMENTS.map((dept) => (
                <SelectItem key={dept} value={dept}>
                  {dept}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="position">职位 *</Label>
          <Select
            value={formData.position}
            onValueChange={(value) => setFormData((prev) => ({ ...prev, position: value }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="选择职位" />
            </SelectTrigger>
            <SelectContent>
              {GARDEN_POSITIONS.map((pos) => (
                <SelectItem key={pos} value={pos}>
                  {pos}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="level">级别</Label>
          <Select value={formData.level} onValueChange={(value) => setFormData((prev) => ({ ...prev, level: value }))}>
            <SelectTrigger>
              <SelectValue placeholder="选择级别" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="初级">初级</SelectItem>
              <SelectItem value="中级">中级</SelectItem>
              <SelectItem value="高级">高级</SelectItem>
              <SelectItem value="专家">专家</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="status">状态</Label>
          <Select
            value={formData.status}
            onValueChange={(value) => setFormData((prev) => ({ ...prev, status: value }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="选择状态" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="在职">在职</SelectItem>
              <SelectItem value="离职">离职</SelectItem>
              <SelectItem value="休假">休假</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <Label htmlFor="region">所属区域 *</Label>
          <Select
            value={formData.region}
            onValueChange={(value) => setFormData((prev) => ({ ...prev, region: value }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="选择区域" />
            </SelectTrigger>
            <SelectContent>
              {REGIONS.map((region) => (
                <SelectItem key={region} value={region}>
                  {region}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="specialization">专业领域</Label>
          <Select
            value={formData.specialization}
            onValueChange={(value) => setFormData((prev) => ({ ...prev, specialization: value }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="选择专业领域" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="住宅景观">住宅景观</SelectItem>
              <SelectItem value="市政园林">市政园林</SelectItem>
              <SelectItem value="生态修复">生态修复</SelectItem>
              <SelectItem value="古建园林">古建园林</SelectItem>
              <SelectItem value="屋顶花园">屋顶花园</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="experience">工作经验 (年)</Label>
          <Input
            id="experience"
            type="number"
            min="0"
            max="50"
            value={formData.experience}
            onChange={(e) => setFormData((prev) => ({ ...prev, experience: Number.parseInt(e.target.value) || 0 }))}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="workload">当前工作负载 (%)</Label>
          <Input
            id="workload"
            type="number"
            min="0"
            max="100"
            value={formData.workload}
            onChange={(e) => setFormData((prev) => ({ ...prev, workload: Number.parseInt(e.target.value) || 0 }))}
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label>专业技能</Label>
        <div className="flex items-center space-x-2">
          <Select value={newSkill} onValueChange={setNewSkill}>
            <SelectTrigger className="flex-1">
              <SelectValue placeholder="选择专业技能" />
            </SelectTrigger>
            <SelectContent>
              {GARDEN_SKILLS.map((skill) => (
                <SelectItem key={skill} value={skill}>
                  {skill}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button type="button" onClick={handleAddSkill} variant="outline">
            添加
          </Button>
        </div>
        <div className="flex flex-wrap gap-2 mt-2">
          {formData.skills.map((skill) => (
            <Badge key={skill} variant="secondary" className="flex items-center gap-1 bg-green-100 text-green-800">
              {skill}
              <X className="w-3 h-3 cursor-pointer" onClick={() => handleRemoveSkill(skill)} />
            </Badge>
          ))}
        </div>
      </div>

      <div className="space-y-2">
        <Label>资质证书</Label>
        <div className="flex items-center space-x-2">
          <Input
            placeholder="输入证书名称后按回车添加"
            value={newCertification}
            onChange={(e) => setNewCertification(e.target.value)}
            onKeyPress={handleCertKeyPress}
          />
          <Button type="button" onClick={handleAddCertification} variant="outline">
            添加
          </Button>
        </div>
        <div className="flex flex-wrap gap-2 mt-2">
          {formData.certifications.map((cert) => (
            <Badge key={cert} variant="secondary" className="flex items-center gap-1 bg-blue-100 text-blue-800">
              {cert}
              <X className="w-3 h-3 cursor-pointer" onClick={() => handleRemoveCertification(cert)} />
            </Badge>
          ))}
        </div>
      </div>

      <div className="flex justify-end space-x-2">
        <Button type="submit" className="bg-primary hover:bg-primary/90">
          {initialData ? "更新" : "添加"}
        </Button>
      </div>
    </form>
  )
}
