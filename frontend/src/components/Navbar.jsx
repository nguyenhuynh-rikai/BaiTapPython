import React from 'react';
import { Home, MessageSquare, Shield, User, LogOut, Bell, Search, Layers } from 'lucide-react';

export default function Navbar({ currentRole, onChangeRole, onNavigate, currentPage, user, onLogout }) {
  return (
    <header className="glass-panel" style={{
      position: 'sticky',
      top: 0,
      zIndex: 100,
      borderRadius: '0 0 var(--radius-lg) var(--radius-lg)',
      boxShadow: 'var(--shadow-sm)',
      padding: '12px 24px',
      marginBottom: '20px'
    }}>
      <div className="flex-between">
        {/* Logo */}
        <div 
          onClick={() => onNavigate('home')} 
          style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}
        >
          <div style={{
            background: 'var(--primary)',
            color: '#fff',
            width: '36px',
            height: '36px',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 10px rgba(99, 102, 241, 0.3)'
          }}>
            <Home size={20} />
          </div>
          <div>
            <h3 style={{ fontSize: '18px', fontWeight: 800, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '4px' }}>
              TroTot <span style={{ color: 'var(--primary)', fontSize: '12px', background: 'var(--primary-light)', padding: '2px 6px', borderRadius: '6px' }}>RentHub</span>
            </h3>
          </div>
        </div>

        {/* Quick Search - Desktop */}
        <div className="search-bar-container" style={{
          display: 'flex',
          alignItems: 'center',
          background: 'var(--bg-primary)',
          border: '1px solid var(--border)',
          borderRadius: '9999px',
          padding: '4px 16px',
          width: '320px',
          maxWidth: '100%',
          transition: 'var(--transition)'
        }}>
          <Search size={16} style={{ color: 'var(--text-muted)', marginRight: '8px' }} />
          <input 
            type="text" 
            placeholder="Tìm quận, đại học..." 
            style={{
              background: 'transparent',
              border: 'none',
              fontSize: '14px',
              width: '100%',
              color: 'var(--text-primary)'
            }}
          />
        </div>

        {/* Dynamic Nav & Role Switcher */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          
          {/* Interactive Role Switcher */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            background: 'var(--primary-light)',
            padding: '4px 12px',
            borderRadius: '9999px',
            border: '1px dashed var(--primary)'
          }}>
            <Layers size={14} style={{ color: 'var(--primary)' }} />
            <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--primary)', marginRight: '4px' }}>Vai trò:</span>
            <select 
              value={currentRole} 
              onChange={(e) => onChangeRole(e.target.value)}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'var(--primary)',
                fontWeight: 700,
                fontSize: '12px',
                cursor: 'pointer',
                outline: 'none'
              }}
            >
              <option value="tenant">Khách thuê</option>
              <option value="landlord">Chủ nhà</option>
              <option value="admin">Quản trị viên</option>
            </select>
          </div>

          {/* Quick Icons */}
          <button 
            onClick={() => onNavigate('chat')} 
            style={{ 
              position: 'relative', 
              color: currentPage === 'chat' ? 'var(--primary)' : 'var(--text-secondary)',
              padding: '6px',
              borderRadius: '50%',
              transition: 'var(--transition)'
            }}
            className="hover-lift"
          >
            <MessageSquare size={20} />
            <span style={{
              position: 'absolute',
              top: '2px',
              right: '2px',
              width: '8px',
              height: '8px',
              background: 'var(--secondary)',
              borderRadius: '50%'
            }} />
          </button>

          {currentRole === 'landlord' && (
            <button 
              onClick={() => onNavigate('landlord')}
              style={{ 
                fontSize: '13px', 
                fontWeight: 600, 
                color: currentPage === 'landlord' ? 'var(--primary)' : 'var(--text-secondary)',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}
              className="hover-lift"
            >
              <User size={16} />
              <span>Chủ nhà</span>
            </button>
          )}

          {currentRole === 'admin' && (
            <button 
              onClick={() => onNavigate('admin')}
              style={{ 
                fontSize: '13px', 
                fontWeight: 600, 
                color: currentPage === 'admin' ? 'var(--primary)' : 'var(--text-secondary)',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}
              className="hover-lift"
            >
              <Shield size={16} />
              <span>Admin</span>
            </button>
          )}

          {/* User Profile / Login */}
          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <img 
                src={user.avatar} 
                alt={user.name} 
                style={{ width: '32px', height: '32px', borderRadius: '50%', objectFit: 'cover', border: '2px solid var(--primary-light)' }} 
              />
              <button 
                onClick={onLogout}
                style={{ color: 'var(--danger)', padding: '6px', borderRadius: '50%' }}
                title="Đăng xuất"
                className="hover-lift"
              >
                <LogOut size={18} />
              </button>
            </div>
          ) : (
            <button 
              onClick={() => onNavigate('auth')}
              style={{
                background: 'var(--primary)',
                color: '#fff',
                padding: '6px 16px',
                borderRadius: '9999px',
                fontSize: '13px',
                fontWeight: 700,
                boxShadow: '0 4px 10px rgba(99, 102, 241, 0.2)'
              }}
              className="hover-lift"
            >
              Đăng nhập
            </button>
          )}
        </div>
      </div>
      
      {/* Mobile styles handling in index.css */}
    </header>
  );
}
