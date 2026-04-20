def loc_tu(s):
    kqua = []
    for i in s:
        if i % 2 == 0:
            kqua.append(i)
    return kqua

def nhap_so():
    s = input("Nhap day so: ")
    return [int(x) for x in s.split()]

print("Day so sau khi loc: ", loc_tu(nhap_so()))


        