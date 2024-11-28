import sqlite3
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
from tkinter import Tk, Canvas, Button, PhotoImage, StringVar, messagebox, Entry, ttk, IntVar, Scrollbar, Frame


# Define paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\enzil\PycharmProjects\pythonProject1\buildregister\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Initialize the window
window = Tk()
window.geometry("1920x1200")
window.configure(bg="#FFFFFF")

canvas = Canvas(window, bg="#FFFFFF", height=1200, width=1920, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)



#background
image_background = r'C:\Users\enzil\PycharmProjects\pythonProject1\buildregister\assets\frame0\backgroundadmin.jpeg'
bg_image = Image.open(image_background)
bg_image = bg_image.resize((1920, 1200), Image.LANCZOS)  # Resize to window size
bg_image_tk = ImageTk.PhotoImage(bg_image)
canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)
canvas.bg_image_tk = bg_image_tk

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(file=relative_to_assets("background.png"))
image_1 = canvas.create_image(960.0,643.0,image=image_image_1)

image_head = PhotoImage(file=relative_to_assets("head.png"))
header = canvas.create_image(960.0, 50.0, image=image_head)

canvas.create_text(220.0, 24.0, anchor="nw", text="Car Rental System", fill="#FFFFFF", font=("Helvetica", 25, "bold"))

car_types = {"Sedan": IntVar(), "SUV": IntVar(), "Truck": IntVar(), "Minivan": IntVar(), "Hatchback": IntVar()}
rate_range = {"< RM100": IntVar(), "RM100-RM200": IntVar(), "RM200-RM300": IntVar(), "RM300 >": IntVar()}
seating_capacity = {2: IntVar(), 5: IntVar(), 6: IntVar(), 7: IntVar()}

# Function to handle hover color on enter
def on_enter_button(e):
    e.widget.config(bg="#90EE90")  # Light green hover color

def on_leave_button(e):
    e.widget.config(bg="#006400")  # Dark green normal color

def on_click_button(e):
    e.widget.config(bg="#90EE90")  # Stay light green on click

def on_click_back_button(e):
    e.widget.config(bg="#4CAF50")  # Change the background to #4CAF50 when clicked
    go_back()  # Trigger the back button action


def go_back():
    messagebox.showinfo("Back", "Going back to the previous page")

backbutton_path = r'C:\Users\enzil\PycharmProjects\pythonProject1\buildregister\assets\frame0\backbutton.png'
backbutton = Image.open(backbutton_path)
backbutton = backbutton.resize((50, 50), Image.LANCZOS)
backbutton = ImageTk.PhotoImage(backbutton)

back_button = Button(window, image=backbutton, bg="#4CAF50", bd=0, highlightthickness=0, activebackground="#4CAF50", command=go_back)
back_button.place(x=100, y=15)
back_button.bind("<Enter>", on_enter_button)
back_button.bind("<Leave>", on_leave_button)
back_button.bind("<Button-1>", on_click_back_button)
canvas.img1 = backbutton



# Create navigation buttons (Home, Search, Bookings, Reviews, Support)
home_button = Button(text="Home", bg="#006400", fg="white", borderwidth=0, highlightthickness=0, command=lambda: print("Home button clicked"), relief="flat", font=("Calibri", 15))
home_button.place(x=970.0, y=27.0, width=130.0, height=37.617591857910156)
home_button.bind("<Enter>", on_enter_button)
home_button.bind("<Leave>", on_leave_button)
home_button.bind("<Button-1>", on_click_button)

search_button = Button(text="Search Car", bg="#006400", fg="white", borderwidth=0, highlightthickness=0, command=lambda: print("Search button clicked"), relief="flat", font=("Calibri", 15))
search_button.place(x=1120.0, y=27.0, width=130.0, height=37.617591857910156)
search_button.bind("<Enter>", on_enter_button)
search_button.bind("<Leave>", on_leave_button)
search_button.bind("<Button-1>", on_click_button)

