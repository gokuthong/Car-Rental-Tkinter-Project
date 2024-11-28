import importlib
import re, sqlite3, os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from PIL import Image, ImageTk  # Import Image and ImageTk for image manipulation
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox, Label, StringVar, Radiobutton, Toplevel
from tkinter.ttk import Combobox  # Import Combobox from tkinter.ttk
from chen.buildregister import login


def main_window():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    # Database setup
    def create_database():
        conn = sqlite3.connect(r'C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.dbb')  # Creates a database file
        cursor = conn.cursor()

        # Create a table for customer registration
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                password TEXT NOT NULL,
                profile_image_path TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    # Call the database creation function
    create_database()


    def insert_customer_data(username, email, age, gender, phone_number, password):
        verification_code = send_verification_email(email)
        if verification_code:
            show_verification_popup(username, email, age, gender, phone_number, password, verification_code)
        else:
            messagebox.showerror("Error", "Failed to send verification email. Data not saved.")

    def save_to_database(username, email, age, gender, phone_number, password, profile_image_path):
        conn = sqlite3.connect(r'C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO customers (username, email, age, gender, phone_number, password, profile_image_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, email, age, gender, phone_number, password, profile_image_path))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful and data saved!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already registered.")
        finally:
            conn.close()


    def check_password_requirements(event=None):
        password = entry_pass.get()
        feedback = []

        # Check if the password meets each requirement and add corresponding feedback
        if len(password) < 8:
            feedback.append("8 Characters")
        if not re.search(r"[A-Z]", password):
            feedback.append("UppercaseLetter")
        if not re.search(r"[a-z]", password):
            feedback.append("LowercaseLetter")
        if not re.search(r"\d", password):
            feedback.append("Number")
        if not re.search(r"[@$!%*?&#]", password):
            feedback.append("SpecialCharacter")

        # Display feedback messages
        if feedback:
            password_feedback.config(text=" | ".join(feedback), fg="red", bg="#FFF8F8")
        else:
            password_feedback.config(text="Password is strong", fg="green", bg="#FFF8F8")

    # Bind the key release event to check password requirements


    def validate_password():
        password = entry_pass.get()
        confirm_password = entry_confirm_password.get()
        username = entry_username.get()
        email = entry_email.get()
        age = entry_age.get()
        gender = selected_gender.get()
        phone_number = entry_num.get()

        # Check if the password meets the requirements (same checks as before)
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long.")
            return
        if not re.search(r"[A-Z]", password):
            messagebox.showerror("Error", "Password must contain at least one uppercase letter.")
            return
        if not re.search(r"[a-z]", password):
            messagebox.showerror("Error", "Password must contain at least one lowercase letter.")
            return
        if not re.search(r"\d", password):
            messagebox.showerror("Error", "Password must contain at least one number.")
            return
        if not re.search(r"[@$!%*?&#]", password):
            messagebox.showerror("Error", "Password must contain at least one special character.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
        else:
            insert_customer_data(username, email, age, gender, phone_number, password)  # Insert data into the database



    # Validate email format
    def validate_email(event=None):
        email = entry_email.get()
        # Basic email pattern
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.com+$"

        if re.match(email_pattern, email):
            email_feedback.config(text="Valid email", fg="green", bg="#FFF8F8")
        else:
            email_feedback.config(text="Invalid email", fg="red", bg="#FFF8F8")



    def toggle_password_visibility_password():
        if entry_pass.cget('show') == '*':
            entry_pass.config(show='')
            toggle_pass_btn.config(text="Hide")
        else:
            entry_pass.config(show='*')
            toggle_pass_btn.config(text="Show")

    def toggle_password_visibility_confirm_password():
        if entry_confirm_password.cget('show') == '*':
            entry_confirm_password.config(show='')
            toggle_confirm_btn.config(text="Hide")
        else:
            entry_confirm_password.config(show='*')
            toggle_confirm_btn.config(text="Show")


    def send_verification_email(email):
        verification_code = str(random.randint(100000, 999999))
        sender_email = "p23015743@student.newinti.edu.my"
        sender_password = "iicp050809070261"  # Use an App Password if 2FA is enabled
        receiver_email = email
        subject = "Email Verification Code"
        body = f"Your email verification code is: {verification_code}"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            return verification_code
        except smtplib.SMTPException as e:
            messagebox.showerror("Error", f"Failed to send email: {e}")
        return None


    def show_verification_popup(username, email, age, gender, phone_number, password, verification_code):
        # Define the popup window for verification
        # Popup setup
        popup = Toplevel(window)
        popup.title("Email Verification")
        popup.geometry("800x450")

        # Make the canvas background fill the entire window
        canvas_popup = Canvas(popup, bg="#E6F2E7", highlightthickness=0)  # Removed border
        canvas_popup.pack(fill="both", expand=True)  # Fill the entire window

        # Centered text for instruction
        canvas_popup.create_text(400, 150, text="Enter the verification code sent to your email",
                                 font=("Livvic Regular", 18), fill="#000000")

        # Entry box for verification code, centered
        entry_verification_code = Entry(popup, bd=0, bg="#D9D9D9", fg="#000716", font=("Calibri", 23))
        entry_verification_code.place(x=250,y=200,width=300, height=40)


        popup.resizable(False, False)

        # Define a nested function to access verification code and other variables
        def verify_code():
            entered_code = entry_verification_code.get()
            if entered_code == verification_code:
                messagebox.showinfo("Success", "Email Verified!")
                popup.destroy()
                save_to_database(username, email, age, gender, phone_number, password, profile_image_path=r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\kit\Profile\assets\frame0\profile_icon_default.png")
                window.destroy()  # Close the registration window
                login.main_window()
            else:
                messagebox.showerror("Error", "Incorrect verification code!")

        # Verify button
        button_verify = Button(popup, text="Verify", font=("Calibri", 14), command=verify_code)
        button_verify.place(x=500, y=200,height=40)
        popup.mainloop()

    window = Tk()
    window.title("Registration Page")
    window.geometry("1920x1200")
    window.configure(bg="#E6F2E7")

    canvas = Canvas(window, bg="#E6F2E7", height=1200, width=1920, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(1235.0, 600.0, image=image_image_1)

    canvas.create_text(960.0, 118.0, anchor="nw", text="Registration Form ", fill="#000000", font=("Livvic Regular", 70 * -1))
    canvas.create_text(891.0, 285.0, anchor="nw", text="Username:", fill="#000000", font=("Livvic Regular", 35 * -1))
    canvas.create_text(963.0, 394.0, anchor="nw", text="Email:", fill="#000000", font=("Livvic Regular", 35 * -1))
    canvas.create_text(982.0, 507.0, anchor="nw", text="Age:", fill="#000000", font=("Livvic Regular", 35 * -1))
    canvas.create_text(930.0, 620.0, anchor="nw", text="Gender:", fill="#000000", font=("Livvic Regular", 35 * -1))
    canvas.create_text(812.0, 733.0, anchor="nw", text="Phone Number:", fill="#000000", font=("Livvic Regular", 35 * -1))
    canvas.create_text(774.0, 940.0, anchor="nw", text="Confirm Password:", fill="#000000", font=("Livvic Regular", 35 * -1))
    canvas.create_text(895.0, 837.0, anchor="nw", text="Password:", fill="#000000", font=("Livvic Regular", 35 * -1))

    entry_username = PhotoImage(file=relative_to_assets("username_entry.png"))
    entry_username_bg = canvas.create_image(1429.0, 301.5, image=entry_username)
    entry_username = Entry(window, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, font=("Calibri 23"))
    entry_username.place(x=1125.0, y=273.0, width=608.0, height=55.0)

    entry_email = PhotoImage(file=relative_to_assets("email_entry.png"))
    entry_email_bg = canvas.create_image(1428.0, 400.5, image=entry_email)
    entry_email = Entry(window, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, font=("Calibri 23"))
    entry_email.place(x=1124.0, y=372.0, width=608.0, height=55.0)

    # Label to show feedback for email validation
    email_feedback = Label(window, text="", font=("Calibri", 15), bg="#E6F2E7", fg="red")
    email_feedback.place(x=1124.0, y=440.0)

    # Bind the key release event to the email validation function
    entry_email.bind("<KeyRelease>", validate_email)

    # Create the combo box for age selection
    age_options = [str(i) for i in range(18, 101)]  # Ages from 18 to 100
    entry_age = Combobox(window, values=age_options, font=("Calibri", 23), state="readonly")
    entry_age.place(x=1124.0, y=494.0, width=608.0, height=55.0)

    # StringVar to hold the selected gender
    selected_gender = StringVar(value="Male")  # Default value set to "Male"
    # Create and place the Male radiobutton
    radiobutton_male = Radiobutton(window, text="Male", variable=selected_gender, value="Male", font=("Calibri", 23), bg="#FFF8F8")
    radiobutton_male.place(x=1125.0, y=609.0)
    # Create and place the Female radiobutton
    radiobutton_female = Radiobutton(window, text="Female", variable=selected_gender, value="Female", font=("Calibri", 23), bg="#FFF8F8")
    radiobutton_female.place(x=1300.0, y=609.0)

    entry_num = PhotoImage(file=relative_to_assets("phone_num_entry.png"))
    entry_num_bg = canvas.create_image(1429.0, 637.5, image=entry_num)
    entry_num = Entry(window, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, font=("Calibri 23"))
    entry_num.place(x=1125.0, y=722.0, width=608.0, height=55.0)

    entry_pass = PhotoImage(file=relative_to_assets("password_entry.png"))
    entry_pass_bg = canvas.create_image(1429.0, 750.5, image=entry_pass)
    entry_pass = Entry(window, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, show="*", font=("Calibri 23"))
    entry_pass.place(x=1125.0, y=825.0, width=608.0, height=55.0)

    password_feedback = Label(window, text="", font=("Calibri", 15), bg="#E6F2E7", fg="red")
    password_feedback.place(x=1124.0, y=890.0)  # Adjust position below the password field
    entry_pass.bind("<KeyRelease>", check_password_requirements)


    entry_confirm_password = PhotoImage(file=relative_to_assets("confirm_password_entry.png"))
    entry_confirm_password_bg = canvas.create_image(1429.0, 863.5, image=entry_confirm_password)
    entry_confirm_password = Entry(window, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, show="*", font=("Calibri 23"))
    entry_confirm_password.place(x=1125.0, y=928.0, width=608.0, height=55.0)

    toggle_pass_btn = Button(window, text="Show", font=("Calibri", 14), bg="white", command=toggle_password_visibility_password)
    toggle_pass_btn.place(x=1682, y=840, height=30, width=50)  # Button for the password field

    toggle_confirm_btn = Button(window, text="Show", font=("Calibri", 14), bg="white", command=toggle_password_visibility_confirm_password)
    toggle_confirm_btn.place(x=1682, y=940, height=30, width=50)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(256.0, 600.0, image=image_image_2)

    image_car = PhotoImage(file=relative_to_assets("car_image.png"))
    image_car_pic = canvas.create_image(419.0, 578.0, image=image_car)

    button_register = PhotoImage(file=relative_to_assets("button_register.png"))
    button_reg = Button(image=button_register,borderwidth=0,highlightthickness=0,command=validate_password,relief="flat")
    button_reg.place(x=1125.0, y=1003.0, width=316.45379638671875, height=79.3388442993164)

    back_button_image = Image.open(relative_to_assets("backbutton.png"))

    # Set your desired width and height for the back button
    button_width = 50  # New width
    button_height = 50  # New height

    # Resize the image using Image.LANCZOS
    resized_image = back_button_image.resize((button_width, button_height), Image.LANCZOS)
    back_button_image = ImageTk.PhotoImage(resized_image)

    # Create a function to handle the back button click
    def go_back():
        window.destroy()
        home_unregistered = importlib.import_module("kit.Profile.home_unregistered")

        home_unregistered.main_window()

    # Create the back button and place it in the top left corner
    back_button = Button(window,image=back_button_image,borderwidth=0,highlightthickness=0,command=go_back,relief="flat",bg="#9ECA60")
    # Adjust the position and size of the button
    back_button.place(x=20, y=20, width=button_width, height=button_height)

    window.resizable(False, False)
    window.mainloop()

if __name__ == '__main__':
    main_window()