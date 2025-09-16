import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  UsersIcon,
  PlusIcon,
  PencilIcon,
  TrashIcon,
  MagnifyingGlassIcon,
  UserPlusIcon,
} from '@heroicons/react/24/outline';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid';
import '../styles/chinese-minimal.css';

interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

interface UserFormData {
  username: string;
  email: string;
  password: string;
  is_active: boolean;
}

const UserManagement: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [formData, setFormData] = useState<UserFormData>({
    username: '',
    email: '',
    password: '',
    is_active: true,
  });
  const [formLoading, setFormLoading] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/v1/users/');
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to fetch users:', error);
      setError('获取用户列表失败');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = () => {
    setEditingUser(null);
    setFormData({
      username: '',
      email: '',
      password: '',
      is_active: true,
    });
    setShowModal(true);
  };

  const handleEditUser = (user: User) => {
    setEditingUser(user);
    setFormData({
      username: user.username,
      email: user.email,
      password: '',
      is_active: user.is_active,
    });
    setShowModal(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormLoading(true);
    setError('');

    try {
      if (editingUser) {
        // 更新用户
        const updateData: any = {
          username: formData.username,
          email: formData.email,
          is_active: formData.is_active,
        };
        
        if (formData.password) {
          updateData.password = formData.password;
        }
        
        await axios.put(`/api/v1/users/${editingUser.id}`, updateData);
      } else {
        // 创建新用户
        await axios.post('/api/v1/users/', formData);
      }
      
      setShowModal(false);
      fetchUsers();
    } catch (error: any) {
      console.error('Failed to save user:', error);
      setError(error.response?.data?.detail || '保存用户失败');
    } finally {
      setFormLoading(false);
    }
  };

  const handleDeleteUser = async (userId: number) => {
    if (!confirm('确定要删除这个用户吗？此操作不可撤销。')) {
      return;
    }

    try {
      await axios.delete(`/api/v1/users/${userId}`);
      fetchUsers();
    } catch (error) {
      console.error('Failed to delete user:', error);
      setError('删除用户失败');
    }
  };

  const handleToggleActive = async (user: User) => {
    try {
      await axios.put(`/api/v1/users/${user.id}`, {
        ...user,
        is_active: !user.is_active,
      });
      fetchUsers();
    } catch (error) {
      console.error('Failed to toggle user status:', error);
      setError('更新用户状态失败');
    }
  };

  const filteredUsers = users.filter(user =>
    user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
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
              <UsersIcon style={{width: '1.75rem', height: '1.75rem', marginRight: '0.5rem', color: 'var(--bamboo-medium)'}} />
              用户管理
            </h1>
            <p style={{marginTop: '0.25rem', fontSize: '0.875rem', color: 'var(--ink-light)'}}>
              管理系统用户账户和权限
            </p>
          </div>
          <button
            onClick={handleCreateUser}
            className="btn-minimal flex items-center transition-all duration-200 hover:scale-105"
            style={{padding: '0.5rem 1rem', background: 'var(--bamboo-medium)', color: 'var(--rice-white)', borderRadius: '0.5rem', border: 'none', gap: '0.5rem'}}
          >
            <UserPlusIcon style={{width: '1rem', height: '1rem'}} />
            <span>新建用户</span>
          </button>
        </div>
      </div>

      {error && (
        <div style={{background: 'var(--rice-cream)', border: '1px solid var(--bamboo-light)', color: 'var(--ink-dark)', padding: '0.75rem 1rem', borderRadius: '0.5rem'}}>
          {error}
        </div>
      )}

      {/* 搜索栏 */}
      <div style={{background: 'var(--rice-white)', boxShadow: '0 2px 8px rgba(0,0,0,0.08)', borderRadius: '0.75rem', padding: '1.5rem', border: '1px solid var(--bamboo-light)'}} className="transition-all duration-300 hover:shadow-lg">
        <div className="relative max-w-md">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <MagnifyingGlassIcon style={{width: '1.25rem', height: '1.25rem', color: 'var(--bamboo-light)'}} />
          </div>
          <input
            type="text"
            style={{width: '100%', paddingLeft: '2.5rem', padding: '0.75rem', border: '1px solid var(--bamboo-light)', borderRadius: '0.5rem', background: 'var(--rice-white)', color: 'var(--ink-dark)', fontSize: '0.875rem'}}
            className="transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-bamboo-medium focus:border-transparent"
            placeholder="搜索用户名或邮箱..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* 用户列表 */}
      <div style={{background: 'var(--rice-white)', boxShadow: '0 2px 8px rgba(0,0,0,0.08)', borderRadius: '0.75rem', overflow: 'hidden', border: '1px solid var(--bamboo-light)'}} className="transition-all duration-300 hover:shadow-lg">
        <div style={{padding: '1.5rem', borderBottom: '1px solid var(--bamboo-light)'}}>
          <h3 style={{fontSize: '1.125rem', fontWeight: '600', color: 'var(--ink-dark)'}}>
            用户列表 ({filteredUsers.length})
          </h3>
        </div>
        
        {filteredUsers.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead style={{background: 'linear-gradient(135deg, var(--rice-cream) 0%, var(--rice-white) 100%)'}}>
                <tr>
                  <th style={{padding: '1rem 1.5rem', textAlign: 'left', fontSize: '0.75rem', fontWeight: '600', color: 'var(--ink-medium)', textTransform: 'uppercase', letterSpacing: '0.05em'}}>
                    用户信息
                  </th>
                  <th style={{padding: '1rem 1.5rem', textAlign: 'left', fontSize: '0.75rem', fontWeight: '600', color: 'var(--ink-medium)', textTransform: 'uppercase', letterSpacing: '0.05em'}}>
                    状态
                  </th>
                  <th style={{padding: '1rem 1.5rem', textAlign: 'left', fontSize: '0.75rem', fontWeight: '600', color: 'var(--ink-medium)', textTransform: 'uppercase', letterSpacing: '0.05em'}}>
                    创建时间
                  </th>
                  <th style={{padding: '1rem 1.5rem', textAlign: 'right', fontSize: '0.75rem', fontWeight: '600', color: 'var(--ink-medium)', textTransform: 'uppercase', letterSpacing: '0.05em'}}>
                    操作
                  </th>
                </tr>
              </thead>
              <tbody style={{background: 'var(--rice-white)'}}>
                {filteredUsers.map((user) => (
                  <tr key={user.id} style={{borderBottom: '1px solid var(--bamboo-light)'}} className="transition-colors duration-200 hover:bg-rice-cream">
                    <td style={{padding: '1rem 1.5rem', whiteSpace: 'nowrap'}}>
                      <div className="flex items-center">
                        <div className="flex-shrink-0">
                          <div style={{width: '2.5rem', height: '2.5rem', borderRadius: '50%', background: 'var(--bamboo-medium)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                            <span style={{fontSize: '0.875rem', fontWeight: '600', color: 'var(--rice-white)'}}>
                              {user.username.charAt(0).toUpperCase()}
                            </span>
                          </div>
                        </div>
                        <div style={{marginLeft: '1rem'}}>
                          <div style={{fontSize: '0.875rem', fontWeight: '600', color: 'var(--ink-dark)'}}>
                            {user.username}
                          </div>
                          <div style={{fontSize: '0.875rem', color: 'var(--ink-light)'}}>
                            {user.email}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td style={{padding: '1rem 1.5rem', whiteSpace: 'nowrap'}}>
                      <button
                        onClick={() => handleToggleActive(user)}
                        className="flex items-center transition-all duration-200 hover:scale-105"
                        style={{gap: '0.25rem', padding: '0.25rem 0.5rem', borderRadius: '0.375rem', border: 'none', background: 'transparent'}}
                      >
                        {user.is_active ? (
                          <>
                            <CheckCircleIcon style={{width: '1.25rem', height: '1.25rem', color: 'var(--bamboo-medium)'}} />
                            <span style={{fontSize: '0.875rem', color: 'var(--bamboo-dark)', fontWeight: '500'}}>活跃</span>
                          </>
                        ) : (
                          <>
                            <XCircleIcon style={{width: '1.25rem', height: '1.25rem', color: 'var(--ink-light)'}} />
                            <span style={{fontSize: '0.875rem', color: 'var(--ink-light)', fontWeight: '500'}}>禁用</span>
                          </>
                        )}
                      </button>
                    </td>
                    <td style={{padding: '1rem 1.5rem', whiteSpace: 'nowrap', fontSize: '0.875rem', color: 'var(--ink-light)'}}>
                      {formatDate(user.created_at)}
                    </td>
                    <td style={{padding: '1rem 1.5rem', whiteSpace: 'nowrap', textAlign: 'right', fontSize: '0.875rem', fontWeight: '500'}}>
                      <div className="flex items-center justify-end" style={{gap: '0.5rem'}}>
                        <button
                          onClick={() => handleEditUser(user)}
                          className="transition-all duration-200 hover:scale-110"
                          style={{color: 'var(--bamboo-medium)', padding: '0.25rem', borderRadius: '0.25rem', border: 'none', background: 'transparent'}}
                          title="编辑用户"
                        >
                          <PencilIcon style={{width: '1rem', height: '1rem'}} />
                        </button>
                        <button
                          onClick={() => handleDeleteUser(user.id)}
                          className="transition-all duration-200 hover:scale-110"
                          style={{color: 'var(--ink-light)', padding: '0.25rem', borderRadius: '0.25rem', border: 'none', background: 'transparent'}}
                          title="删除用户"
                        >
                          <TrashIcon style={{width: '1rem', height: '1rem'}} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center" style={{padding: '3rem 0'}}>
            <UsersIcon style={{margin: '0 auto', width: '3rem', height: '3rem', color: 'var(--ink-light)'}} />
            <h3 style={{marginTop: '0.5rem', fontSize: '0.875rem', fontWeight: '600', color: 'var(--ink-dark)'}}>
              {searchTerm ? '未找到匹配的用户' : '暂无用户'}
            </h3>
            <p style={{marginTop: '0.25rem', fontSize: '0.875rem', color: 'var(--ink-light)'}}>
              {searchTerm ? '请尝试其他搜索条件' : '点击上方按钮创建第一个用户'}
            </p>
          </div>
        )}
      </div>

      {/* 用户表单模态框 */}
      {showModal && (
        <div className="fixed inset-0 overflow-y-auto h-full w-full" style={{backgroundColor: 'rgba(0, 0, 0, 0.5)', zIndex: 50}}>
          <div className="relative mx-auto border shadow-lg rounded-lg" style={{top: '5rem', padding: '1.25rem', width: '24rem', background: 'var(--paper)', borderColor: 'var(--bamboo-light)'}}>
            <div style={{marginTop: '0.75rem'}}>
              <h3 className="chinese-title" style={{fontSize: '1.125rem', fontWeight: '600', color: 'var(--ink-dark)', marginBottom: '1rem'}}>
                {editingUser ? '编辑用户' : '新建用户'}
              </h3>
              
              <form onSubmit={handleSubmit} style={{display: 'flex', flexDirection: 'column', gap: '1rem'}}>
                <div>
                  <label className="block" style={{fontSize: '0.875rem', fontWeight: '500', color: 'var(--ink-dark)', marginBottom: '0.25rem'}}>
                    用户名 *
                  </label>
                  <input
                    type="text"
                    required
                    className="chinese-input"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    disabled={formLoading}
                  />
                </div>
                
                <div>
                  <label className="block" style={{fontSize: '0.875rem', fontWeight: '500', color: 'var(--ink-dark)', marginBottom: '0.25rem'}}>
                    邮箱 *
                  </label>
                  <input
                    type="email"
                    required
                    className="chinese-input"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    disabled={formLoading}
                  />
                </div>
                
                <div>
                  <label className="block" style={{fontSize: '0.875rem', fontWeight: '500', color: 'var(--ink-dark)', marginBottom: '0.25rem'}}>
                    密码 {editingUser ? '(留空则不修改)' : '*'}
                  </label>
                  <input
                    type="password"
                    required={!editingUser}
                    className="chinese-input"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    disabled={formLoading}
                  />
                </div>
                
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="is_active"
                    style={{width: '1rem', height: '1rem', accentColor: 'var(--bamboo-medium)', borderColor: 'var(--bamboo-light)', borderRadius: '0.25rem'}}
                    checked={formData.is_active}
                    onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                    disabled={formLoading}
                  />
                  <label htmlFor="is_active" className="block" style={{marginLeft: '0.5rem', fontSize: '0.875rem', color: 'var(--ink-dark)'}}>
                    激活用户
                  </label>
                </div>
                
                <div className="flex items-center justify-end" style={{gap: '0.75rem', paddingTop: '1rem'}}>
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="chinese-btn-outline"
                    disabled={formLoading}
                  >
                    取消
                  </button>
                  <button
                    type="submit"
                    className="chinese-btn-primary"
                    disabled={formLoading}
                  >
                    {formLoading ? '保存中...' : (editingUser ? '更新' : '创建')}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserManagement;