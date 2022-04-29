from board import Board
import tkinter as tk
import time
import threading

canvases = []
radius = 24
window = None
waiting_time = 0.1

def visualize_init(b: Board):
    global window
    n = 8

    window = tk.Tk()
    bgcolor = "#aaffaa"
    window.configure(background=bgcolor)

    for i in range(n):
        window.columnconfigure(i, weight=1)
        window.rowconfigure(i, weight=1)
        canvases.append([])
        for j in range(n):
            frame = tk.Frame(
                master=window,
                borderwidth=1,
                background=bgcolor,
            )
            frame.grid(row=i, column=j)
            canvas = tk.Canvas(master=frame, width=radius * 2.2, height=radius * 2.2, background=bgcolor)
            canvases[i].append(canvas)
            fill = b.get_color(i, j)
            if fill:
                canvas.create_oval(radius * 0.2, radius * 0.2, radius * 2.2, radius * 2.2, fill=fill, outline="black")
            canvas.pack(padx=radius * 0.1, pady=radius * 0.1)

    window.update()
    time.sleep(waiting_time)

def visualize(b: Board):
    for i in range(b.get_n()):
        for j in range(b.get_n()):
            fill = b.get_color(i, j)
            if fill:
                canvases[i][j].create_oval(radius * 0.2, radius * 0.2, radius * 2.2, radius * 2.2, fill=fill, outline="black")
    window.update()
    time.sleep(waiting_time)
