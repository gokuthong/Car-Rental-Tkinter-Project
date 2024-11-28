import importlib
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, Scrollbar, VERTICAL
from kit.Profile.car_popup import open_car_popup
import sqlite3
from chen.buildregister.header import create_header

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\kit\Profile\assets\frame0")


def main_window():
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def open_popup(car_type):
        try:
            open_car_popup(car_type)
        except Exception as e:
            print(f"Error opening popup for {car_type}: {e}")

    # Function to change button color on hover for Login


    def on_enter_button_reserve(e):
        reserve.config(bg="#90EE90")  # Light green hover color

    def on_leave_button_reserve(e):
        reserve.config(bg="#006400")  # Dark green default color

    window = Tk()
    window.geometry("1920x1200")
    window.configure(bg="green")

    # Create a frame to hold the canvas and scrollbar
    frame = Frame(window, width=1920, height=1200, bg="#F5F5F5")
    frame.pack(fill="both", expand=True)

    # Create the canvas and add it to the frame
    canvas = Canvas(frame, bg="#F5F5F5", width=1920, height=1200, scrollregion=(0, 0, 1920, 2000))
    canvas.pack(side="left", fill="both", expand=True)

    # Add a vertical scrollbar linked to the canvas
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.config(yscrollcommand=scrollbar.set)



    bg = PhotoImage(file=relative_to_assets("background.png"))
    b = canvas.create_image(959.0, 332.0, image=bg)

    reserve = Button(
        window,
        text="Reserve a Vehicle",
        bg="#006400",
        fg="white",
        activebackground="#90EE90",
        activeforeground="white",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        font=("Helvetica", 25, "bold"),
        command=lambda: goto_register()
    )

    def goto_register():
        window.destroy()

        register = importlib.import_module("chen.buildregister.register")
        register.main_window()

    reserve.place(x=760.0, y=380.0, width=415.0, height=75.0)
    reserve.bind("<Enter>", on_enter_button_reserve)
    reserve.bind("<Leave>", on_leave_button_reserve)

    def show_car_types():

        # Check if the review elements are currently visible
        if hasattr(show_reviews, "reviews_shown") and show_reviews.reviews_shown:
            # If reviews are already shown, hide all review elements first
            left_button.place_forget()
            right_button.place_forget()

            canvas.delete("review_img")
            canvas.delete("review_text")

            # Reset any review-related states or elements
            del show_reviews.reviews_shown

        # Show car type elements
        type1.place(x=920.0, y=851.0, width=87.0, height=21.0)
        type2.place(x=1290.0, y=847.0, width=179.0, height=28.0)
        type3.place(x=1120.0, y=1127.0, width=150.0, height=21.0)
        type4.place(x=539.0, y=850.0, width=62.0, height=22.0)
        type5.place(x=687.0, y=1133.0, width=108.0, height=21.0)

        # Create car images with tags to identify them
        canvas.create_image(963.0, 760.0, image=Sedan, tags="car_image")
        canvas.create_image(1365.0, 749.0, image=pickup, tags="car_image")
        canvas.create_image(1194.0, 1042.0, image=hatchback, tags="car_image")
        canvas.create_image(573.0, 756.0, image=suv, tags="car_image")
        canvas.create_image(725.0, 1049.0, image=minivan, tags="car_image")

        # Mark car types as shown
        show_car_types.car_types_shown = True

    def show_reviews():
        # Check if the review elements are already shown
        if hasattr(show_reviews, "reviews_shown") and show_reviews.reviews_shown:
            # If reviews are already shown, do nothing
            return

        # Hide car type elements before showing reviews
        type1.place_forget()
        type2.place_forget()
        type3.place_forget()
        type4.place_forget()
        type5.place_forget()

        # Hide car images
        canvas.delete("car_image")

        # Fetch reviews
        conn = sqlite3.connect(
            r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.review_description, r.rating, c.username, c.profile_image_path
            FROM reviews r
            INNER JOIN customers c ON r.customer_id = c.id
        """)
        reviews = cursor.fetchall()
        conn.close()

        # Pagination setup
        reviews_per_page = 2
        current_index = 0

        def display_reviews():
            # Clear previously displayed reviews
            canvas.delete("review_img")
            canvas.delete("review_text")

            # Display reviews for the current page
            x_position = 640
            for i in range(current_index, min(current_index + reviews_per_page, len(reviews))):
                review_description, rating, username, profile_image_path = reviews[i]

                # Create review image at the current x_position
                canvas.create_image(x_position, 904.0, image=home_review_image, tags="review_img")

                # Create username and rating text
                canvas.create_text(x_position + 125, 1025, anchor="nw", text=f"-{username}", fill="#000000",
                                   font=("Roboto Bold", 25 * -1), tags="review_text")

                stars = "★" * rating + "☆" * (5 - rating)
                canvas.create_text(x_position - 250, 1010, anchor="nw", text=stars, fill="gold",
                                   font=("Roboto Bold", 55 * -1), tags="review_text")

                # Create review description text
                canvas.create_text(x_position - 230, 750, anchor="nw", text=review_description, fill="#000000",
                                   font=("Roboto Bold", 21 * -1), width="480", tags="review_text")


                # Update the x_position for the next iteration (shift by some amount for spacing)
                x_position += 640  # Adjust the spacing between review elements

            # Hide the buttons if there are no pages to navigate
            if current_index == 0:
                left_button.place_forget()  # Hide the left button if on the first page
            else:
                left_button.place(
                    x=261.0,
                    y=860.0,
                    width=57.0,
                    height=91.0
                )  # Show the left button

            if current_index + reviews_per_page >= len(reviews):
                right_button.place_forget()  # Hide the right button if on the last page
            else:
                right_button.place(
                    x=1601.0,
                    y=859.0,
                    width=58.0,
                    height=92.0
                )  # Show the right button

        # Display the first set of reviews
        display_reviews()

        # Button actions with pagination logic
        def on_right_button_click():
            nonlocal current_index
            if current_index + reviews_per_page < len(reviews):
                current_index += reviews_per_page
                display_reviews()

        def on_left_button_click():
            nonlocal current_index
            if current_index - reviews_per_page >= 0:
                current_index -= reviews_per_page
                display_reviews()

        # Button images and actions with tags
        right_button.tag = "review_elements"  # Adding tag to identify this element
        right_button.config(command=on_right_button_click)

        left_button.tag = "review_elements"  # Adding tag to identify this element
        left_button.config(command=on_left_button_click)

        # Mark reviews as shown
        show_reviews.reviews_shown = True

    # Car Type Buttons
    button_sedan = PhotoImage(file=relative_to_assets("button_sedan.png"))
    type1 = Button(canvas, image=button_sedan, borderwidth=0, highlightthickness=0, command=lambda: open_popup('Sedan'),
                   relief="flat")

    button_pickup = PhotoImage(file=relative_to_assets("button_pickup.png"))
    type2 = Button(canvas, image=button_pickup, borderwidth=0, highlightthickness=0,
                   command=lambda: open_popup('Truck'), relief="flat")

    button_hatch = PhotoImage(file=relative_to_assets("button_hatch.png"))
    type3 = Button(canvas, image=button_hatch, borderwidth=0, highlightthickness=0,
                   command=lambda: open_popup('Hatchback'), relief="flat")

    button_suv = PhotoImage(file=relative_to_assets("button_suv.png"))
    type4 = Button(canvas, image=button_suv, borderwidth=0, highlightthickness=0, command=lambda: open_popup('SUV'),
                   relief="flat")

    button_minivan = PhotoImage(file=relative_to_assets("button_minivan.png"))
    type5 = Button(canvas, image=button_minivan, borderwidth=0, highlightthickness=0,
                   command=lambda: open_popup('Minivan'), relief="flat")

    Sedan = PhotoImage(file=relative_to_assets("Sedan.png"))
    pickup = PhotoImage(file=relative_to_assets("image_pickup.png"))
    hatchback = PhotoImage(file=relative_to_assets("image_hatch.png"))
    suv = PhotoImage(file=relative_to_assets("image_suv.png"))
    minivan = PhotoImage(file=relative_to_assets("image_minivan.png"))

    home_review_image = PhotoImage(file=relative_to_assets("home_review_container.png"))
    profile_image = PhotoImage(file=relative_to_assets("prof_container.png"))

    right_button_image = PhotoImage(file=relative_to_assets("right_button.png"))
    left_button_image = PhotoImage(file=relative_to_assets("left_button.png"))

    left_button = Button(
        image=left_button_image,
        borderwidth=0,
        bg="#F5F5F5",
        highlightthickness=0,
        command=lambda: print("left_button clicked"),
        relief="flat"
    )

    right_button = Button(
        image=right_button_image,
        bg="#F5F5F5",
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("right_button clicked"),
        relief="flat"
    )

    # Function to handle hover effects
    def on_enter_tab(event, tab):
        if tab["state"] == "normal":  # Only change hover effect for inactive tabs
            tab.configure(bg="#90EE90", fg="#006400")  # Light green background and dark green text

    def on_leave_tab(event, tab):
        if tab["state"] == "normal":  # Only revert for inactive tabs
            tab.configure(bg="#006400", fg="white")  # Default inactive style

    # Function to highlight the active tab
    def set_active_tab(active_tab):
        # Reset all tabs to inactive state
        for tab in [tab_car_types, tab_reviews]:
            tab.configure(bg="#006400", fg="white", state="normal")  # Default inactive style

        # Set the active tab style
        active_tab.configure(bg="#90EE90", fg="#006400", state="disabled")  # Highlight active tab

    # "Car Types" Tab Button
    tab_car_types = Button(
        canvas,
        text="Car Types",
        bg="#006400",  # Dark green (default)
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        font=("Helvetica", 15, "bold"),
        command=lambda: [show_car_types(), set_active_tab(tab_car_types)]  # Highlight when clicked
    )

    tab_car_types.place(x=820.0, y=615.0, width=150, height=45)

    # Add hover effects to "Car Types" tab
    tab_car_types.bind("<Enter>", lambda event: on_enter_tab(event, tab_car_types))
    tab_car_types.bind("<Leave>", lambda event: on_leave_tab(event, tab_car_types))

    # "Reviews" Tab Button
    tab_reviews = Button(
        canvas,
        text="Reviews",
        bg="#006400",  # Dark green (default)
        fg="white",
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        font=("Helvetica", 15, "bold"),
        command=lambda: [show_reviews(), set_active_tab(tab_reviews)]  # Highlight when clicked
    )

    tab_reviews.place(x=970.0, y=615.0, width=150, height=45)

    # Add hover effects to "Reviews" tab
    tab_reviews.bind("<Enter>", lambda event: on_enter_tab(event, tab_reviews))
    tab_reviews.bind("<Leave>", lambda event: on_leave_tab(event, tab_reviews))

    # Set the default active tab
    set_active_tab(tab_car_types)  # Car Types is active by default

    # Show Car Types by Default
    show_car_types()

    canvas.create_text(435.0, 160.0, anchor="nw",
                       text="Looking to rent a car but struggling to find the best deal?\n\nNo worries, we've got you covered!",
                       fill="#000000", font=("Arial", 30, "bold"))

    create_header(window,canvas)

    # Configure the scrollbar
    window.resizable(False, False)
    window.mainloop()


if __name__ == '__main__':
    main_window()