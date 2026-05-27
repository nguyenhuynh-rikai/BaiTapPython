import React, { useState } from 'react';
import Navbar from './components/Navbar';
import BottomBar from './components/BottomBar';
import Home from './pages/Home';
import RoomDetail from './pages/RoomDetail';
import Chat from './pages/Chat';
import LandlordDashboard from './pages/LandlordDashboard';
import AdminDashboard from './pages/AdminDashboard';
import Auth from './pages/Auth';

import { mockRooms } from './data/mockData';

function App() {
  // Application routing & role state
  const [currentPage, setCurrentPage] = useState('home');
  const [currentRole, setCurrentRole] = useState('tenant'); // 'tenant' | 'landlord' | 'admin'
  const [selectedRoom, setSelectedRoom] = useState(null);
  
  // App shared data state
  const [rooms, setRooms] = useState(mockRooms);
  const [favorites, setFavorites] = useState([1, 3]); // Mock initial saved rooms
  const [activeChatId, setActiveChatId] = useState(null);
  
  // Authenticated user state
  const [user, setUser] = useState({
    name: 'Khánh Linh (Gen Z)',
    avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80',
    role: 'tenant'
  });

  // Toggle favorite room
  const handleToggleFavorite = (roomId) => {
    if (favorites.includes(roomId)) {
      setFavorites(favorites.filter(id => id !== roomId));
    } else {
      setFavorites([...favorites, roomId]);
    }
  };

  // Switch role callback
  const handleChangeRole = (role) => {
    setCurrentRole(role);
    // Redirect to corresponding dashboards to show flow
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
    setRooms([newRoom, ...rooms]);
  };

  // Approve listing from Admin
  const handleApproveRoom = (roomId) => {
    setRooms(rooms.map(room => {
      if (room.id === roomId) {
        return { ...room, status: 'approved' };
      }
      return room;
    }));
  };

  // Reject listing from Admin
  const handleRejectRoom = (roomId, reason) => {
    setRooms(rooms.map(room => {
      if (room.id === roomId) {
        return { ...room, status: 'rejected', rejectionReason: reason };
      }
      return room;
    }));
  };

  // Start chat with Landlord from detail page
  const handleStartChat = (room) => {
    // Find if chat exists or navigate to chat with parameters
    setActiveChatId(1); // Demo chat session 1
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
        onNavigate={(page) => {
          setCurrentPage(page);
          setSelectedRoom(null);
        }}
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

        {currentPage === 'auth' && (
          <Auth onLoginSuccess={handleLoginSuccess} />
        )}

      </main>

      {/* Bottom Navigation for Mobile views */}
      <BottomBar 
        currentPage={currentPage} 
        onNavigate={(page) => {
          setCurrentPage(page);
          setSelectedRoom(null);
        }}
        currentRole={currentRole}
        favoritesCount={favorites.length}
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
