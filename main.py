import tkinter as tk
from PIL import Image, ImageTk
import screeninfo as screen

screen_info = screen.get_monitors()[0]
screen_width = screen_info.width - 200
screen_height = screen_info.height -200


class Window:
    def __init__(self, root):

        root.configure(bg="white")
        root.title("HIM-Distill")
        root.geometry(f"{screen_width}x{screen_height}")

        self.image = Image.open("img/schema.png")
        img_height = self.image.height
        img_width = self.image.width

        # Find which side of the image touch the border of the screen
        ratio = min(screen_width / img_width, screen_height / img_height)
        def_width = int(img_width * ratio)
        def_height = int(img_height * ratio)
        self.image = self.image.resize((def_width, def_height))

        self.photo = ImageTk.PhotoImage(self.image) # Convert PIL image to tkinter


        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="white")
        self.canvas.pack()

        # Display Distill schema
        self.canvas.create_image(screen_width/2, screen_height/2, anchor=tk.CENTER, image=self.photo)

        #PlaceHolder for temp censor
        self.temp_censor1 = self.canvas.create_text((screen_width/2)+115,30, anchor=tk.NW, text="1000,000°C", font=("Arial", 20))
        self.temp_censor1label = self.canvas.create_text((screen_width/2)+50,30, anchor=tk.NW, text="T1", font=("Arial", 20))

        self.temp_censor2 = self.canvas.create_text((screen_width/2)+130,130, anchor=tk.NW, text="2000,000°C", font=("Arial", 20))
        self.temp_censor2label = self.canvas.create_text((screen_width/2)+65,130, anchor=tk.NW, text="T2", font=("Arial", 20))

        self.temp_censor3 = self.canvas.create_text((screen_width/2)+95,235, anchor=tk.NW, text="3000,000°C", font=("Arial", 20))
        self.temp_censor3label = self.canvas.create_text((screen_width/2)+95,290, anchor=tk.NW, text="T3", font=("Arial", 20))

        self.temp_censor4 = self.canvas.create_text((screen_width/2)+180,732, anchor=tk.NW, text="4000,000°C", font=("Arial", 20))
        self.temp_censor4label = self.canvas.create_text((screen_width/2)+110,732, anchor=tk.NW, text="T4", font=("Arial", 20))

        self.print_mouse_pos()

    #get mouse cord, remove for prod ?
    def print_mouse_pos(self):
        x = root.winfo_pointerx() - root.winfo_rootx()
        y = root.winfo_pointery() - root.winfo_rooty()
        print(f"Mouse position: ({x}, {y})")
        root.after(2000, self.print_mouse_pos)
    



root = tk.Tk()
window = Window(root)
root.mainloop()