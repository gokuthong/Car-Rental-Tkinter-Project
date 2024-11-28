import sqlite3
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage,Menu
from PIL import Image, ImageTk
from chen.buildregister.header import create_header
import os
import importlib
import json

# Path setup
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\kit\Profile\assets\frame0")

# Redirect to profile.py after saving and open it before destroying the current window


def main_window():

    def goto_profile_edit():
        window.destroy()
        profile_edit = importlib.import_module("kit.Profile.profile_edit")

        profile_edit.main_window()

    def goto_profile_change_password():
        window.destroy()
        profile_change_password = importlib.import_module("kit.Profile.profile_change_password")

        profile_change_password.main_window()

    def get_current_user_id():
        try:
            with open(
                    r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\user_session.json",
                    "r") as file:
                data = json.load(file)
                print("Loaded data:", data)  # Debugging: check the raw data loaded
                user_id = data["id"]  # Try direct access (not using get)
                print(f"User ID:", user_id)  # Check the value of the ID
                return user_id
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading current user session file: {e}")
            return None

    # Database connection and data fetching function
    def get_customer_data():
        user_id = get_current_user_id()
        if not user_id:
            print("No current user ID found.")
            return

        try:
            conn = sqlite3.connect(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
            cursor = conn.cursor()

            # Fetch details of the logged-in customer using the current user ID
            cursor.execute("""
                SELECT username, email, phone_number, age, gender, password, profile_image_path 
                FROM customers WHERE id = ?
            """, (user_id,))
            data = cursor.fetchone()

            if data:
                username_data, email_data, phone_number_data, age_data, gender_data, password_data, profile_image_path = data

                username.config(state="normal")
                email.config(state="normal")
                phone_number.config(state="normal")
                age.config(state="normal")
                gender.config(state="normal")
                password.config(state="normal")

                username.insert(0, username_data)
                email.insert(0, email_data)
                phone_number.insert(0, phone_number_data)
                age.insert(0, age_data)
                gender.insert(0, gender_data)
                password.insert(0, password_data)

                username.config(state="readonly")
                email.config(state="readonly")
                phone_number.config(state="readonly")
                age.config(state="readonly")
                gender.config(state="readonly")
                password.config(state="readonly")

                welcome_message = f"HI, {username_data}!"
                canvas.create_text(370.0, 858.0, anchor="nw", text=welcome_message, fill="#000000", font=("Inter ExtraBoldItalic", 30 * -1))

                if profile_image_path:
                    display_profile_image(profile_image_path)
                else:
                    print("No profile image found for this customer.")

            else:
                print("No data found for this customer.")

        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
        finally:
            if conn:
                conn.close()


    # Function to display the profile image in the specified canvas area
    def display_profile_image(image_path):
        try:
            # Clean up the image path (remove trailing whitespace or newlines)
            image_path = image_path.strip()

            # Check if the image path exists and is a valid file
            if os.path.isfile(image_path):
                img = Image.open(image_path)
                img = img.resize((400, 320), Image.Resampling.LANCZOS)  # Resize the image
                img = ImageTk.PhotoImage(img)

                # Display the image on the canvas
                canvas.create_image(584.0, 600.0, image=img)
                canvas.image = img  # Keep a reference to the image to prevent garbage collection
            else:
                print(f"File not found or invalid image path: {image_path}")

        except Exception as e:
            print(f"Error displaying profile image: {e}")


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def toggle_password():
        if password.cget('show') == '':
            password.config(show='*')  # Hide password
            show_hide_button.config(text="Show")
        else:
            password.config(show='')   # Show password
            show_hide_button.config(text="Hide")


    # Define hover color functions
    def on_enter_button(e):
        e.widget.config(bg="#90EE90")  # Light green hover color


    def on_leave_button(e):
        e.widget.config(bg="#006400")  # Dark green normal color


    def on_click_button(e):
        e.widget.config(bg="#90EE90")  # Stay light green on click

    def update_welcome_message(username):
        # Create text element for the username
        canvas.create_text(
            370.0, 858.0, anchor="nw",
            text=f"HI, {username}",   # Dynamically insert the username
            fill="#000000",
            font=("Inter ExtraBoldItalic", 30 * -1)
        )

    username_display = ""

    # Initialize window
    window = Tk()
    window.geometry("1920x1200")
    window.configure(bg="#FFFFFF")

    # Create canvas
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

    # Load images and create references
    bg = PhotoImage(file=relative_to_assets("bg.png"))
    bg_place = canvas.create_image(960.0, 643.0, image=bg)

    profile_header = PhotoImage(file=relative_to_assets("profile_header.png"))
    profile_header_place = canvas.create_image(960.0, 233.0, image=profile_header)

    window_bg = PhotoImage(file=relative_to_assets("window_bg.png"))
    window_bg_place = canvas.create_image(960.0, 684.0, image=window_bg)

    profile_border = PhotoImage(file=relative_to_assets("profile_border.png"))
    profile_border_place = canvas.create_image(584.0, 600.0, image=profile_border)

    # Create text elements
    canvas.create_text(370.0, 215.0, anchor="nw", text="View Profile", fill="#FFFFFF", font=("Helvetica", 25, "bold"))
    canvas.create_text(370.0, 858.0, anchor="nw", text=username_display, fill="#000000", font=("Inter ExtraBoldItalic", 30 * -1))

    canvas.create_text(940.0, 446.0, anchor="nw", text="Username:", fill="#000000", font=("Inter Bold", 28 * -1))
    canvas.create_text(1000.0, 549.0, anchor="nw", text="Email:", fill="#000000", font=("Inter Bold", 28 * -1))
    canvas.create_text(1019.0, 755.0, anchor="nw", text="Age:", fill="#000000", font=("Inter Bold", 28 * -1))
    canvas.create_text(889.0, 652.0, anchor="nw", text="Phone number:", fill="#000000", font=("Inter Bold", 28 * -1))
    canvas.create_text(980.0, 858.0, anchor="nw", text="Gender:", fill="#000000", font=("Inter Bold", 28 * -1))
    canvas.create_text(955.0, 953.0, anchor="nw", text="Password:", fill="#000000", font=("Inter Bold", 28 * -1))

    # Create Entry widgets for form inputs (now named appropriately)
    username_bg_image = PhotoImage(file=relative_to_assets("entry_border_1.png"))
    username_bg = canvas.create_image(1335.5, 452.0, image=username_bg_image)
    username = Entry(bd=0, bg="#FFFFFF", fg="#000716", font=("Helvetica", 16), highlightthickness=0, state="readonly")
    username.place(x=1121.0, y=425.0, width=429.0, height=52.0)

    email_bg_image = PhotoImage(file=relative_to_assets("entry_border_1.png"))
    email_bg = canvas.create_image(1335.5, 555.0, image=email_bg_image)
    email = Entry(bd=0, bg="#FFFFFF", fg="#000716", font=("Helvetica", 16), highlightthickness=0, state="readonly")
    email.place(x=1121.0, y=528.0, width=429.0, height=52.0)

    age_bg_image = PhotoImage(file=relative_to_assets("entry_border_2.png"))
    age_bg = canvas.create_image(1184.5, 761.0, image=age_bg_image)
    age = Entry(bd=0, bg="#FFFFFF", fg="#000716", font=("Helvetica", 16), highlightthickness=0, state="readonly")
    age.place(x=1121.0, y=734.0, width=127.0, height=52.0)

    phone_number_bg_image = PhotoImage(file=relative_to_assets("entry_border_1.png"))
    phone_number_bg = canvas.create_image(1335.5, 658.0, image=phone_number_bg_image)
    phone_number = Entry(bd=0, bg="#FFFFFF", fg="#000716", font=("Helvetica", 16), highlightthickness=0, state="readonly")
    phone_number.place(x=1121.0, y=631.0, width=429.0, height=52.0)

    gender_bg_image = PhotoImage(file=relative_to_assets("entry_border_2.png"))
    gender_bg = canvas.create_image(1184.5, 864.0, image=gender_bg_image)
    gender = Entry(bd=0, bg="#FFFFFF", fg="#000716", font=("Helvetica", 16), highlightthickness=0, state="readonly")
    gender.place(x=1121.0, y=837.0, width=127.0, height=52.0)

    pass_bg_image = PhotoImage(file=relative_to_assets("entry_border_1.png"))
    pass_bg = canvas.create_image(1335.5, 967.0, image=pass_bg_image)
    password = Entry(bd=0, bg="#FFFFFF", fg="#000716", font=("Helvetica", 16), highlightthickness=0, show="*", state="normal")
    password.place(x=1121.0, y=940.0, width=429.0, height=52.0)

    show_hide_button = Button(
        text="Show",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=toggle_password,
        relief="flat",
        font=("Calibri", 12)
    )
    show_hide_button.place(x=1490.0, y=940.0, width=60.0, height=52.0)

    show_hide_button.bind("<Enter>", on_enter_button)
    show_hide_button.bind("<Leave>", on_leave_button)
    show_hide_button.bind("<Button-1>", on_click_button)

    def show_edit_menu(event):
        edit_menu = Menu(window, tearoff=0)
        edit_menu.config(bg="#006400", fg="white", font=("Calibri", 16))
        edit_menu.add_command(label="Edit Profile", command=lambda: goto_profile_edit())
        edit_menu.add_command(label="Change Password", command=lambda: goto_profile_change_password())

        # Display the menu at the cursor's position
        edit_menu.post(event.x_root, event.y_root)


    # Create "Edit" button with hover effects
    edit_button = Button(
        text="Edit",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        font=("Calibri", 15)
    )


    edit_button.place(x=1420.0, y=348.0, width=130.0, height=42.59427261352539)

    # Bind hover and click events
    edit_button.bind("<Enter>", on_enter_button)
    edit_button.bind("<Leave>", on_leave_button)
    edit_button.bind("<Button-1>", show_edit_menu)

    # Call header creation after the canvas
    create_header(window, canvas)

    # Fetch customer data after setting up the GUI
    get_customer_data()

    # Ensure window is not resizable and run the main loop
    window.resizable(False, True)
    window.mainloop()

if __name__ == "__main__":
    main_window()



