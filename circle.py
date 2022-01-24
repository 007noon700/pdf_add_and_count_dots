from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import colorchooser

root = Tk()

#setting up a tkinter canvas
w = Canvas(root, width=750, height=750)

w.grid(row=0,column=0)
color = '#000000'
colors_count = {}

#adding the image
# File = askopenfilename(parent=root, initialdir="./",title='Select an image')
# original = Image.open(File)
# original = original.resize((1000,1000)) #resize image
# img = ImageTk.PhotoImage(original)
# w.create_image(0, 0, image=img, anchor="nw")

def create_frame():
    dot_list = tk.LabelFrame(root, text="Dot List")
    dot_list.grid(row=0, column=1)
    button = Button(dot_list, text = "Select color",
                   command = choose_color)            
    button.grid(row=0, column=1)
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
    # return color

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
    r = 1
    for item in colors_count:
        label = tk.Label(dot_list, text='#', bg=item, fg=item).grid(row=r, column=0)
        first_label = tk.Label(dot_list, text=colors_count[item]).grid(row=r, column=1)
        r+=1

create_frame()
w.bind("<Button 1>",draw_circle)
root.mainloop()