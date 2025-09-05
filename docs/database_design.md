# 人力资源调度系统数据库设计方案

## 1. 数据库设计原则

### 1.1 设计理念
- 数据规范化设计，避免数据冗余
- 支持高并发访问和大数据量处理
- 预留扩展性，支持未来功能增长
- 确保数据一致性和完整性
- 优化查询性能

### 1.2 命名规范
- 表名使用复数形式，下划线分隔 (users, user_profiles)
- 字段名使用下划线分隔 (first_name, created_at)
- 主键统一使用 id (UUID类型)
- 外键使用 {table}_id 格式
- 布尔字段使用 is_ 前缀
- 时间字段使用 _at 后缀

### 1.3 数据类型规范
- 主键: UUID
- 字符串: VARCHAR(长度)
- 文本: TEXT
- 整数: INTEGER
- 小数: DECIMAL(精度,小数位)
- 布尔: BOOLEAN
- 时间: TIMESTAMP WITH TIME ZONE
- JSON: JSONB

## 2. 核心业务表设计

### 2.1 用户认证相关表

#### 2.1.1 用户表 (users)
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(32) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    last_login_at TIMESTAMP WITH TIME ZONE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active);
```

#### 2.1.2 角色表 (roles)
```sql
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    description TEXT,
    is_system BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_roles_name ON roles(name);
```

#### 2.1.3 权限表 (permissions)
```sql
CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    resource VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_permissions_resource ON permissions(resource);
CREATE INDEX idx_permissions_action ON permissions(action);
```

#### 2.1.4 用户角色关联表 (user_roles)
```sql
CREATE TABLE user_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    assigned_by UUID REFERENCES users(id),
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    UNIQUE(user_id, role_id)
);

CREATE INDEX idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX idx_user_roles_role_id ON user_roles(role_id);
```

#### 2.1.5 角色权限关联表 (role_permissions)
```sql
CREATE TABLE role_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    permission_id UUID NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(role_id, permission_id)
);

CREATE INDEX idx_role_permissions_role_id ON role_permissions(role_id);
CREATE INDEX idx_role_permissions_permission_id ON role_permissions(permission_id);
```

### 2.2 组织架构相关表

#### 2.2.1 区域表 (regions)
```sql
CREATE TABLE regions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    parent_id UUID REFERENCES regions(id),
    level INTEGER NOT NULL DEFAULT 1,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_regions_code ON regions(code);
CREATE INDEX idx_regions_parent_id ON regions(parent_id);
CREATE INDEX idx_regions_level ON regions(level);
```

#### 2.2.2 部门表 (departments)
```sql
CREATE TABLE departments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    parent_id UUID REFERENCES departments(id),
    region_id UUID REFERENCES regions(id),
    manager_id UUID REFERENCES personnel(id),
    level INTEGER NOT NULL DEFAULT 1,
    sort_order INTEGER DEFAULT 0,
    budget DECIMAL(15,2),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_departments_code ON departments(code);
CREATE INDEX idx_departments_parent_id ON departments(parent_id);
CREATE INDEX idx_departments_region_id ON departments(region_id);
CREATE INDEX idx_departments_manager_id ON departments(manager_id);
```

### 2.3 人员信息相关表

#### 2.3.1 人员基础信息表 (personnel)
```sql
CREATE TABLE personnel (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    employee_id VARCHAR(20) UNIQUE NOT NULL,
    user_id UUID REFERENCES users(id),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    full_name VARCHAR(100) GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    department_id UUID REFERENCES departments(id),
    position VARCHAR(100),
    level VARCHAR(20),
    hire_date DATE,
    termination_date DATE,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'terminated', 'on_leave')),
    availability_status VARCHAR(20) DEFAULT 'available' CHECK (availability_status IN ('available', 'busy', 'unavailable', 'on_project')),
    hourly_rate DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_personnel_employee_id ON personnel(employee_id);
