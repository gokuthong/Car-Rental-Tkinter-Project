from tkinter import Button, Canvas, PhotoImage,Menu
import os
from PIL import Image, ImageTk
import importlib
import json

# Function to handle hover color on enter
def on_enter_button(e):
    e.widget.config(bg="#90EE90")  # Light green hover color


# Function to handle hover color on leave
def on_leave_button(e):
    e.widget.config(bg="#006400")  # Dark green normal color


# Function to handle click color, keeping it the same as hover
def on_click_button(e):
    e.widget.config(bg="#90EE90")  # Stay light green on click


def create_header(window, canvas):
    # Load images using absolute or relative paths

    image_image_4 = PhotoImage(file=os.path.join(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0", "image_4.png"))

    # Create image_4 on the canvas
    canvas.create_image(960.0, 42.0, image=image_image_4)

    # Store references to images to avoid garbage collection

    canvas.image_image_4 = image_image_4

    canvas.create_text(220.0, 22.0, anchor="nw", text="Car Rental Bay", fill="#FFFFFF",
                       font=("Helvetica", 25, "bold"))

    # Create "Home" button
    dashboard_button = Button(
        window,
        text="Dashboard",
        bg="#006400",  # Dark green normal color
        fg="white",  # Text color
        borderwidth=0,
        highlightthickness=0,
        command=lambda: goto_admindashboard(),
        relief="flat",
        font=("Calibri", 15)
    )
    dashboard_button.place(x=1050.0, y=22.0, width=130.0, height=37.617591857910156)
    dashboard_button.bind("<Enter>", on_enter_button)
    dashboard_button.bind("<Leave>", on_leave_button)
    dashboard_button.bind("<Button-1>", on_click_button)

    def goto_admindashboard():
        window.destroy()
        dashboard = importlib.import_module("chen.buildregister.admindashboard")

        dashboard.main_window()

    # Create "Search" button
    import_button = Button(
        window,
        text="Import Car",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: goto_importcar(),
        relief="flat",
        font=("Calibri", 15)
    )
    import_button.place(x=1200.0, y=22.0, width=130.0, height=37.617591857910156)
    import_button.bind("<Enter>", on_enter_button)
    import_button.bind("<Leave>", on_leave_button)
    import_button.bind("<Button-1>", on_click_button)

    def goto_importcar():
        window.destroy()
        importcar = importlib.import_module("chen.buildregister.importcar")

        importcar.main_window()

    # Create "Bookings" button
    update_button = Button(
        window,
        text="Update Car",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: goto_updatecar(),
        relief="flat",
        font=("Calibri", 15)
    )
    update_button.place(x=1350.0, y=22.0, width=130.0, height=37.617591857910156)
    update_button.bind("<Enter>", on_enter_button)
    update_button.bind("<Leave>", on_leave_button)
    update_button.bind("<Button-1>", on_click_button)

    def goto_updatecar():
        window.destroy()

        updatecar = importlib.import_module("chen.buildregister.updatecar")
        updatecar.main_window()

    # Create "Reviews" button
    booking_button = Button(
        window,
        text="Manage Booking",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: goto_manage_bookings(),
        relief="flat",
        font=("Calibri", 15)
    )
    booking_button.place(x=1500.0, y=22.0, width=180.0, height=37.617591857910156)
    booking_button.bind("<Enter>", on_enter_button)
    booking_button.bind("<Leave>", on_leave_button)
    booking_button.bind("<Button-1>", on_click_button)

    def goto_manage_bookings():
        window.destroy()

        manage_bookings = importlib.import_module("kit.Profile.manage_bookings")
        manage_bookings.main_window()

    # # Create "Support" button
    # support_button = Button(
    #     window,
    #     text="Support",
    #     bg="#006400",
    #     fg="white",
    #     borderwidth=0,
    #     highlightthickness=0,
    #     command=lambda: print("Support button clicked"),
    #     relief="flat",
    #     font=("Calibri", 15)
    # )
    # support_button.place(x=1570.0, y=22.0, width=130.0, height=37.617591857910156)
    # support_button.bind("<Enter>", on_enter_button)
    # support_button.bind("<Leave>", on_leave_button)
    # support_button.bind("<Button-1>", on_click_button)

    # Load the profile icon image
    profile_path = os.path.join(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0", "profile_icon.png")
    profile_image = Image.open(profile_path)
    profile_image = profile_image.resize((45, 37), Image.LANCZOS)  # Resize the image
    profile_photo = ImageTk.PhotoImage(profile_image)  # Convert to PhotoImage

    # Create the Profile button with the image instead of text
    profile_button = Button(
        window,
        image=profile_photo,  # Use the image here
        bg="#006400",
        borderwidth=0,
        relief="flat",
        command=lambda: print("Profile button clicked")  # Functionality remains
    )
    profile_button.place(x=1720.0, y=22.0, width=45.0, height=36.0)  # Adjust dimensions based on icon size

    # Create a dropdown menu for the Profile button
    profile_menu = Menu(window, tearoff=0)
    profile_menu.config(bg="#006400", fg="white", font=("Calibri", 12))  # Green theme and larger font
    profile_menu.add_command(label="Logout", command=lambda: logout_admin())

    # Bind the Profile button to show the dropdown menu
    profile_button.bind("<Button-1>", lambda event: profile_menu.post(event.x_root, event.y_root))

    def logout_admin():
        window.destroy()
        home_unregistered = importlib.import_module("kit.Profile.home_unregistered")
        home_unregistered.main_window()

    # Bind hover effects for the Profile button
    def profile_enter(event):
        profile_button.config(bg="#90EE90")  # Light green hover color

    def profile_leave(event):
        profile_button.config(bg="#006400")  # Return to dark green on leave

    # Bind only hover, no click effects to prevent staying white
    profile_button.bind("<Enter>", profile_enter)
    profile_button.bind("<Leave>", profile_leave)

    # Store the profile image reference to avoid garbage collection
    profile_button.image = profile_photo
