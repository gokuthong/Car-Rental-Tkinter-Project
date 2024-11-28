import sqlite3
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, filedialog, Label, END, Radiobutton, StringVar, ttk, messagebox
from PIL import Image, ImageTk
from chen.buildregister.header import create_header
import importlib
import json
import re

# Path setup
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\kit\Profile\assets\frame0")

def main_window():

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    # Load current user ID from JSON file
    def get_current_user_id():
        try:
            with open(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\user_session.json", "r") as file:
                data = json.load(file)
                return data.get("id")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading current user session file: {e}")
            return None

    def toggle_password(password_entry, show_hide_button):
        current_show_state = password_entry.cget('show')
        print(f"Current show state for {password_entry}: '{current_show_state}'")  # Debug print

        if current_show_state == '':
            # Hide password
            password_entry.config(show='*')
            show_hide_button.config(text="Show")
        else:
            # Show password
            password_entry.config(show='')
            show_hide_button.config(text="Hide")

    def check_password(event=None):
        user_id = get_current_user_id()
        if not user_id:
            print("No current user ID found.")
            return
        # Only proceed if the current_password field is not empty
        if current_password.get().strip() != "":
            conn = sqlite3.connect(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM customers WHERE id = ?", (user_id,))
            result = cursor.fetchone()

            if result:
                stored_password = result[0]
                entered_password = current_password.get()

                if entered_password == stored_password:
                    feedback_label.config(text="Password is correct", fg="green")
                    error_label.config(text="")  # Clear error message if current password is correct
                else:
                    feedback_label.config(text="Incorrect password, please try again", fg="red")
                    error_label.config(text="Please confirm the current password first.", fg="red")
            else:
                feedback_label.config(text="Customer not found", fg="red")
                error_label.config(text="Please confirm the current password first.", fg="red")

            conn.close()
        else:
            # Clear the feedback label and error label if no password is entered
            feedback_label.config(text="")
            error_label.config(text="")

    def check_and_change_password():
        user_id = get_current_user_id()

        password_valid = validate_password()

        if not password_valid:
            return

        # Check if feedback_label text is "Password is correct"
        if feedback_label.cget("text") == "Password is correct":
            new_pass_text = new_password.get()
            confirm_pass_text = confirm_password.get()

            # Check if the new password and confirm password match
            if new_pass_text == confirm_pass_text:
                # Connect to the database
                conn = sqlite3.connect(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
                cursor = conn.cursor()

                # Update the password in the database
                cursor.execute("""
                    UPDATE customers
                    SET password = ?
                    WHERE id = ?
                """, (new_pass_text, user_id))
                print(new_pass_text)
                conn.commit()  # Commit the changes
                conn.close()  # Close the database connection

                goto_profile()

            else:
                # Display error if new passwords do not match
                error_label.config(text="New passwords do not match.", fg="red")
        else:
            # Display error if current password is incorrect or not confirmed
            error_label.config(text="Please confirm the current password first.", fg="red")

    def goto_profile():
        window.destroy()
        profile = importlib.import_module("kit.Profile.profile")

        profile.main_window()

    # Define hover color functions
    def on_enter_button(e):
        e.widget.config(bg="#90EE90")  # Light green hover color

    def on_leave_button(e):
        e.widget.config(bg="#006400")  # Dark green normal color

    def on_click_button(e):
        e.widget.config(bg="#90EE90")  # Stay light green on click

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



    bg = PhotoImage(file=relative_to_assets("bg.png"))
    canvas.create_image(960.0, 653.0, image=bg)

    profile_header = PhotoImage(file=relative_to_assets("profile_header.png"))
    canvas.create_image(960.0, 243.0, image=profile_header)

    window_bg = PhotoImage(
        file=relative_to_assets("window_bg.png"))
    canvas.create_image(960.0, 694.0, image=window_bg)

    canvas.create_text(370.0, 225.0, anchor="nw", text="Change Password", fill="#FFFFFF",
                       font=("Helvetica", 25, "bold"))

    # Labels and entry fields moved up by 50px
    canvas.create_text(
        547.0, 442.0, anchor="nw",  # Moved up by 50px
        text="Current Password:",
        fill="#000000",
        font=("Inter", 28 * -1)
    )

    canvas.create_text(
        587.0, 710.0, anchor="nw",  # Moved up by 50px
        text="New Password:",
        fill="#000000",
        font=("Inter", 28 * -1)
    )

    canvas.create_text(
        474.0, 861.0, anchor="nw",  # Moved up by 50px
        text="Confirm New Password:",
        fill="#000000",
        font=("Inter", 28 * -1)
    )

    current_pass = PhotoImage(
        file=relative_to_assets("entry_border_3.png"))
    canvas.create_image(
        1110.0, 459.5, image=current_pass  # Moved up by 50px
    )
    current_password = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        show="*",
        font = ("Helvetica", 20),

    )
    current_password.place(
        x=820.0, y=427.0, width=580.0, height=63.0  # Moved up by 50px
    )

    current_password.bind("<KeyRelease>", check_password)  # Bind the KeyRelease event

    # Label to display feedback on password match status
    feedback_label = Label(window, text="", font=("Helvetica", 16), fg="red")
    feedback_label.place(x=820.0, y=500.0)

    new_pass = PhotoImage(file=relative_to_assets("entry_border_3.png"))
    canvas.create_image(
        1110.0, 726.5, image=new_pass  # Moved up by 50px
    )

    new_password = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        show="*",
        font = ("Helvetica", 20)
    )
    new_password.place(
        x=820.0, y=694.0, width=580.0, height=63.0  # Moved up by 50px
    )

    def check_password_requirements(event=None):
        password = new_password.get()
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


    password_feedback = Label(window, text="", font=("Calibri", 15), bg="#E6F2E7", fg="red")
    password_feedback.place(x=820.0, y=765.0)  # Adjust position below the password field
    new_password.bind("<KeyRelease>", check_password_requirements)
    # Bind the key release event to check password requirements


    def validate_password():
        password = new_password.get()

        # Check if the password meets the requirements (same checks as before)
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long.")
            return False
        if not re.search(r"[A-Z]", password):
            messagebox.showerror("Error", "Password must contain at least one uppercase letter.")
            return False
        if not re.search(r"[a-z]", password):
            messagebox.showerror("Error", "Password must contain at least one lowercase letter.")
            return False
        if not re.search(r"\d", password):
            messagebox.showerror("Error", "Password must contain at least one number.")
            return False
        if not re.search(r"[@$!%*?&#]", password):
            messagebox.showerror("Error", "Password must contain at least one special character.")
            return False

        return True


    confirm_pass = PhotoImage(
        file=relative_to_assets("entry_border_3.png"))
    canvas.create_image(
        1110.0, 877.5, image=confirm_pass  # Moved up by 50px
    )
    confirm_password = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        show="*",
        font = ("Helvetica", 20)
    )
    confirm_password.place(
        x=820.0, y=845.0, width=580.0, height=63.0  # Moved up by 50px
    )

    line = PhotoImage(
        file=relative_to_assets("line.png"))
    canvas.create_image(
        970.0, 593.0, image=line
    )

    show_hide_button_1 = Button(
        text="Show",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        font=("Calibri", 12)
    )
    show_hide_button_1.place(x=1340.0, y=427.5, width=61.0, height=64.0)

    show_hide_button_1.bind("<Enter>", on_enter_button)
    show_hide_button_1.bind("<Leave>", on_leave_button)
    show_hide_button_1.bind("<Button-1>", on_click_button)

    show_hide_button_2 = Button(
        text="Show",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        font=("Calibri", 12)
    )
    show_hide_button_2.place(x=1340.0, y=695, width=61.0, height=64.0)

    show_hide_button_2.bind("<Enter>", on_enter_button)
    show_hide_button_2.bind("<Leave>", on_leave_button)
    show_hide_button_2.bind("<Button-1>", on_click_button)

    show_hide_button_3 = Button(
        text="Show",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        font=("Calibri", 12)
    )
    show_hide_button_3.place(x=1340.0, y=846, width=61.0, height=64.0)

    show_hide_button_3.bind("<Enter>", on_enter_button)
    show_hide_button_3.bind("<Leave>", on_leave_button)
    show_hide_button_3.bind("<Button-1>", on_click_button)

    # Assign the command to each button separately after definition
    show_hide_button_1.config(command=lambda: toggle_password(current_password, show_hide_button_1))
    show_hide_button_2.config(command=lambda: toggle_password(new_password, show_hide_button_2))
    show_hide_button_3.config(command=lambda: toggle_password(confirm_password, show_hide_button_3))

    error_label = Label(window, text="", font=("Helvetica", 12), fg="red")
    error_label.place(x=1420.0, y=400.0)


    # Create "Save" button with hover effects
    save_button = Button(
        text="Save",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command= check_and_change_password,
        relief="flat",
        font=("Calibri", 15)
    )

    save_button.place(x=1420.0, y=348.0, width=130.0, height=42.59427261352539)

    # Bind hover and click events
    save_button.bind("<Enter>", on_enter_button)
    save_button.bind("<Leave>", on_leave_button)
    save_button.bind("<Button-1>", on_click_button)



    # Call header creation after the canvas
    create_header(window, canvas)

    # Ensure window is not resizable and run the main loop
    window.resizable(False, True)
    window.mainloop()

if __name__ == "__main__":
    main_window()
