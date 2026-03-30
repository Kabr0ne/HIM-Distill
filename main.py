import tkinter as tk
from PIL import Image, ImageTk
import screeninfo as screen

screen_info = screen.get_monitors()[0]
screen_width = screen_info.width
screen_height = screen_info.height

class Window:
    def __init__(self, root):

        root.configure(bg="white")

        self.image = Image.open("img/schema.png")
        self.image = self.image.resize((screen_width, screen_height)) # Resize image to fit the screen
        self.photo = ImageTk.PhotoImage(self.image) # Convert PIL image to tkinter

        
        self.label = tk.Label(root, image=self.photo, bg="white")

        self.label.pack()


root = tk.Tk()
window = Window(root)
root.mainloop()