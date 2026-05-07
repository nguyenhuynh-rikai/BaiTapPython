def website_info(request):
    # Trả về một dictionary chứa dữ liệu dùng chung
    return {
        'site_name': 'My Awesome Blog',
        'contact_email': 'admin@example.com',
        'current_year': 2026,
    }