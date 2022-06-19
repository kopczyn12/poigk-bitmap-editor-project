from tkinter import Toplevel, Label, Scale, Button, HORIZONTAL, RIGHT
import cv2


class AdjustFrame(Toplevel):
    """Klasa obslugujaca okno zajmujaca sie dostosywaniem koloru i jasnosci"""
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        #definicja stanow i zmiennych
        self.brightness_value = 0
        self.previous_brightness_value = 0

        self.original_image = self.master.processed_image
        self.processing_image = self.master.processed_image
        
        #label i skala do zmiany janoscii kolor RGB
        self.brightness_label = Label(self, text="Jasność")
        self.brightness_scale = Scale(self, from_=0, to_=2, length=250, resolution=0.1,
                                      orient=HORIZONTAL)
        self.r_label = Label(self, text="R")
        self.r_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.g_label = Label(self, text="G")
        self.g_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.b_label = Label(self, text="B")
        self.b_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        #przyciski - zatwierdz, widok do sprawdzenia zmian, odrzuc
        self.apply_button = Button(self, text="Zatwierdź")
        self.preview_button = Button(self, text="Widok")
        self.cancel_button = Button(self, text="Odrzuć")

        #ustawienie 1 na skali jasnosci
        self.brightness_scale.set(1)

        #bindy
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.preview_button.bind("<ButtonRelease>", self.show_button_release)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        #dodanie do layotu
        self.brightness_label.pack()
        self.brightness_scale.pack()
        self.r_label.pack()
        self.r_scale.pack()
        self.g_label.pack()
        self.g_scale.pack()
        self.b_label.pack()
        self.b_scale.pack()
        self.cancel_button.pack(side=RIGHT)
        self.preview_button.pack(side=RIGHT)
        self.apply_button.pack()
    
    def apply_button_released(self, event):#funkcja obslugujaca zatwierdzenie zmian
        """Funkcja zatwierdzajaca zmiany w oknie adjustFrame"""
     
        self.master.processed_image = self.processing_image
     
        self.close()

    def show_button_release(self, event):#funkcja umozliwiajaca widok zmian i aplikacje
        """Funkcja pokazujaca wprowadzone zmiany w oknie adjustFrame"""
      
        self.processing_image = cv2.convertScaleAbs(self.original_image, alpha=self.brightness_scale.get())

        #rozdzielenie kolorow w celu mozliwosci edycji wartosci pojedynczych barw
     
        b, g, r = cv2.split(self.processing_image)

        for b_value in b:
            cv2.add(b_value, self.b_scale.get(), b_value)
        for g_value in g:
            cv2.add(g_value, self.g_scale.get(), g_value)
        for r_value in r:
            cv2.add(r_value, self.r_scale.get(), r_value)

        #zlaczenie edytowanych kolorow
       
        self.processing_image = cv2.merge((b, g, r))
        
    
        self.show_image(self.processing_image)

    def cancel_button_released(self, event):#odrzucenie zmian
        """Funkcja odrzucajaca wprowadzone zmiany w oknie adjustFrame"""
        self.close()

    def show_image(self, img=None):#pokazanie zdjecia
        """Funkcja pokazujaca zdjecie"""
        self.master.image_viewer.show_image(img=img)

    def close(self):#zamkniecie okna
        """Funkcja zamykajaca okno"""
        self.show_image()
        self.destroy()