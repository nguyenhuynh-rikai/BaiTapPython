def menu():
    print("1. Say Hello")
    print("2. Exit")

    choice = input("Chọn: ")

    if choice == "1":
        print("Hello!")
    elif choice == "2":
        print("Bye!")
    else:
        print("Lựa chọn không hợp lệ")

menu()