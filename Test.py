import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

def start_draw(event):
    canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill='white')

canvas.bind('<Button-1>', start_draw)

root.mainloop()
