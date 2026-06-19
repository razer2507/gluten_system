import tkinter as tk
from views.interface import App

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    root.title("Gluten - Sistema")
    app = App(root)
    root.mainloop()