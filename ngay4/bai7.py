# LBYL
data = {"":20}
if "name" not in data:
    raise ValueError("kh co ten")

# EAFP
try:
    print(data["name"])
except KeyError:
    print("lỗi")