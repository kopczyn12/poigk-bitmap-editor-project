from tkinter import Frame, Button, LEFT
from tkinter import filedialog
from filterFrame import FilterFrame
from adjustFrame import AdjustFrame
import cv2


class EditBar(Frame):
    """Klasa odpowiedzialna za EditBar"""

    def __init__(self, master=None):
        Frame.__init__(self, master=master)

        #Definiowanie przyciskow
        self.load_bmp_button = Button(self, text="Wczytaj")
        self.save_button = Button(self, text="Zapisz")
        self.save_as_button = Button(self, text="Zapisz jako")
        self.draw_button = Button(self, text="Rysuj")
        self.crop_button = Button(self, text="Przytnij")
        self.filter_button = Button(self, text="Filtruj")
        self.adjust_button = Button(self, text="Edytuj kolory i jasność")
        self.clear_button = Button(self, text="Wyczyść")
        
        #Bindery przyciskow
        self.load_bmp_button.bind("<ButtonRelease>", self.load_bmp_button_released)
        self.save_button.bind("<ButtonRelease>", self.save_button_released)
        self.save_as_button.bind("<ButtonRelease>", self.save_as_button_released)
        self.draw_button.bind("<ButtonRelease>", self.draw_button_released)
        self.crop_button.bind("<ButtonRelease>", self.crop_button_released)
        self.filter_button.bind("<ButtonRelease>", self.filter_button_released)
        self.adjust_button.bind("<ButtonRelease>", self.adjust_button_released)
        self.clear_button.bind("<ButtonRelease>", self.clear_button_released)
        
        #Dodanie przyciskow do layoutu
        self.load_bmp_button.pack(side=LEFT)
        self.save_button.pack(side=LEFT)
        self.save_as_button.pack(side=LEFT)
        self.draw_button.pack(side=LEFT)
        self.crop_button.pack(side=LEFT)
        self.filter_button.pack(side=LEFT)
        self.adjust_button.pack(side=LEFT)
        self.clear_button.pack()

#Tu zaczyna sie definiowanie funkcji oblugujace klikniecie przyciskow (eventy).

    def load_bmp_button_released(self, event):
        """Funkcja wczytujaca zdjecie"""
        if self.winfo_containing(event.x_root, event.y_root) == self.load_bmp_button: #sprawdzenie, czy kliknelismy dobry przycisk, aby miec pewnosc ze klikajac odpowiedni przycisk zdarzy sie odpowiedni event
            if self.master.is_draw_state:#sprawdzenie czy rysujemy, jesli  tak to wylaczamy rysowanie bo wczytujemy nowy obraz. Podobnie ponizej z przycinaniem.
                self.master.image_viewer.deactivate_draw()
            if self.master.is_crop_state:
                self.master.image_viewer.deactivate_crop()

            #otworzenie okna dialogowego i wczytanie obrazu
            filename = filedialog.askopenfilename()
            image = cv2.imread(filename)
            
            #jesli zdjecie zostalo poprawnie wczytane, zapisujemy jego nazwe, tworzymy kopie oryginalu i przetwarzanego zdjecia, pokazujemy je na ekranie i zmieniamy stan "wybrania zdjecia" na True"
            if image is not None:
                self.master.filename = filename
                self.master.original_image = image.copy()
                self.master.processed_image = image.copy()
                self.master.image_viewer.show_image()
                self.master.is_image_selected = True

    def save_button_released(self, event):
        """Funkcja zapisuajca zdjecie"""
        if self.winfo_containing(event.x_root, event.y_root) == self.save_button: #ten sam warunek co powyzej.
            if self.master.is_image_selected:
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()

                #zapis zdjecia
                save_image = self.master.processed_image
                image_filename = self.master.filename
                cv2.imwrite(image_filename, save_image)

    def save_as_button_released(self, event):
        """Funckja zapisujaca zdjecie jako..."""
        if self.winfo_containing(event.x_root, event.y_root) == self.save_as_button: #ten sam warunek co wyzej
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                
                #uzyskanie oryginalnego rozszerzenia zdjecia
                original_file_type = self.master.filename.split('.')[-1]
                #podanie nowej nazwy pliku przez uzytkownika
                filename = filedialog.asksaveasfilename()
                #przechowanie nowej nazwy pliku podanej przez uzytkownika z oryginalnym rozszerzeniem
                filename = filename + "." + original_file_type

                #zapis zdjecia
                save_image = self.master.processed_image
                cv2.imwrite(filename, save_image)

                #przypisanie nazwy pliku do zmiennej obiektowej
                self.master.filename = filename

    def draw_button_released(self, event):
        """Funkcja odpowiadajaca za wlaczenie rysowania"""
        if self.winfo_containing(event.x_root, event.y_root) == self.draw_button: #ten sam warunek co wyzej
            if self.master.is_image_selected:
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                else:
                    #aktywacja funkcji rysujacej z img_viewer
                    self.master.image_viewer.activate_draw()

    def crop_button_released(self, event):
        """"Funkcja odpowiadajaca za wlaczenie przycinania"""
        if self.winfo_containing(event.x_root, event.y_root) == self.crop_button: #to samo co wyzej
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                else:
                    #aktywacja funkcji przycinajacej
                    self.master.image_viewer.activate_crop()

    def filter_button_released(self, event):
        """Funkcja odpowiadajaca za wlaczenie okna pozwalajacego na filtrowanie zdjecia"""
        if self.winfo_containing(event.x_root, event.y_root) == self.filter_button: #to samo co wyzej
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()

                #utworzenie okna do wyboru filtru
                self.master.filter_frame = FilterFrame(master=self.master)
                #teraz okno filter frame ma byc przetwarzane przez uzytkownika
                self.master.filter_frame.grab_set()

    def adjust_button_released(self, event):
        """Funkcja odpowiadajaca za wlaczenie okna pozwalajacego na edycje kolorw i jasnosci zdjecia"""
        #wszystko analogicznie jak powyzej tylko dla okna adjustframe
        if self.winfo_containing(event.x_root, event.y_root) == self.adjust_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()

                self.master.adjust_frame = AdjustFrame(master=self.master)
                self.master.adjust_frame.grab_set()
    
    def clear_button_released(self, event):
        """Funkcja cofajaca wprowadzone zmiany"""
        if self.winfo_containing(event.x_root, event.y_root) == self.clear_button: #ten sam warunek co powyzej
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                
                #powrot do oryginalnej wersji zdjecia poprzez utworzenie kopii oryginalnego zdjecia i zapisanie jej w zmiennej filtered image
                self.master.processed_image = self.master.original_image.copy()
                #pokazanie zdjecia
                self.master.image_viewer.show_image()