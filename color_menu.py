import tkinter as tk
from tkinter import colorchooser


class color_menu:
    def __init__(self):
        self.colors = [
            '#00FFFF', #BLUE
            '#8A2BE2', #PURPLE
            '#DC143C', #RED
            '#FFD700', #YELLOW
            '#FF69B4', #PINK
            '#FF4500', #ORANGE
            '#DDA0DD', #PLUM
            '#00FF7F', #GREEN
            '#800000', #MAROON
            '#BDB76B', #KHAKI
        ]
        self.open = True
        self.chosen = '#00FFFF'
    
    def swap_color(self, idx, frame):
        color_code = colorchooser.askcolor(title="Choose color")
        self.colors[idx] = color_code[1]
        c = tk.Label(frame, text='#', bg=self.colors[idx],
                fg=self.colors[idx]).grid(row=idx+1, column=0)
        b = tk.Button(frame, text='Select Color', command=lambda col = self.colors[idx]: self.select_color(col))
        b.grid(row=idx+1, column=1)

    def add_color(self, frame):
        color_code = colorchooser.askcolor(title="Choose color")
        self.colors.append(color_code[1])
        idx = len(self.colors)-1
        c = tk.Label(frame, text='#', bg=self.colors[idx],
                fg=self.colors[idx]).grid(row=idx+1, column=0)
        b = tk.Button(frame, text='Select Color', command=lambda col = self.colors[idx]: self.select_color(col))
        b.grid(row=idx+1, column=1)
        d = tk.Button(frame, text='Replace Color', command=lambda i = idx: self.swap_color(i,frame))
        d.grid(row=idx+1, column=2)

    def select_color(self, color):
        self.chosen = color

    def return_color(self, w):
        self.open = False
        w.destroy()
        return self.chosen
    
    def cancel(self, w):
        self.open = False
        w.destroy()
    
    def generate_window(self, root):

        root.title("Choose Color")
        root.geometry("350x350")

        color_frame = tk.LabelFrame(root, text="Colors")
        r = 1
        color_frame.grid(row = 0, column = 0)
        for i in range(len(self.colors)):
            
            c = tk.Label(color_frame, text='#', bg=self.colors[i],
                fg=self.colors[i]).grid(row=r, column=0)
            b = tk.Button(color_frame, text='Select Color', command=lambda col = self.colors[i]: self.select_color(col))
            b.grid(row=r, column=1)
            d = tk.Button(color_frame, text='Replace Color', command=lambda idx = i: self.swap_color(idx,color_frame))
            d.grid(row=r, column=2)
            r+=1
        spacer = tk.Label(color_frame, text="")
        spacer.grid(row=1, column=4)
        save = tk.Button(color_frame, text='Save', command=lambda: self.return_color(root))
        save.grid(row=1, column=5)
        close = tk.Button(color_frame, text='Cancel', command=lambda: self.cancel(root))
        close.grid(row=1, column = 6)
        add = tk.Button(color_frame, text='Add Color', command=lambda: self.add_color(color_frame))
        add.grid(row=1, column= 7)
        root.wait_window(root)