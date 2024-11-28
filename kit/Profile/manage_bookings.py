import sqlite3
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Label, OptionMenu, StringVar, Checkbutton, BooleanVar, messagebox,Toplevel
from tkcalendar import DateEntry
from chen.buildregister.headeradmin import create_header
import customtkinter as ctk
from PIL import Image, ImageTk
import json


def main_window():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\kit\Profile\assets\frame0")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def open_image_popup(image_path):
        # Create a popup window to display the image
        popup = Toplevel()  # Create a new top-level window
        popup.title("Image Popup")

        # Set a fixed size for the image (e.g., 400x300 pixels)
        fixed_width = 600
        fixed_height = 800

        # Set window size for the popup to prevent it from automatically minimizing
        popup.geometry(f"{fixed_width}x{fixed_height}")

        try:
            # Load and resize the image
            image = Image.open(image_path)  # image_path should be the path from your database
            image = image.resize((fixed_width, fixed_height),
                                 Image.Resampling.LANCZOS)  # Resize image with high quality

            # Convert the PIL image to a Tkinter PhotoImage
            photo = ImageTk.PhotoImage(image)

            # Display the image in the popup
            label = Label(popup, image=photo)
            label.photo = photo  # Keep a reference to avoid garbage collection
            label.pack()

            # Close the popup window when clicked outside or close button
            popup.protocol("WM_DELETE_WINDOW", popup.destroy)

        except Exception as e:
            print(f"Error loading image: {e}")
            error_label = Label(popup, text="Error loading image", font=("Helvetica", 14))
            error_label.pack()

    # Function to fetch the current admin ID from the session file
    def get_current_admin_id():
        session_file_path = "C:/Users/ASUS/PycharmProjects/pythonProject/Car Rental Tkinter Main/chen/buildregister/admin_session.json"

        try:
            with open(session_file_path, 'r') as file:
                session_data = json.load(file)
                return session_data.get("current_admin_id", None)
        except FileNotFoundError:
            print("Admin session file not found.")
            return None
        except json.JSONDecodeError:
            print("Error decoding the admin session file.")
            return None


    # Function to fetch records from the bookings table with filters and include car_plate
    def fetch_bookings(status=None, start_date=None, end_date=None):
        conn = sqlite3.connect(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
        cursor = conn.cursor()

        query = """
        SELECT 
            bookings.id,
            car.car_plate,
            bookings.car_id,
            bookings.customer_id,
            bookings.pickup_location,
            bookings.dropoff_location,
            bookings.pickup_date,
            bookings.dropoff_date,
            payment.payment_amount,
            payment.payment_proof_image_path,
            bookings.status
        FROM 
            bookings
        LEFT JOIN 
            car ON bookings.car_id = car.id
        LEFT JOIN
            payment ON bookings.id = payment.booking_id
        WHERE 
            (bookings.status = 'approved' OR bookings.status = 'rejected' OR bookings.status = 'pending')
        """

        params = []

        if status:
            query += " AND bookings.status = ?"
            params.append(status)
        if start_date and end_date:
            query += " AND bookings.pickup_date BETWEEN ? AND ?"
            params.extend([start_date, end_date])

        cursor.execute(query, params)
        records = cursor.fetchall()
        print(f"Fetched {len(records)} records.")
        conn.close()
        return records

    # Function to delete a booking record
    def delete_booking(booking_id):
        conn = sqlite3.connect(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        conn.commit()
        conn.close()

    # Function to refresh table after deletion
    def refresh_table():
        bookings = fetch_bookings()
        display_bookings(bookings)

    # Function to update booking status in the database and add admin_id
    def update_booking_status(booking_id, new_status):
        admin_id = get_current_admin_id()  # Get the current admin ID

        if admin_id is None:
            messagebox.showerror("Error", "Unable to retrieve admin ID.")
            return

        conn = sqlite3.connect(
            r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
        cursor = conn.cursor()

        try:
            # Update the status and the admin_id in the bookings table
            cursor.execute("""
                UPDATE bookings 
                SET status = ?, admin_id = ? 
                WHERE id = ?
            """, (new_status, admin_id, booking_id))

            conn.commit()
            messagebox.showinfo("Success",
                                f"Booking {booking_id} status updated to '{new_status}' by admin {admin_id}.")
        except sqlite3.Error as e:
            print(f"Error updating booking status: {e}")
            messagebox.showerror("Error", f"Error updating booking status: {e}")
        finally:
            conn.close()

    # Confirmation pop-up before changing the status
    def confirm_status_change(selected_ids, new_status):
        if not selected_ids:
            messagebox.showwarning("No Selection", "Please select at least one booking to change the status.")
            return

        confirm = messagebox.askyesno("Confirm Action", f"Are you sure you want to change the status to '{new_status}'?")
        if confirm:
            for booking_id in selected_ids:
                update_booking_status(booking_id, new_status)  # Update the status and admin_id
            display_bookings(fetch_bookings())  # Refresh displayed bookings

    # Create the main Tkinter window
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

    # Background image and container
    booking_bg_image = PhotoImage(file=relative_to_assets("booking_bg.png"))
    canvas.create_image(960.0, 641.0, image=booking_bg_image)

    booking_container_image = PhotoImage(file=relative_to_assets("booking_container.png"))
    canvas.create_image(948.0, 640.0, image=booking_container_image)

    canvas.create_text(
        251.0,
        155.0,
        anchor="nw",
        text="Manage Bookings",
        fill="#FFFFFF",
        font=("Inter Bold", 36 * -1)
    )

    # Table with Scrollable Frame and Checkboxes (placed on the left side, wider)
    scrollable_table = ctk.CTkScrollableFrame(window, width=1000, height=703, fg_color="#D3D3D3")
    scrollable_table.place(x=220, y=308)

    # Columns and Header Row
    columns = ("", "ID","Car Plate", "Car ID", "Customer ID", "Pickup Location", "Dropoff Location", "Pickup Date", "Dropoff Date","Amount","Receipt", "Status")
    header_bg_color = "#2E8B57"
    header_text_color = "white"

    for col_index, col_name in enumerate(columns):
        header = ctk.CTkLabel(
            scrollable_table,
            text=col_name,
            font=("Helvetica", 14, "bold"),
            fg_color=header_bg_color,
            text_color=header_text_color,
            corner_radius=5
        )
        header.grid(row=0, column=col_index, padx=2, pady=2, sticky="nsew")

    # Checkbox selection tracking
    selected_checkboxes = {}

    def display_bookings(bookings):
        # Clear the existing rows
        for widget in scrollable_table.winfo_children():
            widget.destroy()

        print(f"Displaying {len(bookings)} bookings.")

        # Re-add header
        for col_index, col_name in enumerate(columns):
            header = ctk.CTkLabel(
                scrollable_table,
                text=col_name,
                font=("Helvetica", 13, "bold"),
                fg_color=header_bg_color,
                text_color=header_text_color,
                corner_radius=5
            )
            header.grid(row=0, column=col_index, padx=2, pady=2, sticky="nsew")

            # Bind click event to select row and highlight it

            for col_index in range(len(columns)):
                scrollable_table.grid_columnconfigure(col_index, weight=1)

        # Insert booking records as rows with checkbox
        for row_index, record in enumerate(bookings, start=1):
            select_var = BooleanVar()
            selected_checkboxes[record[0]] = select_var  # Track each row by its ID

            checkbox = Checkbutton(scrollable_table, variable=select_var)
            checkbox.grid(row=row_index, column=0)

            for col_index, item in enumerate(record):

                # Check if the column is "Receipt" to make it clickable
                if col_index == 9:  # "Receipt" column (index 9)
                    # If this is the "Receipt" column, make it a clickable link
                    cell = ctk.CTkLabel(
                        scrollable_table,
                        text="View",  # Display a "View Receipt" text
                        font=("Helvetica", 12, "underline"),
                        fg_color="white",
                        text_color="blue",  # Make it look like a clickable link
                        corner_radius=5
                    )
                    # Bind the label to open an image popup using the path from the "Receipt" column
                    cell.bind("<Button-1>", lambda e, payment_proof_image_path=item: open_image_popup(payment_proof_image_path))
                else:
                    cell = ctk.CTkLabel(
                        scrollable_table,
                        text=item,
                        font=("Helvetica", 12),
                        fg_color="white",
                        text_color="black",
                        corner_radius=5
                    )
                cell.grid(row=row_index, column=col_index + 1, padx=2, pady=2, sticky="nsew")

                # Bind click event to select row and highlight it

                for col_index in range(len(columns)):
                    scrollable_table.grid_columnconfigure(col_index, weight=1)


    # Initial display of all records
    display_bookings(fetch_bookings())

    # Filter Section (Date range, status dropdown, and apply button)
    filter_label = Label(window, text="Filter Bookings", font=("Helvetica", 25, "bold"), bg="white", fg="#2E8B57")
    filter_label.place(x=1300, y=320)

    Label(window, text="Start Date:", font=("Helvetica", 20), bg="white", fg="#2E8B57").place(x=1300, y=400)
    date_start = DateEntry(window, width=15, background="darkblue", foreground="white", date_pattern="y-mm-dd", font=("Helvetica", 20))
    date_start.place(x=1300, y=460)

    Label(window, text="End Date:", font=("Helvetica", 20), bg="white", fg="#2E8B57").place(x=1300, y=540)
    date_end = DateEntry(window, width=15, background="darkblue", foreground="white", date_pattern="y-mm-dd", font=("Helvetica", 20))
    date_end.place(x=1300, y=600)

    # Status Dropdown Menu
    status_options = ["All", "Approved", "Pending", "Rejected"]
    status_var = StringVar()
    status_var.set(status_options[0])

    status_dropdown = OptionMenu(window, status_var, *status_options)
    status_dropdown.config(font=("Helvetica", 15), bg="white", fg="black", width=12)
    status_dropdown.place(x=1300, y=680)

    # Apply Filters Button
    def apply_filters():
        status = status_var.get().lower()
        start_date = date_start.get_date()
        end_date = date_end.get_date()

        if status == "all":
            status = None
        bookings = fetch_bookings(status=status, start_date=start_date, end_date=end_date)
        display_bookings(bookings)

    apply_button = Button(window, text="Apply Filters", bg="white", command=apply_filters, font=("Helvetica", 15))
    apply_button.place(x=1500, y=680)

    # Approve and Reject Buttons with Status Update
    def get_selected_ids():
        return [booking_id for booking_id, var in selected_checkboxes.items() if var.get()]

    approve_button_image = PhotoImage(file=relative_to_assets("approve_button.png"))
    approve_button = Button(
        image=approve_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: confirm_status_change(get_selected_ids(), "approved"),
        relief="flat"
    )
    approve_button.place(x=1300, y=800, width=238, height=77)

    reject_button_image = PhotoImage(file=relative_to_assets("reject_button.png"))
    reject_button = Button(
        image=reject_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: confirm_status_change(get_selected_ids(), "rejected"),
        relief="flat"
    )
    reject_button.place(x=1300, y=900, width=238, height=77)

    # Clear Selected Car Button
    def clear_selected_car():
        selected_ids = [booking_id for booking_id, var in selected_checkboxes.items() if var.get()]
        if not selected_ids:
            messagebox.showwarning("No Selection", "Please select at least one car to clear.")
            return
        confirm = messagebox.askyesno("Confirm Action", "Are you sure you want to delete the selected car?")
        if confirm:
            for booking_id in selected_ids:
                delete_booking(booking_id)
            refresh_table()  # Refresh table after deletion

    clear_button_image = PhotoImage(file=relative_to_assets("clear_button.png"))
    clear_button = Button(image=clear_button_image, borderwidth=0, highlightthickness=0, command=clear_selected_car,
                          relief="flat")
    clear_button.place(x=1300, y=1000, width=238, height=77)

    create_header(window, canvas)
    window.resizable(False, False)
    window.mainloop()

if __name__ == '__main__':
    main_window()