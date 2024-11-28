import sqlite3  # Import SQLite for database interaction
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage,messagebox
import customtkinter as ctk
from chen.buildregister.header import create_header
import json


def main_window():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\kit\Profile\assets\frame0")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    # Function to read the current_user_id from the JSON file
    def get_current_user_id():
        try:
            with open(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\user_session.json", "r") as file:
                session_data = json.load(file)
                return session_data.get("id")
        except FileNotFoundError:
            messagebox.showerror("Error", "User session file not found.")
            return None
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to decode user session file.")
            return None

    # Function to fetch records based on status filter and current_user_id
    def fetch_bookings(status=None):
        current_user_id = get_current_user_id()
        if current_user_id is None:
            return []  # Return empty list if no user ID is found

        conn = sqlite3.connect(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
        cursor = conn.cursor()



        query = """
            SELECT bookings.id, car.car_plate, car.make_model, customers.username,
                   bookings.pickup_location, bookings.dropoff_location,
                   bookings.pickup_date, bookings.dropoff_date, payment.payment_amount, bookings.status
            FROM bookings
            LEFT JOIN car ON bookings.car_id = car.id
            LEFT JOIN customers ON bookings.customer_id = customers.id
            LEFT JOIN payment ON bookings.id = payment.booking_id
            WHERE bookings.customer_id = ?
        """
        params = [current_user_id]

        if status:
            query += " AND bookings.status = ?"
            params.append(status)
        else:
            query += " AND bookings.status IN ('approved', 'rejected', 'pending')"

        cursor.execute(query, params)
        records = cursor.fetchall()
        conn.close()
        return records

    # Function to load bookings into the table
    def load_bookings(status=None):
        global selected_row_id, selected_row  # Reset selection variables on reload
        selected_row_id = None
        selected_row = None

        # Clear existing table content
        for widget in scrollable_table.winfo_children():
            widget.destroy()

        bookings = fetch_bookings(status)
        for col_index, col_name in enumerate(columns):
            header = ctk.CTkLabel(
                scrollable_table,
                text=col_name,
                font=("Helvetica", 13.5, "bold"),
                fg_color=header_bg_color,
                text_color=header_text_color,
                corner_radius=5
            )
            header.grid(row=0, column=col_index, padx=2, pady=2, sticky="nsew")

        # Insert fetched records
        for row_index, record in enumerate(bookings, start=1):
            for col_index, item in enumerate(record):
                cell = ctk.CTkLabel(
                    scrollable_table,
                    text=item,
                    font=("Helvetica", 12),
                    fg_color="white",
                    text_color="black",
                    corner_radius=6
                )
                cell.grid(row=row_index, column=col_index, padx=2, pady=2, sticky="nsew")

                # Bind click event to select row and capture correct row and record_id
                cell.bind("<Button-1>", lambda event, row=row_index, record_id=record[0]: select_row(row, record_id))

                # Bind click event to select row and highlight it
                for col_index in range(len(columns)):
                    scrollable_table.grid_columnconfigure(col_index, weight=1)

    # Define a variable to keep track of the selected row ID
    selected_row_id = None
    selected_row = None

    # Function to handle row selection
    def select_row(row_index, record_id):
        global selected_row_id, selected_row

        if selected_row:
            for cell in selected_row:
                cell.configure(fg_color="white")

        selected_row_id = record_id
        selected_row = [scrollable_table.grid_slaves(row=row_index, column=col_index)[0] for col_index in
                        range(len(columns))]

        for cell in selected_row:
            cell.configure(fg_color="lightgreen")  # Highlight selected row

    # Commands for the filter and clear buttons
    def filter_all():
        load_bookings()  # Show all records with status 'Approved', 'Rejected', or 'Pending'

    def filter_approved():
        load_bookings("approved")  # Show only approved records

    def filter_rejected():
        load_bookings("rejected")  # Show only rejected records

    def filter_pending():
        load_bookings("pending")  # Show only pending records


    window = Tk()
    window.geometry("1920x1200")
    window.configure(bg="#FFFFFF")

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

    # Background image
    booking_bg_image = PhotoImage(file=relative_to_assets("booking_bg.png"))
    canvas.create_image(960.0, 641.0, image=booking_bg_image)

    # Container image
    booking_container_image = PhotoImage(file=relative_to_assets("booking_container.png"))
    canvas.create_image(948.0, 640.0, image=booking_container_image)

    canvas.create_text(
        251.0,
        155.0,
        anchor="nw",
        text="Bookings List",
        fill="#FFFFFF",
        font=("Inter Bold", 36 * -1)
    )

    # Buttons with specific images
    filter_approved_image = PhotoImage(file=relative_to_assets("filter_approved.png"))
    filter_approved_button = Button(
        image=filter_approved_image,
        borderwidth=0,
        highlightthickness=0,
        command=filter_approved,
        relief="flat"
    )
    filter_approved_button.place(x=480.0, y=308.0, width=239.0, height=238.0)

    filter_all_image = PhotoImage(file=relative_to_assets("filter_all.png"))
    filter_all_button = Button(
        image=filter_all_image,
        borderwidth=0,
        highlightthickness=0,
        command=filter_all,
        relief="flat"
    )
    filter_all_button.place(x=208.0, y=308.0, width=238.0, height=238.0)

    filter_reject_image = PhotoImage(file=relative_to_assets("filter_reject.png"))
    filter_reject_button = Button(
        image=filter_reject_image,
        borderwidth=0,
        highlightthickness=0,
        command=filter_rejected,
        relief="flat"
    )
    filter_reject_button.place(x=208.0, y=609.0, width=238.0, height=238.0)

    filter_pending_image = PhotoImage(file=relative_to_assets("filter_pending.png"))
    filter_pending_button = Button(
        image=filter_pending_image,
        borderwidth=0,
        highlightthickness=0,
        command=filter_pending,
        relief="flat"
    )
    filter_pending_button.place(x=480.0, y=609.0, width=239.0, height=238.0)



    # Scrollable frame for the table
    scrollable_table = ctk.CTkScrollableFrame(window, width=960, height=703, fg_color="#D3D3D3")
    scrollable_table.place(x=750, y=308)

    # Table header and initial load
    columns = (
    "ID","Car Plate", "Car Name", "Username", "Pickup Location", "Dropoff Location", "Pickup Date", "Dropoff Date","Amount", "Status")
    header_bg_color = "#2E8B57"  # Dark green for header
    header_text_color = "white"
    load_bookings()  # Initial load showing all statuses

    create_header(window,canvas)

    window.mainloop()

if __name__ == '__main__':
    main_window()
