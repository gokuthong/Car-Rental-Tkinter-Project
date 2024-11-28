import importlib
import json
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, filedialog, Label, END, Radiobutton, StringVar, ttk
from PIL import Image, ImageTk
from chen.buildregister.header import create_header
import os
import re
import sqlite3

# Path setup
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\kit\Profile\assets\frame0")

def main_window():

    def get_logged_in_user_id():
        try:
            with open(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\user_session.json", "r") as f:
                session_data = json.load(f)
            return session_data.get("id")
        except Exception as e:
            print(f"Error reading user session: {e}")
            return None

    logged_in_user_id = get_logged_in_user_id()
    if logged_in_user_id is None:
        print("No user is currently logged in.")
        return

    def save_changes():
        try:
            conn = sqlite3.connect(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
            cursor = conn.cursor()

            new_username = username.get()
            new_email = email.get().strip()
            new_phone_number = phone_number.get()
            new_age = age.get()
            new_gender = gender.get()
            new_profile_image_path = image_path if 'image_path' in globals() else None

            # Email validation
            regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
            if not re.match(regex, new_email):
                print("Invalid email address. Please enter a valid email.")
                return

            # Update customer data in the database
            if new_profile_image_path is None or new_profile_image_path == "":
                cursor.execute("SELECT profile_image_path FROM customers WHERE id = ?", (logged_in_user_id,))
                current_profile_image_path = cursor.fetchone()
                if current_profile_image_path is not None:
                    current_profile_image_path = current_profile_image_path[0]
                    cursor.execute("""UPDATE customers
                        SET username = ?, email = ?, phone_number = ?, age = ?, gender = ?, profile_image_path = ?
                        WHERE id = ?
                    """, (
                        new_username, new_email, new_phone_number, new_age, new_gender, current_profile_image_path, logged_in_user_id
                    ))
            else:
                cursor.execute("""UPDATE customers
                    SET username = ?, email = ?, phone_number = ?, age = ?, gender = ?, profile_image_path = ?
                    WHERE id = ?
                """, (
                    new_username, new_email, new_phone_number, new_age, new_gender, new_profile_image_path, logged_in_user_id
                ))

            conn.commit()
            print("Customer data updated successfully.")
            goto_profile()

        except sqlite3.Error as e:
            print(f"Error updating customer data: {e}")

        finally:
            if conn:
                conn.close()

    def goto_profile():
        window.destroy()
        profile = importlib.import_module("kit.Profile.profile")
        profile.main_window()

    def upload_image():
        global image_path
        try:
            image_path = filedialog.askopenfilename(
                title="Select Profile Image",
                filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")]
            )
            if image_path:
                img = Image.open(image_path)
                img = img.resize((400, 320), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                canvas.create_image(584.0, 600.0, image=img)
                canvas.image = img

        except Exception as e:
            print(f"Error uploading and displaying image: {e}")

    def get_customer_data():
        try:
            conn = sqlite3.connect(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT username, email, phone_number, age, gender, profile_image_path 
                FROM customers WHERE id = ?
            """, (logged_in_user_id,))
            data = cursor.fetchone()
            if data:
                username_data, email_data, phone_number_data, age_data, gender_data, profile_image_path = data
                username.config(state="normal")
                email.config(state="normal")
                phone_number.config(state="normal")
                age.config(state="normal")
                username.insert(0, username_data)
                email.insert(0, email_data)
                phone_number.insert(0, phone_number_data)
                age.insert(0, age_data)
                gender.set(gender_data)
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

    def display_profile_image(image_path):
        try:
            image_path = image_path.strip()
            if os.path.isfile(image_path):
                img = Image.open(image_path)
                img = img.resize((400, 320), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                canvas.create_image(584.0, 600.0, image=img)
                canvas.image = img
            else:
                print(f"File not found or invalid image path: {image_path}")

        except Exception as e:
            print(f"Error displaying profile image: {e}")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

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
            text=f"HI, {username}",  # Dynamically insert the username
            fill="#000000",
            font=("Inter ExtraBoldItalic", 30 * -1)
        )

    # Email validation function
    def validate_email(event=None):
        email_text = email.get()
        # Regular expression for validating an Email
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'

        if re.match(regex, email_text):
            validation_label.config(text="Valid Email Address", fg="green")
        else:
            validation_label.config(text="Invalid Email Address", fg="red")

    # Limit the character count to a maximum of 10 digits
    def limit_phone_input(event):
        if len(phone_number.get()) > 10:
            phone_number.delete(10, END)  # Limit to 10 characters

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
    canvas.create_text(370.0, 215.0, anchor="nw", text="Edit Profile", fill="#FFFFFF", font=("Helvetica", 25, "bold"))
    canvas.create_text(370.0, 858.0, anchor="nw", text=username_display, fill="#000000",
                       font=("Inter ExtraBoldItalic", 30 * -1))

    canvas.create_text(940.0, 446.0, anchor="nw", text="Username:", fill="#000000", font=("Inter Bold", 28 * -1))
    canvas.create_text(1000.0, 549.0, anchor="nw", text="Email:", fill="#000000", font=("Inter Bold", 28 * -1))
    canvas.create_text(1019.0, 775.0, anchor="nw", text="Age:", fill="#000000", font=("Inter Bold", 28 * -1))
    canvas.create_text(889.0, 652.0, anchor="nw", text="Phone number:", fill="#000000", font=("Inter Bold", 28 * -1))
    canvas.create_text(980.0, 858.0, anchor="nw", text="Gender:", fill="#000000", font=("Inter Bold", 28 * -1))

    # Create Entry widgets for form inputs (now named appropriately)
    username_bg_image = PhotoImage(file=relative_to_assets("entry_border_1.png"))
    username_bg = canvas.create_image(1335.5, 452.0, image=username_bg_image)
    username = Entry(bd=0, bg="#FFFFFF", fg="#000716", font=("Helvetica", 16), highlightthickness=0)
    username.place(x=1121.0, y=425.0, width=429.0, height=52.0)

    email_bg = PhotoImage(file=relative_to_assets("entry_border_1.png"))
    email_bg_place = canvas.create_image(1335.5, 555.0, image=email_bg)
    email = Entry(bd=0, bg="#FFFFFF", fg="#000716", font=("Helvetica", 16), highlightthickness=0)
    email.place(x=1121.0, y=528.0, width=429.0, height=52.0)

    # Label to display validation result
    validation_label = Label(window, text="", font=("Helvetica", 12))
    validation_label.place(x=1121.0, y=590.0)  # Position it just below the email field

    # Bind the validation function to key release event
    email.bind("<KeyRelease>", validate_email)

    age_bg_image = PhotoImage(file=relative_to_assets("entry_border_2.png"))
    age_bg = canvas.create_image(1184.5, 781.0, image=age_bg_image)
    age = ttk.Combobox(window, values=[str(i) for i in range(18, 101)], state="normal", font=("Helvetica", 16))  # Age options from 1 to 100
    age.place(x=1121.0, y=754.0, width=127.0, height=52.0)

    # Create phone number entry background and entry widget
    phone_number_bg_image = PhotoImage(file=relative_to_assets("entry_border_1.png"))
    phone_number_bg = canvas.create_image(1335.5, 658.0, image=phone_number_bg_image)
    phone_number = Entry(bd=0, bg="#FFFFFF", fg="#000716", font=("Helvetica", 16), highlightthickness=0)
    phone_number.place(x=1121.0, y=631.0, width=429.0, height=52.0)

    # Label to guide the user on the expected format positioned at the bottom
    phone_label = Label(window, text="Eg:0123456789", font=("Helvetica", 12))
    phone_label.place(x=1121.0, y=695.0)  # Position it just below the phone number field

    # Bind the events
    phone_number.bind("<KeyRelease>", limit_phone_input)

    # Variable to hold the selected gender
    gender = StringVar(value="")  # Default value can be empty or a default selection
    # Create radio buttons for gender selection
    male_radio = Radiobutton(window, text="Male", variable=gender, value="Male", bg="#FFFFFF", fg="#000716", font=("Helvetica", 16))
    male_radio.place(x=1121.0, y=857.0)
    female_radio = Radiobutton(window, text="Female", variable=gender, value="Female", bg="#FFFFFF", fg="#000716", font=("Helvetica", 16))
    female_radio.place(x=1270.0, y=857.0)  # Adjust x position for spacing between radio buttons


    # Create "Save" button with hover effects
    save_button = Button(
        text="Save",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=save_changes,
        relief="flat",
        font=("Calibri", 15)
    )

    save_button.place(x=1420.0, y=348.0, width=130.0, height=42.59427261352539)

    # Bind hover and click events
    save_button.bind("<Enter>", on_enter_button)
    save_button.bind("<Leave>", on_leave_button)
    save_button.bind("<Button-1>", on_click_button)

    # Create "Upload Image" button with hover effects
    upload_button = Button(
        text="Upload Image",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=upload_image,  # Updated to call the new upload_image function
        relief="flat",
        font=("Calibri", 15)
    )

    upload_button.place(x=520.0, y=800.0, width=130.0, height=42.59427261352539)

    # Bind hover and click events
    upload_button.bind("<Enter>", on_enter_button)
    upload_button.bind("<Leave>", on_leave_button)
    upload_button.bind("<Button-1>", on_click_button)

    # Call header creation after the canvas
    create_header(window, canvas)

    # Fetch customer data after setting up the GUI
    get_customer_data()

    # Ensure window is not resizable and run the main loop
    window.resizable(False, True)
    window.mainloop()

if __name__ == "__main__":
    main_window()
