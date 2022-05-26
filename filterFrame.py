from tkinter import END, Toplevel, Button, RIGHT
import tkinter as tk
import numpy as np
import cv2


class FilterFrame(Toplevel):
    """Klasa odpowiedzialna za okno do edycji (nakladania filtrow) obrazu"""

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        #to do
        self.frame_flip = None
        self.original_image = self.master.processed_image
        self.filtered_image = None
        self.h = self.original_image[0]
        self.w = self.original_image[1]
        self.input_angles = None

        #definicja przyciskow
        self.negative_button = Button(master=self, text="Negatyw")
        self.black_white_button = Button(master=self, text="Czarno bialy")
        self.sepia_button = Button(master=self, text="Sepia")
        self.emboss_button = Button(master=self, text="Emboss")
        self.gaussian_blur_button = Button(master=self, text="Gaussian Blur")
        self.median_blur_button = Button(master=self, text="Median Blur")
        self.flip_button = Button(master=self, text ="Obróć o zadana ilosc stopni")
        self.cancel_button = Button(master=self, text="Odrzuć")
        self.apply_button = Button(master=self, text="Zatwierdź")

        #bindy przyciskow
        self.negative_button.bind("<ButtonRelease>", self.negative_button_released)
        self.black_white_button.bind("<ButtonRelease>", self.black_white_released)
        self.sepia_button.bind("<ButtonRelease>", self.sepia_button_released)
        self.emboss_button.bind("<ButtonRelease>", self.emboss_button_released)
        self.gaussian_blur_button.bind("<ButtonRelease>", self.gaussian_blur_button_released)
        self.median_blur_button.bind("<ButtonRelease>", self.median_blur_button_released)
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)
        self.flip_button.bind("<ButtonRelease> ", self.flip_button_released)
        
        #dodanie przyciskow do layoutu
        self.flip_button.pack()
        self.negative_button.pack()
        self.black_white_button.pack()
        self.sepia_button.pack()
        self.emboss_button.pack()
        self.gaussian_blur_button.pack()
        self.median_blur_button.pack()
        self.cancel_button.pack(side=RIGHT)
        self.apply_button.pack()

    #funkcje zajmujace sie reagowaniem na przycisniecie przycisku - eventy
    def flip_button_released(self, event):
        self.flip_img()
        self.show_image()

    def negative_button_released(self, event):
        self.negative()
        self.show_image()

    def black_white_released(self, event):
        self.black_white()
        self.show_image()

    def sepia_button_released(self, event):
        self.sepia()
        self.show_image()

    def emboss_button_released(self, event):
        self.emboss()
        self.show_image()

    def gaussian_blur_button_released(self, event):
        self.gaussian_blur()
        self.show_image()

    def median_blur_button_released(self, event):
        self.gaussian_blur()
        self.show_image()

    def apply_button_released(self, event):
        self.master.processed_image = self.filtered_image
        self.show_image()
        self.close()

    def cancel_button_released(self, event):
        self.master.image_viewer.show_image()
        self.close()

    #funkcje zajmujace sie faktyczna zmiana obrazu
    #todo flip_img
    def flip_img(self):
        self.frame_flip = tk.Tk()
        self.frame_flip.title("Obrót")
        self.frame_flip.geometry('400x200')
        self.input_angles = tk.Text(self.frame_flip, height=5, width=20)
        self.input_angles.pack()
        input = (self.input_angles.get("1.0", END))
        (cX, cY) = (self.w // 2, self.h // 2)
        M = cv2.getRotationMatrix2D((cX, cY), input, 1.0)
        self.filtered_image = cv2.warpAffine(self.filtered_image, M, (self.w, self.h))
        self.show_image()

    def show_image(self):
        """Funkcja pokazujaca zedytowane zdjecie"""
        self.master.image_viewer.show_image(img=self.filtered_image)

    def negative(self):
        """Funkcja zajmujaca sie aplikacja negatywu"""
        self.filtered_image = cv2.bitwise_not(self.original_image)

    def black_white(self):
        """Funkcja zajmujaca sie aktywacja filtru bialo-czarnego"""
        self.filtered_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.filtered_image = cv2.cvtColor(self.filtered_image, cv2.COLOR_GRAY2BGR)

    def sepia(self):
        """Funckja zajmujaca sie aktywacja filtru - sepia"""
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])

        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)

    def emboss(self):
        """Funckja zajmujaca sie aktywacja filtru - emboss"""
        kernel = np.array([[0, -1, -1],
                           [1, 0, -1],
                           [1, 1, 0]])

        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)

    def gaussian_blur(self):
        """Funckja zajmujaca sie aktywacja filtru - gaussian blur"""
        self.filtered_image = cv2.GaussianBlur(self.original_image, (41, 41), 0)

    def median_blur(self):
        """Funckja zajmujaca sie aktywacja filtru - median_blur"""
        self.filtered_image = cv2.medianBlur(self.original_image, 41)

    def close(self):
        """Funkcja zajmujaca sie zamknieciem okna"""
        self.destroy()