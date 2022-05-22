import tkinter as tk
from tkinter import ttk
from editBar import EditBar
from img_viewer import ImageViewer

class App(tk.Tk):
    def __init__(self):
        
        super().__init__()
        #states and path
        self.filename = ""
        self.org_image = None
        self.processed_img = None
        self.is_img_selected = None
        self.is_draw_state = None
        self.is_crop_state = None
        self.previous_img = None #todo

        self.filter_frame = None
        self.adjust_frame = None
        
        #title
        self.title("Edytor obrazów")
        
        #frames
        self.editbar = EditBar(master=self)
        separator1 = ttk.Separator(master=self, orient=tk.HORIZONTAL)
        self.image_viewer = ImageViewer(master=self)

        self.editbar.pack(pady=10)
        separator1.pack(fill=tk.X, padx=20, pady=5)
        self.image_viewer.pack(fill=tk.BOTH, padx=20, pady=10, expand=1)

    

