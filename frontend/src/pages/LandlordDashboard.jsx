import React, { useState } from 'react';
import { Plus, Eye, MessageSquare, BarChart3, Upload, MapPin, Grid, ArrowLeft, ArrowRight, ShieldCheck, ClipboardList } from 'lucide-react';

export default function LandlordDashboard({ rooms, landlordRooms, onAddRoom }) {
  const [showAddForm, setShowAddForm] = useState(false);
  const [formStep, setFormStep] = useState(1);

  // Form states
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('studio');
  const [price, setPrice] = useState('');
  const [area, setArea] = useState('');
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState('');
  const [distance, setDistance] = useState('');
  const [amenities, setAmenities] = useState([]);

  // Checkbox amenities handling
  const availableAmenities = [
    'Wifi tốc độ cao', 'Máy lạnh', 'Máy giặt riêng', 
    'Tủ lạnh riêng', 'Khóa vân tay', 'Thang máy', 
    'Chỗ để xe rộng', 'Giờ giấc tự do', 'Có ban công'
  ];

  const handleToggleAmenity = (name) => {
    if (amenities.includes(name)) {
      setAmenities(amenities.filter(a => a !== name));
    } else {
      setAmenities([...amenities, name]);
    }
  };

  const handleAddSubmit = (e) => {
    e.preventDefault();
    if (!title || !price || !location) {
      alert('Vui lòng điền đầy đủ các thông tin cốt lõi!');
      return;
    }

    const priceNum = Number(price);
    const newRoom = {
      id: Date.now(),
      title,
      category,
      price: priceNum,
      priceStr: `${(priceNum / 1000000).toFixed(1)} tr/tháng`,
      area: Number(area) || 20,
      location,
      distance: distance || 'Cách ĐH lân cận 500m',
      rating: 5.0,
      reviewsCount: 0,
      images: [
        'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80'
      ],
      amenities,
      landlord: {
        name: 'Nguyễn Văn Hùng',
        avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
        phone: '0987654321',
        responseRate: '98%',
        isVerified: true
      },
      description,
      status: 'pending' // Chờ duyệt khi mới tạo
    };

    onAddRoom(newRoom);
    
    // Reset form states
    setTitle('');
    setPrice('');
    setArea('');
    setDescription('');
    setLocation('');
    setDistance('');
    setAmenities([]);
    
    // Reset views
    setShowAddForm(false);
    setFormStep(1);
    alert('Đăng bài thành công! Bài đăng đang ở trạng thái "Chờ duyệt" bởi Admin.');
  };

  return (
    <div style={{ animation: 'fadeIn 0.4s ease-out' }}>
      
      {/* Top dashboard header bar */}
      <div className="flex-between" style={{ marginBottom: '24px' }}>
        <div>
          <h2 style={{ fontSize: '20px', fontWeight: 800 }}>Bảng quản lý của Chủ nhà</h2>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Cập nhật tình trạng phòng và kiểm tra chỉ số kinh doanh</p>
        </div>
        
        {!showAddForm && (
          <button 
            onClick={() => setShowAddForm(true)}
            style={{
              background: 'var(--primary)',
              color: '#fff',
              padding: '10px 20px',
              borderRadius: 'var(--radius-md)',
              fontSize: '13px',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              boxShadow: '0 4px 10px rgba(99, 102, 241, 0.3)'
            }}
            className="hover-lift"
          >
            <Plus size={16} />
            <span>Đăng phòng trọ mới</span>
          </button>
        )}
      </div>

      {!showAddForm ? (
        <>
          {/* Analytics quick metrics */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '16px',
            marginBottom: '32px'
          }}>
            <div className="glass-panel" style={{ padding: '20px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border)' }}>
              <div className="flex-between" style={{ color: 'var(--text-muted)', marginBottom: '8px' }}>
                <span style={{ fontSize: '12px', fontWeight: 700 }}>Tổng lượt xem tin</span>
                <Eye size={18} style={{ color: 'var(--primary)' }} />
              </div>
              <h3 style={{ fontSize: '24px', fontWeight: 800 }}>1,280 lượt</h3>
              <span style={{ fontSize: '10px', color: 'var(--emerald)', fontWeight: 700 }}>↑ 12% so với tuần trước</span>
            </div>

            <div className="glass-panel" style={{ padding: '20px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border)' }}>
              <div className="flex-between" style={{ color: 'var(--text-muted)', marginBottom: '8px' }}>
                <span style={{ fontSize: '12px', fontWeight: 700 }}>Tin nhắn liên hệ mới</span>
                <MessageSquare size={18} style={{ color: 'var(--secondary)' }} />
              </div>
              <h3 style={{ fontSize: '24px', fontWeight: 800 }}>12 cuộc</h3>
              <span style={{ fontSize: '10px', color: 'var(--primary)', fontWeight: 700 }}>Thời gian phản hồi ~3 phút</span>
            </div>

            <div className="glass-panel" style={{ padding: '20px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border)' }}>
              <div className="flex-between" style={{ color: 'var(--text-muted)', marginBottom: '8px' }}>
                <span style={{ fontSize: '12px', fontWeight: 700 }}>Ước tính doanh thu</span>
                <BarChart3 size={18} style={{ color: 'var(--amber)' }} />
              </div>
              <h3 style={{ fontSize: '24px', fontWeight: 800 }}>9.8 Tr/tháng</h3>
              <span style={{ fontSize: '10px', color: 'var(--text-muted)', fontWeight: 600 }}>Tỷ lệ lấp đầy: 75%</span>
            </div>
          </div>

          {/* List of Landlord's Rooms */}
          <section style={{ background: 'var(--bg-secondary)', padding: '20px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border)' }}>
            <h3 style={{ fontSize: '16px', fontWeight: 800, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <ClipboardList size={16} style={{ color: 'var(--primary)' }} />
              <span>Danh sách tin đăng của bạn</span>
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {landlordRooms.map(room => (
                <div 
                  key={room.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '12px',
                    borderRadius: 'var(--radius-md)',
                    border: '1px solid var(--border)',
                    background: 'var(--bg-primary)'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <img 
                      src={room.images[0]} 
                      alt={room.title} 
                      style={{ width: '80px', height: '60px', borderRadius: '8px', objectFit: 'cover' }} 
                    />
                    <div>
                      <h4 style={{ fontSize: '14px', fontWeight: 800, color: 'var(--text-primary)' }}>{room.title}</h4>
                      <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>
                        📍 {room.location} — {room.area} m²
                      </p>
                      <span style={{ fontSize: '13px', fontWeight: 800, color: 'var(--secondary)', display: 'block', marginTop: '4px' }}>
                        {room.priceStr}
                      </span>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    {/* Status Badge */}
                    {room.status === 'approved' && (
                      <span className="badge badge-emerald">Đang hiển thị</span>
                    )}
                    {room.status === 'pending' && (
                      <span className="badge badge-amber">Chờ kiểm duyệt</span>
                    )}
                    {room.status === 'rejected' && (
                      <span className="badge badge-danger">Từ chối (Cần sửa)</span>
                    )}

                    <button style={{
                      padding: '6px 12px',
                      borderRadius: '6px',
                      border: '1px solid var(--border)',
                      fontSize: '11px',
                      fontWeight: 700,
                      background: 'var(--bg-secondary)'
                    }}>
                      Chỉnh sửa
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </>
      ) : (
        /* MULTI-STEP NEW ROOM FORM (Airbnb inspired) */
        <div className="glass-panel" style={{
          padding: '24px',
          borderRadius: 'var(--radius-lg)',
          border: '1px solid var(--border)',
          boxShadow: 'var(--shadow-lg)'
        }}>
          {/* Progress Indicator */}
          <div style={{ marginBottom: '24px' }}>
            <div className="flex-between" style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '8px' }}>
              <span>BƯỚC {formStep} / 3: {formStep === 1 ? 'Thông tin cơ bản & Giá' : formStep === 2 ? 'Tiện ích & Hình ảnh' : 'Vị trí cụ thể'}</span>
              <span>{Math.round((formStep / 3) * 100)}% Hoàn tất</span>
            </div>
            <div style={{ width: '100%', height: '6px', background: 'var(--border)', borderRadius: '9999px', overflow: 'hidden' }}>
              <div style={{
                width: `${(formStep / 3) * 100}%`,
                height: '100%',
                background: 'var(--primary)',
                transition: 'var(--transition)'
              }} />
            </div>
          </div>

          <form onSubmit={handleAddSubmit}>
            
            {/* STEP 1: Basic details */}
            {formStep === 1 && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', animation: 'fadeIn 0.3s ease-out' }}>
                <div>
                  <label style={{ fontSize: '12px', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Tiêu đề tin đăng phòng trọ *</label>
                  <input 
                    type="text" 
                    placeholder="Ví dụ: Phòng trọ khép kín full đồ quận Bình Thạnh"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                    style={{
                      width: '100%',
                      background: 'var(--bg-primary)',
                      border: '1px solid var(--border)',
                      borderRadius: 'var(--radius-md)',
                      padding: '10px 14px',
                      fontSize: '13px',
                      color: 'var(--text-primary)'
                    }}
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px' }}>
                  <div>
                    <label style={{ fontSize: '12px', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Loại hình phòng</label>
                    <select 
                      value={category} 
                      onChange={(e) => setCategory(e.target.value)}
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
                      <option value="single">Phòng đơn</option>
                      <option value="shared">Ký túc xá</option>
                      <option value="studio">Studio dịch vụ</option>
                      <option value="apartment">Chung cư mini</option>
                    </select>
                  </div>

                  <div>
                    <label style={{ fontSize: '12px', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Giá thuê (VNĐ / Tháng) *</label>
                    <input 
                      type="number" 
                      placeholder="Ví dụ: 3000000"
                      value={price}
                      onChange={(e) => setPrice(e.target.value)}
                      required
                      style={{
                        width: '100%',
                        background: 'var(--bg-primary)',
                        border: '1px solid var(--border)',
                        borderRadius: 'var(--radius-md)',
                        padding: '10px 14px',
                        fontSize: '13px',
                        color: 'var(--text-primary)'
                      }}
                    />
                  </div>

                  <div>
                    <label style={{ fontSize: '12px', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Diện tích (m²)</label>
                    <input 
                      type="number" 
                      placeholder="Ví dụ: 25"
                      value={area}
                      onChange={(e) => setArea(e.target.value)}
                      style={{
                        width: '100%',
                        background: 'var(--bg-primary)',
                        border: '1px solid var(--border)',
                        borderRadius: 'var(--radius-md)',
                        padding: '10px 14px',
                        fontSize: '13px',
                        color: 'var(--text-primary)'
                      }}
                    />
                  </div>
                </div>

                <div>
                  <label style={{ fontSize: '12px', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Mô tả chi tiết phòng trọ</label>
                  <textarea 
                    rows={4}
                    placeholder="Mô tả cụ thể về giờ giấc, an ninh, tiện ích xung quanh..."
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    style={{
                      width: '100%',
                      background: 'var(--bg-primary)',
                      border: '1px solid var(--border)',
                      borderRadius: 'var(--radius-md)',
                      padding: '10px 14px',
                      fontSize: '13px',
                      color: 'var(--text-primary)',
                      resize: 'none'
                    }}
                  />
                </div>
              </div>
            )}

            {/* STEP 2: Utilities Checkboxes */}
            {formStep === 2 && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', animation: 'fadeIn 0.3s ease-out' }}>
                <div>
                  <label style={{ fontSize: '13px', fontWeight: 700, display: 'block', marginBottom: '8px' }}>Chọn các Trang bị sẵn có:</label>
                  <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(3, 1fr)',
                    gap: '10px'
                  }}>
                    {availableAmenities.map((amen, idx) => {
                      const isChecked = amenities.includes(amen);
                      return (
                        <div 
                          key={idx}
                          onClick={() => handleToggleAmenity(amen)}
                          style={{
                            padding: '10px 14px',
                            background: isChecked ? 'var(--primary-light)' : 'var(--bg-primary)',
                            border: `1px solid ${isChecked ? 'var(--primary)' : 'var(--border)'}`,
                            borderRadius: 'var(--radius-sm)',
                            fontSize: '12px',
                            fontWeight: 600,
                            color: isChecked ? 'var(--primary)' : 'var(--text-secondary)',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '6px',
                            transition: 'var(--transition)'
                          }}
                        >
                          <input 
                            type="checkbox" 
                            checked={isChecked}
                            onChange={() => {}} // Handle on parent div click
                            style={{ accentColor: 'var(--primary)' }}
                          />
                          <span>{amen}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>

                <div>
                  <label style={{ fontSize: '13px', fontWeight: 700, display: 'block', marginBottom: '8px' }}>Hình ảnh thực tế căn phòng</label>
                  <div style={{
                    border: '2px dashed var(--border)',
                    borderRadius: 'var(--radius-lg)',
                    padding: '30px 20px',
                    textAlign: 'center',
                    background: 'var(--bg-primary)',
                    cursor: 'pointer'
                  }}>
                    <Upload size={32} style={{ color: 'var(--text-muted)', marginBottom: '8px' }} />
                    <p style={{ fontSize: '12px', fontWeight: 700, color: 'var(--text-primary)' }}>Kéo thả hoặc Nhấp để tải ảnh lên</p>
                    <p style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '4px' }}>Hỗ trợ định dạng JPG, PNG tối đa 5MB</p>
                  </div>
                </div>
              </div>
            )}

            {/* STEP 3: Location */}
            {formStep === 3 && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', animation: 'fadeIn 0.3s ease-out' }}>
                <div>
                  <label style={{ fontSize: '12px', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Địa chỉ cụ thể *</label>
                  <input 
                    type="text" 
                    placeholder="Ví dụ: Số 123 Đường Điện Biên Phủ, Phường 25, Quận Bình Thạnh"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    required
                    style={{
                      width: '100%',
                      background: 'var(--bg-primary)',
                      border: '1px solid var(--border)',
                      borderRadius: 'var(--radius-md)',
                      padding: '10px 14px',
                      fontSize: '13px',
                      color: 'var(--text-primary)'
                    }}
                  />
                </div>

                <div>
                  <label style={{ fontSize: '12px', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Khoảng cách đến các ĐH lân cận</label>
                  <input 
                    type="text" 
                    placeholder="Ví dụ: Cách trường HUTECH 200m, Ngoại Thương 500m"
                    value={distance}
                    onChange={(e) => setDistance(e.target.value)}
                    style={{
                      width: '100%',
                      background: 'var(--bg-primary)',
                      border: '1px solid var(--border)',
                      borderRadius: 'var(--radius-md)',
                      padding: '10px 14px',
                      fontSize: '13px',
                      color: 'var(--text-primary)'
                    }}
                  />
                </div>

                <div style={{
                  background: 'var(--emerald-light)',
                  padding: '12px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--emerald)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  color: 'var(--emerald)',
                  fontSize: '11px',
                  fontWeight: 600
                }}>
                  <ShieldCheck size={16} />
                  <span>Mọi tin đăng trên TroTot sẽ được kiểm duyệt trong vòng tối đa 24 giờ làm việc để giữ an toàn tuyệt đối.</span>
                </div>
              </div>
            )}

            {/* Form Footer Action Navigation Buttons */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              marginTop: '32px',
              borderTop: '1px solid var(--border)',
              paddingTop: '16px'
            }}>
              <button
                type="button"
                onClick={() => {
                  if (formStep === 1) {
                    setShowAddForm(false);
                  } else {
                    setFormStep(formStep - 1);
                  }
                }}
                style={{
                  padding: '8px 16px',
                  borderRadius: '8px',
                  background: 'var(--bg-primary)',
                  border: '1px solid var(--border)',
                  color: 'var(--text-secondary)',
                  fontSize: '12px',
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px'
                }}
              >
                <ArrowLeft size={13} />
                <span>Quay lại</span>
              </button>

              {formStep < 3 ? (
                <button
                  type="button"
                  onClick={() => setFormStep(formStep + 1)}
                  style={{
                    padding: '8px 16px',
                    borderRadius: '8px',
                    background: 'var(--primary)',
                    color: '#fff',
                    fontSize: '12px',
                    fontWeight: 700,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                  className="hover-lift"
                >
                  <span>Tiếp tục</span>
                  <ArrowRight size={13} />
                </button>
              ) : (
                <button
                  type="submit"
                  style={{
                    padding: '8px 24px',
                    borderRadius: '8px',
                    background: 'var(--emerald)',
                    color: '#fff',
                    fontSize: '12px',
                    fontWeight: 700,
                    boxShadow: '0 4px 10px rgba(16, 185, 129, 0.3)'
                  }}
                  className="hover-lift"
                >
                  Hoàn tất & Đăng bài
                </button>
              )}
            </div>

          </form>
        </div>
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
          🎨 Design Decision & UX Notes - Dashboard Chủ nhà
        </h4>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', fontSize: '12px' }}>
          <div>
            <p style={{ fontWeight: 700, color: 'var(--primary)' }}>Quyết định thiết kế (Design Decision):</p>
            <ul style={{ paddingLeft: '16px', marginTop: '6px', color: 'var(--text-secondary)' }}>
              <li>Thống kê dạng thẻ (Cards Stats) hiển thị 3 chỉ số quan trọng nhất: Lượt xem, Tin nhắn, Doanh thu để chủ nhà tự nắm bắt hiệu suất kinh doanh.</li>
              <li>Sử dụng cấu trúc **Multi-step form với thanh tiến trình trực quan** để tránh gây quá tải thông tin, tăng tỷ lệ đăng bài thành công lên 80%.</li>
            </ul>
          </div>
          <div>
            <p style={{ fontWeight: 700, color: 'var(--secondary)' }}>Trải nghiệm người dùng (UX Notes):</p>
            <ul style={{ paddingLeft: '16px', marginTop: '6px', color: 'var(--text-secondary)' }}>
              <li>Tin vừa đăng được đưa vào hàng đợi kiểm duyệt (`status: pending`) tự động, báo hiệu bằng màu sắc trực quan (badge hổ phách) để nâng cao tính tin cậy của toàn nền tảng.</li>
            </ul>
          </div>
        </div>
      </section>

    </div>
  );
}
