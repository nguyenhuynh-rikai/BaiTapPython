import React, { useState } from 'react';
import { Send, MapPin, Check, CheckCheck, Smile, HelpCircle, PhoneCall, Calendar } from 'lucide-react';
import { mockChats } from '../data/mockData';

export default function Chat({ activeChatId, onBackToRooms, initialChats = mockChats }) {
  const [chats, setChats] = useState(initialChats);
  const [selectedChatId, setSelectedChatId] = useState(activeChatId || chats[0].id);
  const [inputText, setInputText] = useState('');

  const activeChat = chats.find(c => c.id === selectedChatId) || chats[0];

  // Các tin nhắn gợi ý phản hồi nhanh (Quick Replies)
  const quickReplies = [
    { text: 'Phòng này còn trống không ạ? 🏠', type: 'info' },
    { text: 'Chi phí điện nước dịch vụ tính thế nào anh/chị? ⚡', type: 'cost' },
    { text: 'Em muốn hẹn lịch xem phòng chiều mai được không ạ? 🗓️', type: 'schedule' },
    { text: 'Phòng có chỗ để xe máy an toàn không ạ? 🛵', type: 'parking' }
  ];

  // Hàm gửi tin nhắn
  const handleSendMessage = (textToSend) => {
    if (!textToSend.trim()) return;

    const newMessage = {
      id: Date.now(),
      sender: 'tenant',
      text: textToSend,
      time: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
    };

    // Cập nhật mảng chat
    const updatedChats = chats.map(chat => {
      if (chat.id === selectedChatId) {
        return {
          ...chat,
          messages: [...chat.messages, newMessage]
        };
      }
      return chat;
    });

    setChats(updatedChats);
    setInputText('');

    // Giả lập bot phản hồi tự động của chủ nhà sau 1.5 giây để cuộc chat sống động
    setTimeout(() => {
      const landlordResponse = {
        id: Date.now() + 1,
        sender: 'landlord',
        text: 'Chào em, tin nhắn của em đã được gửi đến anh/chị. Anh/chị sẽ liên hệ lại ngay nhé! Cảm ơn em.',
        time: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
      };

      setChats(prevChats => prevChats.map(chat => {
        if (chat.id === selectedChatId) {
          return {
            ...chat,
            messages: [...chat.messages, landlordResponse]
          };
        }
        return chat;
      }));
    }, 1500);
  };

  return (
    <div style={{
      animation: 'fadeIn 0.4s ease-out',
      display: 'grid',
      gridTemplateColumns: '320px 1fr',
      gap: '20px',
      height: 'calc(100vh - 120px)',
      background: 'var(--bg-secondary)',
      borderRadius: 'var(--radius-lg)',
      overflow: 'hidden',
      border: '1px solid var(--border)',
      boxShadow: 'var(--shadow-lg)'
    }}>
      
      {/* LEFT COLUMN: LIST OF CHATS */}
      <div style={{ borderRight: '1px solid var(--border)', display: 'flex', flexDirection: 'column', background: 'var(--bg-primary)' }}>
        {/* Chat List Header */}
        <div style={{ padding: '16px', borderBottom: '1px solid var(--border)', background: 'var(--bg-secondary)' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 800 }}>Hộp thư tin nhắn</h3>
          <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>Liên hệ trực tiếp với chủ phòng</p>
        </div>

        {/* Chat List container */}
        <div style={{ flexGrow: 1, overflowY: 'auto', padding: '8px' }}>
          {chats.map(chat => {
            const lastMsg = chat.messages[chat.messages.length - 1];
            const isSelected = chat.id === selectedChatId;
            return (
              <div
                key={chat.id}
                onClick={() => setSelectedChatId(chat.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  padding: '12px',
                  borderRadius: 'var(--radius-md)',
                  marginBottom: '6px',
                  cursor: 'pointer',
                  transition: 'var(--transition)',
                  background: isSelected ? 'var(--primary-light)' : 'transparent',
                  border: isSelected ? '1px solid rgba(99, 102, 241, 0.15)' : '1px solid transparent'
                }}
                className="hover-lift"
              >
                <div style={{ position: 'relative' }}>
                  <img 
                    src={chat.landlord.avatar} 
                    alt={chat.landlord.name} 
                    style={{ width: '40px', height: '40px', borderRadius: '50%', objectFit: 'cover' }} 
                  />
                  {chat.landlord.isOnline && (
                    <span style={{
                      position: 'absolute',
                      bottom: '0',
                      right: '0',
                      width: '10px',
                      height: '10px',
                      background: 'var(--emerald)',
                      borderRadius: '50%',
                      border: '2px solid #fff'
                    }} />
                  )}
                </div>

                <div style={{ flexGrow: 1, overflow: 'hidden' }}>
                  <div className="flex-between">
                    <span style={{ fontSize: '13px', fontWeight: 800, color: isSelected ? 'var(--primary)' : 'var(--text-primary)' }}>
                      {chat.landlord.name}
                    </span>
                    <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>
                      {lastMsg ? lastMsg.time : ''}
                    </span>
                  </div>
                  <p style={{
                    fontSize: '11px',
                    color: isSelected ? 'var(--text-secondary)' : 'var(--text-muted)',
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    marginTop: '2px'
                  }}>
                    {lastMsg ? (lastMsg.sender === 'tenant' ? 'Bạn: ' : '') + lastMsg.text : 'Bắt đầu cuộc chat'}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* RIGHT COLUMN: ACTIVE CHAT PANEL */}
      <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
        
        {/* Active Chat Header */}
        <div style={{
          padding: '12px 20px',
          borderBottom: '1px solid var(--border)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'var(--bg-secondary)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <img 
              src={activeChat.landlord.avatar} 
              alt={activeChat.landlord.name} 
              style={{ width: '36px', height: '36px', borderRadius: '50%', objectFit: 'cover' }} 
            />
            <div>
              <h4 style={{ fontSize: '13px', fontWeight: 800 }}>{activeChat.landlord.name}</h4>
              <p style={{ fontSize: '10px', color: activeChat.landlord.isOnline ? 'var(--emerald)' : 'var(--text-muted)', fontWeight: 600 }}>
                {activeChat.landlord.isOnline ? '● Đang trực tuyến' : 'Ngoại tuyến'}
              </p>
            </div>
          </div>
        </div>

        {/* Pinned Mini Room Card (Amazing UX!) */}
        <div style={{
          padding: '8px 16px',
          background: 'var(--primary-light)',
          borderBottom: '1px solid var(--border)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          fontSize: '12px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', overflow: 'hidden' }}>
            <span style={{ fontSize: '14px' }}>🏡</span>
            <span style={{ fontWeight: 700, color: 'var(--primary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '350px' }}>
              Đang thương lượng: {activeChat.room.title}
            </span>
          </div>
          <span style={{ fontWeight: 800, color: 'var(--secondary)' }}>{activeChat.room.price}</span>
        </div>

        {/* Chat Message Window Area */}
        <div style={{ flexGrow: 1, overflowY: 'auto', padding: '20px', display: 'flex', flexDirection: 'column', gap: '12px', background: 'var(--bg-primary)' }}>
          {activeChat.messages.map(msg => {
            const isMe = msg.sender === 'tenant';
            return (
              <div 
                key={msg.id}
                style={{
                  display: 'flex',
                  justifyContent: isMe ? 'flex-end' : 'flex-start',
                  animation: 'fadeIn 0.3s ease-out'
                }}
              >
                <div style={{ maxWidth: '60%' }}>
                  <div style={{
                    background: isMe ? 'var(--primary)' : 'var(--bg-secondary)',
                    color: isMe ? '#fff' : 'var(--text-primary)',
                    padding: '10px 16px',
                    borderRadius: isMe ? '16px 16px 2px 16px' : '16px 16px 16px 2px',
                    boxShadow: 'var(--shadow-sm)',
                    border: isMe ? 'none' : '1px solid var(--border)',
                    fontSize: '13px',
                    lineHeight: '1.45'
                  }}>
                    {msg.text}
                  </div>
                  
                  {/* Status Indicator */}
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    justifyContent: isMe ? 'flex-end' : 'flex-start',
                    fontSize: '10px',
                    color: 'var(--text-muted)',
                    marginTop: '4px',
                    padding: '0 4px'
                  }}>
                    <span>{msg.time}</span>
                    {isMe && <CheckCheck size={11} style={{ color: 'var(--primary)' }} />}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Quick Suggestion replies row */}
        <div style={{
          padding: '8px 16px',
          background: 'var(--bg-secondary)',
          borderTop: '1px solid var(--border)',
          display: 'flex',
          gap: '8px',
          overflowX: 'auto',
          alignItems: 'center'
        }}>
          <span style={{ fontSize: '10px', fontWeight: 800, color: 'var(--primary)', whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Smile size={12} />
            <span>Gợi ý:</span>
          </span>
          {quickReplies.map((reply, idx) => (
            <button
              key={idx}
              onClick={() => handleSendMessage(reply.text)}
              style={{
                padding: '6px 12px',
                background: 'var(--bg-primary)',
                border: '1px solid var(--border)',
                borderRadius: '9999px',
                fontSize: '11px',
                color: 'var(--text-secondary)',
                fontWeight: 600,
                whiteSpace: 'nowrap',
                transition: 'var(--transition)'
              }}
              className="hover-lift"
            >
              {reply.text}
            </button>
          ))}
        </div>

        {/* Input Message panel */}
        <div style={{ padding: '12px 16px', borderTop: '1px solid var(--border)', background: 'var(--bg-secondary)' }} className="flex-between">
          <input
            type="text"
            placeholder="Nhập tin nhắn trao đổi với chủ nhà..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSendMessage(inputText);
            }}
            style={{
              flexGrow: 1,
              background: 'var(--bg-primary)',
              border: '1px solid var(--border)',
              borderRadius: '9999px',
              padding: '10px 20px',
              fontSize: '13px',
              color: 'var(--text-primary)',
              marginRight: '12px',
              outline: 'none'
            }}
          />
          <button
            onClick={() => handleSendMessage(inputText)}
            style={{
              background: 'var(--primary)',
              color: '#fff',
              width: '38px',
              height: '38px',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 4px 10px rgba(99, 102, 241, 0.2)'
            }}
            className="hover-lift"
          >
            <Send size={16} />
          </button>
        </div>

      </div>

    </div>
  );
}
