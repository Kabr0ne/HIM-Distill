import tkinter as tk
from tkinter import ttk
import csv
from tkinter import filedialog, messagebox
import sqlite3
from PIL import Image, ImageTk
import screeninfo as screen
from matplotlib.figure import Figure
from datetime import datetime
import matplotlib.dates as mdates


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

screen_info = screen.get_monitors()[0]
screen_width = screen_info.width - 200
screen_height = screen_info.height -200


class Window:
    def __init__(self, root):

        self.root = root
        self.current_id_session = None

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


        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="#ECECEC")
        self.canvas.pack()

        # Display Distill schema
        self.canvas.create_image(screen_width/schema_offset_x, screen_height/schema_offset_y, anchor=tk.CENTER, image=self.photo)
        self.temp_sensor1 = self.canvas.create_text((screen_width/schema_offset_x)-210,740, anchor=tk.NW, text="PE", font=("Arial", 20))
        self.temp_sensor1label = self.canvas.create_text((screen_width/schema_offset_x)+50,30, anchor=tk.NW, text="T1", font=("Arial", 20))
        self.temp_sensor2label = self.canvas.create_text((screen_width/schema_offset_x)+65,130, anchor=tk.NW, text="T2", font=("Arial", 20))
        self.temp_sensor3label = self.canvas.create_text((screen_width/schema_offset_x)+95,290, anchor=tk.NW, text="T3", font=("Arial", 20))
        self.temp_sensor4label = self.canvas.create_text((screen_width/schema_offset_x)+110,732, anchor=tk.NW, text="T4", font=("Arial", 20))

        #PlaceHolder for temp sensor
        self.temp_sensor1 = self.canvas.create_text((screen_width/schema_offset_x)+115,30, anchor=tk.NW, text="1000,000°C", font=("Arial", 20))
        self.temp_sensor2 = self.canvas.create_text((screen_width/schema_offset_x)+130,130, anchor=tk.NW, text="2000,000°C", font=("Arial", 20))
        self.temp_sensor3 = self.canvas.create_text((screen_width/schema_offset_x)+95,235, anchor=tk.NW, text="3000,000°C", font=("Arial", 20))
        self.temp_sensor4 = self.canvas.create_text((screen_width/schema_offset_x)+180,732, anchor=tk.NW, text="4000,000°C", font=("Arial", 20))

        #PlaceHolder for switch state
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

        self.is_reflux_on = False
        self.canvas.create_text(140, 450, anchor=tk.NW, text="Recette Reflux", font=("Arial", 20))
        self.btn_reflux = self.canvas.create_oval(200, 500, 250, 550, fill="red", outline="black", width=2)
        self.canvas.tag_bind(self.btn_reflux, "<Button-1>", lambda event: self.toggle_reflux())


        #Database history
        self.database_frame = tk.Frame(self.root, bg="white", bd=2, relief="flat")
        self.style_tree = ttk.Style()
        self.style_tree.configure("Treeview", background="white", foreground="black", font=("Arial", 20), rowheight=30)

        self.tree = ttk.Treeview(self.database_frame, columns=("Capteur", "Température", "Heure"), show='headings', height=15)
        self.tree.heading("Capteur", text="Capteur")
        self.tree.heading("Température", text="Température (°C)")
        self.tree.heading("Heure", text="Heure")
        self.tree.column("Capteur", width=200, anchor=tk.CENTER, stretch=True)
        self.tree.column("Température", width=200, anchor=tk.CENTER, stretch=True)
        self.tree.column("Heure", width=200, anchor=tk.CENTER, stretch=True)
        self.tree.pack()
        self.canvas.create_window(screen_width - 20, (screen_height/5)-80, anchor=tk.NE, window=self.database_frame)



        self.canvas.create_text(screen_width/2 + 240, (screen_height/5)-140, anchor=tk.NW, text="Filtres Capteurs", font=("Arial", 20))

        self.is_filter_censor1_on = True
        self.is_filter_censor2_on = True
        self.is_filter_censor3_on = True
        self.is_filter_censor4_on = True


        self.btn_filter_censor4 = self.canvas.create_oval(screen_width - 100, (screen_height/5)-150, screen_width - 50, (screen_height/5)-100, fill="green", outline="black", width=2)
        self.canvas.create_text(screen_width - 95, (screen_height/5)-190, anchor=tk.NW, text="T4", font=("Arial", 25))
        self.canvas.tag_bind(self.btn_filter_censor4, "<Button-1>", lambda event: self.toggle_filter_censor4())



        self.btn_filter_censor3 = self.canvas.create_oval(screen_width - 200, (screen_height/5)-150, screen_width - 150, (screen_height/5)-100, fill="green", outline="black", width=2)
        self.canvas.create_text(screen_width - 195, (screen_height/5)-190, anchor=tk.NW, text="T3", font=("Arial", 25))
        self.canvas.tag_bind(self.btn_filter_censor3, "<Button-1>", lambda event: self.toggle_filter_censor3())


        self.btn_filter_censor2 = self.canvas.create_oval(screen_width - 300, (screen_height/5)-150, screen_width - 250, (screen_height/5)-100, fill="green", outline="black", width=2)
        self.canvas.create_text(screen_width - 295, (screen_height/5)-190, anchor=tk.NW, text="T2", font=("Arial", 25))
        self.canvas.tag_bind(self.btn_filter_censor2, "<Button-1>", lambda event: self.toggle_filter_censor2())


        self.btn_filter_censor1 = self.canvas.create_oval(screen_width - 400, (screen_height/5)-150, screen_width - 350, (screen_height/5)-100, fill="green", outline="black", width=2)
        self.canvas.create_text(screen_width - 395, (screen_height/5)-190, anchor=tk.NW, text="T1", font=("Arial", 25))
        self.canvas.tag_bind(self.btn_filter_censor1, "<Button-1>", lambda event: self.toggle_filter_censor1())

        #graphic history
        self.graphic_frame = tk.Frame(self.root, bg="white", bd=2, relief="flat")
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Graphique Température")
        self.ax.set_facecolor("#F0F0F0")

        self.canvas_graphic = FigureCanvasTkAgg(self.fig, master=self.graphic_frame)
        self.canvas_graphic.get_tk_widget().pack()
        self.canvas.create_window(screen_width - 20, (screen_height/1.5)-60, anchor=tk.NE, window=self.graphic_frame)   

        self.start_session()
        self.menu()
        self.refresh_data()

                                                               

    def toggle_switch(self):
        self.is_on = not self.is_on #Swap between true and false
        if self.is_on:
            self.canvas.itemconfig(self.btn_setON, fill="green")
        else:
            self.canvas.itemconfig(self.btn_setON, fill="red")

    def toggle_heating(self):
        self.is_heating_on = not self.is_heating_on
        self.is_heating_on1 = False
        self.is_heating_on2 = False
        self.is_heating_on3 = False
        
        if self.is_heating_on:
            self.canvas.itemconfig(self.btn_heating, fill="green")
            self.canvas.itemconfig(self.btn_heating1, fill="red")
            self.canvas.itemconfig(self.btn_heating2, fill="red")
            self.canvas.itemconfig(self.btn_heating3, fill="red")
        else:
            self.canvas.itemconfig(self.btn_heating, fill="red")
            self.canvas.itemconfig(self.btn_heating1, fill="gray")
            self.canvas.itemconfig(self.btn_heating2, fill="gray")
            self.canvas.itemconfig(self.btn_heating3, fill="gray")
            

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
    
    def toggle_reflux(self):
        self.is_reflux_on = not self.is_reflux_on
        if self.is_reflux_on:
            self.canvas.itemconfig(self.btn_reflux, fill="green")
        else:
            self.canvas.itemconfig(self.btn_reflux, fill="red")

    #Filter methods for database history
    def toggle_filter_censor1(self):
        self.is_filter_censor1_on = not self.is_filter_censor1_on
        if self.is_filter_censor1_on:
            self.canvas.itemconfig(self.btn_filter_censor1, fill="green")
        else:
            self.canvas.itemconfig(self.btn_filter_censor1, fill="red")
        self.refresh_data()

    def toggle_filter_censor2(self):
        self.is_filter_censor2_on = not self.is_filter_censor2_on
        if self.is_filter_censor2_on:
            self.canvas.itemconfig(self.btn_filter_censor2, fill="green")
        else:
            self.canvas.itemconfig(self.btn_filter_censor2, fill="red")
        self.refresh_data()

    def toggle_filter_censor3(self):
        self.is_filter_censor3_on = not self.is_filter_censor3_on
        if self.is_filter_censor3_on:
            self.canvas.itemconfig(self.btn_filter_censor3, fill="green")
        else:
            self.canvas.itemconfig(self.btn_filter_censor3, fill="red")
        self.refresh_data()

    def toggle_filter_censor4(self):
        self.is_filter_censor4_on = not self.is_filter_censor4_on
        if self.is_filter_censor4_on:
            self.canvas.itemconfig(self.btn_filter_censor4, fill="green")
        else:
            self.canvas.itemconfig(self.btn_filter_censor4, fill="red")
        self.refresh_data()


    def refresh_data(self):
        self.update_temp()
        try:

            active_sensors = []
            if self.is_filter_censor1_on: active_sensors.append("T1")
            if self.is_filter_censor2_on: active_sensors.append("T2")
            if self.is_filter_censor3_on: active_sensors.append("T3")
            if self.is_filter_censor4_on: active_sensors.append("T4")

            if not active_sensors or self.current_id_session is None:
                for item in self.tree.get_children():
                    self.tree.delete(item)
                self.ax.clear()
                self.canvas_graphic.draw()
            else:
                conn = sqlite3.connect('db/him_distill.db')
                cursor = conn.cursor()

                placeholders = ', '.join(['?'] * len(active_sensors))
                query = f"SELECT sensor_name, temperature, timestamp FROM temperature_readings WHERE sensor_name IN ({placeholders}) AND session_id = ? ORDER BY id DESC LIMIT 30"
                
                cursor.execute(query, (*active_sensors, self.current_id_session))
                rows = cursor.fetchall()
                conn.close()

                
                for item in self.tree.get_children():
                    self.tree.delete(item)

                for row in rows[:15]:
                    name, temp, full_time = row
                    time_display = full_time.split()[-1]
                    self.tree.insert("", tk.END, values=(name, f"{temp:.2f}", time_display))
                    

                self.ax.clear()
                self.ax.set_title("Graphique Température")

                sensor_data = {sensor: {'x': [], 'y': []} for sensor in active_sensors}

                for row in reversed(rows): 
                    name, temp, full_time = row
                    if name in sensor_data:
                        try:
                            dt_obj = datetime.strptime(full_time, '%Y-%m-%d %H:%M:%S')
                            sensor_data[name]['x'].append(dt_obj)
                            sensor_data[name]['y'].append(temp)
                        except ValueError:
                            continue
                
                colors = {"T1": "blue", "T2": "orange", "T3": "green", "T4": "red"}

                has_legend = False
                for sensor, data in sensor_data.items():
                    if data['x']:
                        self.ax.plot(data['x'], data['y'], label=sensor, color=colors.get(sensor, "black"))
                        has_legend = True

                self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

                #Legend don't draw herself if no data
                if has_legend:   
                    self.ax.legend(loc="upper left", fontsize=10)

                self.canvas_graphic.draw()

        except Exception as e:
            print(f"Error : {e}")

        self.root.after(2000, self.refresh_data)
    
    def update_temp(self):
        conn = sqlite3.connect('db/him_distill.db')
        cursor = conn.cursor()
        cursor.execute("SELECT sensor_name, temperature, timestamp FROM temperature_readings WHERE session_id = ? ORDER BY id DESC LIMIT 30", (self.current_id_session,))
        rows = cursor.fetchall()
        conn.close()

        if rows :
            value_temp = {row[0]: row[1] for row in reversed(rows)}

            sensors_map = {
                "T1": self.temp_sensor1,
                "T2": self.temp_sensor2,
                "T3": self.temp_sensor3,
                "T4": self.temp_sensor4
            }

            for name, canvas_id in sensors_map.items():
                if name in value_temp:
                    new_temp = f"{value_temp[name]:.2f}°C"
                    self.canvas.itemconfig(canvas_id, text=new_temp, fill="red")



    def menu(self):
        self.menu_bar = tk.Menu(self.root)

        self.history_menu = tk.Menu(self.menu_bar, postcommand=self.update_history)
        self.menu_bar.add_cascade(label="historique des Sessions", menu=self.history_menu)
        self.menu_bar.add_command(label="Nouvelle Session", command=self.start_session)
        self.menu_bar.add_command(label="Exporter la session", command=self.export_session)
        self.menu_bar.add_command(label="Supprimer les sessions", command=self.delete_sessions)

        self.root.config(menu=self.menu_bar)

    def start_session(self):
        conn = sqlite3.connect('db/him_distill.db')
        cursor = conn.cursor()
        name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO sessions (start_time) VALUES (?)", (name,))
        self.current_id_session = cursor.lastrowid
        conn.commit()
        conn.close()
    

    def update_history(self):
        self.history_menu.delete(0, tk.END)#clear existing list
        try:
            conn = sqlite3.connect('db/him_distill.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, start_time FROM sessions ORDER BY id DESC LIMIT 15")
            sessions = cursor.fetchall()
            conn.close()

            for session_id, session_date in sessions:
                self.history_menu.add_command(label=f"Session du {session_date}", command=lambda id=session_id: self.load_session(id))
        except Exception as e:
            print(f"Error : {e}")

    def load_session(self, session_id):
        self.current_id_session = session_id
        self.refresh_data()

    def export_session(self):
        if self.current_id_session is None:
            messagebox.showwarning("Avertissement", "Aucune session active à exporter.")
            return
    
        path_file = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Exporter la session",
            initialfile=f"session_{self.current_id_session}.csv"
        )

        if not path_file:
            return
        else :
            try:
                conn = sqlite3.connect('db/him_distill.db')
                cursor = conn.cursor()
                cursor.execute("SELECT sensor_name, temperature, timestamp FROM temperature_readings WHERE session_id = ? ORDER BY timestamp ASC", (self.current_id_session,))
                rows = cursor.fetchall()
                conn.close()

                if not rows:
                    messagebox.showinfo("Information", "Aucune donnée à exporter pour cette session.")
                    return
                
                with open(path_file, mode='w', newline='', encoding="utf-8") as file:
                    writer = csv.writer(file, delimiter=";")
                    writer.writerow(["Capteur", "Temp", "Timestamp"])
                    writer.writerows(rows)
                messagebox.showinfo("Succès", f"Session exportée avec succès vers {path_file}")
            except Exception as e:
                messagebox.showerror("Erreur", {e})

    def delete_sessions(self):
        if messagebox.askyesno("Confirmer", "Cette action aura pour conséquence de supprimer la session en cours et toutes les données associées. Voulez-vous continuer ?"):
            try:
                conn = sqlite3.connect('db/him_distill.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM sessions WHERE id = ?", (self.current_id_session,))
                cursor.execute("DELETE FROM temperature_readings WHERE session_id = ?", (self.current_id_session,))
                conn.commit()
                conn.close()
                self.current_id_session = None
                self.refresh_data()
                messagebox.showinfo("Succès", "Session supprimée avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur",{e})

        




root = tk.Tk()
window = Window(root)
root.mainloop()