CREATE INDEX idx_personnel_email ON personnel(email);
CREATE INDEX idx_personnel_department_id ON personnel(department_id);
CREATE INDEX idx_personnel_status ON personnel(status);
CREATE INDEX idx_personnel_availability ON personnel(availability_status);
CREATE INDEX idx_personnel_full_name ON personnel(full_name);
```

#### 2.3.2 人员详细信息表 (personnel_profiles)
```sql
CREATE TABLE personnel_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    personnel_id UUID UNIQUE NOT NULL REFERENCES personnel(id) ON DELETE CASCADE,
    gender VARCHAR(10) CHECK (gender IN ('male', 'female', 'other')),
    birth_date DATE,
    nationality VARCHAR(50),
    id_card_number VARCHAR(50),
    passport_number VARCHAR(50),
    education_level VARCHAR(50),
    graduation_school VARCHAR(200),
    major VARCHAR(100),
    address JSONB,
    emergency_contact JSONB,
    personal_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_personnel_profiles_personnel_id ON personnel_profiles(personnel_id);
```

#### 2.3.3 技能表 (skills)
```sql
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50),
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_skills_name ON skills(name);
CREATE INDEX idx_skills_category ON skills(category);
```

#### 2.3.4 人员技能关联表 (personnel_skills)
```sql
CREATE TABLE personnel_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    personnel_id UUID NOT NULL REFERENCES personnel(id) ON DELETE CASCADE,
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    level VARCHAR(20) DEFAULT 'beginner' CHECK (level IN ('beginner', 'intermediate', 'advanced', 'expert')),
    years_experience INTEGER DEFAULT 0,
    certification VARCHAR(200),
    verified_by UUID REFERENCES personnel(id),
    verified_at TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(personnel_id, skill_id)
);

CREATE INDEX idx_personnel_skills_personnel_id ON personnel_skills(personnel_id);
CREATE INDEX idx_personnel_skills_skill_id ON personnel_skills(skill_id);
CREATE INDEX idx_personnel_skills_level ON personnel_skills(level);
```

#### 2.3.5 工作经验表 (work_experiences)
```sql
CREATE TABLE work_experiences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    personnel_id UUID NOT NULL REFERENCES personnel(id) ON DELETE CASCADE,
    company_name VARCHAR(200) NOT NULL,
    position VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    is_current BOOLEAN DEFAULT false,
    description TEXT,
    achievements TEXT,
    technologies_used TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_work_experiences_personnel_id ON work_experiences(personnel_id);
CREATE INDEX idx_work_experiences_dates ON work_experiences(start_date, end_date);
```

### 2.4 项目管理相关表

#### 2.4.1 项目表 (projects)
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    client_name VARCHAR(200),
    project_type VARCHAR(50),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    status VARCHAR(20) DEFAULT 'planning' CHECK (status IN ('planning', 'active', 'on_hold', 'completed', 'cancelled')),
    start_date DATE,
    end_date DATE,
    actual_start_date DATE,
    actual_end_date DATE,
    budget DECIMAL(15,2),
    actual_cost DECIMAL(15,2) DEFAULT 0,
    region_id UUID REFERENCES regions(id),
    manager_id UUID REFERENCES personnel(id),
    created_by UUID REFERENCES users(id),
    progress DECIMAL(5,2) DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    risk_level VARCHAR(20) DEFAULT 'low' CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_code ON projects(code);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_priority ON projects(priority);
CREATE INDEX idx_projects_region_id ON projects(region_id);
CREATE INDEX idx_projects_manager_id ON projects(manager_id);
CREATE INDEX idx_projects_dates ON projects(start_date, end_date);
```

#### 2.4.2 项目需求表 (project_requirements)
```sql
CREATE TABLE project_requirements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    skill_id UUID NOT NULL REFERENCES skills(id),
    required_level VARCHAR(20) DEFAULT 'intermediate' CHECK (required_level IN ('beginner', 'intermediate', 'advanced', 'expert')),
    required_count INTEGER NOT NULL DEFAULT 1,
    allocated_count INTEGER DEFAULT 0,
    min_experience_years INTEGER DEFAULT 0,
    is_mandatory BOOLEAN DEFAULT true,
    priority INTEGER DEFAULT 1,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_project_requirements_project_id ON project_requirements(project_id);
CREATE INDEX idx_project_requirements_skill_id ON project_requirements(skill_id);
```

