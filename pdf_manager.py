import fitz
from tkinter import *
import tkinter as tk
from tkinter import filedialog

def convert_pdf_to_tk(file):
    print(file)
    if file is not None:
        doc = fitz.open(file)
        page = doc[0]
        pix = page.get_pixmap()
        pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix  # PPM does not support transparency
        imgdata = pix1.tobytes("ppm")  # extremely fast!
        return tk.PhotoImage(data = imgdata)
    else:
        return tk.PhotoImage()

def load_pdf():
    filename = filedialog.askopenfilename()
    return filename
