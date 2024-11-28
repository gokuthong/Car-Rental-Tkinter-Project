import sqlite3
from pathlib import Path
from PIL import Image, ImageTk
from chen.buildregister.headeradmin import create_header
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox, Entry, ttk, filedialog
import importlib
import re


def main_window():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0")


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    def create_car_table():
        conn = sqlite3.connect(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
        cursor = conn.cursor()

        # Create the car table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS car (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_plate TEXT NOT NULL,
            make_model TEXT NOT NULL,
            car_type TEXT NOT NULL,
            rate REAL NOT NULL,
            seating_capacity INTEGER NOT NULL,
            colour TEXT NOT NULL,
            location TEXT NOT NULL,
            image_path TEXT
            is_rented INTEGER DEFAULT 0
        );
        """)

        conn.commit()
        conn.close()

    # Call the function to create the car table
    create_car_table()

    window = Tk()

    window.geometry("1920x1200")
    window.configure(bg = "#FFFFFF")


    canvas = Canvas(window,bg = "#FFFFFF",height = 1200,width = 1920,bd = 0,highlightthickness = 0,relief = "ridge")

    def upload_car_image():
        global image_path  # Use global variable to store image path
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
        )
        if file_path:
            image_path = file_path  # Store the file path in the global variable
            car_image = Image.open(file_path)
            car_image = car_image.resize((500, 380), Image.LANCZOS)  # Resize the image for display
            car_image_tk = ImageTk.PhotoImage(car_image)
            canvas.create_image(1404, 580, image=car_image_tk)  # Display the image on the canvas
            canvas.img_car = car_image_tk  # Keep a reference to the image

    def validate_car_plate(car_plate):
        """Validate the car plate using regex"""
        pattern = r'^[A-Z]{1,3} ?\d{1,4}$'  # 1-3 uppercase letters followed by 1-4 digits
        if re.match(pattern, car_plate):
            return True
        else:
            messagebox.showerror("Invalid Car Plate", "Please enter a valid Malaysian car plate (e.g., ABC 1234).")
            return False

    def import_car_data():
        try:
            car_plate = entry_plate.get()
            make_model = entry_model.get()
            car_type = car_type_combobox.get()
            rate = float(entry_rate.get())
            seating_capacity = int(entry_seat.get())
            colour = entry_colour.get()
            location = car_location_combobox.get()

            # Check if any field is empty
            if not car_plate or not make_model or not car_type or not rate or not seating_capacity or not colour or not location:
                messagebox.showerror("Missing Fields", "All fields must be filled out.")
                return

            # Validate Car Plate format using regex
            if not validate_car_plate(car_plate):
                return

            # Validate numeric fields
            try:
                rate = float(rate)
                if rate <= 0:
                    messagebox.showerror("Invalid Input", "Rate must be greater than 0.")
                    return
            except ValueError:
                messagebox.showerror("Invalid Input", "Rate must be a valid number.")
                return

            try:
                seating_capacity = int(seating_capacity)
                if seating_capacity <= 0:
                    messagebox.showerror("Invalid Input", "Seating capacity must be greater than 0.")
                    return
            except ValueError:
                messagebox.showerror("Invalid Input", "Seating capacity must be a valid number.")
                return

            # Ensure that an image was uploaded
            if not image_path:
                messagebox.showerror("Error", "Please upload a car image.")
                return

            # Insert the data into the SQLite database
            conn = sqlite3.connect(
                r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
            cursor = conn.cursor()

            cursor.execute("""
                    INSERT INTO car (car_plate, make_model, car_type, rate, seating_capacity, colour, location, image_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (car_plate, make_model, car_type, rate, seating_capacity, colour, location, image_path))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Car information imported successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    # Add an "Add Car Image" button to upload the image
    add_image_button = Button(window, text="Add Car Image", bg="#006400", fg="white", font=("Calibri", 15), command=upload_car_image)
    add_image_button.place(x=1320.0, y=788.0, width=150.0, height=50.0)

    # Add an "Import Car Data" button to trigger the import function
    import_button = Button(window, text="Import", bg="#006400", fg="white", font=("Calibri", 18, "bold"), command=import_car_data)
    import_button.place(x=1220.0, y=988.0, width=330.0, height=52.0)


    canvas.place(x = 0, y = 0)
    image_background = r'C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0\backgroundadmin.jpeg'
    bg_image = Image.open(image_background)
    bg_image = bg_image.resize((1920, 1200), Image.LANCZOS)  # Resize to window size
    bg_image_tk = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)
    canvas.bg_image_tk = bg_image_tk


    # Title text
    canvas.create_text(220.0, 24.0, anchor="nw", text="Car Rental System", fill="#FFFFFF", font=("Helvetica", 25, "bold"))

    # Function to handle hover color on enter
    def on_enter_button(e):
        e.widget.config(bg="#90EE90")  # Light green hover color

    def on_leave_button(e):
        e.widget.config(bg="#006400")  # Dark green normal color

    def on_click_button(e):
        e.widget.config(bg="#90EE90")  # Stay light green on click

    def on_click_back_button(e):
        e.widget.config(bg="#4CAF50")  # Change the background to #4CAF50 when clicked
        goto_admindashboard()  # Trigger the back button action

    # Back button functionality
    def goto_admindashboard():
        window.destroy()
        dashboard = importlib.import_module("admindashboard")

        dashboard.main_window()

    # Add the back button and align it with the title
    backbutton_path = r'C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0\backbutton.png'
    backbutton = Image.open(backbutton_path)
    backbutton = backbutton.resize((50, 50), Image.LANCZOS)
    backbutton = ImageTk.PhotoImage(backbutton)

    # Place the back button at the top-left, aligning with the title
    back_button = Button(window, image=backbutton, bg="#4CAF50", bd=0, highlightthickness=0, activebackground="#4CAF50", command=goto_admindashboard)
    back_button.place(x=100, y=15)  # Adjust position to align with the title
    back_button.bind("<Enter>", on_enter_button)
    back_button.bind("<Leave>", on_leave_button)
    back_button.bind("<Button-1>", on_click_back_button)  # Apply custom click event for back button

    canvas.img1 = backbutton  # Keep a reference to the image

    image_import_head = PhotoImage(file=relative_to_assets("import_head.png"))
    import_head = canvas.create_image( 960.0, 283.0, image=image_import_head)




    image_image_4 = PhotoImage(file=relative_to_assets("import_background.png"))
    image_4 = canvas.create_image(960.0,734.0,image=image_image_4)

    canvas.create_text(330.0,272.0,anchor="nw",text="Import Car",fill="#FFFFFF",font=("Inter ExtraBold", 35 * -1))


    importcar_path = r'C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0\import_car.png'
    importcar = Image.open(importcar_path)
    importcar = importcar.resize((500, 380), Image.LANCZOS)
    importcar = ImageTk.PhotoImage(importcar)
    import_car = canvas.create_image(1404.0, 580.0, image=importcar)


    canvas.create_text(330.0, 395.0, anchor="nw", text="No.Car Plate:", fill="#000000", font=("Inter Bold", 28 * -1))
    entry_plate = Entry(bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Calibri",21))
    entry_plate.place(x=556.0, y=388.0, width=300.0, height=52.0)

    canvas.create_text(330.0, 495.0, anchor="nw", text="Make & Model:", fill="#000000", font=("Inter Bold", 28 * -1))
    entry_model = Entry(bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Calibri", 21))
    entry_model.place(x=556.0, y=488.0, width=429.0, height=52.0)

    car_type_label = canvas.create_text(330.0, 595.0, anchor="nw", text="Car Type:", fill="#000000", font=("Inter Bold", 28 * -1))
    car_types = ["-", "Sedan", "SUV", "Truck", "Minivan", "Hatchback"]
    car_type_combobox = ttk.Combobox(window, values=car_types, font=("Calibri", 21))
    car_type_combobox.place(x=556.0, y=588.0, width=429.0, height=52.0)
    car_type_combobox.current(0)

    canvas.create_text(330.0, 695.0, anchor="nw", text="Rate (RM):", fill="#000000", font=("Inter Bold", 28 * -1))
    entry_rate = Entry(bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Calibri", 21))
    entry_rate.place(x=556.0, y=688.0, width=127.0, height=52.0)

    canvas.create_text(330.0, 795.0, anchor="nw", text="Seating Capacity:", fill="#000000", font=("Inter Bold", 28 * -1))
    entry_seat = Entry(bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Calibri", 21))
    entry_seat.place(x=556.0, y=788.0, width=127.0, height=52.0)

    canvas.create_text(330.0, 895.0, anchor="nw", text="Colour:", fill="#000000", font=("Inter Bold", 28 * -1))
    entry_colour = Entry(bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Calibri", 21))
    entry_colour.place(x=556.0, y=888.0, width=127.0, height=52.0)

    car_location_label = canvas.create_text(330.0, 995.0, anchor="nw", text="Location:", fill="#000000", font=("Inter Bold", 28 * -1))
    location = ["-", "Queensbay Mall, Bayan Lepas", "Setia Triangle, Bayan Lepas", "Gurney Plaza, Pulau Tikus"]
    car_location_combobox = ttk.Combobox(window, values=location, font=("Calibri", 21))
    car_location_combobox.place(x=556.0, y=988.0, width=429.0, height=52.0)
    car_location_combobox.current(0)

    create_header(window, canvas)


    window.resizable(False, False)
    window.mainloop()

if __name__ == '__main__':
    main_window()