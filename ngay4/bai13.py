try:
    int("abc")
except ValueError as e:
    raise RuntimeError("Xử lý dữ liệu thất bại") from e