#### 2.4.3 项目人员分配表 (project_assignments)
```sql
CREATE TABLE project_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    personnel_id UUID NOT NULL REFERENCES personnel(id) ON DELETE CASCADE,
    role VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    planned_end_date DATE,
    allocation_percentage INTEGER DEFAULT 100 CHECK (allocation_percentage > 0 AND allocation_percentage <= 100),
    hourly_rate DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'assigned' CHECK (status IN ('assigned', 'active', 'completed', 'cancelled')),
    assigned_by UUID REFERENCES users(id),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_project_assignments_project_id ON project_assignments(project_id);
CREATE INDEX idx_project_assignments_personnel_id ON project_assignments(personnel_id);
CREATE INDEX idx_project_assignments_dates ON project_assignments(start_date, end_date);
CREATE INDEX idx_project_assignments_status ON project_assignments(status);
```

### 2.5 调度管理相关表

#### 2.5.1 调度计划表 (scheduling_plans)
```sql
CREATE TABLE scheduling_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    plan_type VARCHAR(50) DEFAULT 'regular' CHECK (plan_type IN ('regular', 'emergency', 'temporary')),
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'pending_approval', 'approved', 'active', 'completed', 'cancelled')),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_by UUID NOT NULL REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    approved_at TIMESTAMP WITH TIME ZONE,
    executed_at TIMESTAMP WITH TIME ZONE,
    total_assignments INTEGER DEFAULT 0,
    successful_assignments INTEGER DEFAULT 0,
    failed_assignments INTEGER DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scheduling_plans_status ON scheduling_plans(status);
CREATE INDEX idx_scheduling_plans_dates ON scheduling_plans(start_date, end_date);
CREATE INDEX idx_scheduling_plans_created_by ON scheduling_plans(created_by);
```

#### 2.5.2 调度分配表 (scheduling_assignments)
```sql
CREATE TABLE scheduling_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID NOT NULL REFERENCES scheduling_plans(id) ON DELETE CASCADE,
    personnel_id UUID NOT NULL REFERENCES personnel(id),
    project_id UUID NOT NULL REFERENCES projects(id),
    role VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    allocation_percentage INTEGER DEFAULT 100 CHECK (allocation_percentage > 0 AND allocation_percentage <= 100),
    priority INTEGER DEFAULT 1,
    status VARCHAR(20) DEFAULT 'planned' CHECK (status IN ('planned', 'confirmed', 'active', 'completed', 'cancelled', 'failed')),
    match_score DECIMAL(5,2),
    assignment_reason TEXT,
    conflict_resolution TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scheduling_assignments_plan_id ON scheduling_assignments(plan_id);
CREATE INDEX idx_scheduling_assignments_personnel_id ON scheduling_assignments(personnel_id);
CREATE INDEX idx_scheduling_assignments_project_id ON scheduling_assignments(project_id);
CREATE INDEX idx_scheduling_assignments_dates ON scheduling_assignments(start_date, end_date);
CREATE INDEX idx_scheduling_assignments_status ON scheduling_assignments(status);
```

#### 2.5.3 调度冲突表 (scheduling_conflicts)
```sql
CREATE TABLE scheduling_conflicts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assignment_id UUID NOT NULL REFERENCES scheduling_assignments(id) ON DELETE CASCADE,
    conflict_type VARCHAR(50) NOT NULL CHECK (conflict_type IN ('time_overlap', 'resource_shortage', 'skill_mismatch', 'budget_exceed', 'policy_violation')),
    severity VARCHAR(20) DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    description TEXT NOT NULL,
    affected_entities JSONB,
    suggested_solutions JSONB,
    resolution_status VARCHAR(20) DEFAULT 'unresolved' CHECK (resolution_status IN ('unresolved', 'in_progress', 'resolved', 'ignored')),
    resolved_by UUID REFERENCES users(id),
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolution_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scheduling_conflicts_assignment_id ON scheduling_conflicts(assignment_id);
CREATE INDEX idx_scheduling_conflicts_type ON scheduling_conflicts(conflict_type);
CREATE INDEX idx_scheduling_conflicts_severity ON scheduling_conflicts(severity);
CREATE INDEX idx_scheduling_conflicts_status ON scheduling_conflicts(resolution_status);
```

### 2.6 审批流程相关表

#### 2.6.1 审批流程定义表 (approval_workflows)
```sql
CREATE TABLE approval_workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    workflow_type VARCHAR(50) NOT NULL,
    steps JSONB NOT NULL,
    conditions JSONB,
    is_active BOOLEAN DEFAULT true,
    version INTEGER DEFAULT 1,
    created_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_approval_workflows_type ON approval_workflows(workflow_type);
CREATE INDEX idx_approval_workflows_active ON approval_workflows(is_active);
```

