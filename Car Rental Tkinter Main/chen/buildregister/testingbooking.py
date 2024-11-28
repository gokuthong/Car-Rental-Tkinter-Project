import sqlite3
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
from chen.buildregister.header import create_header
from tkinter import Tk, Canvas, Button, PhotoImage, StringVar, messagebox, Entry, ttk, IntVar, Scrollbar, Frame
import json
from datetime import datetime

def main_window():
    # Define paths
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    global current_user_id
    try:
        with open(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\user_session.json", "r") as file:
            data = json.load(file)
            current_user_id = data["id"]
            print(f"Current User ID: {current_user_id}")
    except FileNotFoundError:
        print("User session file not found.")
        current_user_id = None


    # Initialize the window
    window = Tk()
    window.geometry("1920x1200")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=1200, width=1920, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)



    #background
    image_background = r'C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0\background.png'
    bg_image = Image.open(image_background)
    bg_image = bg_image.resize((1920, 1200), Image.LANCZOS)  # Resize to window size
    bg_image_tk = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)
    canvas.bg_image_tk = bg_image_tk



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

    backbutton_path = r'C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0\backbutton.png'
    backbutton = Image.open(backbutton_path)
    backbutton = backbutton.resize((50, 50), Image.LANCZOS)
    backbutton = ImageTk.PhotoImage(backbutton)

    back_button = Button(window, image=backbutton, bg="#4CAF50", bd=0, highlightthickness=0, activebackground="#4CAF50", command=go_back)
    back_button.place(x=100, y=15)
    back_button.bind("<Enter>", on_enter_button)
    back_button.bind("<Leave>", on_leave_button)
    back_button.bind("<Button-1>", on_click_back_button)
    canvas.img1 = backbutton




    canvas.create_text(250.0, 243.0, anchor="nw", text="Showing All Vehicles Results", fill="Black", font=("Inter Italic", 32 * -1, "bold"))



    def fetch_car_details(filter_query=None):
        conn = sqlite3.connect(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
        cursor = conn.cursor()
        if filter_query:
            cursor.execute(
                f"SELECT car_plate, make_model, car_type, rate, seating_capacity, colour, image_path FROM car WHERE {filter_query}"
            )
        else:
            cursor.execute("SELECT car_plate, make_model, car_type, rate, seating_capacity, colour, image_path FROM car")
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
    scrollable_frame = Frame(canvas_frame, bg="ivory")
    canvas_frame.create_window((0, 0), window=scrollable_frame, anchor="nw")


    def add_booking(car_id, customer_id, pickup_location, dropoff_location, pickup_date, dropoff_date):
        # Ensure customer_id and car_id are valid
        if not car_id or not customer_id:
            messagebox.showerror("Error", "Invalid car or customer ID.")
            return

        # Ensure required fields are not None
        if not pickup_location or not dropoff_location or not pickup_date or not dropoff_date:
            messagebox.showerror("Error", "Missing booking details.")
            return

        # Convert dates to proper format (if they are in string format)
        try:
            pickup_date = datetime.strptime(pickup_date, "%Y-%m-%d").date()
            dropoff_date = datetime.strptime(dropoff_date, "%Y-%m-%d").date()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid date format: {e}")
            return

        # Ensure dropoff_date is after pickup_date
        if dropoff_date < pickup_date:
            messagebox.showerror("Error", "Dropoff date must be after pickup date.")
            return

        # Connect to the database
        conn = sqlite3.connect(
            r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
        cursor = conn.cursor()

        # Insert booking into the bookings table
        try:
            cursor.execute("""
                INSERT INTO bookings (car_id, customer_id, pickup_location, dropoff_location, pickup_date, dropoff_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (car_id, customer_id, pickup_location, dropoff_location, pickup_date, dropoff_date, "in_cart"))

            conn.commit()
            messagebox.showinfo("Success", "Booking added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while adding the booking: {e}")
        finally:
            conn.close()


    def car_clicked(car_plate, make_model, car_type, rate, seating_capacity):
        # Get the car_id from the database based on car_plate
        conn = sqlite3.connect(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM car WHERE car_plate = ?", (car_plate,))
        result = cursor.fetchone()
        conn.close()

        if result:
            car_id = result[0]  # Assuming the first column is the ID
        else:
            messagebox.showerror("Error", "Car ID not found.")
            return

        # Show car details in a pop-up
        details = (
            f"Car Plate: {car_plate}\n"
            f"Make & Model: {make_model}\n"
            f"Type: {car_type}\n"
            f"Rate: RM{rate:.2f}\n"
            f"Seating Capacity: {seating_capacity}"
        )

        # Display car details and ask user if they want to add the car to their cart
        response = messagebox.askyesno("Car Details", f"{details}\n\nDo you want to add this car to your cart?")

        def add_to_cart():
            # Logic to add car to the cart (e.g., add to database)
            # Use the car_id and current_user_id here
            # Load search parameters from JSON for booking details
            try:
                with open(
                        r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\SearchPage\search_params.json",
                        "r") as file:
                    search_params = json.load(file)
                    pickup_location = search_params.get("pickup_location", None)
                    dropoff_location = search_params.get("dropoff_location", None)
                    pickup_date = search_params.get("pickup_date", None)
                    dropoff_date = search_params.get("dropoff_date", None)
            except FileNotFoundError:
                print("Search parameters file not found.")
                pickup_location = dropoff_location = pickup_date = dropoff_date = None

            # Set user booking to 1 / True
            with open(
                    r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\user_booking.json",
                    "w") as file:
                json.dump({"has_booking": 1}, file)

            # Validate that we have all the necessary details
            if not pickup_location or not dropoff_location or not pickup_date or not dropoff_date:
                messagebox.showerror("Error", "Missing booking details.")
                return

            add_booking(car_id, current_user_id, pickup_location, dropoff_location, pickup_date, dropoff_date)

        # If the user clicks 'Yes', proceed with adding to cart logic
        if response:
            add_to_cart()


    def display_car_data(cars):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        num_columns = 3  # Number of cars per row
        car_width = 350  # Approximate width of each car image
        frame_width = 1500  # Width of the scrollable frame

        # Calculate padding to balance spacing
        total_padding = frame_width - (num_columns * car_width)
        left_padding = total_padding // (num_columns + 1)

        for index, car in enumerate(cars):
            row = index // num_columns
            column = index % num_columns

            car_plate, make_model, car_type, rate, seating_capacity, colour, image_path = car

            try:
                car_image = Image.open(image_path)
                car_image = car_image.resize((350, 250), Image.LANCZOS)
                car_image_tk = ImageTk.PhotoImage(car_image)

                # Set padding for the first and last items in each row
                if column == 0:
                    padx = (left_padding, left_padding // 2)
                elif column == num_columns - 1:
                    padx = (left_padding // 2, left_padding)
                else:
                    padx = (left_padding // 2, left_padding // 2)

                # Display car image
                car_label = tk.Label(scrollable_frame, image=car_image_tk, bg="#FFFFFF")
                car_label.image = car_image_tk
                car_label.grid(row=row * 2, column=column, padx=padx, pady=10)

                # Bind the click event to car_label
                car_label.bind("<Button-1>", lambda e, cp=car_plate, mm=make_model, ct=car_type, rt=rate, sc=seating_capacity:
                               car_clicked(cp, mm, ct, rt, sc))

                # Display car details below the image, including color and car plate
                details_text = f"Plate: {car_plate}\n{make_model} - Colour: {colour}\n{car_type} - {seating_capacity} Seats\nRate: RM{rate:.2f}"
                details_label = tk.Label(scrollable_frame, text=details_text, font=("Calibri", 14), bg="ivory")
                details_label.grid(row=row * 2 + 1, column=column, padx=padx, pady=10)

            except Exception as e:
                print(f"Error loading image: {e}")
                # # Load a placeholder image if needed
                # placeholder_image = Image.open("path_to_placeholder.png")
                # placeholder_image = placeholder_image.resize((350, 250), Image.LANCZOS)
                # car_image_tk = ImageTk.PhotoImage(placeholder_image)
                # car_label = tk.Label(scrollable_frame, image=car_image_tk, bg="#FFFFFF")
                # car_label.image = car_image_tk
                # car_label.grid(row=row * 2, column=column, padx=padx, pady=10)

        # Update the scroll region to accommodate new widgets
        canvas_frame.update_idletasks()
        canvas_frame.configure(scrollregion=canvas_frame.bbox("all"))



    def apply_filters():
        search_text = search_var.get()
        car_type = car_type_var.get()
        rate_range = rate_var.get()
        seating_capacity = seat_var.get()

        filters = []

        # Load search parameters from JSON file for pickup location
        try:
            with open(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\SearchPage\search_params.json", "r") as file:
                search_params = json.load(file)
                pickup_location = search_params.get("pickup_location", None)
        except FileNotFoundError:
            print("Search parameters file not found.")
            pickup_location = None

        # Add pickup location filter if it exists
        if pickup_location:
            filters.append(f"location = '{pickup_location}'")

        # Add other filters based on user input
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

    search_button = Button(window, text="Search", bg="#006400", fg="white", borderwidth=0, highlightthickness=0,
                           command=apply_filters, relief="flat", font=("Calibri", 15))
    search_button.place(x=1220.0, y=166.0, width=130.0, height=40.0)

    # Apply filters button
    apply_filter_button = Button(text="Apply Filters", bg="#006400", fg="white", borderwidth=0, highlightthickness=0, command=apply_filters, relief="flat", font=("Calibri", 15))
    apply_filter_button.place(x=1370.0, y=220.0, width=130.0, height=40.0)

    # Load search parameters from JSON file
    try:
        with open(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\SearchPage\search_params.json", "r") as file:
            search_params = json.load(file)
            pickup_location = search_params.get("pickup_location", None)  # Use None as default if not found
    except FileNotFoundError:
        print("Search parameters file not found.")
        pickup_location = None

    # Define the filter for initial load
    initial_filter_query = f"location = '{pickup_location}'" if pickup_location else None

    # Call header creation after the canvas
    create_header(window, canvas)

    # Fetch and display cars with initial filter
    car_data = fetch_car_details(initial_filter_query)
    display_car_data(car_data)

    window.resizable(False, False)
    window.mainloop()

if __name__ == '__main__':
    main_window()

