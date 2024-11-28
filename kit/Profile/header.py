from tkinter import Button, Canvas, PhotoImage,Menu
import os
import customtkinter as ctk
from PIL import Image, ImageTk

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

    image_image_4 = PhotoImage(file=os.path.join("C:/Users/User/Desktop/Profile/assets/frame0", "image_4.png"))



    # Create image_4 on the canvas
    canvas.create_image(960.0, 42.0, image=image_image_4)

    # Store references to images to avoid garbage collection

    canvas.image_image_4 = image_image_4

    canvas.create_text(220.0, 22.0, anchor="nw", text="Car Rental System", fill="#FFFFFF",
                       font=("Helvetica", 25, "bold"))

    # Create "Home" button
    home_button = Button(
        window,
        text="Home",
        bg="#006400",  # Dark green normal color
        fg="white",  # Text color
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Home button clicked"),
        relief="flat",
        font=("Calibri", 15)
    )
    home_button.place(x=970.0, y=22.0, width=130.0, height=37.617591857910156)
    home_button.bind("<Enter>", on_enter_button)
    home_button.bind("<Leave>", on_leave_button)
    home_button.bind("<Button-1>", on_click_button)

    # Create "Search" button
    search_button = Button(
        window,
        text="Search",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Search button clicked"),
        relief="flat",
        font=("Calibri", 15)
    )
    search_button.place(x=1120.0, y=22.0, width=130.0, height=37.617591857910156)
    search_button.bind("<Enter>", on_enter_button)
    search_button.bind("<Leave>", on_leave_button)
    search_button.bind("<Button-1>", on_click_button)

    # Create "Bookings" button
    bookings_button = Button(
        window,
        text="Bookings",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Bookings button clicked"),
        relief="flat",
        font=("Calibri", 15)
    )
    bookings_button.place(x=1270.0, y=22.0, width=130.0, height=37.617591857910156)
    bookings_button.bind("<Enter>", on_enter_button)
    bookings_button.bind("<Leave>", on_leave_button)
    bookings_button.bind("<Button-1>", on_click_button)

    # Create "Reviews" button
    reviews_button = Button(
        window,
        text="Reviews",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Reviews button clicked"),
        relief="flat",
        font=("Calibri", 15)
    )
    reviews_button.place(x=1420.0, y=22.0, width=130.0, height=37.617591857910156)
    reviews_button.bind("<Enter>", on_enter_button)
    reviews_button.bind("<Leave>", on_leave_button)
    reviews_button.bind("<Button-1>", on_click_button)

    # Create "Support" button
    support_button = Button(
        window,
        text="Support",
        bg="#006400",
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Support button clicked"),
        relief="flat",
        font=("Calibri", 15)
    )
    support_button.place(x=1570.0, y=22.0, width=130.0, height=37.617591857910156)
    support_button.bind("<Enter>", on_enter_button)
    support_button.bind("<Leave>", on_leave_button)
    support_button.bind("<Button-1>", on_click_button)

    # Load the profile icon image
    profile_path = os.path.join("C:/Users/User/Desktop/Profile/assets/frame0", "profile_icon.png")
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
    profile_menu.config(bg="#006400", fg="white", font=("Calibri", 16))  # Green theme and larger font
    profile_menu.add_command(label="View Profile", command=lambda: print("View Profile clicked"))
    profile_menu.add_command(label="Edit Profile", command=lambda: print("Edit Profile clicked"))
    profile_menu.add_command(label="Logout", command=lambda: print("Logout clicked"))

    # Bind the Profile button to show the dropdown menu
    profile_button.bind("<Button-1>", lambda event: profile_menu.post(event.x_root, event.y_root))

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