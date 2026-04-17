from posixpath import split
def binh_Phuong(s):
    k_qua = []
    for i in s:
        k_qua.append(i*i)
    return k_qua

def nhap_so():
    s = input("Nhap day so nguyen: ")
    return [int(x) for x in s.split()]

print("Day so sau khi binh phuong: ", binh_Phuong(nhap_so()))