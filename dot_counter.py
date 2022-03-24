from fileinput import close
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import colorchooser
from turtle import xcor
from PIL import Image, ImageTk
import pdf_manager as pdf
import webcolors
import csv
import zoom
import pickle

root = Tk()


#TODO: Rebuild into classes
class counter:
    def __init__(self):
            self.color = '#000000'
            self.curr_color= tk.Label(root, text='#', bg='#000000', fg='#000000')
            self.colors_count= {}
            self.dot_list=tk.LabelFrame(root, text="Menu")
            self.pages = []
            self.canvas = None
            self.last_circle = None
            self.diam = 10

this = counter()

def create_frame():

    if this.dot_list:
        this.dot_list.destroy()
    this.dot_list = tk.LabelFrame(root, text="Menu")
    this.dot_list.grid(row=0, column=1)
    lButton = Button(this.dot_list, text="<- Prev Page",
                    command=lambda: chng_pg(False))
    lButton.grid(row=0, column=0)
    nButton = Button(this.dot_list, text="Next Page ->",
                    command=lambda: chng_pg(True))
    nButton.grid(row=0, column=1)
    this.curr_color = tk.Label(this.dot_list, text='#', bg=this.color, fg=this.color)
    this.curr_color.grid(row=1, column=0)
    first_label = tk.Label(
        this.dot_list, text="<- Current Color").grid(row=1, column=1)
    button = Button(this.dot_list, text="Select color",
                    command=choose_color)
    button.grid(row=2, column=1)
    sButton = Button(this.dot_list, text="Change dot size", command=set_size)
    sButton.grid(row=2, column=0)
    saveButton = Button(this.dot_list, text="Save all counts", command=export)
    saveButton.grid(row=1, column=3)
    return this.dot_list


def create_circle(x, y, r, canvasName):  # center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill=this.color, outline=this.color, tags=this.color) #tags: make sure the color is stored in the circle!


def choose_color():
    # variable to store hexadecimal code of color
    color_code = colorchooser.askcolor(title="Choose color")
    this.curr_color.config(bg=color_code[1], fg=color_code[1])
    print(color_code[1])
    this.color = color_code[1]


def draw_circle(event):
    if this.color in this.colors_count:
        this.colors_count[this.color] += 1
    else:
        this.colors_count[this.color] = 1
    print(this.colors_count)
    create_circle(event.x, event.y, this.diam, this.canvas)
    generate_list()

def del_circle(event):
    item = this.canvas.find_closest(event.x, event.y)
    print()
    if this.canvas.type(item[0]) == 'oval':
        tags = this.canvas.gettags(item[0])
        print(tags)
        this.colors_count[tags[0]] -= 1 #decrement the color!
        this.canvas.delete(item)

    else:
        tk.messagebox.showerror(title='Error', message='No circle present!', )
    # this.canvas.bind("<Button 1>", draw_circle)

def delete():
    this.canvas.bind("<Button 2>", del_circle)

def generate_list():
    this.dot_list = create_frame()
    r = 3
    for item in this.colors_count:
        label = tk.Label(this.dot_list, text='#', bg=item,
                        fg=item).grid(row=r, column=0)
        first_label = tk.Label(
            this.dot_list, text=this.colors_count[item]).grid(row=r, column=1)
        r += 1

def chng_pg(next):
    idx = this.curr_idx
    # this.pages[idx] = pickle.dumps(this.canvas)
    # this.canvas.delete()
    this.pdf_img, this.curr_idx =p.change_page(this.curr_idx, next)
    # img = this.pdf_img.getimage()
    wx = this.pdf_img.width() + 50  # get the width dynamically and add a buffer of 50px
    hx = this.pdf_img.height() + 50  # get the width dynamically and add a buffer of 50px
    if this.pages[idx] is not None:
        this.canvas=this.pages[idx].loads()
    else:
        this.canvas = create_canvas(wx, hx)

def create_canvas(wx, hx):
    # w = zoom.CanvasImage(root, this.pdf_img, draw_circle)
    w = tk.Canvas(root, width=wx, height=hx)
    w.bind('<Button 1>',draw_circle)
    w.bind('<Button 3>',del_circle)
    w.grid(row=0, column=0)
    w.create_image(20, 20, anchor='nw', image=this.pdf_img)
    create_frame()
    this.canvas = w
    return w

def set_size():

     # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(root)
    newWindow.title("Set dot size")
    newWindow.geometry("200x200")
    Label(newWindow,
          text ="This is a new window").pack()
    d = this.diam
    s = tk.Scale(newWindow, variable=d)
    s.set(d)
    s.pack()
    close = tk.Button(newWindow, text="Save and close", command=lambda: close_and_save(s, newWindow))
    close.pack()

def close_and_save(scale, window):
    this.diam = scale.get()
    window.destroy()

def export():
    headers = ['color', 'count']
    data = []
    for color in this.colors_count:
        name = get_color_name(color)
        count = this.colors_count[color]
        data.append([name, count])
    with open('count.csv', 'w', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(headers)
        print(data)
        for row in data:
        # write a row to the csv file
            writer.writerow(row)

#https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python
def closest_color(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_b, g_b, b_b = webcolors.hex_to_rgb(requested_colour)
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - r_b) ** 2
        gd = (g_c - g_b) ** 2
        bd = (b_c - b_b) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_color_name(requested_colour):
    try:
        return webcolors.hex_to_name(requested_colour)
    except ValueError:
        closest_name = closest_color(requested_colour)
    return closest_name

class MainWindow(ttk.Frame):
    """ Main window class """
    def __init__(self, mainframe, wx, hx):
        """ Initialize the main Frame """
        ttk.Frame.__init__(self, master=mainframe)
        self.master.title('Advanced Zoom v3.0')
        w = str(wx)
        h = str(hx)
        dim = w+'x'+h
        self.master.geometry(dim)  # size of the main window
        self.master.rowconfigure(0, weight=1)  # make the CanvasImage widget expandable
        self.master.columnconfigure(0, weight=1)
        this.canvas= create_canvas(wx, hx)  # create widget

p = pdf.pdf_manager(root)
file, len = p.load_pdf()
this.pages = [None] * len
print(this.pages)
this.pdf_img, this.curr_idx = p.convert_pdf_to_tk(file)
wx = this.pdf_img.width() + 50  # get the width dynamically and add a buffer of 50px
hx = this.pdf_img.height() + 50  # get the width dynamically and add a buffer of 50px
# setting up a tkinter canvas
this.canvas = create_canvas(wx, hx)
root.mainloop()
# app = MainWindow(root, wx, hx)
# app.mainloop()