#### 2.6.2 审批申请表 (approval_requests)
```sql
CREATE TABLE approval_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL REFERENCES approval_workflows(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    request_type VARCHAR(50) NOT NULL,
    request_data JSONB NOT NULL,
    current_step INTEGER DEFAULT 1,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'approved', 'rejected', 'cancelled', 'expired')),
    priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    applicant_id UUID NOT NULL REFERENCES users(id),
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deadline TIMESTAMP WITH TIME ZONE,
    approved_at TIMESTAMP WITH TIME ZONE,
    rejected_at TIMESTAMP WITH TIME ZONE,
    final_approver_id UUID REFERENCES users(id),
    rejection_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_approval_requests_workflow_id ON approval_requests(workflow_id);
CREATE INDEX idx_approval_requests_status ON approval_requests(status);
CREATE INDEX idx_approval_requests_applicant_id ON approval_requests(applicant_id);
CREATE INDEX idx_approval_requests_type ON approval_requests(request_type);
```

#### 2.6.3 审批步骤记录表 (approval_steps)
```sql
CREATE TABLE approval_steps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id UUID NOT NULL REFERENCES approval_requests(id) ON DELETE CASCADE,
    step_number INTEGER NOT NULL,
    step_name VARCHAR(100) NOT NULL,
    approver_id UUID NOT NULL REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'skipped')),
    action_taken VARCHAR(20),
    comments TEXT,
    processed_at TIMESTAMP WITH TIME ZONE,
    deadline TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_approval_steps_request_id ON approval_steps(request_id);
CREATE INDEX idx_approval_steps_approver_id ON approval_steps(approver_id);
CREATE INDEX idx_approval_steps_status ON approval_steps(status);
```

### 2.7 风险管控相关表

#### 2.7.1 风险识别表 (risk_identifications)
```sql
CREATE TABLE risk_identifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    risk_type VARCHAR(50) NOT NULL CHECK (risk_type IN ('resource_shortage', 'skill_mismatch', 'budget_overrun', 'timeline_delay', 'quality_risk', 'compliance_risk')),
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    severity VARCHAR(20) DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    probability DECIMAL(3,2) CHECK (probability >= 0 AND probability <= 1),
    impact_score DECIMAL(4,2),
    risk_score DECIMAL(6,2) GENERATED ALWAYS AS (probability * impact_score) STORED,
    affected_entities JSONB,
    predicted_timeline JSONB,
    mitigation_suggestions JSONB,
    status VARCHAR(20) DEFAULT 'identified' CHECK (status IN ('identified', 'analyzing', 'mitigating', 'monitoring', 'resolved', 'accepted')),
    identified_by UUID REFERENCES users(id),
    assigned_to UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_risk_identifications_type ON risk_identifications(risk_type);
CREATE INDEX idx_risk_identifications_severity ON risk_identifications(severity);
CREATE INDEX idx_risk_identifications_status ON risk_identifications(status);
CREATE INDEX idx_risk_identifications_score ON risk_identifications(risk_score DESC);
```

#### 2.7.2 预警规则表 (alert_rules)
```sql
CREATE TABLE alert_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    rule_type VARCHAR(50) NOT NULL,
    conditions JSONB NOT NULL,
    scope JSONB,
    notification_config JSONB NOT NULL,
    severity VARCHAR(20) DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    is_enabled BOOLEAN DEFAULT true,
    trigger_count INTEGER DEFAULT 0,
    last_triggered_at TIMESTAMP WITH TIME ZONE,
    created_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_alert_rules_type ON alert_rules(rule_type);
CREATE INDEX idx_alert_rules_enabled ON alert_rules(is_enabled);
```

