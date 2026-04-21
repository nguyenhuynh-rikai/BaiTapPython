f = None
try:
    f = open("ngay4/testbai4.txt", "r")
    content = f.read()
    print(content)
except FileNotFoundError:
    print("File not found")
finally:
    if f:
        f.close()
        print("File closed")