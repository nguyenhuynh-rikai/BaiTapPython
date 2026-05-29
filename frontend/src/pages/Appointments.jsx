import React, { useState, useEffect } from 'react';
import { Calendar, Clock, User, Check, X, ArrowLeft, Building, MapPin, ClipboardList, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { api } from '../utils/api';

export default function Appointments({ onBackToRooms, currentRole }) {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchAppointments = async () => {
    try {
      setLoading(true);
      const data = await api.get('/appointments/');
      // Đảm bảo dữ liệu là mảng
      setAppointments(Array.isArray(data) ? data : []);
      setError('');
    } catch (err) {
      console.error('Lỗi tải danh sách lịch hẹn:', err);
      setError(err.message || 'Không thể tải danh sách lịch hẹn.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAppointments();
  }, []);

  const handleUpdateStatus = async (apptId, newStatus) => {
    const confirmMsg = newStatus === 'CONFIRMED' 
      ? 'Bạn có chắc chắn muốn xác nhận lịch hẹn này?' 
      : newStatus === 'CANCELLED' 
        ? 'Bạn có chắc chắn muốn hủy lịch hẹn này?' 
        : 'Xác nhận khách đã xem phòng xong?';
        
    if (!window.confirm(confirmMsg)) return;

    try {
      await api.patch(`/appointments/${apptId}/`, { status: newStatus });
      alert('Cập nhật trạng thái lịch hẹn thành công!');
      fetchAppointments();
    } catch (err) {
      alert(`Cập nhật thất bại: ${err.message}`);
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'PENDING':
        return <span className="badge badge-amber">Chờ xác nhận</span>;
      case 'CONFIRMED':
        return <span className="badge badge-emerald">Đã xác nhận</span>;
      case 'CANCELLED':
        return <span className="badge badge-danger">Đã hủy</span>;
      case 'COMPLETED':
        return <span className="badge" style={{ background: 'var(--border)', color: 'var(--text-secondary)', fontWeight: 700 }}>Đã xem phòng</span>;
      default:
        return <span className="badge">{status}</span>;
    }
  };

  const formatDateTime = (isoString) => {
    try {
      const date = new Date(isoString);
      const dateStr = date.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' });
      const timeStr = date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
      return `${timeStr} ngày ${dateStr}`;
    } catch (e) {
      return isoString;
    }
  };

  return (
    <div style={{ animation: 'fadeIn 0.4s ease-out' }}>
      
      {/* Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '12px 0',
        marginBottom: '24px',
        borderBottom: '1px solid var(--border)'
      }}>
        <button 
          onClick={onBackToRooms}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: '14px',
            fontWeight: 700,
            color: 'var(--text-secondary)',
            background: 'none',
            border: 'none',
            cursor: 'pointer'
          }}
          className="hover-lift"
        >
          <ArrowLeft size={18} />
          <span>Quay lại Trang chủ</span>
        </button>

        <h3 style={{ fontSize: '18px', fontWeight: 800, color: 'var(--text-primary)' }}>
          📅 Quản lý Lịch hẹn Xem phòng
        </h3>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px 0' }}>
          <p style={{ color: 'var(--text-muted)' }}>Đang tải danh sách lịch hẹn...</p>
        </div>
      ) : error ? (
        <div style={{ 
          background: 'var(--danger-light)', 
          color: 'var(--danger)', 
          padding: '16px', 
          borderRadius: 'var(--radius-md)', 
          border: '1px solid var(--danger)',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          marginBottom: '20px'
        }}>
          <ShieldAlert size={18} />
          <span>{error}</span>
        </div>
      ) : appointments.length === 0 ? (
        <div style={{ 
          textAlign: 'center', 
          padding: '80px 20px', 
          background: 'var(--bg-secondary)', 
          borderRadius: 'var(--radius-lg)', 
          border: '1px dashed var(--border)' 
        }}>
          <Calendar size={48} style={{ color: 'var(--text-muted)', marginBottom: '12px' }} />
          <h4 style={{ fontSize: '16px', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '6px' }}>
            Không có lịch hẹn nào
          </h4>
          <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
            {currentRole === 'landlord' 
              ? 'Hiện tại chưa có khách hàng nào đặt lịch xem phòng của bạn.' 
              : 'Bạn chưa đặt lịch hẹn xem phòng nào.'}
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {appointments.map((appt) => {
            const prop = appt.property_detail || {};
            const isUserLandlord = currentRole === 'landlord';
            const counterpartName = isUserLandlord ? appt.guest_username : appt.landlord_username;

            return (
              <div 
                key={appt.id}
                className="glass-panel hover-lift"
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  padding: '20px',
                  borderRadius: 'var(--radius-lg)',
                  border: '1px solid var(--border)',
                  background: 'var(--bg-secondary)',
                  boxShadow: 'var(--shadow-sm)'
                }}
              >
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  flexWrap: 'wrap', 
                  gap: '16px',
                  borderBottom: '1px solid var(--border)',
                  paddingBottom: '16px',
                  marginBottom: '16px'
                }}>
                  {/* Cột trái: Thông tin phòng trọ */}
                  <div style={{ display: 'flex', gap: '16px', flex: 1, minWidth: '280px' }}>
                    {prop.images && prop.images.length > 0 ? (
                      <img 
                        src={prop.images[0].image_url} 
                        alt={prop.title}
                        style={{ width: '100px', height: '75px', borderRadius: '8px', objectFit: 'cover', border: '1px solid var(--border)' }}
                      />
                    ) : (
                      <div style={{ width: '100px', height: '75px', borderRadius: '8px', background: 'var(--border)', display: 'flex', alignItems: 'center', justify: 'center' }}>
                        <Building size={24} style={{ color: 'var(--text-muted)' }} />
                      </div>
                    )}
                    
                    <div>
                      <h4 style={{ fontSize: '15px', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '4px' }}>
                        {prop.title || 'Phòng trọ'}
                      </h4>
                      <p style={{ fontSize: '12px', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '4px' }}>
                        <MapPin size={12} style={{ color: 'var(--primary)' }} />
                        <span>{prop.address || 'Địa chỉ'}</span>
                      </p>
                      <strong style={{ fontSize: '13px', color: 'var(--secondary)' }}>
                        {prop.price ? `${(prop.price / 1000000).toFixed(1)} tr/tháng` : 'Liên hệ'}
                      </strong>
                    </div>
                  </div>

                  {/* Cột phải: Trạng thái & Người liên hệ */}
                  <div style={{ textAlign: 'right', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', alignItems: 'flex-end', minWidth: '150px' }}>
                    <div>
                      {getStatusBadge(appt.status)}
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', color: 'var(--text-secondary)', marginTop: '8px' }}>
                      <User size={13} style={{ color: 'var(--text-muted)' }} />
                      <span>
                        {isUserLandlord ? `Khách đặt: ` : `Chủ trọ: `}
                        <strong>{counterpartName || 'Demo User'}</strong>
                      </span>
                    </div>
                  </div>
                </div>

                {/* Chi tiết lịch hẹn */}
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '24px', fontSize: '13px', background: 'var(--bg-primary)', padding: '12px 16px', borderRadius: '8px', border: '1px solid var(--border)', marginBottom: '16px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-primary)' }}>
                    <Calendar size={15} style={{ color: 'var(--primary)' }} />
                    <span>Hẹn lúc: <strong>{formatDateTime(appt.appointment_date)}</strong></span>
                  </div>
                  {appt.note && (
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '6px', color: 'var(--text-secondary)', flex: 1, minWidth: '200px' }}>
                      <ClipboardList size={15} style={{ color: 'var(--text-muted)', marginTop: '2px' }} />
                      <span>Ghi chú: <em>"{appt.note}"</em></span>
                    </div>
                  )}
                </div>

                {/* Nút hành động */}
                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
                  {appt.status === 'PENDING' && (
                    <>
                      {isUserLandlord ? (
                        <>
                          <button
                            onClick={() => handleUpdateStatus(appt.id, 'CONFIRMED')}
                            style={{
                              background: 'var(--emerald)',
                              color: '#fff',
                              border: 'none',
                              padding: '8px 16px',
                              borderRadius: '6px',
                              fontWeight: 700,
                              fontSize: '12px',
                              display: 'flex',
                              alignItems: 'center',
                              gap: '4px',
                              cursor: 'pointer'
                            }}
                            className="hover-lift"
                          >
                            <Check size={14} />
                            <span>Xác nhận lịch</span>
                          </button>
                          <button
                            onClick={() => handleUpdateStatus(appt.id, 'CANCELLED')}
                            style={{
                              background: 'var(--danger)',
                              color: '#fff',
                              border: 'none',
                              padding: '8px 16px',
                              borderRadius: '6px',
                              fontWeight: 700,
                              fontSize: '12px',
                              display: 'flex',
                              alignItems: 'center',
                              gap: '4px',
                              cursor: 'pointer'
                            }}
                            className="hover-lift"
                          >
                            <X size={14} />
                            <span>Từ chối</span>
                          </button>
                        </>
                      ) : (
                        <button
                          onClick={() => handleUpdateStatus(appt.id, 'CANCELLED')}
                          style={{
                            background: 'transparent',
                            color: 'var(--danger)',
                            border: '1px solid var(--danger)',
                            padding: '8px 16px',
                            borderRadius: '6px',
                            fontWeight: 700,
                            fontSize: '12px',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px',
                            cursor: 'pointer'
                          }}
                          className="hover-lift"
                        >
                          <X size={14} />
                          <span>Hủy lịch hẹn</span>
                        </button>
                      )}
                    </>
                  )}

                  {appt.status === 'CONFIRMED' && (
                    <>
                      {isUserLandlord ? (
                        <button
                          onClick={() => handleUpdateStatus(appt.id, 'COMPLETED')}
                          style={{
                            background: 'var(--primary)',
                            color: '#fff',
                            border: 'none',
                            padding: '8px 16px',
                            borderRadius: '6px',
                            fontWeight: 700,
                            fontSize: '12px',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px',
                            cursor: 'pointer'
                          }}
                          className="hover-lift"
                        >
                          <CheckCircle2 size={14} />
                          <span>Hoàn thành xem phòng</span>
                        </button>
                      ) : null}
                      <button
                        onClick={() => handleUpdateStatus(appt.id, 'CANCELLED')}
                        style={{
                          background: 'transparent',
                          color: 'var(--text-secondary)',
                          border: '1px solid var(--border)',
                          padding: '8px 16px',
                          borderRadius: '6px',
                          fontWeight: 700,
                          fontSize: '12px',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '4px',
                          cursor: 'pointer'
                        }}
                        className="hover-lift"
                      >
                        <X size={14} />
                        <span>Hủy lịch hẹn</span>
                      </button>
                    </>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

    </div>
  );
}
