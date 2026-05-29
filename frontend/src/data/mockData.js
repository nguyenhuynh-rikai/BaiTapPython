export const mockCategories = [
  { id: 'all', name: 'Tất cả', icon: 'Home' },
  { id: 'single', name: 'Phòng đơn', icon: 'User' },
  { id: 'shared', name: 'Ký túc xá', icon: 'Users' },
  { id: 'studio', name: 'Studio dịch vụ', icon: 'Sparkles' },
  { id: 'apartment', name: 'Chung cư mini', icon: 'Building' }
];

export const mockRooms = [
  {
    id: 1,
    title: 'Phòng trọ Studio Premium có ban công riêng',
    category: 'studio',
    price: 3800000,
    priceStr: '3.8 tr/tháng',
    area: 28,
    location: 'Quận 7, TP. Hồ Chí Minh',
    distance: 'Cách ĐH Tôn Đức Thắng 500m',
    rating: 4.8,
    reviewsCount: 24,
    images: [
      'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=800&q=80'
    ],
    amenities: ['Wifi tốc độ cao', 'Máy lạnh', 'Máy giặt chung', 'Tủ lạnh riêng', 'Khóa vân tay', 'Giờ giấc tự do', 'Có ban công'],
    landlord: {
      name: 'Nguyễn Văn Hùng',
      avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
      phone: '0987654321',
      responseRate: '98%',
      isVerified: true
    },
    description: 'Phòng trọ mới xây 100%, thiết kế phong cách Hàn Quốc tối giản và hiện đại. Phòng đầy đủ tiện nghi, chỉ cần xách vali vào ở. Khu vực an ninh có camera giám sát 24/7, khóa cửa vân tay thông minh ở cửa chính. Vị trí đắc địa gần siêu thị Lotte Mart, nhiều trường đại học lớn như UEF, TDTU, Nguyễn Tất Thành.',
    status: 'approved'
  },
  {
    id: 2,
    title: 'Ký túc xá cao cấp Homestay máy lạnh cực mát',
    category: 'shared',
    price: 1500000,
    priceStr: '1.5 tr/tháng',
    area: 35,
    location: 'Bình Thạnh, TP. Hồ Chí Minh',
    distance: 'Cách ĐH HUTECH 300m',
    rating: 4.9,
    reviewsCount: 42,
    images: [
      'https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1566665797739-1674de7a421a?auto=format&fit=crop&w=800&q=80'
    ],
    amenities: ['Wifi tốc độ cao', 'Máy lạnh', 'Máy giặt chung', 'Tủ lạnh riêng', 'Bảo vệ 24/7', 'Dọn phòng hàng tuần', 'Bếp chung'],
    landlord: {
      name: 'Trần Thị Mai',
      avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80',
      phone: '0912345678',
      responseRate: '95%',
      isVerified: true
    },
    description: 'Mô hình ký túc xá giường tầng cao cấp phong cách homestay. Phù hợp cho các bạn sinh viên muốn tiết kiệm chi phí nhưng vẫn được hưởng trọn tiện ích cao cấp. Phòng trang bị giường tầng gỗ chắc chắn, có rèm che riêng tư, tủ đồ cá nhân khóa riêng. Có cô lao công dọn dẹp vệ sinh phòng 3 lần/tuần.',
    status: 'approved'
  },
  {
    id: 3,
    title: 'Chung cư mini 1 phòng ngủ tách biệt, đủ đồ',
    category: 'apartment',
    price: 4500000,
    priceStr: '4.5 tr/tháng',
    area: 32,
    location: 'Cầu Giấy, Hà Nội',
    distance: 'Cách ĐH Quốc Gia HN 600m',
    rating: 4.7,
    reviewsCount: 15,
    images: [
      'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80'
    ],
    amenities: ['Wifi tốc độ cao', 'Máy lạnh', 'Máy giặt riêng', 'Tủ lạnh riêng', 'Khóa vân tay', 'Thang máy', 'Chỗ để xe rộng'],
    landlord: {
      name: 'Lê Hoàng Nam',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80',
      phone: '0966778899',
      responseRate: '90%',
      isVerified: false
    },
    description: 'Chung cư mini cao cấp có thang máy thẻ từ, bảo vệ trông xe dưới hầm. Phòng ngủ được ngăn cách riêng với bếp bằng vách kính chống mùi. Ban công phơi đồ ngập tràn ánh sáng tự nhiên. Rất phù hợp cho các cặp đôi trẻ hoặc người đi làm mong muốn không gian sống tiện nghi yên tĩnh.',
    status: 'approved'
  },
  {
    id: 4,
    title: 'Phòng trọ giá rẻ cho sinh viên tự quản lối đi riêng',
    category: 'single',
    price: 2200000,
    priceStr: '2.2 tr/tháng',
    area: 18,
    location: 'Quận 9, TP. Thủ Đức',
    distance: 'Cách Đại học FPT 1km',
    rating: 4.5,
    reviewsCount: 8,
    images: [
      'https://images.unsplash.com/photo-1484101403633-562f891dc89a?auto=format&fit=crop&w=800&q=80',
      'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80'
    ],
    amenities: ['Wifi tốc độ cao', 'Quạt trần', 'Nhà vệ sinh riêng', 'Chỗ phơi đồ', 'Lối đi riêng', 'Giờ giấc tự do'],
    landlord: {
      name: 'Phạm Minh Đức',
      avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80',
      phone: '0933445566',
      responseRate: '85%',
      isVerified: true
    },
    description: 'Phòng trọ độc lập có lối đi riêng không chung chủ. Phòng có gác lửng đúc sạch sẽ làm chỗ ngủ thoải mái, bên dưới làm khu sinh hoạt và bếp ăn. Giá điện nước tính theo giá nhà nước rất tiết kiệm cho các bạn sinh viên học tập lâu dài.',
    status: 'pending'
  }
];

export const mockChats = [
  {
    id: 1,
    landlord: {
      name: 'Nguyễn Văn Hùng',
      avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80',
      isOnline: true
    },
    room: {
      title: 'Phòng trọ Studio Premium có ban công riêng',
      price: '3.8 tr/tháng'
    },
    messages: [
      { id: 1, sender: 'landlord', text: 'Chào bạn, mình là chủ phòng trọ Studio Quận 7 đây.', time: '20:15' },
      { id: 2, sender: 'tenant', text: 'Dạ anh Hùng ơi, phòng này còn trống không anh? Em muốn qua xem phòng vào chiều mai ạ.', time: '20:17' },
      { id: 3, sender: 'landlord', text: 'Phòng vẫn còn trống em nhé. Chiều mai tầm 5h em qua xem được không? Có gì alo anh số 0987654321 nhé.', time: '20:18' }
    ]
  },
  {
    id: 2,
    landlord: {
      name: 'Trần Thị Mai',
      avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80',
      isOnline: false
    },
    room: {
      title: 'Ký túc xá cao cấp Homestay máy lạnh cực mát',
      price: '1.5 tr/tháng'
    },
    messages: [
      { id: 1, sender: 'tenant', text: 'Chào chị Mai, cho em hỏi ký túc xá bên mình tiền điện nước tính thế nào ạ?', time: 'Hôm qua' },
      { id: 2, sender: 'landlord', text: 'Chào em, tiền điện nước bên KTX trọn gói trong tiền phòng luôn rồi em nhé, không phát sinh thêm chi phí nào nữa.', time: 'Hôm qua' }
    ]
  }
];