#### 2.7.3 预警记录表 (alert_logs)
```sql
CREATE TABLE alert_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_id UUID NOT NULL REFERENCES alert_rules(id),
    alert_level VARCHAR(20) NOT NULL CHECK (alert_level IN ('info', 'warning', 'error', 'critical')),
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    trigger_data JSONB,
    affected_entities JSONB,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'acknowledged', 'resolved', 'ignored')),
    acknowledged_by UUID REFERENCES users(id),
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    resolved_by UUID REFERENCES users(id),
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolution_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_alert_logs_rule_id ON alert_logs(rule_id);
CREATE INDEX idx_alert_logs_level ON alert_logs(alert_level);
CREATE INDEX idx_alert_logs_status ON alert_logs(status);
CREATE INDEX idx_alert_logs_created_at ON alert_logs(created_at DESC);
```

### 2.8 数据分析相关表

#### 2.8.1 配置评估表 (configuration_assessments)
```sql
CREATE TABLE configuration_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assessment_type VARCHAR(50) NOT NULL,
    target_entity_type VARCHAR(50) NOT NULL,
    target_entity_id UUID NOT NULL,
    assessment_period JSONB NOT NULL,
    metrics JSONB NOT NULL,
    scores JSONB NOT NULL,
    overall_score DECIMAL(5,2),
    recommendations JSONB,
    assessment_data JSONB,
    status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('pending', 'in_progress', 'completed', 'failed')),
    assessed_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_configuration_assessments_type ON configuration_assessments(assessment_type);
CREATE INDEX idx_configuration_assessments_target ON configuration_assessments(target_entity_type, target_entity_id);
CREATE INDEX idx_configuration_assessments_score ON configuration_assessments(overall_score DESC);
```

#### 2.8.2 预测分析数据表 (predictive_analysis_data)
```sql
CREATE TABLE predictive_analysis_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_type VARCHAR(50) NOT NULL,
    model_version VARCHAR(20),
    input_data JSONB NOT NULL,
    predictions JSONB NOT NULL,
    confidence_scores JSONB,
    accuracy_metrics JSONB,
    prediction_period JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'expired', 'superseded')),
    generated_by VARCHAR(100),
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_predictive_analysis_type ON predictive_analysis_data(analysis_type);
CREATE INDEX idx_predictive_analysis_status ON predictive_analysis_data(status);
CREATE INDEX idx_predictive_analysis_generated_at ON predictive_analysis_data(generated_at DESC);
```

### 2.9 系统管理相关表

#### 2.9.1 系统配置表 (system_configurations)
```sql
CREATE TABLE system_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value JSONB NOT NULL,
    config_type VARCHAR(50) NOT NULL,
    description TEXT,
    is_encrypted BOOLEAN DEFAULT false,
    is_system BOOLEAN DEFAULT false,
    updated_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_system_configurations_key ON system_configurations(config_key);
CREATE INDEX idx_system_configurations_type ON system_configurations(config_type);
```

#### 2.9.2 操作日志表 (audit_logs)
```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(100),
    status VARCHAR(20) DEFAULT 'success' CHECK (status IN ('success', 'failed', 'error')),
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at DESC);
```

#### 2.9.3 通知表 (notifications)
```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipient_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    status VARCHAR(20) DEFAULT 'unread' CHECK (status IN ('unread', 'read', 'archived')),
    related_entity_type VARCHAR(50),
    related_entity_id UUID,
    action_url VARCHAR(500),
    read_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notifications_recipient_id ON notifications(recipient_id);
CREATE INDEX idx_notifications_status ON notifications(status);
CREATE INDEX idx_notifications_type ON notifications(notification_type);
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);
```

## 3. 视图定义

### 3.1 人员完整信息视图
```sql
CREATE VIEW v_personnel_full AS
SELECT 
    p.id,
    p.employee_id,
    p.full_name,
    p.email,
    p.phone,
    p.position,
    p.level,
    p.status,
    p.availability_status,
    p.hire_date,
    p.hourly_rate,
    d.name as department_name,
    d.code as department_code,
    r.name as region_name,
    pp.gender,
    pp.birth_date,
    pp.education_level,
    COALESCE(skill_summary.skills, '[]'::jsonb) as skills,
    COALESCE(project_summary.current_projects, '[]'::jsonb) as current_projects
FROM personnel p
LEFT JOIN departments d ON p.department_id = d.id
LEFT JOIN regions r ON d.region_id = r.id
LEFT JOIN personnel_profiles pp ON p.id = pp.personnel_id
LEFT JOIN (
    SELECT 
        ps.personnel_id,
        jsonb_agg(
            jsonb_build_object(
                'skill_name', s.name,
                'level', ps.level,
                'years_experience', ps.years_experience
            )
        ) as skills
    FROM personnel_skills ps
    JOIN skills s ON ps.skill_id = s.id
    GROUP BY ps.personnel_id
) skill_summary ON p.id = skill_summary.personnel_id
LEFT JOIN (
    SELECT 
        pa.personnel_id,
        jsonb_agg(
            jsonb_build_object(
                'project_name', proj.name,
                'role', pa.role,
                'allocation_percentage', pa.allocation_percentage,
                'start_date', pa.start_date,
                'end_date', pa.end_date
            )
        ) as current_projects
    FROM project_assignments pa
    JOIN projects proj ON pa.project_id = proj.id
    WHERE pa.status = 'active'
    GROUP BY pa.personnel_id
) project_summary ON p.id = project_summary.personnel_id;
```