bookings_button = Button(text="Bookings", bg="#006400", fg="white", borderwidth=0, highlightthickness=0, command=lambda: print("Bookings button clicked"), relief="flat", font=("Calibri", 15))
bookings_button.place(x=1270.0, y=27.0, width=130.0, height=37.617591857910156)
bookings_button.bind("<Enter>", on_enter_button)
bookings_button.bind("<Leave>", on_leave_button)
bookings_button.bind("<Button-1>", on_click_button)

reviews_button = Button(text="Reviews", bg="#006400", fg="white", borderwidth=0, highlightthickness=0, command=lambda: print("Reviews button clicked"), relief="flat", font=("Calibri", 15))
reviews_button.place(x=1420.0, y=27.0, width=130.0, height=37.617591857910156)
reviews_button.bind("<Enter>", on_enter_button)
reviews_button.bind("<Leave>", on_leave_button)
reviews_button.bind("<Button-1>", on_click_button)

support_button = Button(text="Support", bg="#006400", fg="white", borderwidth=0, highlightthickness=0, command=lambda: print("Support button clicked"), relief="flat", font=("Calibri", 15))
support_button.place(x=1570.0, y=27.0, width=130.0, height=37.617591857910156)
support_button.bind("<Enter>", on_enter_button)
support_button.bind("<Leave>", on_leave_button)
support_button.bind("<Button-1>", on_click_button)

canvas.create_text(177.0, 243.0, anchor="nw", text="Showing All Vehicles Results", fill="#000000", font=("Inter Italic", 32 * -1))


def fetch_car_details(filter_query=None):
    conn = sqlite3.connect("customer_registration.db")
    cursor = conn.cursor()
    if filter_query:
        cursor.execute(
            f"SELECT car_plate, make_model, car_type, rate, seating_capacity, image_path FROM car WHERE {filter_query}")
    else:
        cursor.execute("SELECT car_plate, make_model, car_type, rate, seating_capacity, image_path FROM car")
    cars = cursor.fetchall()
    conn.close()
    return cars
main_frame = Frame(window, bg="#FFFFFF")
main_frame.place(x=200, y=300, width=1500, height=800)

