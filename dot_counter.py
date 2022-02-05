from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import colorchooser
import pdf_manager as pdf

def create_frame():
    global dot_list
    if dot_list:
        dot_list.destroy()
    dot_list = tk.LabelFrame(root, text="Menu")
    dot_list.grid(row=0, column=1)
    curr_color = tk.Label(dot_list, text='#', bg=color, fg=color).grid(row=0, column=0)
    first_label = tk.Label(dot_list, text="<- Current Color").grid(row=0, column=1)
    button = Button(dot_list, text = "Select color",
                   command = choose_color)            
    button.grid(row=1, column=1)
    fButton = Button(dot_list, text='Open', command=pdf.load_pdf)
    fButton.grid(row=2, column=1)
    return dot_list

def create_circle(x, y, r, canvasName): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill=color, outline=color)

def choose_color():
    global color
    # variable to store hexadecimal code of color
    color_code = colorchooser.askcolor(title ="Choose color")
    print(color_code[1])
    color = color_code[1]

def draw_circle(event):
    if color in colors_count:
        colors_count[color] += 1
    else:
        colors_count[color] = 1
    print(colors_count)
    create_circle(event.x,event.y,10,w)
    generate_list()

def generate_list():
    dot_list = create_frame()
    r = 2
    for item in colors_count:
        label = tk.Label(dot_list, text='#', bg=item, fg=item).grid(row=r, column=0)
        first_label = tk.Label(dot_list, text=colors_count[item]).grid(row=r, column=1)
        r+=1

root = Tk()
file = pdf.load_pdf()
color = '#000000'
colors_count = {}
dot_list = tk.LabelFrame(root, text="Menu")
pdf_img = pdf.convert_pdf_to_tk(file)
#setting up a tkinter canvas
w = Canvas(root, width=750, height=1000)
w.grid(row=0,column=0)
w.create_image(20,20, anchor='nw', image=pdf_img)
create_frame()
w.bind("<Button 1>",draw_circle)
root.mainloop()