### 3.2 项目资源概览视图
```sql
CREATE VIEW v_project_resource_overview AS
SELECT 
    p.id,
    p.name,
    p.code,
    p.status,
    p.priority,
    p.start_date,
    p.end_date,
    p.budget,
    p.progress,
    r.name as region_name,
    manager.full_name as manager_name,
    COALESCE(assignment_summary.total_assignments, 0) as total_assignments,
    COALESCE(assignment_summary.active_assignments, 0) as active_assignments,
    COALESCE(requirement_summary.total_requirements, 0) as total_requirements,
    COALESCE(requirement_summary.fulfilled_requirements, 0) as fulfilled_requirements,
    CASE 
        WHEN requirement_summary.total_requirements > 0 
        THEN ROUND((requirement_summary.fulfilled_requirements::decimal / requirement_summary.total_requirements * 100), 2)
        ELSE 0 
    END as fulfillment_percentage
FROM projects p
LEFT JOIN regions r ON p.region_id = r.id
LEFT JOIN personnel manager ON p.manager_id = manager.id
LEFT JOIN (
    SELECT 
        project_id,
        COUNT(*) as total_assignments,
        COUNT(CASE WHEN status = 'active' THEN 1 END) as active_assignments
    FROM project_assignments
    GROUP BY project_id
) assignment_summary ON p.id = assignment_summary.project_id
LEFT JOIN (
    SELECT 
        project_id,
        COUNT(*) as total_requirements,
        COUNT(CASE WHEN allocated_count >= required_count THEN 1 END) as fulfilled_requirements
    FROM project_requirements
    GROUP BY project_id
) requirement_summary ON p.id = requirement_summary.project_id;
```

## 4. 触发器和函数

### 4.1 更新时间戳触发器函数
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为所有需要的表创建触发器
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_personnel_updated_at BEFORE UPDATE ON personnel
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 为其他表添加类似触发器...
```

### 4.2 人员可用性检查函数
```sql
CREATE OR REPLACE FUNCTION check_personnel_availability(
    p_personnel_id UUID,
    p_start_date DATE,
    p_end_date DATE,
    p_allocation_percentage INTEGER DEFAULT 100
) RETURNS JSONB AS $$
DECLAR
    existing_allocation INTEGER := 0;
    availability_result JSONB;
BEGIN
    -- 计算指定时间段内的现有分配百分比
    SELECT COALESCE(SUM(allocation_percentage), 0)
    INTO existing_allocation
    FROM project_assignments
    WHERE personnel_id = p_personnel_id
    AND status IN ('assigned', 'active')
    AND (
        (start_date <= p_end_date AND end_date >= p_start_date)
        OR (start_date <= p_end_date AND end_date IS NULL)
    );
    
    -- 构建返回结果
    availability_result := jsonb_build_object(
        'is_available', (existing_allocation + p_allocation_percentage) <= 100,
        'current_allocation', existing_allocation,
        'requested_allocation', p_allocation_percentage,
        'total_allocation', existing_allocation + p_allocation_percentage,
        'available_capacity', 100 - existing_allocation
    );
    
    RETURN availability_result;
END;
$$ LANGUAGE plpgsql;
```

## 5. 索引优化策略

### 5.1 复合索引
```sql
-- 人员技能查询优化
CREATE INDEX idx_personnel_skills_composite ON personnel_skills(skill_id, level, years_experience);

-- 项目分配查询优化
CREATE INDEX idx_project_assignments_composite ON project_assignments(personnel_id, status, start_date, end_date);

