import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import BottomBar from './components/BottomBar';
import Home from './pages/Home';
import RoomDetail from './pages/RoomDetail';
import Chat from './pages/Chat';
import LandlordDashboard from './pages/LandlordDashboard';
import AdminDashboard from './pages/AdminDashboard';
import Auth from './pages/Auth';
import Appointments from './pages/Appointments';
import { api } from './utils/api';

const ROOM_IMAGES = [
  'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1493809842364-78817add7ffb?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1502672023488-70e25813eb80?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1554995207-c18c203602cb?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1536376072261-38c75010e6c9?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?auto=format&fit=crop&w=800&q=80'
];

// Helper làm sạch và định dạng vị trí, loại bỏ hoàn toàn các chuỗi "nan" rác từ CSV
const cleanLocation = (room) => {
  const cleanStr = (val) => {
    if (!val) return '';
    const s = String(val).trim();
    if (s.toLowerCase() === 'nan' || s.toLowerCase() === 'none' || s.toLowerCase() === 'null') return '';
    return s;
  };

  const address = cleanStr(room.address);
  const ward = cleanStr(room.ward_name);
  const district = cleanStr(room.district_name);

  if (address) return address;
  
  const parts = [ward, district].filter(Boolean);
  if (parts.length > 0) return parts.join(', ');
  
  return 'Quận Cầu Giấy, Hà Nội'; // Fallback mặc định đẹp đẽ thay vì NaN
};

// Adapter mapper chuyển đổi cấu trúc API Django sang cấu trúc UI React
const mapBackendRoomToFrontend = (room) => {
  let imageUrls = [];
  if (room.images && room.images.length > 0) {
    imageUrls = room.images.map(img => img.image_url);
  }
  
  if (imageUrls.length === 0) {
    // Gán 2 ảnh minh họa khác nhau ngẫu nhiên nhưng nhất quán dựa theo ID phòng
    const idx1 = room.id % ROOM_IMAGES.length;
    const idx2 = (room.id + 1) % ROOM_IMAGES.length;
    imageUrls = [ROOM_IMAGES[idx1], ROOM_IMAGES[idx2]];
  }

  let catSlug = 'single';
  if (room.category_name) {
    const name = room.category_name.toLowerCase();
    if (name.includes('ktx') || name.includes('ký túc xá') || name.includes('shared')) {
      catSlug = 'shared';
    } else if (name.includes('studio')) {
      catSlug = 'studio';
    } else if (name.includes('chung cư') || name.includes('apartment')) {
      catSlug = 'apartment';
    }
  }

  // Bảo vệ giá thuê khỏi lỗi NaN
  const rawPrice = Number(room.price);
  const priceNum = !isNaN(rawPrice) && rawPrice > 0 ? rawPrice : 3000000; // Mặc định 3 triệu nếu lỗi
  const priceStr = priceNum >= 1000000 
    ? `${(priceNum / 1000000).toFixed(1)} tr/tháng`
    : `${priceNum.toLocaleString()} đ/tháng`;

  // Bảo vệ diện tích khỏi lỗi NaN
  const rawArea = Number(room.area);
  const areaNum = !isNaN(rawArea) && rawArea > 0 ? rawArea : 25; // Mặc định 25m2 nếu lỗi

  return {
    id: room.id,
    title: room.title,
    category: catSlug,
    price: priceNum,
    priceStr: priceStr,
    area: areaNum,
    location: cleanLocation(room),
    distance: room.posted_at_text || 'Cách trường ĐH lân cận ~500m',
    rating: 4.8,
    reviewsCount: 12,
    images: imageUrls,
    amenities: room.amenities_detail && room.amenities_detail.length > 0
      ? room.amenities_detail.map(a => a.name)
      : ['Wifi tốc độ cao', 'Chỗ để xe rộng', 'Giờ giấc tự do'],
    landlord: {
      name: 'Nguyễn Văn Hùng',
      avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
      phone: '0987654321',
      responseRate: '98%',
      isVerified: true
    },
    description: room.description || 'Chưa có mô tả chi tiết.',
    status: room.status || (room.is_active ? 'approved' : 'pending')
  };
};

