import tkinter as tk

def say_hello():
    label.config(text="Hello Nguyên 👋")

root = tk.Tk()
root.title("My App")

label = tk.Label(root, text="Click button")
label.pack()

btn = tk.Button(root, text="Click me", command=say_hello)
btn.pack()

root.mainloop()