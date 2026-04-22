try:
    print(10/0)
except Exception as e:
    print(e)
finally:
    print("The try...except block is finished")
