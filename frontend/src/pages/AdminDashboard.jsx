import React, { useState, useEffect } from 'react';
import { ShieldCheck, ShieldAlert, Check, X, AlertTriangle, Users, ClipboardCheck } from 'lucide-react';
import { api } from '../utils/api';

export default function AdminDashboard({ rooms, onApproveRoom, onRejectRoom }) {
  const pendingRooms = rooms.filter(room => room.status === 'pending');
  const [rejectingRoomId, setRejectingRoomId] = useState(null);
  const [rejectionReason, setRejectionReason] = useState('Ảnh mờ/Kém chất lượng');

  // Tab control state
  const [activeTab, setActiveTab] = useState('review'); // 'review' | 'users'
  const [users, setUsers] = useState([]);
  const [loadingUsers, setLoadingUsers] = useState(false);

  const rejectionReasons = [
    'Ảnh mờ/Kém chất lượng',
    'Giá phòng trọ không thực tế hoặc quá cao',
    'Thiếu địa chỉ cụ thể / Bản đồ sai lệch',
    'Trùng lặp với tin đăng có sẵn',
    'Mô tả phòng chứa nội dung vi phạm tiêu chuẩn cộng đồng'
  ];

  const fetchUsers = async () => {
    setLoadingUsers(true);
    try {
      const data = await api.get('/admin/users/');
      setUsers(data);
    } catch (err) {
      console.error('Lỗi tải danh sách người dùng:', err);
    } finally {
      setLoadingUsers(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'users') {
      fetchUsers();
    }
  }, [activeTab]);

  const handleChangeUserRole = async (userId, newRole) => {
    try {
      await api.put(`/admin/users/${userId}/`, { role: newRole });
      alert('Cập nhật vai trò và phân quyền người dùng thành công!');
      fetchUsers();
    } catch (err) {
      alert(`Lỗi cập nhật vai trò: ${err.message}`);
    }
  };

  const handleRejectSubmit = (id) => {
    onRejectRoom(id, rejectionReason);
    setRejectingRoomId(null);
    alert(`Đã từ chối kiểm duyệt tin đăng. Lý do: ${rejectionReason}`);
  };

  return (
    <div style={{ animation: 'fadeIn 0.4s ease-out' }}>

      {/* Dashboard Top Header */}
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '20px', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '8px' }}>
          <ShieldCheck size={24} style={{ color: 'var(--primary)' }} />
          <span>Bảng Điều Khiển của Quản trị viên (Admin)</span>
        </h2>
        <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Kiểm duyệt tính chính xác của bài đăng phòng trọ và phân quyền người dùng hệ thống</p>
      </div>

      {/* Tabs Switcher Navigation */}
      <div style={{ display: 'flex', gap: '12px', marginBottom: '24px', borderBottom: '1px solid var(--border)', paddingBottom: '8px' }}>
        <button
          onClick={() => setActiveTab('review')}
          style={{
            padding: '8px 16px',
            borderRadius: 'var(--radius-md)',
            background: activeTab === 'review' ? 'var(--primary)' : 'transparent',
            color: activeTab === 'review' ? '#fff' : 'var(--text-secondary)',
            border: 'none',
            fontWeight: 700,
            fontSize: '13px',
            cursor: 'pointer',
            transition: 'var(--transition)'
          }}
        >
          📋 Kiểm Duyệt Tin Chờ ({pendingRooms.length})
        </button>
        <button
          onClick={() => setActiveTab('users')}
          style={{
            padding: '8px 16px',
            borderRadius: 'var(--radius-md)',
            background: activeTab === 'users' ? 'var(--primary)' : 'transparent',
            color: activeTab === 'users' ? '#fff' : 'var(--text-secondary)',
            border: 'none',
            fontWeight: 700,
            fontSize: '13px',
            cursor: 'pointer',
            transition: 'var(--transition)'
          }}
        >
          👥 Phân Quyền Người Dùng
        </button>
      </div>

      {activeTab === 'review' && (
        <>
          {/* Admin stats boxes row */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '16px',
            marginBottom: '32px'
          }}>
            <div className="glass-panel" style={{ padding: '20px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border)' }}>
              <div className="flex-between" style={{ color: 'var(--text-muted)', marginBottom: '8px' }}>
                <span style={{ fontSize: '12px', fontWeight: 700 }}>Số tin chờ duyệt</span>
                <AlertTriangle size={18} style={{ color: 'var(--amber)' }} />
              </div>
              <h3 style={{ fontSize: '24px', fontWeight: 800 }}>{pendingRooms.length} tin</h3>
              <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 600 }}>Cần duyệt trong ngày hôm nay</span>
            </div>

            <div className="glass-panel" style={{ padding: '20px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border)' }}>
              <div className="flex-between" style={{ color: 'var(--text-muted)', marginBottom: '8px' }}>
                <span style={{ fontSize: '12px', fontWeight: 700 }}>Tổng tin đăng an toàn</span>
                <ClipboardCheck size={18} style={{ color: 'var(--emerald)' }} />
              </div>
              <h3 style={{ fontSize: '24px', fontWeight: 800 }}>
                {rooms.filter(r => r.status === 'approved').length} tin
              </h3>
              <span style={{ fontSize: '10px', color: 'var(--emerald)', fontWeight: 700 }}>Tỷ lệ duyệt thành công: ~85%</span>
            </div>

            <div className="glass-panel" style={{ padding: '20px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border)' }}>
              <div className="flex-between" style={{ color: 'var(--text-muted)', marginBottom: '8px' }}>
                <span style={{ fontSize: '12px', fontWeight: 700 }}>Tổng số phòng trọ</span>
                <Users size={18} style={{ color: 'var(--primary)' }} />
              </div>
              <h3 style={{ fontSize: '24px', fontWeight: 800 }}>{rooms.length} phòng</h3>
              <span style={{ fontSize: '10px', color: 'var(--primary)', fontWeight: 700 }}>Hệ thống chuẩn hóa dữ liệu</span>
            </div>
          </div>

          {/* Main Review Queue section */}
          <section style={{ background: 'var(--bg-secondary)', padding: '24px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border)', marginBottom: '30px' }}>
            <h3 style={{ fontSize: '16px', fontWeight: 800, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span>🔔 Hàng đợi kiểm duyệt phòng trọ</span>
              <span style={{ fontSize: '11px', background: 'var(--amber-light)', color: 'var(--amber)', padding: '2px 8px', borderRadius: '9999px', fontWeight: 800 }}>
                {pendingRooms.length} Tin mới
              </span>
            </h3>

            {pendingRooms.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '40px 20px', border: '1px dashed var(--border)', borderRadius: 'var(--radius-lg)' }}>
                <ShieldCheck size={40} style={{ color: 'var(--emerald)', marginBottom: '8px' }} />
                <h4 style={{ fontSize: '14px', fontWeight: 700 }}>Tuyệt vời! Đã hoàn tất mọi tin đăng kiểm duyệt</h4>
                <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>Không có tin phòng trọ nào đang nằm trong hàng đợi chờ duyệt.</p>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {pendingRooms.map(room => (
                  <div
                    key={room.id}
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      padding: '16px',
                      background: 'var(--bg-primary)',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--border)'
                    }}
                  >
                    {/* Header item with landlord metadata */}
                    <div className="flex-between" style={{ marginBottom: '12px', borderBottom: '1px solid var(--border)', paddingBottom: '10px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <img
                          src={room.landlord.avatar}
                          alt={room.landlord.name}
                          style={{ width: '32px', height: '32px', borderRadius: '50%', objectFit: 'cover' }}
                        />
                        <div>
                          <span style={{ fontSize: '12px', fontWeight: 700, display: 'block' }}>Chủ nhà: {room.landlord.name}</span>
                          <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>SĐT: {room.landlord.phone}</span>
                        </div>
                      </div>
                      <span style={{ fontSize: '11px', background: 'var(--primary-light)', color: 'var(--primary)', padding: '2px 8px', borderRadius: '4px', fontWeight: 700 }}>
                        {room.category === 'studio' ? 'Studio' : room.category === 'shared' ? 'KTX Homestay' : 'Phòng trọ'}
                      </span>
                    </div>

                    {/* Details layout split */}
                    <div style={{ display: 'grid', gridTemplateColumns: '120px 1fr', gap: '16px', marginBottom: '16px' }}>
                      <img
                        src={room.images[0]}
                        alt={room.title}
                        style={{ width: '100%', height: '90px', borderRadius: '8px', objectFit: 'cover' }}
                      />
                      <div>
                        <h4 style={{ fontSize: '14px', fontWeight: 800 }}>{room.title}</h4>
                        <p style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '4px' }}>
                          📍 {room.location} — {room.distance}
                        </p>
                        <p style={{ fontSize: '13px', fontWeight: 800, color: 'var(--secondary)', marginTop: '6px' }}>
                          {room.priceStr} — Diện tích: {room.area}m²
                        </p>
                        <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '8px', borderLeft: '3px solid var(--border)', paddingLeft: '8px', fontStyle: 'italic' }}>
                          "{room.description}"
                        </p>
                      </div>
                    </div>

                    {/* Reject menu form */}
                    {rejectingRoomId === room.id && (
                      <div className="glass-panel" style={{
                        padding: '12px',
                        borderRadius: 'var(--radius-sm)',
                        border: '1px solid var(--danger)',
                        background: 'var(--danger-light)',
                        marginBottom: '12px',
                        animation: 'fadeIn 0.2s ease-out'
                      }}>
                        <label style={{ fontSize: '11px', fontWeight: 700, color: 'var(--danger)', display: 'block', marginBottom: '6px' }}>
                          ⚠️ Chọn Lý Do Từ Chối Duyệt Tin:
                        </label>
                        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                          <select
                            value={rejectionReason}
                            onChange={(e) => setRejectionReason(e.target.value)}
                            style={{
                              flexGrow: 1,
                              padding: '6px 10px',
                              borderRadius: '6px',
                              border: '1px solid var(--border)',
                              fontSize: '12px'
                            }}
                          >
                            {rejectionReasons.map((reason, index) => (
                              <option key={index} value={reason}>{reason}</option>
                            ))}
                          </select>
                          <button
                            onClick={() => handleRejectSubmit(room.id)}
                            style={{
                              background: 'var(--danger)',
                              color: '#fff',
                              padding: '6px 12px',
                              borderRadius: '6px',
                              fontSize: '11px',
                              fontWeight: 700
                            }}
                          >
                            Xác nhận Từ chối
                          </button>
                          <button
                            onClick={() => setRejectingRoomId(null)}
                            style={{
                              background: 'transparent',
                              color: 'var(--text-secondary)',
                              fontSize: '11px',
                              fontWeight: 600
                            }}
                          >
                            Hủy
                          </button>
                        </div>
                      </div>
                    )}

                    {/* Approve / Reject Actions buttons */}
                    {rejectingRoomId !== room.id && (
                      <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end', borderTop: '1px solid var(--border)', paddingTop: '12px' }}>
                        <button
                          onClick={() => setRejectingRoomId(room.id)}
                          style={{
                            background: 'transparent',
                            color: 'var(--danger)',
                            border: '1px solid var(--danger)',
                            padding: '6px 14px',
                            borderRadius: '6px',
                            fontSize: '12px',
                            fontWeight: 700,
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px'
                          }}
                          className="hover-lift"
                        >
                          <X size={14} />
                          <span>Từ chối duyệt</span>
                        </button>

                        <button
                          onClick={() => {
                            onApproveRoom(room.id);
                            alert('Đã kiểm duyệt bài đăng thành công! Tin sẽ hiển thị ngay trên Trang chủ.');
                          }}
                          style={{
                            background: 'var(--emerald)',
                            color: '#fff',
                            padding: '6px 14px',
                            borderRadius: '6px',
                            fontSize: '12px',
                            fontWeight: 700,
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px'
                          }}
                          className="hover-lift"
                        >
                          <Check size={14} />
                          <span>Phê duyệt tin</span>
                        </button>
                      </div>
                    )}

                  </div>
                ))}
              </div>
            )}
          </section>
        </>
      )}

      {activeTab === 'users' && (
        <section style={{ background: 'var(--bg-secondary)', padding: '24px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border)', marginBottom: '30px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 800, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>👥 Phân Quyền Vai Trò Người Dùng Hệ Thống</span>
            <span style={{ fontSize: '11px', background: 'var(--primary-light)', color: 'var(--primary)', padding: '2px 8px', borderRadius: '9999px', fontWeight: 800 }}>
              {users.length} Thành viên
            </span>
          </h3>

          {loadingUsers ? (
            <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-secondary)' }}>Đang tải danh sách người dùng...</div>
          ) : users.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px 20px', border: '1px dashed var(--border)', borderRadius: 'var(--radius-lg)' }}>
              Chưa có thành viên nào tham gia hệ thống.
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
                <thead>
                  <tr style={{ borderBottom: '2px solid var(--border)', color: 'var(--text-muted)' }}>
                    <th style={{ padding: '12px 8px', fontWeight: 700 }}>ID</th>
                    <th style={{ padding: '12px 8px', fontWeight: 700 }}>Tên Đăng Nhập / SĐT</th>
                    <th style={{ padding: '12px 8px', fontWeight: 700 }}>Ngày Tham Gia</th>
                    <th style={{ padding: '12px 8px', fontWeight: 700 }}>Vai Trò Hiện Tại</th>
                    <th style={{ padding: '12px 8px', fontWeight: 700 }}>Phân Quyền Vai Trò</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map(u => (
                    <tr key={u.id} style={{ borderBottom: '1px solid var(--border)', transition: 'var(--transition)' }} className="hover-lift">
                      <td style={{ padding: '12px 8px', fontWeight: 700, color: 'var(--text-muted)' }}>#{u.id}</td>
                      <td style={{ padding: '12px 8px', fontWeight: 700, color: 'var(--text-primary)' }}>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                          👤 {u.username}
                        </span>
                      </td>
                      <td style={{ padding: '12px 8px', color: 'var(--text-secondary)' }}>{u.date_joined}</td>
                      <td style={{ padding: '12px 8px' }}>
                        <span style={{
                          padding: '4px 10px',
                          borderRadius: '6px',
                          fontSize: '11px',
                          fontWeight: 700,
                          background: u.role === 'admin' ? '#8b5cf6' : u.role === 'landlord' ? '#10b981' : '#3b82f6',
                          color: '#fff',
                          boxShadow: 'var(--shadow-sm)'
                        }}>
                          {u.role === 'admin' ? 'Quản Trị Viên' : u.role === 'landlord' ? 'Chủ Cho Thuê' : 'Khách Thuê'}
                        </span>
                      </td>
                      <td style={{ padding: '12px 8px' }}>
                        <select
                          value={u.role}
                          onChange={(e) => handleChangeUserRole(u.id, e.target.value)}
                          style={{
                            padding: '6px 12px',
                            borderRadius: '6px',
                            border: '1px solid var(--border)',
                            background: 'var(--bg-primary)',
                            color: 'var(--text-primary)',
                            fontSize: '12px',
                            fontWeight: 700,
                            cursor: 'pointer',
                            outline: 'none',
                            transition: 'var(--transition)'
                          }}
                        >
                          <option value="tenant">Khách Thuê Phòng</option>
                          <option value="landlord">Chủ Cho Thuê</option>
                          <option value="admin">Quản Trị Viên (Admin)</option>
                        </select>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      )}

      {/* Visual Design Decisions & UX notes */}
      <section style={{
        marginTop: '40px',
        padding: '20px',
        background: 'var(--bg-secondary)',
        borderRadius: 'var(--radius-lg)',
        border: '1px solid var(--border)',
        marginBottom: '30px'
      }}>
        <h4 style={{ fontSize: '15px', fontWeight: 800, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          🎨 Quyết định Thiết kế & UX Bảng điều khiển Admin
        </h4>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', fontSize: '12px' }}>
          <div>
            <p style={{ fontWeight: 700, color: 'var(--primary)' }}>Quyết định thiết kế (Design Decision):</p>
            <ul style={{ paddingLeft: '16px', marginTop: '6px', color: 'var(--text-secondary)' }}>
              <li>Thanh phân quyền trực quan kết nối trực tiếp với DB qua REST API, tự động đồng bộ vai trò của các tài khoản qua Group chuẩn Django.</li>
              <li>Bộ chọn vai trò dạng Dropdown mượt mà giúp Admin điều hướng quyền hạn người dùng tức thì chỉ với một thao tác bấm.</li>
            </ul>
          </div>
          <div>
            <p style={{ fontWeight: 700, color: 'var(--secondary)' }}>Trải nghiệm người dùng (UX Notes):</p>
            <ul style={{ paddingLeft: '16px', marginTop: '6px', color: 'var(--text-secondary)' }}>
              <li>Xóa bỏ hoàn toàn trường email (gmail) khỏi hệ thống quản lý, thống nhất và tinh gọn dữ liệu đăng nhập bằng Số điện thoại/Tên đăng nhập theo thói quen người dùng.</li>
            </ul>
          </div>
        </div>
      </section>

    </div>
  );
}
