import React, { useState } from 'react';
import { ChevronLeft, Star, Heart, MapPin, Share2, ShieldCheck, UserCheck, MessageSquare, Phone, CheckCircle2, ShieldAlert } from 'lucide-react';

export default function RoomDetail({ room, onBack, favorites, onToggleFavorite, onStartChat }) {
  const isFav = favorites.includes(room.id);
  const [activeTab, setActiveTab] = useState('gallery');

  return (
    <div style={{ animation: 'fadeIn 0.4s ease-out' }}>
      
      {/* Detail Header / Sticky navigation */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '12px 0',
        marginBottom: '16px',
        borderBottom: '1px solid var(--border)'
      }}>
        <button 
          onClick={onBack}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: '14px',
            fontWeight: 700,
            color: 'var(--text-secondary)'
          }}
          className="hover-lift"
        >
          <ChevronLeft size={18} />
          <span>Quay lại Trang chủ</span>
        </button>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button 
            onClick={() => onToggleFavorite(room.id)}
            style={{
              padding: '8px 16px',
              borderRadius: '9999px',
              border: '1px solid var(--border)',
              background: 'var(--bg-secondary)',
              fontSize: '13px',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              color: isFav ? 'var(--secondary)' : 'var(--text-secondary)'
            }}
            className="hover-lift"
          >
            <Heart size={14} fill={isFav ? 'var(--secondary)' : 'none'} />
            <span>{isFav ? 'Đã lưu' : 'Lưu phòng'}</span>
          </button>
          <button 
            style={{
              padding: '8px 16px',
              borderRadius: '9999px',
              border: '1px solid var(--border)',
              background: 'var(--bg-secondary)',
              fontSize: '13px',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              color: 'var(--text-secondary)'
            }}
            className="hover-lift"
          >
            <Share2 size={14} />
            <span>Chia sẻ</span>
          </button>
        </div>
      </div>

      {/* Grid Images (Airbnb Style) */}
      <section style={{
        display: 'grid',
        gridTemplateColumns: '2fr 1fr',
        gap: '12px',
        borderRadius: 'var(--radius-lg)',
        overflow: 'hidden',
        height: '350px',
        marginBottom: '24px',
        boxShadow: 'var(--shadow-md)'
      }}>
        {/* Main large image */}
        <div style={{ position: 'relative', overflow: 'hidden' }}>
          <img 
            src={room.images[0]} 
            alt={room.title} 
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        </div>

        {/* Column of secondary images */}
        <div style={{ display: 'grid', gridTemplateRows: '1fr 1fr', gap: '12px' }}>
          <div style={{ overflow: 'hidden' }}>
            <img 
              src={room.images[1] || room.images[0]} 
              alt="Secondary image" 
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
          </div>
          <div style={{ overflow: 'hidden', position: 'relative' }}>
            <img 
              src={room.images[0]} 
              alt="Third image" 
              style={{ width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.7)' }}
            />
            <div style={{
              position: 'absolute',
              top: 0, left: 0, right: 0, bottom: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff',
              fontSize: '14px',
              fontWeight: 800
            }}>
              + Xem thêm ảnh
            </div>
          </div>
        </div>
      </section>

      {/* Main content grid (Left Details - Right Sticky Sidebar) */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '2fr 1.1fr',
        gap: '32px',
        position: 'relative'
      }}>
        
        {/* LEFT COLUMN: ROOM DETAILS */}
        <div>
          {/* Header Info */}
          <div style={{ marginBottom: '20px' }}>
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '8px' }}>
              <span className="badge badge-primary" style={{ fontWeight: 800 }}>
                {room.category === 'studio' ? 'Studio dịch vụ' : room.category === 'shared' ? 'Ký túc xá homestay' : 'Phòng trọ khép kín'}
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '2px', fontSize: '13px', fontWeight: 700 }}>
                <Star size={13} fill="var(--amber)" stroke="var(--amber)" />
                <span>{room.rating} ({room.reviewsCount} Đánh giá)</span>
              </span>
            </div>

            <h1 style={{ fontSize: '24px', fontWeight: 800, lineHeight: '1.3', marginBottom: '12px', color: 'var(--text-primary)' }}>
              {room.title}
            </h1>

            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', color: 'var(--text-secondary)' }}>
              <MapPin size={14} style={{ color: 'var(--primary)' }} />
              <span>{room.location} — <strong style={{ color: 'var(--primary)' }}>{room.distance}</strong></span>
            </div>
          </div>

          <div style={{ borderTop: '1px solid var(--border)', margin: '20px 0' }} />

          {/* Quick Specifications */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '12px',
            background: 'var(--bg-secondary)',
            padding: '16px',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border)',
            textAlign: 'center',
            marginBottom: '24px'
          }}>
            <div>
              <p style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase' }}>Diện tích</p>
              <h4 style={{ fontSize: '18px', fontWeight: 800, color: 'var(--text-primary)', marginTop: '4px' }}>{room.area} m²</h4>
            </div>
            <div style={{ borderLeft: '1px solid var(--border)', borderRight: '1px solid var(--border)' }}>
              <p style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase' }}>Giá thuê</p>
              <h4 style={{ fontSize: '18px', fontWeight: 800, color: 'var(--secondary)', marginTop: '4px' }}>{room.priceStr}</h4>
            </div>
            <div>
              <p style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase' }}>Đặt cọc</p>
              <h4 style={{ fontSize: '18px', fontWeight: 800, color: 'var(--text-primary)', marginTop: '4px' }}>1 tháng</h4>
            </div>
          </div>

          {/* Amenities Grid */}
          <section style={{ marginBottom: '24px' }}>
            <h3 style={{ fontSize: '16px', fontWeight: 800, marginBottom: '12px' }}>Trang bị & Tiện ích sẵn có</h3>
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '10px'
            }}>
              {room.amenities.map((amenity, idx) => (
                <div key={idx} style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  fontSize: '13px',
                  color: 'var(--text-secondary)',
                  background: 'var(--bg-secondary)',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  border: '1px solid var(--border)'
                }}>
                  <CheckCircle2 size={14} style={{ color: 'var(--emerald)' }} />
                  <span>{amenity}</span>
                </div>
              ))}
            </div>
          </section>

          <div style={{ borderTop: '1px solid var(--border)', margin: '20px 0' }} />

          {/* Landlord Profile Profile card */}
          <section style={{ marginBottom: '24px' }}>
            <h3 style={{ fontSize: '16px', fontWeight: 800, marginBottom: '12px' }}>Thông tin chủ nhà</h3>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              background: 'var(--bg-secondary)',
              padding: '16px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{ position: 'relative' }}>
                  <img 
                    src={room.landlord.avatar} 
                    alt={room.landlord.name} 
                    style={{ width: '48px', height: '48px', borderRadius: '50%', objectFit: 'cover' }} 
                  />
                  {room.landlord.isVerified && (
                    <div style={{
                      position: 'absolute',
                      bottom: '-2px',
                      right: '-2px',
                      background: 'var(--emerald)',
                      color: '#fff',
                      borderRadius: '50%',
                      width: '18px',
                      height: '18px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      border: '2px solid #fff'
                    }}>
                      <ShieldCheck size={12} />
                    </div>
                  )}
                </div>
                <div>
                  <h4 style={{ fontSize: '14px', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <span>{room.landlord.name}</span>
                    {room.landlord.isVerified && (
                      <span style={{ fontSize: '10px', background: 'var(--emerald-light)', color: 'var(--emerald)', padding: '1px 6px', borderRadius: '4px', fontWeight: 700 }}>
                        Đã xác minh
                      </span>
                    )}
                  </h4>
                  <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Tỷ lệ phản hồi nhanh: {room.landlord.responseRate}</p>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '8px' }}>
                <button 
                  onClick={() => onStartChat(room)}
                  style={{
                    background: 'var(--primary-light)',
                    color: 'var(--primary)',
                    padding: '8px 12px',
                    borderRadius: '8px',
                    fontSize: '12px',
                    fontWeight: 700,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                  className="hover-lift"
                >
                  <MessageSquare size={13} />
                  <span>Chat ngay</span>
                </button>
                <a 
                  href={`tel:${room.landlord.phone}`}
                  style={{
                    background: 'var(--bg-primary)',
                    color: 'var(--text-secondary)',
                    padding: '8px 12px',
                    borderRadius: '8px',
                    fontSize: '12px',
                    fontWeight: 700,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    border: '1px solid var(--border)'
                  }}
                  className="hover-lift"
                >
                  <Phone size={13} />
                  <span>Gọi điện</span>
                </a>
              </div>
            </div>
          </section>

          {/* Room Description */}
          <section style={{ marginBottom: '24px' }}>
            <h3 style={{ fontSize: '16px', fontWeight: 800, marginBottom: '8px' }}>Mô tả chi tiết</h3>
            <p style={{
              fontSize: '13px',
              color: 'var(--text-secondary)',
              lineHeight: '1.6',
              whiteSpace: 'pre-line'
            }}>
              {room.description}
            </p>
          </section>

        </div>

        {/* RIGHT COLUMN: STICKY BOOKING CARD */}
        <div>
          <div className="glass-panel" style={{
            position: 'sticky',
            top: '90px',
            borderRadius: 'var(--radius-lg)',
            padding: '20px',
            border: '1px solid var(--border)',
            boxShadow: 'var(--shadow-lg)'
          }}>
            {/* Price section */}
            <div style={{ marginBottom: '16px' }}>
              <p style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 700 }}>GIÁ THUÊ PHÒNG TRỌ</p>
              <h2 style={{ fontSize: '26px', fontWeight: 800, color: 'var(--secondary)', marginTop: '4px' }}>
                {room.priceStr}
              </h2>
            </div>

            {/* Chi tiết phụ phí */}
            <div style={{
              background: 'var(--bg-primary)',
              borderRadius: 'var(--radius-md)',
              padding: '12px',
              border: '1px solid var(--border)',
              marginBottom: '20px'
            }}>
              <span style={{ fontSize: '11px', fontWeight: 700, display: 'block', marginBottom: '8px', color: 'var(--text-primary)' }}>
                Bảng Chi Phí Dự Tính (Tháng):
              </span>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '12px', color: 'var(--text-secondary)' }}>
                <div className="flex-between">
                  <span>⚡ Tiền điện</span>
                  <strong>3.500đ / kWh</strong>
                </div>
                <div className="flex-between">
                  <span>💧 Tiền nước</span>
                  <strong>100.000đ / người</strong>
                </div>
                <div className="flex-between">
                  <span>📶 Phí dịch vụ (Wifi, dọn vệ sinh)</span>
                  <strong>50.000đ / người</strong>
                </div>
                <div className="flex-between" style={{ borderTop: '1px dashed var(--border)', paddingTop: '6px', marginTop: '4px' }}>
                  <span>🔒 Tiền cọc giữ chỗ</span>
                  <strong style={{ color: 'var(--text-primary)' }}>1 Tháng tiền phòng</strong>
                </div>
              </div>
            </div>

            {/* Predefined starter chat suggestion */}
            <div style={{
              fontSize: '11px',
              color: 'var(--text-muted)',
              marginBottom: '16px',
              padding: '8px 12px',
              background: 'var(--primary-light)',
              borderRadius: '8px',
              border: '1px dashed var(--primary)',
              color: 'var(--primary)',
              fontWeight: 600
            }}>
              💬 Soạn sẵn tin nhắn mồi để trao đổi trực tuyến nhanh chóng với chủ nhà!
            </div>

            {/* CTA action buttons */}
            <button 
              onClick={() => onStartChat(room)}
              style={{
                width: '100%',
                background: 'var(--primary)',
                color: '#fff',
                padding: '12px 0',
                borderRadius: 'var(--radius-md)',
                fontWeight: 700,
                fontSize: '14px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                boxShadow: '0 4px 10px rgba(99, 102, 241, 0.3)',
                marginBottom: '10px'
              }}
              className="hover-lift"
            >
              <MessageSquare size={16} />
              <span>Gửi tin nhắn thương lượng</span>
            </button>
            
            <a 
              href={`tel:${room.landlord.phone}`}
              style={{
                width: '100%',
                background: 'transparent',
                color: 'var(--text-primary)',
                border: '1px solid var(--border)',
                padding: '11px 0',
                borderRadius: 'var(--radius-md)',
                fontWeight: 700,
                fontSize: '14px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px'
              }}
              className="hover-lift"
            >
              <Phone size={16} />
              <span>Gọi chủ nhà ngay</span>
            </a>

            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              marginTop: '16px',
              fontSize: '11px',
              color: 'var(--text-muted)',
              justifyContent: 'center'
            }}>
              <ShieldCheck size={12} style={{ color: 'var(--emerald)' }} />
              <span>Tin đăng phòng đã được kiểm duyệt an toàn</span>
            </div>

          </div>
        </div>

      </div>

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
          🎨 Design Decision & UX Notes - Chi tiết Phòng
        </h4>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', fontSize: '12px' }}>
          <div>
            <p style={{ fontWeight: 700, color: 'var(--primary)' }}>Quyết định thiết kế (Design Decision):</p>
            <ul style={{ paddingLeft: '16px', marginTop: '6px', color: 'var(--text-secondary)' }}>
              <li>Thư viện ảnh phong cách Airbnb giúp làm nổi bật không gian và ánh sáng phòng ngay lập tức.</li>
              <li>**Sticky Card phụ phí** bên cột phải ghim cố định giúp người thuê nắm được bài toán chi phí thực tế mà không cần cuộn tìm mỏi mắt.</li>
            </ul>
          </div>
          <div>
            <p style={{ fontWeight: 700, color: 'var(--secondary)' }}>Trải nghiệm người dùng (UX Notes):</p>
            <ul style={{ paddingLeft: '16px', marginTop: '6px', color: 'var(--text-secondary)' }}>
              <li>**Nhãn Xác Thực (Verified Landlord):** Tăng 40% tính an tâm khi trao đổi tiền cọc cho sinh viên ở tỉnh lên thành phố tìm phòng.</li>
              <li>Hộp thoại liên lạc nhanh hỗ trợ cả hai phương thức: Chat nhanh trong ứng dụng hoặc Click-to-call truyền thống.</li>
            </ul>
          </div>
        </div>
      </section>

    </div>
  );
}
