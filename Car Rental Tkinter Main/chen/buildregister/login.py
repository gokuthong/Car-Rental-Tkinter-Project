import sqlite3, subprocess, json
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox, Label
from SearchPage import SigmaTest3
from chen.buildregister import admindashboard
import importlib
from PIL import Image, ImageTk

def main_window():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0")

    def open_script(window, is_admin=False):
        window.destroy()
        if is_admin:
            admindashboard.main_window()
        else:
            SigmaTest3.main_window()

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def toggle_password_visibility():
        if entry_password.cget('show') == '*':
            entry_password.config(show='')
            toggle_pass_btn.config(text="Hide")
        else:
            entry_password.config(show='*')
            toggle_pass_btn.config(text="Show")

    def login_user():
        email = entry_email.get()
        password = entry_password.get()

        conn = sqlite3.connect(r'C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db')
        cursor = conn.cursor()

        # Check for admin credentials first
        cursor.execute("SELECT id FROM admin WHERE email = ? AND password = ?", (email, password))
        admin_result = cursor.fetchone()

        if admin_result:
            current_admin_id = admin_result[0]
            messagebox.showinfo("Login Success", "Logged in as Admin!")

            # Save `id` to admin_session.json
            with open(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\admin_session.json", "w") as file:
                json.dump({"current_admin_id": current_admin_id}, file)

            open_script(window, is_admin=True)
        else:
            # If not an admin, check for regular user
            cursor.execute("SELECT id FROM customers WHERE email = ? AND password = ?", (email, password))
            result = cursor.fetchone()

            if result:
                current_user_id = result[0]
                messagebox.showinfo("Login Success", "Login successful!")

                # Save `id` to user_session.json
                with open(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\user_session.json", "w") as file:
                    json.dump({"id": current_user_id}, file)
                    print(f"User ID saved successfully: {current_user_id}")

                print("Login successful")

                open_script(window)
            else:
                messagebox.showerror("Error", "Invalid email or password")

        conn.close()


    window = Tk()
    window.title("Login Page")
    window.geometry("1920x1200")
    window.configure(bg = "#E6F2E7")


    canvas = Canvas(window, bg = "#E6F2E7", height = 1200, width = 1920, bd = 0, highlightthickness = 0, relief = "ridge")

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(688.0,600.0,image=image_image_1)

    canvas.create_text(530.0,169.0,anchor="nw",text="Login Form",fill="#000000",font=("Livvic Regular", 70 * -1))

    canvas.create_text(276.0, 485.0, anchor="nw", text="Email:", fill="#000000", font=("Livvic Regular", 35 * -1))

    canvas.create_text(220.0,612.0,anchor="nw",text="Password:",fill="#000000",font=("Livvic Regular", 35 * -1))

    entry_email_image = PhotoImage(file=relative_to_assets("email_entry.png"))
    entry_email_bg = canvas.create_image( 741.0, 629.5, image=entry_email_image)
    entry_email = Entry( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0,font=("Calibri",23))
    entry_email.place(x=437.0,y=473.0,width=608.0,height=55.0)

    entry_password_image = PhotoImage(file=relative_to_assets("password_entry.png"))
    entry_password_bg = canvas.create_image(741.0,501.5,image=entry_password_image)
    entry_password = Entry(bd=0,bg="#D9D9D9",fg="#000716",highlightthickness=0,show="*",font=("Calibri",23))
    entry_password.place(x=437.0, y=601.0, width=608.0, height=55.0)

    toggle_pass_btn = Button(window, text="Show", font=("Calibri", 14), bg="white", command=toggle_password_visibility)
    toggle_pass_btn.place(x=993, y=614, height=30, width=50)  # Button for the password field

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(1663.0,600.0,image=image_image_2)

    image_car_image = PhotoImage(file=relative_to_assets("car_image.png"))
    image_car = canvas.create_image(1452.0,578.0,image=image_car_image)

    button_image_login = PhotoImage(file=relative_to_assets("button_login.png"))
    button_login = Button(image=button_image_login, borderwidth=0, highlightthickness=0, command=login_user, relief="flat")
    button_login.place(x=530.0, y=924.0, width=316.45379638671875, height=79.3388442993164)


    # Create a label for the login text above the register button
    login_label = Label(window,text="Not registered yet? Register!", font=("Calibri", 16,"underline"),bg="#FFF8F8",fg="darkblue", cursor="hand2")
    login_label.place(x=575, y=700)

    # Bind the label click to the go_to_login function
    login_label.bind("<Button-1>", lambda e: goto_register())

    def goto_register():
        window.destroy()
        register = importlib.import_module("chen.buildregister.register")

        register.main_window()

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
    back_button = Button(window, image=back_button_image, borderwidth=0, highlightthickness=0, command=go_back,
                         relief="flat", bg="#E6F2E7")
    # Adjust the position and size of the button
    back_button.place(x=20, y=20, width=button_width, height=button_height)

    window.resizable(False, False)
    window.mainloop()

if __name__ == '__main__':
    main_window()