# Create a canvas within the main_frame
canvas_frame = Canvas(main_frame, bg="#FFFFFF")
canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a scrollbar to the canvas
scrollbar = Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas_frame.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas to respond to the scrollbar
canvas_frame.configure(yscrollcommand=scrollbar.set)
canvas_frame.bind("<Configure>", lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all")))

# Create a frame inside the canvas to hold the car data
scrollable_frame = Frame(canvas_frame, bg="#FFFFFF")
canvas_frame.create_window((0, 0), window=scrollable_frame, anchor="nw")
# Modify the display_car_data function to display cars in the scrollable frame
def display_car_data(cars):
    # Clear previous car data
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    x_start = 50
    y_start = 0
    x_offset = 647
    y_offset = 400
    max_columns = 3

    for index, car in enumerate(cars):
        x_position = x_start + (index % max_columns) * x_offset
        y_position = y_start + (index // max_columns) * y_offset

        car_plate, make_model, car_type, rate, seating_capacity, image_path = car

        try:
            car_image = Image.open(image_path)
            car_image = car_image.resize((350, 250), Image.LANCZOS)
            car_image_tk = ImageTk.PhotoImage(car_image)

            car_label = tk.Label(scrollable_frame, image=car_image_tk)
            car_label.image = car_image_tk
            car_label.grid(row=index // max_columns, column=index % max_columns, padx=10, pady=10)

            details_text = f"{make_model}\n{car_type} - {seating_capacity} Seats\nRate: {rate}"
            details_label = tk.Label(scrollable_frame, text=details_text, font=("Calibri", 14), bg="#FFFFFF")
            details_label.grid(row=(index // max_columns) + 1, column=index % max_columns, padx=10, pady=10)

        except Exception as e:
            print(f"Error loading image: {e}")
            placeholder_image = Image.open("path_to_placeholder.png")
            placeholder_image = placeholder_image.resize((350, 250), Image.LANCZOS)
            car_image_tk = ImageTk.PhotoImage(placeholder_image)
            car_label = tk.Label(scrollable_frame, image=car_image_tk)
            car_label.image = car_image_tk
            car_label.grid(row=index // max_columns, column=index % max_columns, padx=10, pady=10)

def apply_filters():
    search_text = search_var.get()
    car_type = car_type_var.get()
    rate_range = rate_var.get()
    seating_capacity = seat_var.get()

    filters = []
    if search_text:
        filters.append(f"make_model LIKE '%{search_text}%'")
    if car_type:
        filters.append(f"car_type = '{car_type}'")
    if rate_range:
        if rate_range == "< RM100":
            filters.append("rate < 100")
        elif rate_range == "RM100-RM200":
            filters.append("rate BETWEEN 100 AND 200")
        elif rate_range == "RM200-RM300":
            filters.append("rate BETWEEN 200 AND 300")
        elif rate_range == "RM300 >":
            filters.append("rate > 300")
    if seating_capacity:
        filters.append(f"seating_capacity = {seating_capacity}")

    filter_query = " AND ".join(filters) if filters else None
    cars = fetch_car_details(filter_query)
    display_car_data(cars)

def apply_filters():
    search_text = search_var.get()
    car_type = car_type_var.get()
    rate_range = rate_var.get()
    seating_capacity = seat_var.get()

    filters = []
    if search_text:
        filters.append(f"make_model LIKE '%{search_text}%'")
    if car_type:
        filters.append(f"car_type = '{car_type}'")
    if rate_range:
        if rate_range == "< RM100":
            filters.append("rate < 100")
        elif rate_range == "RM100-RM200":
            filters.append("rate BETWEEN 100 AND 200")
        elif rate_range == "RM200-RM300":
            filters.append("rate BETWEEN 200 AND 300")
        elif rate_range == "RM300 >":
            filters.append("rate > 300")
    if seating_capacity:
        filters.append(f"seating_capacity = {seating_capacity}")

    filter_query = " AND ".join(filters) if filters else None
    cars = fetch_car_details(filter_query)
    display_car_data(cars)

# Search input box and filter dropdown
search_button = Button(window, text="Search", bg="#006400", fg="white", borderwidth=0, highlightthickness=0,
                       command=apply_filters, relief="flat", font=("Calibri", 15))
search_button.place(x=1220.0, y=166.0, width=130.0, height=40.0)

search_var = StringVar()
search_entry = Entry(window, textvariable=search_var, font=("Calibri", 15), width=35)
search_entry.place(x=860.0, y=166.0, width=350.0, height=40.0)

car_type_var = StringVar(value="")
car_type_combobox = ttk.Combobox(window, textvariable=car_type_var, values=["", "Sedan", "Hatchback", "Minivan", "Truck", "SUV"], font=("Calibri", 15))
car_type_combobox.place(x=860.0, y=220.0, width=150.0)

rate_var = StringVar(value="")
rate_combobox = ttk.Combobox(window, textvariable=rate_var, values=["", "< RM100", "RM100-RM200", "RM200-RM300", "RM300 >"], font=("Calibri", 15))
rate_combobox.place(x=1030.0, y=220.0, width=150.0)

seat_var = IntVar(value=0)
seating_capacity_combobox = ttk.Combobox(window, textvariable=seat_var, values=[5, 6, 7], font=("Calibri", 15))
seating_capacity_combobox.place(x=1200.0, y=220.0, width=150.0)

# Search button
search_button = Button(window, text="Search", bg="#006400", fg="white", borderwidth=0, highlightthickness=0,
                       command=apply_filters, relief="flat", font=("Calibri", 15))
search_button.place(x=1220.0, y=166.0, width=130.0, height=40.0)

# Apply filters button
apply_filter_button = Button(text="Apply Filters", bg="#006400", fg="white", borderwidth=0, highlightthickness=0, command=apply_filters, relief="flat", font=("Calibri", 15))
apply_filter_button.place(x=1370.0, y=220.0, width=130.0, height=40.0)


car_data = fetch_car_details()
display_car_data(car_data)
window.resizable(False, False)
window.mainloop()
