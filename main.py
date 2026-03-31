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
        schema_offset_x = 2.5 #the more the number the more to the left
        schema_offset_y = 2

        # Find which side of the image touch the border of the screen
        ratio = min(screen_width / img_width, screen_height / img_height)
        def_width = int(img_width * ratio)
        def_height = int(img_height * ratio)
        self.image = self.image.resize((def_width, def_height))

        self.photo = ImageTk.PhotoImage(self.image) # Convert PIL image to tkinter


        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="white")
        self.canvas.pack()

        # Display Distill schema
        self.canvas.create_image(screen_width/schema_offset_x, screen_height/schema_offset_y, anchor=tk.CENTER, image=self.photo)
        self.temp_censor1 = self.canvas.create_text((screen_width/schema_offset_x)-210,740, anchor=tk.NW, text="PE", font=("Arial", 20))
        self.temp_censor1label = self.canvas.create_text((screen_width/schema_offset_x)+50,30, anchor=tk.NW, text="T1", font=("Arial", 20))
        self.temp_censor2label = self.canvas.create_text((screen_width/schema_offset_x)+65,130, anchor=tk.NW, text="T2", font=("Arial", 20))
        self.temp_censor3label = self.canvas.create_text((screen_width/schema_offset_x)+95,290, anchor=tk.NW, text="T3", font=("Arial", 20))
        self.temp_censor4label = self.canvas.create_text((screen_width/schema_offset_x)+110,732, anchor=tk.NW, text="T4", font=("Arial", 20))

        #PlaceHolder for temp censor
        self.temp_censor1 = self.canvas.create_text((screen_width/schema_offset_x)+115,30, anchor=tk.NW, text="1000,000°C", font=("Arial", 20))
        self.temp_censor2 = self.canvas.create_text((screen_width/schema_offset_x)+130,130, anchor=tk.NW, text="2000,000°C", font=("Arial", 20))
        self.temp_censor3 = self.canvas.create_text((screen_width/schema_offset_x)+95,235, anchor=tk.NW, text="3000,000°C", font=("Arial", 20))
        self.temp_censor4 = self.canvas.create_text((screen_width/schema_offset_x)+180,732, anchor=tk.NW, text="4000,000°C", font=("Arial", 20))
        
        #PlaceHolder for swich state
        self.is_on = False
        self.btn_setON = self.canvas.create_oval(200, 120, 250, 170, fill="red", outline="black", width=2)
        self.canvas.create_text(140, 70, anchor=tk.NW, text="Mise en Marche", font=("Arial", 20))
        self.canvas.tag_bind(self.btn_setON, "<Button-1>", lambda event: self.toggle_switch())


        self.is_heating_on = False
        self.btn_heating = self.canvas.create_oval(200, 250, 250, 300, fill="red", outline="black", width=2)
        self.canvas.create_text(140, 210, anchor=tk.NW, text="Chauffe Ballon", font=("Arial", 20))
        self.canvas.tag_bind(self.btn_heating, "<Button-1>", lambda event: self.toggle_heating())
        
        self.is_heating_on1 = False
        self.canvas.create_text(30, 330, anchor=tk.NW, text="Chauffe 1", font=("Arial", 20))
        self.btn_heating1 = self.canvas.create_oval(60, 370, 110, 420, fill="gray", outline="black", width=2)
        self.canvas.tag_bind(self.btn_heating1, "<Button-1>", lambda event: self.toggle_heating1())

        self.is_heating_on2 = False
        self.canvas.create_text(170, 330, anchor=tk.NW, text="Chauffe 2", font=("Arial", 20))
        self.btn_heating2 = self.canvas.create_oval(200, 370, 250, 420, fill="gray", outline="black", width=2)
        self.canvas.tag_bind(self.btn_heating2, "<Button-1>", lambda event: self.toggle_heating2())

        self.is_heating_on3 = False
        self.canvas.create_text(310, 330, anchor=tk.NW, text="Chauffe 3", font=("Arial", 20))
        self.btn_heating3 = self.canvas.create_oval(340, 370, 390, 420, fill="gray", outline="black", width=2)
        self.canvas.tag_bind(self.btn_heating3, "<Button-1>", lambda event: self.toggle_heating3())


        self.print_mouse_pos()

    def toggle_switch(self):
        self.is_on = not self.is_on #Swap between true and false
        if self.is_on:
            self.canvas.itemconfig(self.btn_setON, fill="green")
        else:
            self.canvas.itemconfig(self.btn_setON, fill="red")

    def toggle_heating(self):
        self.is_heating_on = not self.is_heating_on
        if self.is_heating_on:
            self.canvas.itemconfig(self.btn_heating, fill="green")
        else:
            self.canvas.itemconfig(self.btn_heating, fill="red")

    def toggle_heating1(self):
        if self.is_heating_on:
            self.is_heating_on1 = not self.is_heating_on1
            if self.is_heating_on1:
                self.canvas.itemconfig(self.btn_heating1, fill="green")
            else:
                self.canvas.itemconfig(self.btn_heating1, fill="red")

    def toggle_heating2(self):
        if self.is_heating_on:
            self.is_heating_on2 = not self.is_heating_on2
            if self.is_heating_on2:
                self.canvas.itemconfig(self.btn_heating2, fill="green")
            else:
                self.canvas.itemconfig(self.btn_heating2, fill="red")

    def toggle_heating3(self):
        if self.is_heating_on:
            self.is_heating_on3 = not self.is_heating_on3
            if self.is_heating_on3:
                self.canvas.itemconfig(self.btn_heating3, fill="green")
            else:
                self.canvas.itemconfig(self.btn_heating3, fill="red")


    #get mouse cord, remove for prod ?
    def print_mouse_pos(self):
        x = root.winfo_pointerx() - root.winfo_rootx()
        y = root.winfo_pointery() - root.winfo_rooty()
        print(f"Mouse position: ({x}, {y})")
        root.after(2000, self.print_mouse_pos)
    



root = tk.Tk()
window = Window(root)
root.mainloop()