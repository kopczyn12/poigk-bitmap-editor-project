import tkinter as tk
from tkinter import ttk
from editBar import EditBar
from img_viewer import ImageViewer

class App(tk.Tk):
    """Glowna klasa okna"""
    def __init__(self):
        
        super().__init__()
        #zmienne - sciezki, stany
        self.filename = ""
        self.org_image = None
        self.processed_image = None
        self.is_img_selected = None
        self.is_draw_state = None
        self.is_crop_state = None
       

        #dwa pozostale okna
        self.filter_frame = None
        self.adjust_frame = None
        
        #tytul okna
        self.title("Edytor obrazów")
       
        #elementy aplikacji - editbar i image viewer
        self.editbar = EditBar(master=self)
        #separator dzielacy 2 pola, edit bar i image viewer.
        separator1 = ttk.Separator(master=self, orient=tk.HORIZONTAL)
        self.image_viewer = ImageViewer(master=self)

        #zaladowanie elementow do layout'u
        self.editbar.pack(pady=10)
        separator1.pack(fill=tk.X, padx=20, pady=5)
        self.image_viewer.pack(fill=tk.BOTH, padx=20, pady=10, expand=1)

    

