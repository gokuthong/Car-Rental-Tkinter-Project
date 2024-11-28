from tkinter import Button, Canvas, PhotoImage,Menu
import os
from PIL import Image, ImageTk
import importlib
import json

# Function to handle hover color on enter
def on_enter_button(e):
    try:
        e.widget.config(bg="#90EE90", highlightbackground="#90EE90")  # Light green hover color
    except Exception as ex:
        print(f"Error on enter: {ex}")

# Function to handle hover color on leave
def on_leave_button(e):
    try:
        e.widget.config(bg="#006400", highlightbackground="#006400")  # Dark green normal color
    except Exception as ex:
        print(f"Error on leave: {ex}")


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
    home_button = Button(
        window,
        text="Home",
        bg="#006400",  # Dark green normal color
        fg="white",  # Text color
        borderwidth=0,
        highlightthickness=0,
        command=lambda: goto_home_registered(),
        relief="flat",
        font=("Calibri", 15)
    )
    canvas.create_window(1033.0, 42.0, width=130.0, height=37.617591857910156, window=home_button)
    home_button.bind("<Enter>", on_enter_button)
    home_button.bind("<Leave>", on_leave_button)
    home_button.bind("<Button-1>", on_click_button)

    def goto_home_registered():
        window.destroy()

        SigmaTest3 = importlib.import_module("kit.Profile.home_registered")
        SigmaTest3.main_window()

    # Create "Search" button
    search_button = Button(
        window,
        text="Search",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: goto_search(),
        relief="flat",
        font=("Calibri", 15)
    )
    canvas.create_window(1183.0, 42.0, width=130.0, height=37.617591857910156, window=search_button)
    search_button.bind("<Enter>", on_enter_button)
    search_button.bind("<Leave>", on_leave_button)
    search_button.bind("<Button-1>", on_click_button)

    def goto_search():
        window.destroy()

        SigmaTest3 = importlib.import_module("SearchPage.SigmaTest3")
        SigmaTest3.main_window()

    # Create "Bookings" button
    bookings_button = Button(
        window,
        text="Bookings",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: goto_booking_list(),
        relief="flat",
        font=("Calibri", 15)
    )
    canvas.create_window(1333.0, 42.0, width=130.0, height=37.617591857910156, window=bookings_button)
    bookings_button.bind("<Enter>", on_enter_button)
    bookings_button.bind("<Leave>", on_leave_button)
    bookings_button.bind("<Button-1>", on_click_button)

    def goto_booking_list():
        window.destroy()

        booking_list = importlib.import_module("kit.Profile.booking_list")
        booking_list.main_window()

    # Create "Reviews" button
    reviews_button = Button(
        window,
        text="Reviews",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: goto_reviews(),
        relief="flat",
        font=("Calibri", 15)
    )
    canvas.create_window(1483.0, 42.0, width=130.0, height=37.617591857910156, window=reviews_button)
    reviews_button.bind("<Enter>", on_enter_button)
    reviews_button.bind("<Leave>", on_leave_button)
    reviews_button.bind("<Button-1>", on_click_button)

    def goto_reviews():
        window.destroy()

        reviews = importlib.import_module("kit.Profile.reviews")
        reviews.main_window()

    # Create "Support" button
    support_button = Button(
        window,
        text="Support",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: goto_support(),
        relief="flat",
        font=("Calibri", 15)
    )
    canvas.create_window(1633.0, 42.0, width=130.0, height=37.617591857910156, window=support_button)
    support_button.bind("<Enter>", on_enter_button)
    support_button.bind("<Leave>", on_leave_button)
    support_button.bind("<Button-1>", on_click_button)

    def goto_support():
        window.destroy()
        support = importlib.import_module("chen.buildregister.support")

        support.main_window()

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
    canvas.create_window(1783.0, 42.0, width=45.0, height=36.0, window=profile_button)

    # Create a dropdown menu for the Profile button
    profile_menu = Menu(window, tearoff=0)
    profile_menu.config(bg="#006400", fg="white", font=("Calibri", 16))  # Green theme and larger font
    profile_menu.add_command(label="View Profile", command=lambda: goto_profile())
    profile_menu.add_command(label="Edit Profile", command=lambda: goto_profile_edit())
    profile_menu.add_command(label="Logout", command=lambda: logout_user())

    # Bind the Profile button to show the dropdown menu
    profile_button.bind("<Button-1>", lambda event: profile_menu.post(event.x_root, event.y_root))

    def goto_profile():
        window.destroy()

        profile = importlib.import_module("kit.Profile.profile")
        profile.main_window()

    def goto_profile_edit():
        window.destroy()

        profile_edit = importlib.import_module("kit.Profile.profile_edit")
        profile_edit.main_window()

    def logout_user():
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


    # Load the cart icon image
    cart_path = os.path.join(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0",
                             "cart.png")
    cart_image = Image.open(cart_path)
    cart_image = cart_image.resize((45, 37), Image.LANCZOS)  # Resize the image
    cart_photo = ImageTk.PhotoImage(cart_image)  # Convert to PhotoImage

    # Create the Cart button with the image
    cart_button = Button(
        window,
        image=cart_photo,  # Use the image here
        bg="#006400",
        borderwidth=0,
        relief="flat",
        command=lambda: print("Cart button clicked")
    )
    canvas.create_window(1730.0, 42.0, width=45.0, height=36.0, window=cart_button)
    cart_button.bind("<Enter>", on_enter_button)
    cart_button.bind("<Leave>", on_leave_button)
    cart_button.bind("<Button-1>", lambda e: goto_cart())

    def goto_cart():
        window.destroy()
        testgui = importlib.import_module("ConfirmBookingPage.build.testgui")

        testgui.main_window()

    # Store the image reference to avoid garbage collection
    cart_button.image = cart_photo
