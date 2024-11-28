import sqlite3
from pathlib import Path
from PIL import Image, ImageTk
from chen.buildregister.headeradmin import create_header
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox, Entry, StringVar, Label, font, ttk, filedialog


def main_window():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0")


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    window = Tk()

    window.geometry("1920x1200")
    window.configure(bg = "#FFFFFF")


    canvas = Canvas(window,bg = "#FFFFFF",height = 1200,width = 1920,bd = 0,highlightthickness = 0,relief = "ridge")



    canvas.place(x = 0, y = 0)
    image_background = r'C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0\backgroundadmin.jpeg'
    bg_image = Image.open(image_background)
    bg_image = bg_image.resize((1920, 1200), Image.LANCZOS)  # Resize to window size
    bg_image_tk = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)
    canvas.bg_image_tk = bg_image_tk


    importcar_path = r'C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0\import_car.png'
    importcar = Image.open(importcar_path)
    importcar = importcar.resize((500, 380), Image.LANCZOS)
    importcar = ImageTk.PhotoImage(importcar)
    import_car = canvas.create_image(504.0, 760.0, image=importcar)



    # Title text
    canvas.create_text(220.0, 24.0, anchor="nw", text="Car Rental System", fill="#FFFFFF", font=("Helvetica", 25, "bold"))

    # Function to handle hover color on enter
    def on_enter_button(e):
        e.widget.config(bg="#90EE90")  # Light green hover color

    def on_leave_button(e):
        e.widget.config(bg="#006400")  # Dark green normal color

    def on_click_button(e):
        e.widget.config(bg="#90EE90")  # Stay light green on click

    def on_click_back_button(e):
        e.widget.config(bg="#4CAF50")  # Change the background to #4CAF50 when clicked
        go_back()  # Trigger the back button action

    # Back button functionality
    def go_back():
        messagebox.showinfo("Back", "Going back to the previous page")

    # Add the back button and align it with the title
    backbutton_path = r'C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\assets\frame0\backbutton.png'
    backbutton = Image.open(backbutton_path)
    backbutton = backbutton.resize((50, 50), Image.LANCZOS)
    backbutton = ImageTk.PhotoImage(backbutton)

    # Place the back button at the top-left, aligning with the title
    back_button = Button(window, image=backbutton, bg="#4CAF50", bd=0, highlightthickness=0, activebackground="#4CAF50", command=go_back)
    back_button.place(x=100, y=15)  # Adjust position to align with the title
    back_button.bind("<Enter>", on_enter_button)
    back_button.bind("<Leave>", on_leave_button)
    back_button.bind("<Button-1>", on_click_back_button)  # Apply custom click event for back button

    canvas.img1 = backbutton  # Keep a reference to the image


    def connect_db():
        return sqlite3.connect(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")


    # Function to change the car image
    global new_image_path
    new_image_path = None


    def change_car_image():
        global new_image_path  # Use a global variable to temporarily hold the new image path
        selected_item = car_tree.selection()
        if not selected_item:
            messagebox.showwarning("Select Car", "Please select a car to change the image.")
            return

        # Open a file dialog to select a new image
        new_image_path = filedialog.askopenfilename(
            title="Select Car Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )

        if new_image_path:
            try:
                # Display the new image as a preview without updating the database
                car_image = Image.open(new_image_path)
                car_image = car_image.resize((500, 380), Image.LANCZOS)
                car_image_tk = ImageTk.PhotoImage(car_image)
                canvas.itemconfig(import_car, image=car_image_tk)
                canvas.car_image_tk = car_image_tk  # Keep a reference to avoid garbage collection

            except Exception as e:
                messagebox.showerror("Image Error", f"Unable to load image: {e}")

    # Attach this function to the button

    add_image_button = Button(window, text="Change Car Image", bg="#006400", fg="white", font=("Calibri", 15), command=change_car_image)
    add_image_button.place(x=950.0, y=1000.0, width=150.0, height=50.0)
    add_image_button.config(command=change_car_image)

    # Fetch all car details
    def fetch_all_cars():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM car")
        cars = cursor.fetchall()
        conn.close()
        return cars

    # Display car details in the treeview
    def display_cars():
        for car in fetch_all_cars():
            car_tree.insert("", "end", values=car)

    def update_car():
        global new_image_path
        selected_item = car_tree.selection()
        if not selected_item:
            messagebox.showwarning("Select Car", "Please select a car to update.")
            return

        car_id = car_tree.item(selected_item, "values")[0]
        new_car_plate = car_plate_var.get()
        new_make_model = make_model_var.get()
        new_car_type = car_type_var.get()
        new_rate = rate_var.get()
        new_seating_capacity = seating_capacity_var.get()
        new_colour = colour_var.get()
        new_location = location_var.get()

        # Retrieve the current image path or use the new one if selected
        image_path = new_image_path if new_image_path else car_tree.item(selected_item, "values")[8]

        # Validate input
        try:
            new_rate = float(new_rate)
            new_seating_capacity = int(new_seating_capacity)
        except ValueError:
            messagebox.showerror("Invalid Input", "Rate must be a number and Seating Capacity an integer.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE car
            SET car_plate = ?, make_model = ?, car_type = ?, rate = ?, seating_capacity = ?, colour=?, location=?, image_path = ?
            WHERE id = ?
        """, (new_car_plate, new_make_model, new_car_type, new_rate, new_seating_capacity,new_colour, new_location, image_path, car_id))
        conn.commit()
        conn.close()

        # Refresh treeview and clear input fields
        car_tree.delete(*car_tree.get_children())
        display_cars()
        car_plate_var.set("")
        make_model_var.set("")
        car_type_var.set("")
        rate_var.set("")
        seating_capacity_var.set("")
        colour_var.set("")
        location_var.set("")

        # Reset new_image_path after update
        new_image_path = None

        messagebox.showinfo("Update Successful", "Car details updated successfully.")

    # Function to delete a selected car
    def delete_car():
        selected_item = car_tree.selection()  # Get selected item in the Treeview
        if not selected_item:
            messagebox.showwarning("Select Car", "Please select a car to delete.")
            return

        car_id = car_tree.item(selected_item, "values")[0]  # Get the car ID from the selected item
        response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this car?")
        if response:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM car WHERE id = ?", (car_id,))  # Delete the car from the database
            conn.commit()
            conn.close()

            car_tree.delete(selected_item)  # Remove the car from the Treeview
            messagebox.showinfo("Delete Successful", "Car deleted successfully.")

    # Add Delete button to the window
    delete_button = Button(window, text="Delete Car", command=delete_car, font=("Calibri", 18), bg="#FF0000", fg="white")
    delete_button.place(x=1400, y=1000)



    # Populate fields when a car is selected
    def on_car_select(event):
        selected_item = car_tree.selection()
        if selected_item:
            car_details = car_tree.item(selected_item, "values")
            car_plate_var.set(car_details[1])
            make_model_var.set(car_details[2])
            car_type_var.set(car_details[3])
            rate_var.set(car_details[4])
            seating_capacity_var.set(car_details[5])
            colour_var.set(car_details[6])
            location_var.set(car_details[7])

            # Show car image in the placeholder
            image_path = car_details[8]
            try:
                car_image = Image.open(image_path)
                car_image = car_image.resize((500, 380), Image.LANCZOS)
                car_image_tk = ImageTk.PhotoImage(car_image)
                canvas.itemconfig(import_car, image=car_image_tk)
                canvas.car_image_tk = car_image_tk
            except Exception as e:
                messagebox.showerror("Image Error", f"Unable to load image: {e}")

    # Car table (Treeview)
    columns = ("ID", "Plate", "Make & Model", "Type", "Rate", "Seating Capacity", "Colour", "Location", "Image Path")
    car_tree = ttk.Treeview(window, columns=columns, show="headings", height=10)
    car_tree.tag_configure('centered', anchor="center")

    # Set up the columns, hiding the "Image Path" column by setting its width to 0
    for col in columns:
        car_tree.heading(col, text=col)  # Set the header text
        if col == "ID" :
            car_tree.column(col, width=50, anchor="center")
        if col == "Location":
            car_tree.column(col, width=250, anchor="center")
        elif col == "Image Path":
            car_tree.column(col, width=0, stretch=False)  # Hide the Image Path column visually
        else:
            car_tree.column(col, anchor="center")  # Center-align headers and cells for visible columns

    car_tree.place(x=200, y=130)


    # Ensure the Treeview selection binding is still active
    car_tree.bind("<<TreeviewSelect>>", on_car_select)

    # Create vertical and horizontal scrollbars
    scroll_y = ttk.Scrollbar(window, orient="vertical", command=car_tree.yview)

    # Configure the scrollbars with the Treeview
    car_tree.configure(yscrollcommand=scroll_y.set)

    # Place the scrollbars near the Treeview table
    scroll_y.place(x=1700, y=130, height=327)  # Adjust height to match the table height


    table_font = font.Font(family="Calibri", size=14)  # Font for table content
    header_font = font.Font(family="Calibri", size=16, weight="bold")  # Font for table headers

    # Apply the fonts using ttk.Style
    style = ttk.Style()
    style.configure("Treeview", rowheight=30)
    style.configure("Treeview.Heading", font=header_font)  # Header font
    style.configure("Treeview", font=table_font)

    # Entry fields for updating car details
    car_plate_var = StringVar()
    make_model_var = StringVar()
    car_type_var = StringVar()
    rate_var = StringVar()
    seating_capacity_var = StringVar()
    colour_var = StringVar()
    location_var = StringVar()



    Label(window, text="Car Plate:",font=("Calibri",20)).place(x=930,y=480)
    car_plate_entry = Entry(window, textvariable=car_plate_var, width=30, font=("Calibri",20))
    car_plate_entry.place(x=1200,y=480)

    Label(window, text="Make & Model:",font=("Calibri",20)).place(x=930,y=550)
    make_model_entry = Entry(window, textvariable=make_model_var, width=30, font=("Calibri",20))
    make_model_entry.place(x=1200,y=550)

    car_types = ["Sedan", "SUV", "Hatchback", "Truck", "Minivan"]
    Label(window, text="Car Type:",font=("Calibri",20)).place(x=930,y=620)
    car_type_entry = ttk.Combobox(window, textvariable=car_type_var,values=car_types, width=28,font=("Calibri",20))
    car_type_entry.place(x=1200,y=620)

    Label(window, text="Rate:",font=("Calibri",20)).place(x=930,y=690)
    rate_entry = Entry(window, textvariable=rate_var, width=30,font=("Calibri",20))
    rate_entry.place(x=1200,y=690)

    car_seat = [5,6,7]
    Label(window, text="Seating Capacity:",font=("Calibri",20)).place(x=930,y=760)
    seating_capacity_entry = ttk.Combobox(window, textvariable=seating_capacity_var, values=car_seat, width=28,font=("Calibri",20))
    seating_capacity_entry.place(x=1200,y=760)

    Label(window, text="Colour:",font=("Calibri",20)).place(x=930,y=830)
    colour_entry = Entry(window, textvariable=colour_var, width=30,font=("Calibri",20))
    colour_entry.place(x=1200,y=830)

    location_place = ["Queensbay Mall, Bayan Lepas", "Setia Triangle, Bayan Lepas", "Gurney Plaza, Pulau Tikus"]
    Label(window, text="Location:",font=("Calibri",20)).place(x=930,y=900)
    location_entry = ttk.Combobox(window, textvariable=location_var, values=location_place, width=28,font=("Calibri",20))
    location_entry.place(x=1200,y=900)

    # Update button
    update_button = Button(window, text="Update Car", command=update_car, font=("Calibri",18))
    update_button.place(x=1200,y=1000)

    # Display cars on startup
    display_cars()


    create_header(window, canvas)
    window.resizable(False, False)
    window.mainloop()

if __name__ == '__main__':
    main_window()