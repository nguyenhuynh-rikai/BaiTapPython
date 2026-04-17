def loai_tu(s):
    kqua = []
    for i in s:
        if i not in kqua:
            kqua.append(i)
    return kqua

def nhap_so():
    s = input("Nhap day so: ")
    return [int(x) for x in s.split()]

print("Day so sau khi loai: ", loai_tu(nhap_so()))

    