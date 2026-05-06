import tkinter as tk

# Command: pyinstaller --onefile --noconsole 05_gui_no_console.py
root = tk.Tk()
root.title("GUI App")
root.geometry("300x100")
tk.Label(root, text="No black terminal window here!").pack(pady=20)
root.mainloop()