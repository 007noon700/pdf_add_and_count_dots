import fitz
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class pdf_manager:
    def __init__(self, root):
        self.root = root
        self.doc = None

    def convert_pdf_to_tk(self, file):
        if file is not None:
            self.doc = fitz.open(file)
            return self.change_page(0, False)
        else:
            return tk.PhotoImage()

    def load_pdf(self):
        filename = filedialog.askopenfilename()
        self.doc = fitz.open(filename)
        return filename, len(self.doc)

    def change_page(self, curr_idx, next): #we encode next as a bool, True for next, False for last
        if self.doc is not None:
            if next and len(self.doc) > curr_idx+1: #if next and we still have pages in doc,
                return (self.generate_img(self.doc[curr_idx+1]), curr_idx+1) #return a tuple with next page and the new index
            elif next and len(self.doc) == curr_idx+1: #if next but we're at end of doc
                return (self.generate_img(self.doc[curr_idx]), curr_idx) #return existing page and new idx
            elif not next and curr_idx > 0: #if last and this isn't page one,
                return (self.generate_img(self.doc[curr_idx-1]), curr_idx-1)#return prev page and new idx
            elif not next and curr_idx == 0:#if last but page one
                return (self.generate_img(self.doc[0]),0)#return page one and new idx

    def scale_img(self, img):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w = img.width
        h = img.height
        while sw<w or sh<h:
            w = (3*w) // 4
            h = (3*h) // 4
            img = img.resize((w, h))
        return ImageTk.PhotoImage(img)


    def generate_img(self, page):
        pix = page.get_pixmap()
        img = Image.frombytes("RGB",(pix.width, pix.height), pix.samples)
        pil_img = self.scale_img(img)
        return pil_img
        