function App() {
  const storedUser = localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null;

  // Application routing & role state
  const [currentPage, setCurrentPage] = useState('home');
  const [currentRole, setCurrentRole] = useState(storedUser ? storedUser.role : 'tenant'); // 'tenant' | 'landlord' | 'admin'
  const [selectedRoom, setSelectedRoom] = useState(null);
  
  // App shared data state
  const [rooms, setRooms] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [activeChatId, setActiveChatId] = useState(null);
  const [chats, setChats] = useState([]);
  
  // Authenticated user state
  const [user, setUser] = useState(storedUser ? {
    name: storedUser.username,
    avatar: storedUser.role === 'landlord' 
      ? 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80' 
      : 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80',
    role: storedUser.role
  } : null);

  // Sync chats with user-scoped localStorage
  useEffect(() => {
    if (user) {
      const stored = localStorage.getItem(`chats_${user.name}`);
      setChats(stored ? JSON.parse(stored) : []);
    } else {
      setChats([]);
    }
  }, [user]);

  const saveChats = (newChats) => {
    setChats(newChats);
    if (user) {
      localStorage.setItem(`chats_${user.name}`, JSON.stringify(newChats));
    }
  };

  // Centralized router with Auth Guard
  const handleNavigate = (page) => {
    if (page === 'chat' && !user) {
      alert('Vui lòng đăng ký hoặc đăng nhập để sử dụng tính năng nhắn tin!');
      setCurrentPage('auth');
      return;
    }
    setCurrentPage(page);
    setSelectedRoom(null);
  };

  // Gọi API lấy danh sách phòng trọ từ database Postgres
  const fetchRooms = async () => {
    try {
      const data = await api.get('/properties/');
      const formatted = data.map(mapBackendRoomToFrontend);
      setRooms(formatted);
    } catch (err) {
      console.error('Lỗi tải danh sách phòng:', err);
    }
  };

  // Gọi API lấy danh sách yêu thích
  const fetchFavorites = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;
      const data = await api.get('/favorites/');
      const favIds = data.map(f => f.property);
      setFavorites(favIds);
    } catch (err) {
      console.error('Lỗi tải danh sách yêu thích:', err);
    }
  };

  useEffect(() => {
    fetchRooms();
    fetchFavorites();
  }, [user]);

  // Toggle favorite room qua API thật
  const handleToggleFavorite = async (roomId) => {
    const token = localStorage.getItem('token');
    if (!token) {
      alert('Vui lòng đăng nhập để lưu phòng trọ yêu thích!');
      setCurrentPage('auth');
      return;
    }

    try {
      await api.post(`/properties/${roomId}/favorite/`);
      if (favorites.includes(roomId)) {
        setFavorites(favorites.filter(id => id !== roomId));
      } else {
        setFavorites([...favorites, roomId]);
      }
    } catch (err) {
      alert(`Lỗi: ${err.message}`);
    }
  };

  // Switch role callback
  const handleChangeRole = (role) => {
    setCurrentRole(role);
    if (role === 'landlord') {
      setCurrentPage('landlord');
    } else if (role === 'admin') {
      setCurrentPage('admin');
    } else {
      setCurrentPage('home');
    }
  };

  // Add listing from Landlord
  const handleAddRoom = (newRoom) => {
    fetchRooms(); // Tải lại danh sách từ DB
  };

  // Approve listing from Admin
  const handleApproveRoom = async (roomId) => {
    try {
      await api.patch(`/properties/${roomId}/`, { is_active: true, status: 'approved' });
      fetchRooms();
      alert('Đã duyệt tin đăng thành công!');
    } catch (err) {
      alert(`Lỗi duyệt bài: ${err.message}`);
    }
  };

  // Reject listing from Admin
  const handleRejectRoom = async (roomId, reason) => {
    try {
      await api.patch(`/properties/${roomId}/`, { is_active: false, status: 'rejected' });
      fetchRooms();
      alert(`Đã từ chối bài đăng với lý do: ${reason}`);
    } catch (err) {
      alert(`Lỗi: ${err.message}`);
    }
  };

  // Start chat with Landlord from detail page
  const handleStartChat = (room) => {
    if (!user) {
      alert('Vui lòng đăng ký hoặc đăng nhập để sử dụng tính năng nhắn tin!');
      setCurrentPage('auth');
      return;
    }

    const existingChat = chats.find(c => c.room.id === room.id);
    let targetChatId;

    if (existingChat) {
      targetChatId = existingChat.id;
    } else {
      const newChat = {
        id: Date.now(),
        landlord: {
          name: room.landlord?.name || 'Nguyễn Văn Hùng',
          avatar: room.landlord?.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
          isOnline: true
        },
        room: {
          id: room.id,
          title: room.title,
          price: room.priceStr
        },
        messages: [
          {
            id: 1,
            sender: 'landlord',
            text: `Chào bạn, mình là chủ phòng '${room.title}'. Bạn cần hỏi thêm thông tin gì cứ nhắn mình nhé!`,
            time: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
          }
        ]
      };
      const updatedChats = [newChat, ...chats];
      saveChats(updatedChats);
      targetChatId = newChat.id;
    }

    setActiveChatId(targetChatId);
    setCurrentPage('chat');
  };

  // Handle successful login
  const handleLoginSuccess = (loggedUser, selectedRole) => {
    setUser(loggedUser);
    setCurrentRole(selectedRole);
    if (selectedRole === 'landlord') {
      setCurrentPage('landlord');
    } else if (selectedRole === 'admin') {
      setCurrentPage('admin');
    } else {
      setCurrentPage('home');
    }
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setCurrentRole('tenant');
    setCurrentPage('home');
    alert('Đã đăng xuất tài khoản.');
  };

  // Filter approved rooms for Guest/Tenant view
  const approvedRooms = rooms.filter(r => r.status === 'approved');
  // Landlord owns room ID 1, 2 and any newly created room
  const landlordRooms = rooms.filter(r => r.id === 1 || r.id === 2 || r.id > 4);

  return (
    <div className="app-container" style={{ paddingBottom: '90px' }}>
      
      {/* Top Header Navbar */}
      <Navbar 
        currentRole={currentRole} 
        onChangeRole={handleChangeRole} 
        onNavigate={handleNavigate}
        currentPage={currentPage}
        user={user}
        onLogout={handleLogout}
      />

      {/* Main Dynamic View Page Container */}
      <main style={{ flexGrow: 1, minHeight: 'calc(100vh - 200px)' }}>
        
        {currentPage === 'home' && !selectedRoom && (
          <Home 
            rooms={rooms} 
            onSelectRoom={(room) => {
              setSelectedRoom(room);
              setCurrentPage('detail');
            }}
            favorites={favorites}
            onToggleFavorite={handleToggleFavorite}
          />
        )}

        {currentPage === 'detail' && selectedRoom && (
          <RoomDetail 
            room={selectedRoom}
            onBack={() => {
              setSelectedRoom(null);
              setCurrentPage('home');
            }}
            favorites={favorites}
            onToggleFavorite={handleToggleFavorite}
            onStartChat={handleStartChat}
            onNavigate={handleNavigate}
          />
        )}

        {currentPage === 'favorites' && (
          <div style={{ animation: 'fadeIn 0.4s ease-out' }}>
            <h2 style={{ fontSize: '20px', fontWeight: 800, marginBottom: '20px' }}>
              ❤️ Phòng trọ yêu thích của bạn ({favorites.length})
            </h2>
            {favorites.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '60px 20px', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-lg)', border: '1px dashed var(--border)' }}>
                <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>Bạn chưa lưu phòng trọ nào.</p>
                <button 
                  onClick={() => setCurrentPage('home')}
                  style={{
                    marginTop: '12px',
                    background: 'var(--primary)',
                    color: '#fff',
                    padding: '8px 20px',
                    borderRadius: '9999px',
                    fontWeight: 700,
                    fontSize: '13px'
                  }}
                >
                  Khám phá phòng ngay
                </button>
              </div>
            ) : (
              <Home 
                rooms={rooms.filter(r => favorites.includes(r.id))} 
                onSelectRoom={(room) => {
                  setSelectedRoom(room);
                  setCurrentPage('detail');
                }}
                favorites={favorites}
                onToggleFavorite={handleToggleFavorite}
              />
            )}
          </div>
        )}

        {currentPage === 'chat' && (
          <Chat 
            activeChatId={activeChatId} 
            onBackToRooms={() => setCurrentPage('home')} 
            chats={chats}
            onUpdateChats={saveChats}
          />
        )}

        {currentPage === 'landlord' && (
          <LandlordDashboard 
            rooms={rooms}
            landlordRooms={landlordRooms}
            onAddRoom={handleAddRoom}
          />
        )}

        {currentPage === 'admin' && (
          <AdminDashboard 
            rooms={rooms}
            onApproveRoom={handleApproveRoom}
            onRejectRoom={handleRejectRoom}
          />
        )}

        {currentPage === 'appointments' && (
          <Appointments 
            onBackToRooms={() => setCurrentPage('home')} 
            currentRole={currentRole}
          />
        )}

        {currentPage === 'auth' && (
          <Auth onLoginSuccess={handleLoginSuccess} />
        )}

      </main>

      {/* Bottom Navigation for Mobile views */}
      <BottomBar 
        currentPage={currentPage} 
        onNavigate={handleNavigate}
        currentRole={currentRole}
        favoritesCount={favorites.length}
        user={user}
      />

      {/* Footer view */}
      <footer style={{
        marginTop: '60px',
        padding: '24px 0',
        borderTop: '1px solid var(--border)',
        textAlign: 'center',
        fontSize: '12px',
        color: 'var(--text-muted)'
      }}>
        <p>© 2026 TroTot RentHub. Được thiết kế với đam mê cho sinh viên Việt Nam 🇻🇳</p>
        <p style={{ marginTop: '4px', fontSize: '10px' }}>
          Phong cách Tối giản • Tương tác Real-time • Tối ưu di động
        </p>
      </footer>

    </div>
  );
}

export default App;