-- 审批流程查询优化
CREATE INDEX idx_approval_requests_composite ON approval_requests(status, request_type, applicant_id);

-- 风险监控查询优化
CREATE INDEX idx_risk_identifications_composite ON risk_identifications(risk_type, severity, status);
```

### 5.2 部分索引
```sql
-- 仅为活跃用户创建索引
CREATE INDEX idx_users_active_email ON users(email) WHERE is_active = true;

-- 仅为进行中的项目创建索引
CREATE INDEX idx_projects_active_dates ON projects(start_date, end_date) WHERE status IN ('active', 'planning');

-- 仅为未解决的风险创建索引
CREATE INDEX idx_risks_unresolved ON risk_identifications(severity, created_at) WHERE status NOT IN ('resolved', 'accepted');
```

## 6. 数据分区策略

### 6.1 按时间分区的表
```sql
-- 审计日志按月分区
CREATE TABLE audit_logs_partitioned (
    LIKE audit_logs INCLUDING ALL
) PARTITION BY RANGE (created_at);

-- 创建分区表
CREATE TABLE audit_logs_2024_01 PARTITION OF audit_logs_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE audit_logs_2024_02 PARTITION OF audit_logs_partitioned
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- 预警日志按月分区
CREATE TABLE alert_logs_partitioned (
    LIKE alert_logs INCLUDING ALL
) PARTITION BY RANGE (created_at);
```

## 7. 数据完整性约束

### 7.1 检查约束
```sql
-- 确保项目结束日期晚于开始日期
ALTER TABLE projects ADD CONSTRAINT chk_project_dates 
    CHECK (end_date IS NULL OR end_date >= start_date);

-- 确保人员分配百分比合理
ALTER TABLE project_assignments ADD CONSTRAINT chk_allocation_percentage 
    CHECK (allocation_percentage > 0 AND allocation_percentage <= 100);

-- 确保风险概率在合理范围内
ALTER TABLE risk_identifications ADD CONSTRAINT chk_probability_range 
    CHECK (probability >= 0 AND probability <= 1);
```

### 7.2 唯一约束
```sql
-- 确保同一人员在同一项目中不能有重叠的活跃分配
CREATE UNIQUE INDEX idx_unique_active_assignment 
    ON project_assignments(personnel_id, project_id) 
    WHERE status IN ('assigned', 'active');

-- 确保用户角色分配的唯一性
CREATE UNIQUE INDEX idx_unique_user_role 
    ON user_roles(user_id, role_id) 
    WHERE is_active = true;
```

## 8. 性能优化建议

### 8.1 查询优化
1. 使用适当的索引策略
2. 避免SELECT *，只查询需要的字段
3. 使用LIMIT限制结果集大小
4. 合理使用JOIN，避免笛卡尔积
5. 使用EXISTS代替IN子查询

### 8.2 写入优化
1. 批量插入使用COPY或批量INSERT
2. 合理使用事务，避免长事务
3. 在大量数据操作时临时删除索引
4. 使用UPSERT处理冲突数据

### 8.3 维护策略
1. 定期执行VACUUM和ANALYZE
2. 监控表膨胀和索引膨胀
3. 定期清理历史数据
4. 监控慢查询并优化

## 9. 备份和恢复策略

### 9.1 备份策略
- 每日全量备份
- 每小时增量备份
- WAL日志连续备份
- 重要表的实时复制

### 9.2 恢复策略
- 点时间恢复(PITR)
- 表级别恢复
- 数据验证和一致性检查
- 灾难恢复预案

---

**注意事项：**
1. 所有表都使用UUID作为主键，确保分布式环境下的唯一性
2. 时间字段统一使用TIMESTAMP WITH TIME ZONE
3. 敏感数据字段需要加密存储
4. 定期监控数据库性能和存储使用情况
5. 建立完善的数据备份和恢复机制
6. 遵循数据保护法规，确保个人信息安全

**实施优先级：**
1. 用户认证和权限管理表 (高)
2. 组织架构和人员信息表 (高)
3. 项目管理相关表 (高)
4. 调度管理相关表 (高)
5. 审批流程表 (中)
6. 风险管控表 (中)
7. 数据分析表 (中)
8. 系统管理表 (低)