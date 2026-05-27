import React, { useState } from 'react';
import { Heart, Search, Map, List, Compass, Star, ChevronLeft, ChevronRight, SlidersHorizontal } from 'lucide-react';
import { mockCategories } from '../data/mockData';

export default function Home({ rooms, onSelectRoom, favorites, onToggleFavorite }) {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [maxPrice, setMaxPrice] = useState(5000000); // 5 triệu VNĐ
  const [showMap, setShowMap] = useState(false);
  const [showFilterDrawer, setShowFilterDrawer] = useState(false);

  // Lọc phòng trọ theo category, search, và giá
  const filteredRooms = rooms.filter(room => {
    const matchesCategory = selectedCategory === 'all' || room.category === selectedCategory;
    const matchesSearch = room.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          room.location.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesPrice = room.price <= maxPrice;
    const isApproved = room.status === 'approved'; // Chỉ hiển thị tin đã duyệt
    return matchesCategory && matchesSearch && matchesPrice && isApproved;
  });

  return (
    <div style={{ animation: 'fadeIn 0.5s ease-out' }}>
      
      {/* Hero Banner Section */}
      <section style={{
        background: 'linear-gradient(135deg, var(--primary) 0%, #818cf8 100%)',
        color: '#fff',
        borderRadius: 'var(--radius-lg)',
        padding: '40px 24px',
        textAlign: 'center',
        position: 'relative',
        overflow: 'hidden',
        marginBottom: '24px',
        boxShadow: 'var(--shadow-lg)'
      }}>
        {/* Decorative ambient bubbles */}
        <div style={{
          position: 'absolute',
          top: '-20px',
          right: '-20px',
          width: '120px',
          height: '120px',
          background: 'rgba(255,255,255,0.1)',
          borderRadius: '50%',
          filter: 'blur(10px)'
        }} />
        <div style={{
          position: 'absolute',
          bottom: '-30px',
          left: '-30px',
          width: '150px',
          height: '150px',
          background: 'rgba(255,255,255,0.1)',
          borderRadius: '50%',
          filter: 'blur(20px)'
        }} />

        <h1 style={{ fontSize: '28px', fontWeight: 800, marginBottom: '8px', color: '#fff', letterSpacing: '-0.5px' }}>
          Tìm phòng trọ hợp gu, sống trọn chất trẻ ⚡
        </h1>
        <p style={{ fontSize: '14px', color: 'rgba(255,255,255,0.85)', marginBottom: '24px', fontWeight: 500 }}>
          Hơn 1,000+ phòng trọ, KTX cao cấp đầy đủ tiện nghi quanh các trường Đại học lớn
        </p>

        {/* Hero Search Box */}
        <div className="glass-panel" style={{
          maxWidth: '600px',
          margin: '0 auto',
          padding: '6px',
          borderRadius: '9999px',
          display: 'flex',
          alignItems: 'center',
          boxShadow: '0 10px 25px -5px rgba(0,0,0,0.1)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', flex: 1, paddingLeft: '16px' }}>
            <Search size={18} style={{ color: 'var(--primary)', marginRight: '8px' }} />
            <input 
              type="text" 
              placeholder="Bạn muốn tìm quanh Đại học nào?" 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                border: 'none',
                background: 'transparent',
                fontSize: '14px',
                width: '100%',
                outline: 'none',
                color: 'var(--text-primary)'
              }}
            />
          </div>
          <button style={{
            background: 'var(--primary)',
            color: '#fff',
            padding: '10px 24px',
            borderRadius: '9999px',
            fontWeight: 700,
            fontSize: '13px',
            boxShadow: '0 4px 10px rgba(99, 102, 241, 0.3)'
          }} className="hover-lift">
            Tìm ngay
          </button>
        </div>
      </section>

      {/* Categories & Main Filters row */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', flexWrap: 'wrap', gap: '12px' }}>
        
        {/* Badges categories filter */}
        <div style={{
          display: 'flex',
          gap: '8px',
          overflowX: 'auto',
          paddingBottom: '4px',
          maxWidth: '100%',
          scrollSnapType: 'x mandatory'
        }}>
          {mockCategories.map(cat => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              style={{
                padding: '8px 16px',
                borderRadius: '9999px',
                fontSize: '13px',
                fontWeight: 700,
                whiteSpace: 'nowrap',
                transition: 'var(--transition)',
                background: selectedCategory === cat.id ? 'var(--primary)' : 'var(--bg-secondary)',
                color: selectedCategory === cat.id ? '#fff' : 'var(--text-secondary)',
                border: `1px solid ${selectedCategory === cat.id ? 'var(--primary)' : 'var(--border)'}`,
                boxShadow: selectedCategory === cat.id ? '0 4px 10px rgba(99, 102, 241, 0.15)' : 'none'
              }}
              className="hover-lift"
            >
              {cat.name}
            </button>
          ))}
        </div>

        {/* Filter Slider & Map buttons */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          
          {/* Price quick filter button */}
          <button 
            onClick={() => setShowFilterDrawer(!showFilterDrawer)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '8px 16px',
              borderRadius: '9999px',
              background: 'var(--bg-secondary)',
              border: '1px solid var(--border)',
              fontSize: '13px',
              fontWeight: 700,
              color: 'var(--text-secondary)'
            }}
            className="hover-lift"
          >
            <SlidersHorizontal size={14} />
            <span>Lọc Giá: ≤ {(maxPrice / 1000000).toFixed(1)}Tr</span>
          </button>

          {/* Toggle Map View button */}
          <button 
            onClick={() => setShowMap(!showMap)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '8px 16px',
              borderRadius: '9999px',
              background: 'var(--primary)',
              color: '#fff',
              fontSize: '13px',
              fontWeight: 700,
              boxShadow: '0 4px 10px rgba(99, 102, 241, 0.2)'
            }}
            className="hover-lift"
          >
            {showMap ? <List size={14} /> : <Map size={14} />}
            <span>{showMap ? 'Hiện Danh sách' : 'Xem Bản đồ'}</span>
          </button>
        </div>
      </div>

      {/* Floating filter drawer */}
      {showFilterDrawer && (
        <div className="glass-panel" style={{
          borderRadius: 'var(--radius-lg)',
          padding: '16px',
          marginBottom: '20px',
          boxShadow: 'var(--shadow-md)',
          animation: 'fadeIn 0.2s ease-out'
        }}>
          <div className="flex-between" style={{ marginBottom: '12px' }}>
            <span style={{ fontSize: '14px', fontWeight: 700 }}>Chọn khoảng giá tối đa:</span>
            <span style={{ fontSize: '14px', fontWeight: 800, color: 'var(--primary)' }}>
              {(maxPrice / 1000000).toFixed(1)} triệu VNĐ
            </span>
          </div>
          <input 
            type="range" 
            min="1000000" 
            max="10000000" 
            step="500000"
            value={maxPrice}
            onChange={(e) => setMaxPrice(Number(e.target.value))}
            style={{
              width: '100%',
              accentColor: 'var(--primary)',
              cursor: 'pointer',
              marginBottom: '10px'
            }}
          />
          <div className="flex-between" style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
            <span>1.0 triệu</span>
            <span>5.0 triệu</span>
            <span>10.0 triệu</span>
          </div>
        </div>
      )}

      {/* Split view content (List and Map) */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: showMap ? '1.2fr 1fr' : '1fr',
        gap: '24px',
        transition: 'var(--transition)'
      }}>
        
        {/* Grid List Rooms */}
        <div>
          {filteredRooms.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '60px 20px', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-lg)', border: '1px dashed var(--border)' }}>
              <Compass size={48} style={{ color: 'var(--text-muted)', marginBottom: '12px' }} />
              <h3 style={{ fontSize: '18px', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '4px' }}>Không tìm thấy phòng phù hợp</h3>
              <p style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Hãy thử điều chỉnh lại bộ lọc giá hoặc từ khóa tìm kiếm nhé.</p>
            </div>
          ) : (
            <div className="grid-responsive">
              {filteredRooms.map(room => {
                const isFav = favorites.includes(room.id);
                return (
                  <div 
                    key={room.id} 
                    className="hover-lift"
                    style={{
                      background: 'var(--bg-secondary)',
                      borderRadius: 'var(--radius-lg)',
                      overflow: 'hidden',
                      boxShadow: 'var(--shadow-md)',
                      border: '1px solid var(--border)',
                      position: 'relative',
                      display: 'flex',
                      flexDirection: 'column',
                      height: '100%'
                    }}
                  >
                    {/* Favorite Button */}
                    <button 
                      onClick={(e) => {
                        e.stopPropagation();
                        onToggleFavorite(room.id);
                      }}
                      style={{
                        position: 'absolute',
                        top: '12px',
                        right: '12px',
                        zIndex: 10,
                        background: 'rgba(255,255,255,0.85)',
                        border: 'none',
                        width: '32px',
                        height: '32px',
                        borderRadius: '50%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        cursor: 'pointer',
                        boxShadow: '0 4px 6px rgba(0,0,0,0.05)',
                        color: isFav ? 'var(--secondary)' : 'var(--text-secondary)',
                        transition: 'var(--transition-bounce)'
                      }}
                    >
                      <Heart size={16} fill={isFav ? 'var(--secondary)' : 'none'} style={{ transform: isFav ? 'scale(1.15)' : 'scale(1)' }} />
                    </button>

                    {/* Room Image */}
                    <div 
                      onClick={() => onSelectRoom(room)}
                      style={{ height: '180px', overflow: 'hidden', cursor: 'pointer', position: 'relative' }}
                    >
                      <img 
                        src={room.images[0]} 
                        alt={room.title} 
                        style={{ width: '100%', height: '100%', objectFit: 'cover', transition: 'transform 0.4s ease' }} 
                        className="room-img"
                      />
                      <span className="badge badge-primary" style={{
                        position: 'absolute',
                        bottom: '12px',
                        left: '12px',
                        background: 'rgba(99, 102, 241, 0.95)',
                        color: '#fff',
                        fontWeight: 700,
                        boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
                      }}>
                        {room.category === 'shared' ? 'KTX' : room.category === 'studio' ? 'Studio' : room.category === 'apartment' ? 'Chung cư' : 'Phòng trọ'}
                      </span>
                    </div>

                    {/* Room Details Info */}
                    <div 
                      onClick={() => onSelectRoom(room)}
                      style={{ padding: '16px', display: 'flex', flexDirection: 'column', flexGrow: 1, cursor: 'pointer' }}
                    >
                      {/* Dist and Rating */}
                      <div className="flex-between" style={{ marginBottom: '6px' }}>
                        <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--primary)' }}>
                          {room.distance}
                        </span>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '2px' }}>
                          <Star size={12} fill="var(--amber)" stroke="var(--amber)" />
                          <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--text-primary)' }}>{room.rating}</span>
                        </div>
                      </div>

                      {/* Title */}
                      <h4 style={{
                        fontSize: '14px',
                        fontWeight: 700,
                        color: 'var(--text-primary)',
                        marginBottom: '8px',
                        lineHeight: '1.4',
                        height: '40px',
                        overflow: 'hidden',
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical'
                      }}>
                        {room.title}
                      </h4>

                      {/* Location */}
                      <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '12px' }}>
                        {room.location}
                      </p>

                      {/* Divider */}
                      <div style={{ borderTop: '1px solid var(--border)', margin: 'auto 0 12px 0' }} />

                      {/* Price & Area */}
                      <div className="flex-between">
                        <span style={{ fontSize: '16px', fontWeight: 800, color: 'var(--secondary)' }}>
                          {room.priceStr}
                        </span>
                        <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>
                          Diện tích: {room.area} m²
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Map View Pane */}
        {showMap && (
          <div className="glass-panel fade-in" style={{
            borderRadius: 'var(--radius-lg)',
            overflow: 'hidden',
            border: '1px solid var(--border)',
            height: 'calc(100vh - 180px)',
            position: 'sticky',
            top: '80px',
            display: 'flex',
            flexDirection: 'column'
          }}>
            {/* Mock Map Header */}
            <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--border)', background: 'var(--bg-secondary)' }} className="flex-between">
              <span style={{ fontSize: '12px', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Map size={14} style={{ color: 'var(--primary)' }} />
                <span>Bản đồ vị trí phòng trọ</span>
              </span>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', background: 'var(--primary-light)', padding: '2px 8px', borderRadius: '4px', color: 'var(--primary)', fontWeight: 700 }}>
                {filteredRooms.length} Ghim phòng
              </span>
            </div>

            {/* Mock Map body representation with visual UI */}
            <div style={{
              flexGrow: 1,
              background: '#e0ece4',
              backgroundImage: 'radial-gradient(#ccdcd0 2px, transparent 2px)',
              backgroundSize: '24px 24px',
              position: 'relative',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              overflow: 'hidden'
            }}>
              
              {/* Central Map graphics simulation */}
              <div style={{
                position: 'absolute',
                top: 0, left: 0, right: 0, bottom: 0,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                {/* Mock roads */}
                <div style={{ position: 'absolute', width: '100%', height: '8px', background: '#fff', transform: 'rotate(15deg)' }} />
                <div style={{ position: 'absolute', width: '100%', height: '8px', background: '#fff', transform: 'rotate(-45deg)' }} />
                <div style={{ position: 'absolute', height: '100%', width: '8px', background: '#fff', left: '40%' }} />

                {/* Mock river */}
                <div style={{ position: 'absolute', width: '100%', height: '24px', background: '#bae6fd', bottom: '20%', transform: 'rotate(-5deg)' }} />
              </div>

              {/* Dynamic room markers */}
              {filteredRooms.map((room, index) => {
                // Generates random distributed mock positions based on ID
                const positions = [
                  { top: '30%', left: '25%' },
                  { top: '45%', left: '55%' },
                  { top: '20%', left: '70%' },
                  { top: '65%', left: '30%' },
                  { top: '75%', left: '60%' }
                ];
                const pos = positions[index % positions.length];

                return (
                  <button
                    key={room.id}
                    onClick={() => onSelectRoom(room)}
                    style={{
                      position: 'absolute',
                      top: pos.top,
                      left: pos.left,
                      background: 'var(--secondary)',
                      color: '#fff',
                      padding: '4px 10px',
                      borderRadius: '12px',
                      fontSize: '11px',
                      fontWeight: 800,
                      boxShadow: '0 4px 10px rgba(244, 63, 94, 0.4)',
                      border: '2px solid #fff',
                      cursor: 'pointer',
                      zIndex: 20,
                      transition: 'var(--transition)'
                    }}
                    className="hover-lift"
                  >
                    📌 {room.priceStr}
                  </button>
                );
              })}

              {/* Guide card on map bottom */}
              <div className="glass-panel" style={{
                position: 'absolute',
                bottom: '16px',
                left: '16px',
                right: '16px',
                padding: '12px',
                borderRadius: 'var(--radius-md)',
                boxShadow: 'var(--shadow-lg)'
              }}>
                <p style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-primary)' }}>
                  💡 Trải nghiệm bản đồ
                </p>
                <p style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>
                  Nhấp vào ghim để hiển thị nhanh chi tiết phòng trọ quanh vị trí của bạn.
                </p>
              </div>

            </div>
          </div>
        )}

      </div>
      
      {/* Visual Design Decisions & UX notes for user review */}
      <section style={{
        marginTop: '40px',
        padding: '20px',
        background: 'var(--bg-secondary)',
        borderRadius: 'var(--radius-lg)',
        border: '1px solid var(--border)'
      }}>
        <h4 style={{ fontSize: '15px', fontWeight: 800, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          🎨 Design Decision & UX Notes - Trang chủ
        </h4>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', fontSize: '12px' }}>
          <div>
            <p style={{ fontWeight: 700, color: 'var(--primary)' }}>Quyết định thiết kế (Design Decision):</p>
            <ul style={{ paddingLeft: '16px', marginTop: '6px', color: 'var(--text-secondary)' }}>
              <li>Ứng dụng bố cục **Split-screen Map** trực quan giúp tăng khả năng tương tác địa lý (như Airbnb).</li>
              <li>Thanh lọc danh mục (Category filter badges) dạng trượt ngang tối ưu không gian hiển thị trên mobile.</li>
            </ul>
          </div>
          <div>
            <p style={{ fontWeight: 700, color: 'var(--secondary)' }}>Trải nghiệm người dùng (UX Notes):</p>
            <ul style={{ paddingLeft: '16px', marginTop: '6px', color: 'var(--text-secondary)' }}>
              <li>Khoảng cách đến các trường ĐH được hiển thị nổi bật trên thẻ phòng vì đây là tiêu chí chọn phòng số 1 của sinh viên.</li>
              <li>Nút bộ lọc tối giản, kéo Slider chọn giá mượt mà giúp thu hẹp nhanh kết quả.</li>
            </ul>
          </div>
        </div>
      </section>

    </div>
  );
}
