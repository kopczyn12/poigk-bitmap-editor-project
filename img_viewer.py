from tkinter import Frame, Canvas, CENTER, ROUND
from PIL import Image, ImageTk
import cv2

#tkinter potrzebuje PIL aby pokazac obraz (odpowiedni typ) na swoim canvasie.
class ImageViewer(Frame):
    """Klasa implemetujaca image viewer frame, odpowiedzialna odtarzanie obrazu"""

    def __init__(self, master=None):

        #utworzenie canvasu po dziedziczeniu frame z tkinter
        Frame.__init__(self, master=master, bg="gray", width=600, height=400)

        #deklaracja instancji
        self.shown_image = None
        self.x = 0
        self.y = 0
        #zmienne potrzebne do przycinania
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.draw_ids = list()
        self.rectangle_id = 0
        #zmienna do zmieniania rozmiaru zdjecia
        self.ratio = 0

        self.canvas = Canvas(self, bg="gray", width=600, height=400)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

    def show_image(self, img=None):
        """Funkcja pokazujaca zdjecie na canvasie"""
        self.clear_canvas()

        #przypisanie zdjecia jezeli nie jest podane
        if img is None:
            image = self.master.processed_image.copy()
        else:
            image = img

        #zmiana do RGB, poniewaz opencv przyjmuje zdjecia w formacie BGR
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #wyciagniecie inf. ze zdjecia - wysokosci, szerokosci, kanalow kolorow
        height, width, channels = image.shape
        #policzenie wspolczynnika
        ratio = height / width

        new_width = width
        new_height = height

        #dostosowanie nowego rozmiaru zdjecia do canvasu, poniewaz to zdjecie sie zmienia, a nie canvas
        if height > self.winfo_height() or width > self.winfo_width():
            if ratio < 1:
                new_width = self.winfo_width()
                new_height = int(new_width * ratio)
            else:
                new_height = self.winfo_height()
                new_width = int(new_height * (width / height))
        
        #zmiana rozmiaru zdjecia
        self.shown_image = cv2.resize(image, (new_width, new_height))
        #przetworzenie zdjecia do obiektu Image
        self.shown_image = ImageTk.PhotoImage(Image.fromarray(self.shown_image))
        #oryginalny wspolczynnik zdjecia
        self.ratio = height / new_height

        #skonfigurowanie zdjecia i stworzenie na canvasie
        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(new_width / 2, new_height / 2, anchor=CENTER, image=self.shown_image)

    #funckje zajmujace sie aktywacja rysowania i przycinania, jak i deaktywacja
    def activate_draw(self):
        """Funkcja aktywujaca przycinanie"""
        #binding gdy zostal wcisniety guzik
        self.canvas.bind("<ButtonPress>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)

        self.master.is_draw_state = True

    def activate_crop(self):
        """Funkcja aktywujaca przycinanie"""
        #binding gdy zostal wcisniety guzik
        self.canvas.bind("<ButtonPress>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.crop)
        self.canvas.bind("<ButtonRelease>", self.end_crop)

        #zmiana stanu
        self.master.is_crop_state = True

    def deactivate_draw(self):
        """Funkcja deaktywujaca rysowanie"""
        #unbinding 
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")

        self.master.is_draw_state = False

    def deactivate_crop(self):
        """Funkcja deaktywujaca przycinanie"""
        #unbinding 
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease>")

        #zmiana stanu
        self.master.is_crop_state = False

    def start_draw(self, event):
        """Funkcja zajmujaca sie przypisaniem poczatku rysowania"""
        #funkcja zajmujaca sie poczatkiem rysowania, przypisanie poczatkowych zmiennych (tam gdzie klikniemy)
        self.x = event.x
        self.y = event.y
 
    def draw(self, event):
        """funckja rysujaca"""
        #tworzy linie na canvasie od naszzego poczatkowego klikniecia do nastepnego
        self.draw_ids.append(self.canvas.create_line(self.x, self.y, event.x, event.y, width=2,
                                                     fill="red", capstyle=ROUND, smooth=True))

        #rysowanie linii na naszej tablicy (zdjeciu) i przeliczenie tego wedlug wspolczynnika
        cv2.line(self.master.processed_image, (int(self.x * self.ratio), int(self.y * self.ratio)),
                 (int(event.x * self.ratio), int(event.y * self.ratio)),
                 (0, 0, 255), thickness=int(self.ratio * 2),
                 lineType=8)

        #update zmiennych
        self.x = event.x
        self.y = event.y

    def start_crop(self, event):
        """Funkcja zajmujaca sie przypisaniem startu przycinania"""
        #start przycinania, poczatkowe wspolrzedne
        self.crop_start_x = event.x
        self.crop_start_y = event.y

    def crop(self, event):
        """Funkcja przycinajaca"""
        #jesli jest teraz jakis prostokat to go usun (przycinanie)
        if self.rectangle_id:
            self.canvas.delete(self.rectangle_id)

        #update zmiennych 
        self.crop_end_x = event.x
        self.crop_end_y = event.y

        #tworzenie nowego prostokatu na canvasie (przyciecie)
        self.rectangle_id = self.canvas.create_rectangle(self.crop_start_x, self.crop_start_y,
                                                         self.crop_end_x, self.crop_end_y, width=1)

    def end_crop(self, event):
        """Funckja konczaca przyciecie"""
        #Warunki sprawdzajace przyciecie, poniewaz mozemy przycinac z roznych stron
        if self.crop_start_x <= self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x > self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x <= self.crop_end_x and self.crop_start_y > self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        else:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)

        #przycinanie zdjecia
        x = slice(start_x, end_x, 1)
        y = slice(start_y, end_y, 1)

        #nadpisanie
        self.master.processed_image = self.master.processed_image[y, x]

        #pokazanie zdjecia
        self.show_image()
    
    def clear_canvas(self):
        """Funckja czyszczaca canvas"""
        self.canvas.delete("all")

    def clear_draw(self):
        """Funckja czyszczaca rysowanie z canvasu"""
        self.canvas.delete(self.draw_ids)