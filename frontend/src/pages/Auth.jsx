import React, { useState } from 'react';
import { Lock, Phone, User, ShieldCheck, LogIn } from 'lucide-react';

export default function Auth({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('tenant');

  // Inline validation feedback
  const [phoneError, setPhoneError] = useState('');
  const [passwordError, setPasswordError] = useState('');

  const handlePhoneChange = (e) => {
    const val = e.target.value;
    setPhone(val);
    if (val && !/^[0-9]{10}$/.test(val)) {
      setPhoneError('Số điện thoại phải gồm đúng 10 số!');
    } else {
      setPhoneError('');
    }
  };

  const handlePasswordChange = (e) => {
    const val = e.target.value;
    setPassword(val);
    if (val && val.length < 6) {
      setPasswordError('Mật khẩu phải dài tối thiểu 6 ký tự!');
    } else {
      setPasswordError('');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (phoneError || passwordError || !phone || !password) {
      alert('Vui lòng điền đúng và đầy đủ các thông tin đăng nhập!');
      return;
    }

    // Mock successful login/register
    const mockUser = {
      name: name || (role === 'landlord' ? 'Nguyễn Văn Hùng' : role === 'admin' ? 'Hồ Anh Admin' : 'Khách Thuê Trẻ'),
      avatar: role === 'landlord' 
        ? 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80' 
        : 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80',
      role: role
    };

    onLoginSuccess(mockUser, role);
    alert(`Chào mừng ${mockUser.name} đã đăng nhập thành công vào TroTot!`);
  };

  return (
    <div style={{
      animation: 'fadeIn 0.4s ease-out',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '40px 20px',
      minHeight: 'calc(100vh - 160px)'
    }}>
      <div className="glass-panel" style={{
        width: '400px',
        maxWidth: '100%',
        borderRadius: 'var(--radius-lg)',
        padding: '32px 24px',
        border: '1px solid var(--border)',
        boxShadow: 'var(--shadow-premium)',
        textAlign: 'center'
      }}>
        
        {/* Toggle Slide tabs tab buttons */}
        <div style={{
          display: 'flex',
          background: 'var(--bg-primary)',
          borderRadius: '9999px',
          padding: '4px',
          marginBottom: '24px',
          border: '1px solid var(--border)'
        }}>
          <button
            type="button"
            onClick={() => setIsLogin(true)}
            style={{
              flex: 1,
              padding: '8px 0',
              borderRadius: '9999px',
              fontSize: '13px',
              fontWeight: 700,
              transition: 'var(--transition)',
              background: isLogin ? 'var(--primary)' : 'transparent',
              color: isLogin ? '#fff' : 'var(--text-secondary)'
            }}
          >
            Đăng nhập
          </button>
          <button
            type="button"
            onClick={() => setIsLogin(false)}
            style={{
              flex: 1,
              padding: '8px 0',
              borderRadius: '9999px',
              fontSize: '13px',
              fontWeight: 700,
              transition: 'var(--transition)',
              background: !isLogin ? 'var(--primary)' : 'transparent',
              color: !isLogin ? '#fff' : 'var(--text-secondary)'
            }}
          >
            Đăng ký mới
          </button>
        </div>

        <h3 style={{ fontSize: '20px', fontWeight: 800, marginBottom: '6px' }}>
          {isLogin ? 'Chào mừng bạn quay lại 👋' : 'Tạo tài khoản TroTot ✨'}
        </h3>
        <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '24px' }}>
          {isLogin ? 'Đăng nhập để liên hệ nhanh với chủ phòng trọ' : 'Khám phá hơn 1,000+ phòng trọ trọn gói giá tốt'}
        </p>

        {/* Auth form input field */}
        <form onSubmit={handleSubmit} style={{ textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '14px' }}>
          
          {!isLogin && (
            <div>
              <label style={{ fontSize: '11px', fontWeight: 700, display: 'block', marginBottom: '4px', color: 'var(--text-secondary)' }}>Họ và tên *</label>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                background: 'var(--bg-primary)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-md)',
                padding: '10px 14px'
              }}>
                <User size={16} style={{ color: 'var(--text-muted)', marginRight: '8px' }} />
                <input 
                  type="text" 
                  placeholder="Ví dụ: Nguyễn Văn A"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  style={{ background: 'transparent', border: 'none', width: '100%', fontSize: '13px', color: 'var(--text-primary)', outline: 'none' }}
                />
              </div>
            </div>
          )}

          <div>
            <label style={{ fontSize: '11px', fontWeight: 700, display: 'block', marginBottom: '4px', color: 'var(--text-secondary)' }}>Số điện thoại *</label>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              background: 'var(--bg-primary)',
              border: `1px solid ${phoneError ? 'var(--danger)' : 'var(--border)'}`,
              borderRadius: 'var(--radius-md)',
              padding: '10px 14px'
            }}>
              <Phone size={16} style={{ color: 'var(--text-muted)', marginRight: '8px' }} />
              <input 
                type="tel" 
                placeholder="Nhập 10 số điện thoại"
                value={phone}
                onChange={handlePhoneChange}
                required
                style={{ background: 'transparent', border: 'none', width: '100%', fontSize: '13px', color: 'var(--text-primary)', outline: 'none' }}
              />
            </div>
            {phoneError && <span style={{ fontSize: '10px', color: 'var(--danger)', marginTop: '4px', display: 'block', fontWeight: 600 }}>{phoneError}</span>}
          </div>

          <div>
            <label style={{ fontSize: '11px', fontWeight: 700, display: 'block', marginBottom: '4px', color: 'var(--text-secondary)' }}>Mật khẩu bảo mật *</label>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              background: 'var(--bg-primary)',
              border: `1px solid ${passwordError ? 'var(--danger)' : 'var(--border)'}`,
              borderRadius: 'var(--radius-md)',
              padding: '10px 14px'
            }}>
              <Lock size={16} style={{ color: 'var(--text-muted)', marginRight: '8px' }} />
              <input 
                type="password" 
                placeholder="Tối thiểu 6 ký tự"
                value={password}
                onChange={handlePasswordChange}
                required
                style={{ background: 'transparent', border: 'none', width: '100%', fontSize: '13px', color: 'var(--text-primary)', outline: 'none' }}
              />
            </div>
            {passwordError && <span style={{ fontSize: '10px', color: 'var(--danger)', marginTop: '4px', display: 'block', fontWeight: 600 }}>{passwordError}</span>}
          </div>

          {/* Quick Role picker selection for demo */}
          <div>
            <label style={{ fontSize: '11px', fontWeight: 700, display: 'block', marginBottom: '4px', color: 'var(--text-secondary)' }}>
              Đăng nhập với vai trò kiểm thử:
            </label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              style={{
                width: '100%',
                background: 'var(--bg-primary)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius-md)',
                padding: '10px 14px',
                fontSize: '13px',
                color: 'var(--text-primary)'
              }}
            >
              <option value="tenant">Khách Thuê Phòng</option>
              <option value="landlord">Chủ Nhà Cho Thuê</option>
              <option value="admin">Quản Trị Viên (Admin)</option>
            </select>
          </div>

          {/* CTA Submit Button */}
          <button
            type="submit"
            style={{
              width: '100%',
              background: 'var(--primary)',
              color: '#fff',
              padding: '12px 0',
              borderRadius: 'var(--radius-md)',
              fontWeight: 700,
              fontSize: '13px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
              boxShadow: '0 4px 10px rgba(99, 102, 241, 0.2)',
              marginTop: '10px'
            }}
            className="hover-lift"
          >
            <LogIn size={15} />
            <span>{isLogin ? 'Đăng nhập tài khoản' : 'Đăng ký tài khoản mới'}</span>
          </button>

        </form>

        {/* Divider and social login integration */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', margin: '20px 0' }}>
          <div style={{ flexGrow: 1, borderTop: '1px solid var(--border)' }} />
          <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 600 }}>HOẶC ĐĂNG NHẬP NHANH</span>
          <div style={{ flexGrow: 1, borderTop: '1px solid var(--border)' }} />
        </div>

        {/* Social Buttons */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
          <button 
            onClick={() => onLoginSuccess({ name: 'Google User', avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80', role: 'tenant' }, 'tenant')}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
              padding: '10px 0',
              borderRadius: 'var(--radius-md)',
              background: 'var(--bg-primary)',
              border: '1px solid var(--border)',
              fontSize: '11px',
              fontWeight: 700,
              color: 'var(--text-secondary)'
            }}
            className="hover-lift"
          >
            <span style={{ fontSize: '14px' }}>🌐</span>
            <span>Google ID</span>
          </button>

          <button 
            onClick={() => onLoginSuccess({ name: 'Chủ Nhà Hùng', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80', role: 'landlord' }, 'landlord')}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
              padding: '10px 0',
              borderRadius: 'var(--radius-md)',
              background: 'var(--bg-primary)',
              border: '1px solid var(--border)',
              fontSize: '11px',
              fontWeight: 700,
              color: 'var(--text-secondary)'
            }}
            className="hover-lift"
          >
            <span style={{ fontSize: '14px' }}>👤</span>
            <span>Chủ nhà Demo</span>
          </button>
        </div>

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          marginTop: '24px',
          fontSize: '11px',
          color: 'var(--text-muted)',
          justifyContent: 'center'
        }}>
          <ShieldCheck size={14} style={{ color: 'var(--emerald)' }} />
          <span>TroTot cam kết bảo mật 100% dữ liệu cá nhân</span>
        </div>

      </div>
    </div>
  );
}
