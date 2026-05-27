import React from 'react';
import { Home, Heart, MessageSquare, User, Shield } from 'lucide-react';

export default function BottomBar({ currentPage, onNavigate, currentRole, favoritesCount }) {
  return (
    <div className="glass-panel mobile-nav-bar" style={{
      position: 'fixed',
      bottom: 0,
      left: 0,
      right: 0,
      zIndex: 90,
      display: 'none', /* Bật hiển thị qua Media Query trong CSS */
      justifyContent: 'space-around',
      alignItems: 'center',
      padding: '10px 0',
      borderRadius: '20px 20px 0 0',
      boxShadow: '0 -4px 20px rgba(0,0,0,0.06)',
      borderTop: '1px solid var(--border)'
    }}>
      {/* Tab Home */}
      <button 
        onClick={() => onNavigate('home')} 
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '4px',
          color: currentPage === 'home' ? 'var(--primary)' : 'var(--text-secondary)',
          background: 'none',
          border: 'none',
          cursor: 'pointer'
        }}
      >
        <Home size={20} style={{ transform: currentPage === 'home' ? 'scale(1.1)' : 'scale(1)', transition: 'var(--transition)' }} />
        <span style={{ fontSize: '10px', fontWeight: 600 }}>Trang chủ</span>
      </button>

      {/* Tab Yêu thích */}
      <button 
        onClick={() => onNavigate('favorites')} 
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '4px',
          color: currentPage === 'favorites' ? 'var(--secondary)' : 'var(--text-secondary)',
          position: 'relative'
        }}
      >
        <Heart size={20} style={{ transform: currentPage === 'favorites' ? 'scale(1.1)' : 'scale(1)', transition: 'var(--transition)' }} />
        {favoritesCount > 0 && (
          <span style={{
            position: 'absolute',
            top: '-4px',
            right: '2px',
            background: 'var(--secondary)',
            color: '#fff',
            fontSize: '8px',
            fontWeight: 800,
            width: '14px',
            height: '14px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>{favoritesCount}</span>
        )}
        <span style={{ fontSize: '10px', fontWeight: 600 }}>Yêu thích</span>
      </button>

      {/* Tab Chat */}
      <button 
        onClick={() => onNavigate('chat')} 
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '4px',
          color: currentPage === 'chat' ? 'var(--primary)' : 'var(--text-secondary)'
        }}
      >
        <MessageSquare size={20} />
        <span style={{ fontSize: '10px', fontWeight: 600 }}>Tin nhắn</span>
      </button>

      {/* Tab Dashboard (Chủ nhà hoặc Admin) */}
      {currentRole === 'landlord' && (
        <button 
          onClick={() => onNavigate('landlord')} 
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '4px',
            color: currentPage === 'landlord' ? 'var(--primary)' : 'var(--text-secondary)'
          }}
        >
          <User size={20} />
          <span style={{ fontSize: '10px', fontWeight: 600 }}>Chủ nhà</span>
        </button>
      )}

      {currentRole === 'admin' && (
        <button 
          onClick={() => onNavigate('admin')} 
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '4px',
            color: currentPage === 'admin' ? 'var(--primary)' : 'var(--text-secondary)'
          }}
        >
          <Shield size={20} />
          <span style={{ fontSize: '10px', fontWeight: 600 }}>Admin</span>
        </button>
      )}
      
      {currentRole === 'tenant' && (
        <button 
          onClick={() => onNavigate('auth')} 
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '4px',
            color: currentPage === 'auth' ? 'var(--primary)' : 'var(--text-secondary)'
          }}
        >
          <User size={20} />
          <span style={{ fontSize: '10px', fontWeight: 600 }}>Cá nhân</span>
        </button>
      )}
    </div>
  );
}
