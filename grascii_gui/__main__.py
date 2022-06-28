import tkinter as tk

from grascii_gui.app import Application


def main():
    root = tk.Tk()
    root.title("Grascii Search")
    app = Application(root)
    app.mainloop()


if __name__ == "__main__":
    main()
