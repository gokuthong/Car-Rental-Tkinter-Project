import importlib
from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Frame, Scrollbar, Entry, Listbox, font as tkFont, Toplevel, filedialog, messagebox
import sqlite3
from chen.buildregister.header import create_header
import os
from PIL import Image, ImageTk
from kit.Payment import gui
from datetime import datetime
from chen.buildregister import testingbooking
import json


def main_window():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(
        r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\ConfirmBookingPage\build\assets\frame0"
    )

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    try:
        with open(
                r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\user_booking.json",
                "r") as file:
            data = json.load(file)
            has_booking = data["has_booking"]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading user booking file: {e}")


    global dropoff_suggestions
    dropoff_suggestions = ["Queensbay Mall, Bayan Lepas", "Setia Triangle, Bayan Lepas", "Gurney Plaza, Pulau Tikus"]

    # AutocompleteEntry class for dropdown selection
    class AutocompleteEntry(Entry):
        def __init__(self, master=None, suggestions=[], *args, **kwargs):
            super().__init__(master, *args, **kwargs)
            self.suggestions = suggestions
            self.listbox = None
            self.listbox_open = False

            # Set the font
            self.custom_font = tkFont.Font(family="Red Hat Display Medium", size=20)
            self.config(font=self.custom_font)

            # Bind events
            self.bind("<KeyRelease>", self.on_keyrelease)
            self.bind("<FocusOut>", self.on_focus_out)
            self.bind("<FocusIn>", self.on_focus_in)

            # Bind to detect clicks outside
            self.master.bind_all("<Button-1>", self.click_outside)

        def on_focus_in(self, event):
            if not self.get().strip():
                self.show_suggestions(self.suggestions)

        def on_keyrelease(self, event):
            input_value = self.get().strip()
            if input_value:
                filtered_suggestions = [s for s in self.suggestions if s.lower().startswith(input_value.lower())]
                if filtered_suggestions:
                    self.show_suggestions(filtered_suggestions)
                else:
                    self.hide_suggestions()
            else:
                self.show_suggestions(self.suggestions)

        def show_suggestions(self, suggestions):
            if self.listbox:
                self.listbox.destroy()

            self.listbox = Listbox(self.master, height=5, font=self.custom_font, borderwidth=0, relief='flat')
            self.listbox.bind("<ButtonRelease-1>", self.on_suggestion_select)
            self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height() + 18, width=self.winfo_width() + 62)

            for suggestion in suggestions:
                self.listbox.insert('end', suggestion)

            self.listbox.lift()
            self.listbox_open = True

        def on_suggestion_select(self, event):
            if self.listbox and self.listbox.curselection():
                selected_index = self.listbox.curselection()[0]
                selected_value = self.listbox.get(selected_index)
                self.delete(0, 'end')
                self.insert(0, selected_value)
                self.hide_suggestions()
                self.update_database(selected_value)  # Update database on selection

        def update_database(self, location):
            """Update the dropoff location in the database for the most recent booking."""
            try:
                conn = sqlite3.connect(
                    r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
                cursor = conn.cursor()

                # Retrieve the most recent booking ID
                cursor.execute("SELECT id FROM bookings ORDER BY id DESC LIMIT 1")
                latest_booking_id = cursor.fetchone()

                if latest_booking_id:
                    booking_id = latest_booking_id[0]
                    cursor.execute("UPDATE bookings SET dropoff_location = ? WHERE id = ?", (location, booking_id))
                    conn.commit()
                    print(f"Updated dropoff_location to {location} for booking id {booking_id} in database.")
                else:
                    print("No recent booking found to update.")

            except sqlite3.Error as e:
                print(f"Error updating database: {e}")
            finally:
                if conn:
                    conn.close()

        def on_focus_out(self, event):
            self.after(100, self.hide_suggestions)

        def hide_suggestions(self):
            if self.listbox:
                self.listbox.destroy()
                self.listbox = None
                self.listbox_open = False

        def click_outside(self, event):
            widget = event.widget
            if widget != self and widget != self.listbox:
                self.hide_suggestions()


    # Database connection and data fetching functions
    def get_data():
        try:
            conn = sqlite3.connect(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
            cursor = conn.cursor()

            # Get booking details, car details, and customer details using INNER JOIN
            cursor.execute("""
                SELECT 
                    b.pickup_location, b.dropoff_location, b.pickup_date, b.dropoff_date,
                    c.username, c.email, c.phone_number,
                    car.car_plate, car.make_model, car.car_type, car.rate, car.seating_capacity, car.colour, car.image_path
                FROM bookings b
                INNER JOIN car car ON b.car_id = car.id
                INNER JOIN customers c ON b.customer_id = c.id
                ORDER BY b.id DESC
                LIMIT 1
            """, )  # Most recent booking
            data = cursor.fetchone()

            if data:
                # Unpack the data
                pickup_location, dropoff_location, pickup_date, dropoff_date, username, email, phone_number, \
                car_plate, make_model, car_type, rate, seating_capacity, color, car_image_path = data

                # Calculate the total number of days between pickup and dropoff dates
                total_days = calculate_total_days(pickup_date, dropoff_date)

                # Calculate the total rate
                total_rate = rate * total_days

                # Update fetched data in the canvas text fields
                canvas.itemconfig(pickup_location_text, text=pickup_location)
                autocomplete_dropoff.delete(0, 'end')  # Clear and insert fetched dropoff location
                autocomplete_dropoff.insert(0, dropoff_location)
                canvas.itemconfig(pickup_date_text, text=pickup_date)
                canvas.itemconfig(dropoff_date_text, text=dropoff_date)

                # Update car details
                canvas.itemconfig(car_plate_text, text=car_plate)
                canvas.itemconfig(make_model_text, text=make_model)
                canvas.itemconfig(car_type_text, text=car_type)
                canvas.itemconfig(rate_text, text=f"RM{total_rate:.2f}")
                canvas.itemconfig(seating_capacity_text, text=seating_capacity)
                canvas.itemconfig(color_text, text=color)

                if car_image_path:
                    display_car_image(car_image_path)
                else:
                    print("No car image found.")

                # Update customer details
                canvas.itemconfig(username_text, text=username)
                canvas.itemconfig(email_text, text=email)
                canvas.itemconfig(phone_number_text, text=phone_number)

            else:
                print("No data found for this booking.")

        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
        finally:
            if conn:
                conn.close()

    def calculate_total_days(pickup_date, dropoff_date):
        """Calculate the total number of days between pickup and dropoff dates."""
        try:
            pickup_date_obj = datetime.strptime(pickup_date, '%Y-%m-%d')  # Assuming format 'YYYY-MM-DD'
            dropoff_date_obj = datetime.strptime(dropoff_date, '%Y-%m-%d')
            if pickup_date_obj == dropoff_date_obj:
                total_days = 1
            else:
                total_days = (dropoff_date_obj - pickup_date_obj).days
            return total_days
        except ValueError as e:
            print(f"Error calculating total days: {e}")
            return 0  # Return 0 if there's an error in date conversion


    def display_car_image(car_image_path):
        try:
            # Clean up the image path (remove trailing whitespace or newlines)
            image_path = car_image_path.strip()

            # Check if the image path exists and is a valid file
            if os.path.isfile(image_path):
                img = Image.open(image_path)
                img = img.resize((478, 502), Image.Resampling.LANCZOS)  # Resize the image
                img = ImageTk.PhotoImage(img)

                # Display the image on the canvas
                canvas.create_image(373.0, 590.0, image=img)
                canvas.image = img  # Keep a reference to the image to prevent garbage collection
            else:
                print(f"File not found or invalid image path: {image_path}")

        except Exception as e:
            print(f"Error displaying profile image: {e}")


    window = Tk()
    window.geometry("1920x1200")
    window.configure(bg="#FFFFFF")

    if not has_booking:
        messagebox.showerror("Error", "No items found in cart")
        window.destroy()

        SigmaTest3 = importlib.import_module("SearchPage.SigmaTest3")
        SigmaTest3.main_window()


    # Create the main canvas and frame for scrolling
    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=1200,
        width=1920,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Scrollable frame container
    canvas_frame = Frame(canvas, bg="#FFFFFF")
    canvas_scrollbar = Scrollbar(window)

    def update_scroll_region():
        """Update canvas scroll region."""
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def create_scrollable_container():
        """Set up vertical scrolling for canvas."""
        canvas.config(yscrollcommand=canvas_scrollbar.set, highlightthickness=0)
        canvas_scrollbar.config(orient="vertical", command=canvas.yview)

        canvas_scrollbar.pack(fill="y", side="right", expand=False)
        canvas.pack(fill="both", side="left", expand=True)

        # Create a window in the canvas for the scrollable frame
        bg_image_height = 1920
        canvas.create_window(0, bg_image_height, window=canvas_frame, anchor="nw")

    def on_mouse_wheel(event):
        if canvas.yview()[0] > 0 or event.delta < 0:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        if autocomplete_dropoff.listbox_open:
            autocomplete_dropoff.hide_suggestions()

    # Bind mouse wheel to canvas
    window.bind_all("<MouseWheel>", on_mouse_wheel)

    # Create the scrollable container
    create_scrollable_container()


    # To store references for images and text fields to avoid garbage collection
    image_references = []
    text_entries = {}

    # List of images with their coordinates
    images = [
        ("image_1.png", 960.0, 1200.0),
        ("image_21.png", 923.0, 1210.0),
        ("image_2.png", 959.0, 190.0),
        ("image_3.png", 373.0, 590.0),
        ("image_4.png", 1211.0, 369.0),
        ("image_5.png", 1356.0, 474.0),
        ("image_6.png", 1263.0, 579.0),
        ("image_7.png", 1163.0, 683.0),
        ("image_8.png", 1161.0, 788.0),
        ("image_9.png", 1594.0, 788.0),
        ("image_10.png", 468.0, 962.0),
        ("image_11.png", 1294.0, 962.0),
        ("image_12.png", 1294.0, 1113.0),
        ("image_13.png", 464.0, 1113.0),
        ("image_15.png", 1281.0, 1880.0),
        ("image_16.png", 1084.0, 2052.0),
        ("image_17.png", 883.0, 1880.0),
        ("image_18.png", 1305.0, 1332.0),
        ("image_19.png", 1305.0, 1487.0),
        ("image_20.png", 1305.0, 1653.0),
    ]


    # Create images and associated entry widgets dynamically
    for index, (image_file, x, y) in enumerate(images):
        img = PhotoImage(file=relative_to_assets(image_file))
        image_references.append(img)  # Store reference
        image_id = canvas.create_image(x, y, image=img)

        # Check if this is image_15 and bind it to a command
        if image_file == "image_15.png":
            canvas.tag_bind(image_id, "<Button-1>", lambda e: popup_payment(e))
        elif image_file == "image_16.png":
            canvas.tag_bind(image_id, "<Button-1>", lambda e: upload_payment_proof(e))
        elif image_file == "image_17.png":
            canvas.tag_bind(image_id, "<Button-1>", lambda e: return_to_booking_list(e))

    def popup_payment(e):
        gui.main_window()

    def upload_payment_proof(e):
        # Open a file dialog to choose an image
        payment_proof_image_path = filedialog.askopenfilename(
            parent=window,  # Use the existing root window
            title="Select Payment Proof Image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )

        if payment_proof_image_path:  # If the user selected a file
            try:
                # Clean up the image path (remove trailing whitespace or newlines)
                payment_proof_image_path = payment_proof_image_path.strip()

                # Check if the image path exists and is a valid file
                if os.path.isfile(payment_proof_image_path):
                    img_payment = Image.open(payment_proof_image_path)
                    img_payment = img_payment.resize((478, 502), Image.Resampling.LANCZOS)  # Resize the image
                    img_payment = ImageTk.PhotoImage(img_payment)

                    # Display the image on the canvas
                    canvas.create_image(373.0, 1452.0, image=img_payment)
                    canvas.image_payment = img_payment # Keep a reference to the image to prevent garbage collection
                else:
                    print(f"File not found or invalid image path: {payment_proof_image_path}")

                # Now fetch the booking_id and insert payment data
                conn = sqlite3.connect(
                    r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
                cursor = conn.cursor()

                # Retrieve the latest booking ID
                cursor.execute("SELECT id FROM bookings ORDER BY id DESC LIMIT 1")
                latest_booking_id = cursor.fetchone()

                if latest_booking_id:
                    booking_id = latest_booking_id[0]

                    # Assuming payment_amount is calculated based on rate * days or predefined value
                    payment_amount = float(
                        canvas.itemcget(rate_text, "text").replace("RM", ""))  # Extract payment amount from canvas

                    # Insert payment into the payment table
                    cursor.execute("""
                        INSERT INTO payment (payment_amount, payment_proof_image_path, booking_id)
                        VALUES (?, ?, ?)
                    """, (payment_amount, payment_proof_image_path, booking_id))

                    # Get the last inserted payment_id
                    payment_id = cursor.lastrowid

                    # Update the bookings table with the new payment_id and set booking status to "pending"
                    cursor.execute("""
                                        UPDATE bookings
                                        SET payment_id = ?, status = 'pending'
                                        WHERE id = ?
                                    """, (payment_id, booking_id))

                    conn.commit()
                    print(
                        f"Payment of RM{payment_amount:.2f} linked to booking ID {booking_id} and payment ID {payment_id}")
                    print(f"Booking status updated to 'pending'.")

                else:
                    print("No booking found to link to payment.")

                conn.close()

            except Exception as e:
                print(f"Error displaying payment proof image: {e}")
        else:
            print("No file selected.")


    # Function to return to previous page (bookinglist page)
    def return_to_booking_list(e):
        window.destroy()
        testingbooking.main_window()

    # Mapping of text fields to variable names for database configuration
    text_entries = {
        "car_plate": canvas.create_text(1085.0, 348.0, text="", font=("Red Hat Display Medium", 20), anchor="nw"),
        "make_model": canvas.create_text(1085.0, 454.0, text="", font=("Red Hat Display Medium", 20), anchor="nw"),
        "car_type": canvas.create_text(1085.0, 559.0, text="", font=("Red Hat Display Medium", 20), anchor="nw"),
        "rate": canvas.create_text(1085.0, 663.0, text="", font=("Red Hat Display Medium", 20), anchor="nw"),
        "seating_capacity": canvas.create_text(1085.0, 768.0, text="", font=("Red Hat Display Medium", 20), anchor="nw"),
        "color": canvas.create_text(1517.0, 768.0, text="", font=("Red Hat Display Medium", 20), anchor="nw"),
        "pickup_location": canvas.create_text(150.0, 942.0, text="", font=("Red Hat Display Medium", 20), anchor="nw"),
        "pickup_date": canvas.create_text(980.0, 942.0, text="", font=("Red Hat Display Medium", 20), anchor="nw"),
        "dropoff_date": canvas.create_text(980.0, 1092.0, text="", font=("Red Hat Display Medium", 20), anchor="nw"),
        "username": canvas.create_text(1085.0, 1312.0, text="", font=("Red Hat Display Medium", 20), anchor="nw"),
        "email": canvas.create_text(1085.0, 1467.0, text="", font=("Red Hat Display Medium", 20), anchor="nw"),
        "phone_number": canvas.create_text(1085.0, 1632.0, text="", font=("Red Hat Display Medium", 20), anchor="nw"),
    }

    autocomplete_dropoff = AutocompleteEntry(canvas, suggestions=dropoff_suggestions, font=("Red Hat Display Medium", 20))
    canvas.create_window(320.0, 1112.0, window=autocomplete_dropoff)

    # Assign text items to variables for easier access in `get_car_data`
    car_plate_text = text_entries["car_plate"]
    make_model_text = text_entries["make_model"]
    car_type_text = text_entries["car_type"]
    rate_text = text_entries["rate"]
    seating_capacity_text = text_entries["seating_capacity"]
    color_text = text_entries["color"]
    pickup_location_text = text_entries["pickup_location"]
    # dropoff_location_text = text_entries["dropoff_location"]
    pickup_date_text = text_entries["pickup_date"]
    dropoff_date_text = text_entries["dropoff_date"]
    username_text = text_entries["username"]
    email_text = text_entries["email"]
    phone_number_text = text_entries["phone_number"]

    canvas.create_text(
        726.0,
        345.0,
        anchor="nw",
        text="Car Plate",
        fill="#000000",
        font=("Red Hat Display Medium", 36 * -1)
    )

    canvas.create_text(
        726.0,
        450.0,
        anchor="nw",
        text="Make/Model",
        fill="#000000",
        font=("Red Hat Display Medium", 36 * -1)
    )

    canvas.create_text(
        726.0,
        555.0,
        anchor="nw",
        text="Car Type",
        fill="#000000",
        font=("Red Hat Display Medium", 36 * -1)
    )

    canvas.create_text(
        726.0,
        660.0,
        anchor="nw",
        text="Total Rate",
        fill="#000000",
        font=("Red Hat Display Medium", 36 * -1)
    )

    canvas.create_text(
        726.0,
        765.0,
        anchor="nw",
        text="Seating Capacity",
        fill="#000000",
        font=("Red Hat Display Medium", 36 * -1)
    )

    canvas.create_text(
        1365.0,
        765.0,
        anchor="nw",
        text="Color",
        fill="#000000",
        font=("Red Hat Display Medium", 36 * -1)
    )

    canvas.create_text(
        134.0,
        867.0,
        anchor="nw",
        text="Pickup Location",
        fill="#000000",
        font=("Red Hat Display Medium", 36 * -1)
    )

    canvas.create_text(
        960.0,
        867.0,
        anchor="nw",
        text="Pickup Date",
        fill="#000000",
        font=("Red Hat Display Medium", 36 * -1)
    )

    canvas.create_text(
        134.0,
        1018.0,
        anchor="nw",
        text="Dropoff Location",
        fill="#000000",
        font=("Red Hat Display Medium", 36 * -1)
    )

    canvas.create_text(
        960.0,
        1018.0,
        anchor="nw",
        text="Dropoff Date",
        fill="#000000",
        font=("Red Hat Display Medium", 36 * -1)
    )


    canvas.create_text(
        726.0,
        1308.0,
        anchor="nw",
        text="Username",
        fill="#000000",
        font=("Red Hat Display Medium", 36 * -1)
    )

    canvas.create_text(
        726.0,
        1463.0,
        anchor="nw",
        text="Email",
        fill="#000000",
        font=("Red Hat Display Medium", 36 * -1)
    )

    canvas.create_text(
        726.0,
        1629.0,
        anchor="nw",
        text="Phone Number",
        fill="#000000",
        font=("Red Hat Display Medium", 36 * -1)
    )

    canvas_frame.update_idletasks()  # Update layout for scroll region
    update_scroll_region()

    get_data()

    create_header(window, canvas)

    window.resizable(False, False)
    window.mainloop()

if __name__ == '__main__':
    main_window()