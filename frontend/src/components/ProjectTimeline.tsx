import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragOverlay,
} from '@dnd-kit/core';
import type { DragEndEvent, DragStartEvent } from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
  useSortable,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { format, addDays, differenceInDays, parseISO } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import {
  CalendarDaysIcon,
  UserIcon,
  PlusIcon,
  AdjustmentsHorizontalIcon,
} from '@heroicons/react/24/outline';
import '../styles/chinese-minimal.css';

interface Project {
  id: number;
  name: string;
  description: string;
  start_date: string;
  end_date: string;
  status: string;
  budget: number;
  assignments?: Assignment[];
}

interface Assignment {
  id: number;
  user_id: number;
  project_id: number;
  role: string;
  start_date: string;
  end_date: string;
  allocation_percentage: number;
  user?: {
    id: number;
    username: string;
    email: string;
  };
}

interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
}

interface TimelineProject extends Project {
  duration: number;
  startOffset: number;
  width: number;
}

// 可拖拽的用户项组件
function DraggableUser({ user }: { user: User }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: user.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="draggable-item flex items-center space-x-2 mb-2"
    >
      <UserIcon className="h-4 w-4 text-gray-500" />
      <span className="text-sm font-medium">{user.username}</span>
    </div>
  );
}

// 项目条组件
function ProjectBar({ project, onAssignUser }: { 
  project: TimelineProject; 
  onAssignUser: (projectId: number, userId: number) => void;
}) {
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const userId = parseInt(e.dataTransfer.getData('text/plain'));
    if (userId) {
      onAssignUser(project.id, userId);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  return (
    <div className="relative mb-4">
      <div className="flex items-center mb-2">
        <h4 className="text-sm font-medium text-gray-900 w-48 truncate">
          {project.name}
        </h4>
        <span className="text-xs text-gray-500 ml-2">
          预算: ¥{project.budget.toLocaleString()}
        </span>
      </div>
      
      <div className="relative h-12 bg-gray-100 rounded-md">
        {/* 项目时间条 */}
        <div
          className="project-bar h-8 flex items-center justify-between px-3 text-white text-xs font-medium"
          style={{
            left: `${project.startOffset}%`,
            width: `${project.width}%`,
            top: '2px',
          }}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          <span className="truncate">{project.name}</span>
          <span>{project.duration}天</span>
        </div>
        
        {/* 分配的用户 */}
        <div className="absolute bottom-0 left-0 right-0 h-2 flex space-x-1 px-1">
          {project.assignments?.map((assignment, index) => (
            <div
              key={assignment.id}
              className="h-2 bg-blue-400 rounded-sm flex-1 max-w-8"
              title={`${assignment.user?.username} - ${assignment.allocation_percentage}%`}
            />
          ))}
        </div>
      </div>
      
      {/* 项目详情 */}
      <div className="mt-1 text-xs text-gray-500 flex space-x-4">
        <span>开始: {format(parseISO(project.start_date), 'MM/dd', { locale: zhCN })}</span>
        <span>结束: {format(parseISO(project.end_date), 'MM/dd', { locale: zhCN })}</span>
        <span>状态: {project.status}</span>
        <span>分配: {project.assignments?.length || 0}人</span>
      </div>
    </div>
  );
}

const ProjectTimeline: React.FC = () => {
  const [projects, setProjects] = useState<TimelineProject[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [timelineStart, setTimelineStart] = useState<Date>(new Date());
  const [timelineEnd, setTimelineEnd] = useState<Date>(addDays(new Date(), 90));
  const [activeId, setActiveId] = useState<number | null>(null);
  
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [projectsResponse, usersResponse] = await Promise.all([
        axios.get('/api/v1/projects/'),
        axios.get('/api/v1/users/'),
      ]);
      
      const projectsData = projectsResponse.data;
      const usersData = usersResponse.data.filter((user: User) => user.is_active);
      
      // 计算时间轴范围
      if (projectsData.length > 0) {
        const allDates: Date[] = projectsData.flatMap((p: Project) => [parseISO(p.start_date), parseISO(p.end_date)]);
        const minDate = new Date(Math.min(...allDates.map((d: Date) => d.getTime())));
        const maxDate = new Date(Math.max(...allDates.map((d: Date) => d.getTime())));
        
        setTimelineStart(addDays(minDate, -7));
        setTimelineEnd(addDays(maxDate, 7));
      }
      
      setUsers(usersData);
      updateProjectsTimeline(projectsData);
      
    } catch (error) {
      console.error('Failed to fetch data:', error);
      setError('获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  const updateProjectsTimeline = (projectsData: Project[]) => {
    const totalDays = differenceInDays(timelineEnd, timelineStart);
    
    const timelineProjects: TimelineProject[] = projectsData.map((project) => {
      const startDate = parseISO(project.start_date);
      const endDate = parseISO(project.end_date);
      const duration = differenceInDays(endDate, startDate) + 1;
      const startOffset = (differenceInDays(startDate, timelineStart) / totalDays) * 100;
      const width = (duration / totalDays) * 100;
      
      return {
        ...project,
        duration,
        startOffset: Math.max(0, startOffset),
        width: Math.min(100 - Math.max(0, startOffset), width),
      };
    });
    
    setProjects(timelineProjects);
  };

  const handleAssignUser = async (projectId: number, userId: number) => {
    try {
      const project = projects.find(p => p.id === projectId);
      if (!project) return;
      
      const assignmentData = {
        user_id: userId,
        project_id: projectId,
        role: 'developer',
        start_date: project.start_date,
        end_date: project.end_date,
        allocation_percentage: 100,
      };
      
      await axios.post('/api/v1/assignments/', assignmentData);
      
      // 刷新数据
      fetchData();
      
    } catch (error) {
      console.error('Failed to assign user:', error);
      setError('分配用户失败');
    }
  };

  const handleDragStart = (event: DragStartEvent) => {
    setActiveId(event.active.id as number);
  };

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    
    if (over && active.id !== over.id) {
      setUsers((items) => {
        const oldIndex = items.findIndex(item => item.id === active.id);
        const newIndex = items.findIndex(item => item.id === over.id);
        
        return arrayMove(items, oldIndex, newIndex);
      });
    }
    
    setActiveId(null);
  };

  // 生成时间轴刻度
  const generateTimeScale = () => {
    const totalDays = differenceInDays(timelineEnd, timelineStart);
    const scales = [];
    
    for (let i = 0; i <= totalDays; i += 7) {
      const date = addDays(timelineStart, i);
      const position = (i / totalDays) * 100;
      
      scales.push({
        date,
        position,
        label: format(date, 'MM/dd', { locale: zhCN }),
      });
    }
    
    return scales;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12" style={{borderTop: '2px solid var(--bamboo-medium)', borderRight: '2px solid var(--bamboo-medium)', borderBottom: '2px solid var(--bamboo-medium)', borderLeft: '2px solid transparent'}}></div>
      </div>
    );
  }

  return (
    <div style={{display: 'flex', flexDirection: 'column', gap: '1.5rem'}} className="animate-fade-in-up">
      {/* 页面标题 */}
      <div style={{borderBottom: '1px solid var(--bamboo-light)', paddingBottom: '1rem'}} className="seal-accent">
        <div className="flex items-center justify-between">
          <div>
            <h1 style={{fontSize: '1.5rem', fontWeight: '700', color: 'var(--ink-dark)'}} className="flex items-center">
              <CalendarDaysIcon style={{width: '1.75rem', height: '1.75rem', marginRight: '0.5rem', color: 'var(--bamboo-medium)'}} />
              项目时间轴调度
            </h1>
            <p style={{marginTop: '0.25rem', fontSize: '0.875rem', color: 'var(--ink-light)'}}>
              拖拽用户到项目条上进行人员分配
            </p>
          </div>
          <button
            onClick={fetchData}
            className="btn-minimal flex items-center transition-all duration-200 hover:scale-105"
            style={{padding: '0.5rem 1rem', background: 'var(--bamboo-medium)', color: 'var(--rice-white)', borderRadius: '0.5rem', border: 'none', gap: '0.5rem'}}
          >
            <AdjustmentsHorizontalIcon style={{width: '1rem', height: '1rem'}} />
            <span>刷新数据</span>
          </button>
        </div>
      </div>

      {error && (
        <div style={{background: 'var(--rice-cream)', border: '1px solid var(--bamboo-light)', color: 'var(--ink-dark)', padding: '0.75rem 1rem', borderRadius: '0.5rem'}}>
          {error}
        </div>
      )}

      <div style={{display: 'grid', gridTemplateColumns: '1fr', gap: '1.5rem'}} className="lg:grid-cols-4">
        {/* 用户列表 */}
        <div className="lg:col-span-1">
          <div style={{background: 'var(--rice-white)', borderRadius: '0.75rem', padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.08)', border: '1px solid var(--bamboo-light)'}} className="transition-all duration-300 hover:shadow-lg">
            <h3 style={{fontSize: '1.125rem', fontWeight: '600', color: 'var(--ink-dark)', marginBottom: '1rem'}} className="flex items-center">
              <UserIcon style={{width: '1.25rem', height: '1.25rem', marginRight: '0.5rem', color: 'var(--bamboo-medium)'}} />
              可分配用户 ({users.length})
            </h3>
            
            <DndContext
              sensors={sensors}
              collisionDetection={closestCenter}
              onDragStart={handleDragStart}
              onDragEnd={handleDragEnd}
            >
              <SortableContext items={users} strategy={verticalListSortingStrategy}>
                {users.map((user) => (
                  <DraggableUser key={user.id} user={user} />
                ))}
              </SortableContext>
              
              <DragOverlay>
                {activeId ? (
                  <div style={{background: 'var(--rice-white)', padding: '0.5rem', borderRadius: '0.5rem', boxShadow: '0 4px 12px rgba(0,0,0,0.15)', border: '1px solid var(--bamboo-medium)'}} className="flex items-center">
                    <UserIcon style={{width: '1rem', height: '1rem', color: 'var(--bamboo-medium)', marginRight: '0.5rem'}} />
                    <span style={{fontSize: '0.875rem', fontWeight: '500', color: 'var(--ink-dark)'}}>
                      {users.find(u => u.id === activeId)?.username}
                    </span>
                  </div>
                ) : null}
              </DragOverlay>
            </DndContext>
            
            {users.length === 0 && (
              <p style={{fontSize: '0.875rem', color: 'var(--ink-light)', textAlign: 'center', padding: '1rem 0'}}>
                暂无可分配用户
              </p>
            )}
          </div>
        </div>

        {/* 时间轴区域 */}
        <div className="lg:col-span-3">
          <div style={{background: 'var(--rice-white)', borderRadius: '0.75rem', overflow: 'hidden', border: '1px solid var(--bamboo-light)'}}>
            {/* 时间轴标尺 */}
            <div style={{height: '3rem', position: 'relative', background: 'linear-gradient(135deg, var(--rice-cream) 0%, var(--rice-white) 100%)', borderBottom: '1px solid var(--bamboo-light)'}}>
              <div className="absolute inset-0 flex items-center px-4">
                <span style={{fontSize: '0.75rem', fontWeight: '600', color: 'var(--ink-dark)', width: '12rem'}}>
                  项目 / 时间轴
                </span>
              </div>
              
              {generateTimeScale().map((scale, index) => (
                <div
                  key={index}
                  className="absolute top-0 bottom-0"
                  style={{ left: `${scale.position}%`, borderLeft: '1px solid var(--bamboo-light)' }}
                >
                  <div style={{position: 'absolute', top: '0.5rem', marginLeft: '-1.5rem', fontSize: '0.75rem', color: 'var(--ink-medium)', width: '3rem', textAlign: 'center'}}>
                    {scale.label}
                  </div>
                </div>
              ))}
            </div>
            
            {/* 项目列表 */}
            <div style={{padding: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem', maxHeight: '24rem', overflowY: 'auto'}}>
              {projects.length > 0 ? (
                projects.map((project) => (
                  <ProjectBar
                    key={project.id}
                    project={project}
                    onAssignUser={handleAssignUser}
                  />
                ))
              ) : (
                <div style={{textAlign: 'center', padding: '2rem 0'}}>
                  <CalendarDaysIcon style={{margin: '0 auto', width: '3rem', height: '3rem', color: 'var(--bamboo-light)'}} />
                  <h3 style={{marginTop: '0.5rem', fontSize: '0.875rem', fontWeight: '600', color: 'var(--ink-dark)'}}>暂无项目</h3>
                  <p style={{marginTop: '0.25rem', fontSize: '0.875rem', color: 'var(--ink-light)'}}>
                    请先创建项目以查看时间轴
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      
      {/* 说明信息 */}
      <div style={{background: 'linear-gradient(135deg, var(--rice-cream) 0%, var(--rice-white) 100%)', border: '1px solid var(--bamboo-light)', borderRadius: '0.75rem', padding: '1rem'}} className="seal-accent">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg style={{width: '1.25rem', height: '1.25rem', color: 'var(--bamboo-medium)'}} viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
          </div>
          <div style={{marginLeft: '0.75rem'}}>
            <h3 style={{fontSize: '0.875rem', fontWeight: '600', color: 'var(--ink-dark)'}}>
              使用说明
            </h3>
            <div style={{marginTop: '0.5rem', fontSize: '0.875rem', color: 'var(--ink-medium)'}}>
              <ul style={{listStyleType: 'disc', paddingLeft: '1rem', display: 'flex', flexDirection: 'column', gap: '0.25rem'}}>
                <li>从左侧用户列表拖拽用户到右侧项目条上进行人员分配</li>
                <li>项目条的长度表示项目持续时间，位置表示时间范围</li>
                <li>项目条下方的蓝色小条表示已分配的用户</li>
                <li>鼠标悬停在用户分配条上可查看详细信息</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectTimeline;