import importlib
import json
from pathlib import Path
from tkinter import Tk, Canvas, Entry, PhotoImage, Frame, Scrollbar, Listbox, font as tkFont, Toplevel, Button, messagebox
from tkcalendar import DateEntry
from datetime import date, timedelta
from chen.buildregister.header import create_header


def main_window():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\SearchPage\build\assets\frame0")
    PARAMS_FILE = OUTPUT_PATH / "search_params.json"  # JSON file path to store parameters


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    # Custom entry to show available locations and
    class AutocompleteEntry(Entry):
        def __init__(self, master=None, suggestions=[], *args, **kwargs):
            super().__init__(master, *args, **kwargs)
            self.suggestions = suggestions
            self.listbox = None
            self.listbox_open = False  # Track if the listbox is open

            # Set the font to "Red Hat Display Medium" size 20
            self.custom_font = tkFont.Font(family="Red Hat Display Medium", size=20)
            self.config(font=self.custom_font)

            # Bind events for this specific entry
            self.bind("<KeyRelease>", self.on_keyrelease)
            self.bind("<FocusOut>", self.on_focus_out)
            self.bind("<FocusIn>", self.on_focus_in)  # To show suggestions when clicked

            # Bind to detect clicks outside, specific to each instance
            self.master.bind_all("<Button-1>", self.click_outside)

        def on_focus_in(self, event):
            """Show all suggestions when the entry gains focus."""
            if not self.get().strip():
                self.show_suggestions(self.suggestions)

        def on_keyrelease(self, event):
            """Filter suggestions based on the current entry value."""
            input_value = self.get().strip()
            if input_value:
                filtered_suggestions = [s for s in self.suggestions if s.lower().startswith(input_value.lower())]
                if filtered_suggestions:
                    self.show_suggestions(filtered_suggestions)
                else:
                    self.hide_suggestions()
            else:
                self.show_suggestions(self.suggestions)  # Show all suggestions when input is empty

        def show_suggestions(self, suggestions):
            """Display the filtered suggestions in the Listbox."""
            if self.listbox:
                self.listbox.destroy()

            # Create a new listbox with the same master as the entry
            self.listbox = Listbox(self.master, height=5, font=self.custom_font, borderwidth=0, relief='flat')

            # Bind Listbox to suggestion selection
            self.listbox.bind("<ButtonRelease-1>", self.on_suggestion_select)

            # Position the Listbox directly below the Entry widget
            self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height() + 18, width=self.winfo_width() + 62)

            for suggestion in suggestions:
                self.listbox.insert('end', suggestion)

            self.listbox.lift()  # Bring the Listbox to the front
            self.listbox_open = True  # Mark the listbox as open

        def on_suggestion_select(self, event):
            """Update the entry with the selected suggestion from the Listbox."""
            if self.listbox and self.listbox.curselection():
                selected_index = self.listbox.curselection()[0]
                selected_value = self.listbox.get(selected_index)
                self.delete(0, 'end')  # Clear the current value of the entry
                self.insert(0, selected_value)  # Insert the selected suggestion
                self.hide_suggestions()

        def on_focus_out(self, event):
            """Hide suggestions if the user clicks away."""
            # Delay hiding to allow suggestion to be selected
            self.after(100, self.hide_suggestions)

        def hide_suggestions(self):
            """Destroy the suggestions Listbox if it exists."""
            if self.listbox:
                self.listbox.destroy()
                self.listbox = None
                self.listbox_open = False  # Mark the listbox as closed

        def click_outside(self, event):
            """Hide the Listbox if the user clicks outside of the entry or Listbox."""
            widget = event.widget
            if widget != self and widget != self.listbox:
                self.hide_suggestions()


    def update_scroll_region():
        """Update canvas scroll region."""
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


    def create_scrollable_container():
        """Set up vertical scrolling for canvas."""
        canvas.config(yscrollcommand=canvas_scrollbar.set, highlightthickness=0)
        canvas_scrollbar.config(orient="vertical", command=canvas.yview)

        canvas_scrollbar.pack(fill="y", side="right", expand=False)
        canvas.pack(fill="both", side="left", expand=True)

        # Create a window in the canvas for the scrollable frame
        bg_image_height = 1920
        canvas.create_window(0, bg_image_height, window=canvas_frame, anchor="nw")


    def on_mouse_wheel(event):
        global cal_pickup_opened, cal_dropoff_opened, entry_2, entry_3, listbox_open
        """Scroll canvas on mouse wheel movement, prevent scrolling above y=0."""
        if cal_pickup_opened or cal_dropoff_opened:
            return

        if canvas.yview()[0] > 0 or event.delta < 0:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            # Close the autocomplete suggestions if the listbox is open
            if entry_2.listbox_open:
                entry_2.hide_suggestions()

            if entry_3.listbox_open:
                entry_3.hide_suggestions()


    def toggle_date_entry_pickup(event):
        global cal_pickup_opened
        cal_pickup.drop_down()
        cal_pickup_opened = True

    def select_date_pickup(event):
        global cal_pickup_opened
        cal_pickup_opened = False


    def toggle_date_entry_dropoff(event):
        global cal_dropoff_opened
        cal_dropoff.drop_down()
        cal_dropoff_opened = True

    def select_date_dropoff(event):
        global cal_dropoff_opened
        cal_dropoff_opened = False


    def toggle_checkbox(event, image_id, img_1, img_2, elements_to_toggle, text_and_entry_data, pickup_text_id,
                        canvas_image_4, is_toggled):
        """Toggle between img_1 and img_2 on click for a canvas image and toggle visibility of specified elements."""
        global entry_3

        if not is_toggled[0]:  # If the state is not toggled yet
            # Switch to img_2 and show elements
            canvas.itemconfig(image_id, image=img_2)

            # Change the text to "Pickup Location"
            canvas.itemconfig(pickup_text_id, text="Pickup Location")

            # Move image_4 to the left by 135px
            canvas.move(canvas_image_4, -135, 0)

            # Create the dynamic text and entry only when toggled
            dropoff_text = canvas.create_text(
                204.0,
                616.0,
                anchor="nw",
                text="Dropoff Location",
                fill="#000000",
                font=("Red Hat Display Medium", 28 * -1)
            )
            entry_3 = AutocompleteEntry(
                window,
                locations,
                bd=0,
                bg="#FFFFFF",
                fg="#000716",
                highlightthickness=0,
                font=("Red Hat Display Medium", 20)
            )
            entry_3_window = canvas.create_window(501, 696.5, window=entry_3, width=448, height=44)

            # Show the images
            for element in elements_to_toggle:
                canvas.itemconfig(element, state='normal')

            # Store the references in case we need to hide them later
            text_and_entry_data["dropoff_text"] = dropoff_text
            text_and_entry_data["entry_3"] = entry_3_window

            is_toggled[0] = True  # Update toggle state

        else:
            # Switch back to img_1 and hide elements
            canvas.itemconfig(image_id, image=img_1)

            # Change the text back to "Pickup & Dropoff Location"
            canvas.itemconfig(pickup_text_id, text="Pickup & Dropoff Location")

            # Move image_4 back to its original position
            canvas.move(canvas_image_4, 135, 0)

            # Destroy the dynamic text and entry if they exist
            if "dropoff_text" in text_and_entry_data:
                canvas.delete(text_and_entry_data["dropoff_text"])
            if "entry_3" in text_and_entry_data:
                canvas.delete(text_and_entry_data["entry_3"])

            # Hide the images
            for element in elements_to_toggle:
                canvas.itemconfig(element, state='hidden')

            is_toggled[0] = False  # Update toggle state


    # UI
    global canvas, canvas_frame, canvas_scrollbar, locations, window, cal_pickup, cal_dropoff, cal_pickup_opened,\
        cal_dropoff_opened, entry_2, entry_3, listbox_open
    locations = ["Queensbay Mall, Bayan Lepas", "Setia Triangle, Bayan Lepas", "Gurney Plaza, Pulau Tikus"]
    cal_pickup_opened = False
    cal_dropoff_opened = False

    window = Tk()
    window.geometry("1920x1200")
    window.title("CarRentalTkinter - Search")
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
    canvas_frame = Frame(canvas)
    canvas_scrollbar = Scrollbar(window)

    # Scrolling functionality
    create_scrollable_container()

    # List to hold image references
    image_references = []

    # Entry Image 1
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    image_references.append(entry_image_1)
    canvas.create_image(121.5, 52.5, image=entry_image_1)

    # Image Creation
    images = [
        ("image_1.png", 960.0, 600.0),
        ("image_2.png", 953.0, 583.0),
        ("image_3.png", 993.0, 145.0),
        ("image_4.png", 578.0, 332.0),
        ("image_5.png", 1259.0, 503.0),
        ("image_6.png", 486.0, 404.921875),
        ("image_7.png", 407.3333435058594, 404.125),
        ("image_8.png", 1139.0, 405.9765625),
        ("image_9.png", 1063.0, 400.0),
        ("image_12.png", 1139.0, 620.078125),
        ("image_13.png", 1063.0, 614.0),
        ("image_16.png", 461.0, 628.0),
        ("image_17.png", 486.0, 701.2890625),
        ("image_18.png", 407.3333435058594, 700.4921875),
        ("image_19.png", 618.0, 153.0),
        ("image_20.png", 241.0, 530.0),
        ("image_21.png", 962.0, 1053.0),
        ("image_22.png", 1236.3333129882812, 777.5),
        ("image_25.png", 960.0, 1800.0),
        ("image_26.png", 959.0, 1406.0),
        ("image_27.png", 1551.0, 1881.0),
        ("image_28.png", 961.0, 1881.0),
        ("image_29.png", 368.0, 1881.0),
    ]

    # Variables for image toggle
    image_20 = PhotoImage(file=relative_to_assets("image_20.png"))
    image_23 = PhotoImage(file=relative_to_assets("image_23.png"))
    image_references.extend([image_20, image_23])

    # Create the canvas images and set dynamic names
    for image_file, x, y in images:
        img = PhotoImage(file=relative_to_assets(image_file))
        image_references.append(img)
        canvas_image = canvas.create_image(x, y, image=img)

        if image_file == "image_22.png":
            canvas.tag_bind(canvas_image, "<Button-1>", lambda event: retrieve_values())

        setattr(window, f"canvas_image_{image_file.split('.')[0]}", canvas_image)

    # Set the initial state of images 16, 17, 18 to hidden
    canvas.itemconfig(getattr(window, "canvas_image_image_16"), state='hidden')
    canvas.itemconfig(getattr(window, "canvas_image_image_17"), state='hidden')
    canvas.itemconfig(getattr(window, "canvas_image_image_18"), state='hidden')

    # image_21 button move down to 2nd window
    def smooth_scroll_to_position(target_y, step=1, delay=10):
        """
        Smoothly scroll the canvas to the target Y position.

        :param target_y: Target Y position to scroll to (e.g., 1200)
        :param step: Number of pixels to scroll per step (can be fractional for more smoothness)
        :param delay: Delay in milliseconds between each scroll step
        """
        current_scroll = canvas.canvasy(0)  # Get the current top Y coordinate of the canvas

        # Check if the canvas has reached or gone beyond the target scroll position
        if current_scroll < target_y:
            # Scroll the canvas down by 'step' units
            canvas.yview_scroll(step, "units")

            # Call this function again after 'delay' milliseconds to continue scrolling
            window.after(delay, smooth_scroll_to_position, target_y, step, delay)
        else:
            # If the canvas is exactly at the target, stop scrolling
            return

    canvas.tag_bind(getattr(window, "canvas_image_image_21"), "<Button-1>", lambda e: smooth_scroll_to_position(1200))

    # Calendar
    current_date = date.today()
    year, month, day = str(current_date).split("-")

    cal_pickup = DateEntry(
        window,
        selectmode="day",
        year=int(year),
        month=int(month),
        day=int(day),
        font=("Red Hat Display Medium", 18),
        width=15,
        borderwidth=0,
        highlightthickness=0,
        date_pattern="dd-MM-yyyy"
    )
    canvas.create_window(1160.0, 400.0, window=cal_pickup)

    cal_pickup.bind("<Button-1>", toggle_date_entry_pickup)
    cal_pickup._top_cal.bind("<Button-1>", select_date_pickup)

    cal_dropoff = DateEntry(
        window,
        selectmode="day",
        year=int(year),
        month=int(month),
        day=int(day),
        font=("Red Hat Display Medium", 18),
        width=15,
        borderwidth=0,
        highlightthickness=0,
        date_pattern="dd-MM-yyyy"
    )
    canvas.create_window(1160.0, 615.0, window=cal_dropoff)
    cal_dropoff.bind("<Button-1>", toggle_date_entry_dropoff)
    cal_dropoff._top_cal.bind("<Button-1>", select_date_dropoff)

    # Date validation
    def validate_dates():
        pickup_date = cal_pickup.get_date()
        dropoff_date = cal_dropoff.get_date()
        current_date = date.today()
        max_future_date = current_date + timedelta(days=180)

        # Condition A: Pickup date cannot be before the current date
        if pickup_date < current_date:
            messagebox.showerror("Invalid Date Selection", "Pickup date cannot be before the current date.")
            return False

        # Condition B: Dropoff date cannot be more than one month after pickup date
        if (dropoff_date - pickup_date).days > 30:
            messagebox.showerror("Invalid Date Selection",
                                 "Dropoff date cannot be more than 1 month after pickup date.")
            return False

        # Condition C: Both dates cannot be more than 6 months from today
        if pickup_date > max_future_date or dropoff_date > max_future_date:
            messagebox.showerror("Invalid Date Selection", "Dates cannot be more than 6 months in the future.")
            return False

        # Condition D: Pickup date cannot be after dropoff date
        if pickup_date > dropoff_date:
            messagebox.showerror("Invalid Date Selection",
                                 "Pickup date cannot be after dropoff date!")
            return False

        return True

    def validate_pickup_location():
        pickup_location = entry_2.get()

        if pickup_location not in locations:
            messagebox.showerror("Invalid Pickup Location",
                                 "Pickup location must be a valid location!")
            return False

        if not pickup_location:
            messagebox.showerror("Pickup Location not Selected",
                                 "You must select a pickup location!")
            return False

        return True


    # Pickup and Dropoff Text
    pickup_and_dropoff_text = canvas.create_text(
        204.0,
        320.0,
        anchor="nw",
        text="Pickup & Dropoff Location",
        fill="#000000",
        font=("Red Hat Display Medium", 28 * -1)
    )

    # Bind the toggle functionality to image_20
    canvas_image_20 = getattr(window, "canvas_image_image_20")
    canvas_image_4 = getattr(window, "canvas_image_image_4")  # Image to move

    elements_to_toggle = [
        getattr(window, "canvas_image_image_16"),
        getattr(window, "canvas_image_image_17"),
        getattr(window, "canvas_image_image_18"),
    ]
    text_and_entry_data = {}
    is_toggled = [False]  # Track the toggle state

    canvas.tag_bind(canvas_image_20, "<Button-1>",
                    lambda event: toggle_checkbox(event, canvas_image_20, image_20, image_23, elements_to_toggle,
                                                  text_and_entry_data, pickup_and_dropoff_text, canvas_image_4,
                                                  is_toggled))

    # Entry Background and Entry Fields
    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    image_references.append(entry_image_2)
    canvas.create_image(501.0, 405.0, image=entry_image_2)

    entry_2 = AutocompleteEntry(
        window,
        locations,
        bd=0,
        bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Red Hat Display Medium", 20)
        )
        canvas.create_window(501, 400, window=entry_2, width=448, height=44)  # Fixes entry in place

        canvas.create_text(
            963.0,
            321.0,
            anchor="nw",
            text="Pickup Date",
            fill="#000000",
            font=("Red Hat Display Medium", 28 * -1)
        )

        canvas.create_text(
            963.0,
            535.0,
            anchor="nw",
            text="Dropoff Date",
            fill="#000000",
            font=("Red Hat Display Medium", 28 * -1)
        )

        canvas.create_text(
            315.0,
            510.0,
            anchor="nw",
            text="Return at a different location",
            fill="#000000",
            font=("Red Hat Display Medium", 28 * -1)
        )


        def retrieve_values():
            global entry_2, entry_3
            # Retrieve Pickup and Dropoff location inputs
            pickup_location = entry_2.get()  # Value entered for Pickup Location
            try:
                dropoff_location = entry_3.get()
                if not dropoff_location:
                    dropoff_location = pickup_location  # Set default to empty string if no input is given
            except NameError:
                dropoff_location = pickup_location  # Set default to empty string if entry_3 doesn't exist

            # Retrieve Pickup and Dropoff dates
            pickup_date = cal_pickup.get_date().isoformat()
            dropoff_date = cal_dropoff.get_date().isoformat()

            # Store retrieved values in a dictionary
            params = {
                "pickup_location": pickup_location,
                "dropoff_location": dropoff_location,
                "pickup_date": pickup_date,
                "dropoff_date": dropoff_date,
            }

        # Write the parameters to a JSON file
        with open(PARAMS_FILE, 'w') as file:
            json.dump(params, file)
        print("Search parameters saved successfully.")

        if validate_dates() and validate_pickup_location():
            goto_booking()
        else:
            return

    def goto_booking():
        window.destroy()
        testingbooking = importlib.import_module("chen.buildregister.testingbooking")

        testingbooking.main_window()

    create_header(window, canvas)

    # Bind mouse wheel to canvas
    window.bind_all("<MouseWheel>", on_mouse_wheel)

    update_scroll_region()

    # Start the main event loop
    window.mainloop()



if __name__ == '__main__':
    main_window()