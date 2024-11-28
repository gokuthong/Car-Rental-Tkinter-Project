import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Canvas, Button, messagebox
from tkinter.ttk import Combobox
import sqlite3
import json
from fpdf import FPDF
import datetime
from chen.buildregister.headeradmin import create_header
from PIL import Image, ImageTk, ImageFilter
import os


def main_window():
    # Function to get current admin username from the database
    def get_admin_username():
        try:
            with open(
                    r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\admin_session.json",
                    "r") as f:
                data = json.load(f)
                current_admin_id = data.get("current_admin_id")
                print(f"Current Admin ID: {current_admin_id}")
            if current_admin_id is None:
                return None
            conn = sqlite3.connect(
                r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM admin WHERE id = ?", (current_admin_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except (sqlite3.Error, json.JSONDecodeError):
            return None
        finally:
            if conn:
                conn.close()

    # Function to fetch data based on time range
    def fetch_data(time_range):
        conn = sqlite3.connect(
            r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\chen\buildregister\customer_registration.db")
        cursor = conn.cursor()

        # Adjust time range filters
        date_filter = ""
        if time_range != "All Time":
            today = datetime.date.today()
            if time_range == "1 Day":
                date_filter = f"AND pickup_date >= '{today - datetime.timedelta(days=1)}'"
            elif time_range == "1 Week":
                date_filter = f"AND pickup_date >= '{today - datetime.timedelta(weeks=1)}'"
            elif time_range == "1 Month":
                date_filter = f"AND pickup_date >= '{today - datetime.timedelta(days=30)}'"
            elif time_range == "YTD":
                date_filter = f"AND pickup_date >= '{today.replace(month=1, day=1)}'"

        # Fetch data (exclude non-approved bookings)
        cursor.execute(f"""
            SELECT
                c.location,
                COUNT(b.id) AS total_cars,
                SUM(p.payment_amount) AS total_revenue
            FROM bookings b
            JOIN car c ON b.car_id = c.id
            LEFT JOIN payment p ON b.payment_id = p.id
            WHERE b.status = 'approved' {date_filter}
            GROUP BY c.location
        """)
        data = cursor.fetchall()

        # Total revenue and total sales
        cursor.execute(f"""
            SELECT SUM(p.payment_amount), COUNT(b.id)
            FROM bookings b
            LEFT JOIN payment p ON b.payment_id = p.id
            WHERE b.status = 'approved' {date_filter}
        """)
        totals = cursor.fetchone()
        conn.close()

        return data, totals

    # Function to render visualizations
    def render_visualizations(canvas, time_range="All Time"):
        # Fetch new data based on the selected time range
        data, totals = fetch_data(time_range)

        # Clear existing widgets (including previous text)
        if 'total_sales_text' in canvas.data:
            canvas.delete(canvas.data['total_sales_text'])
        if 'total_revenue_text' in canvas.data:
            canvas.delete(canvas.data['total_revenue_text'])

        # Clear existing offset texts
        if 'total_sales_text_offset' in canvas.data:
            canvas.delete(canvas.data['total_sales_text_offset'])
        if 'total_revenue_text_offset' in canvas.data:
            canvas.delete(canvas.data['total_revenue_text_offset'])

        # Total Sales and Revenue
        total_revenue, total_sales = totals if totals else (0, 0)

        # Draw new text for total sales and revenue
        total_sales_text = canvas.create_text(962, 272, text=f"Total Sales: {total_sales}",
                                              font=("Red Hat Display Medium", 24),
                                              fill="#FFFFFF")
        total_sales_text_offset = canvas.create_text(960, 270, text=f"Total Sales: {total_sales}",
                                                     font=("Red Hat Display Medium", 24),
                                                     fill="#000000")
        total_revenue_text = canvas.create_text(962, 322, text=f"Total Revenue: RM{total_revenue:.2f}",
                                                font=("Red Hat Display Medium", 24), fill="#FFFFFF")
        total_revenue_text_offset = canvas.create_text(960, 320, text=f"Total Revenue: RM{total_revenue:.2f}",
                                                       font=("Red Hat Display Medium", 24), fill="#000000")

        # Store the text references in canvas.data
        canvas.data['total_sales_text'] = total_sales_text
        canvas.data['total_revenue_text'] = total_revenue_text
        canvas.data['total_sales_text_offset'] = total_sales_text_offset
        canvas.data['total_revenue_text_offset'] = total_revenue_text_offset

        # Cars per location
        locations = [row[0] for row in data]
        cars_count = [row[1] for row in data]
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.bar(locations, cars_count, color="skyblue")
        ax.set_title("Cars from Each Location", fontsize=18)
        ax.set_xlabel("Location")
        ax.set_ylabel("Number of Cars")
        chart1_path = r"C:\Users\ASUS\Downloads\cars_location_chart.png"
        fig.savefig(chart1_path)
        chart1 = FigureCanvasTkAgg(fig, canvas)
        chart1.get_tk_widget().place(x=50, y=450)

        # Set the background color of the chart
        fig.patch.set_facecolor("#d0f5ce")

        # Revenue per location (Pie chart)
        revenue = [row[2] for row in data]

        # Custom function to format the labels for the pie chart
        def func(pct, allvals):
            absolute = int(pct / 100. * sum(allvals))  # Revenue value
            return f"{pct:.1f}%\nRM {absolute:.2f}"  # Show percentage and revenue amount

        fig2, ax2 = plt.subplots(figsize=(7, 5))
        wedges, texts, autotexts = ax2.pie(revenue, labels=locations, autopct=lambda pct: func(pct, revenue),
                                           startangle=140)

        # Set title
        ax2.set_title("Revenue by Location", fontsize=18)

        # Customize the appearance of the pie chart
        for autotext in autotexts:
            autotext.set_fontsize(14)
            autotext.set_color('black')

        chart2_path = r"C:\Users\ASUS\Downloads\revenue_location_chart.png"
        fig2.savefig(chart2_path)
        chart2 = FigureCanvasTkAgg(fig2, canvas)
        chart2.get_tk_widget().place(x=1200, y=450)

        # Set the background color of the chart
        fig2.patch.set_facecolor("#d0f5ce")

        return chart1_path, chart2_path

    # Function to generate and download PDF
    def generate_pdf(chart1_path, chart2_path):
        data, totals = fetch_data("All Time")
        total_revenue, total_sales = totals if totals else (0, 0)

        # Ensure we have data
        if not data:
            messagebox.showerror("Error", "No data available for the report.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Car Rental Bay Admin Report", ln=True, align="C")

        # Add total sales and revenue
        pdf.cell(200, 10, txt=f"Total Sales: {total_sales}", ln=True)
        pdf.cell(200, 10, txt=f"Total Revenue: RM{total_revenue:.2f}", ln=True)

        # Add location-wise data
        pdf.cell(200, 10, txt="Location Data:", ln=True)
        for row in data:
            location = row[0]
            total_cars = row[1]
            revenue = row[2]
            pdf.cell(200, 10, txt=f"{location}: {total_cars} cars, RM{revenue:.2f} revenue", ln=True)

        # Place charts
        pdf.image(chart1_path, x=10, y=90, w=120)
        pdf.image(chart2_path, x=10, y=150, w=120)

        # Save the PDF
        file_path = r"C:\Users\ASUS\Downloads\admin_report.pdf"
        pdf.output(file_path)
        messagebox.showinfo("Report Generated", f"PDF saved to {file_path}")
        os.startfile(file_path)  # This will open the PDF file automatically

    # Initialize Tkinter window
    window = Tk()
    window.geometry("1920x1200")
    window.configure(bg="#FFFFFF")

    # Initialize the canvas and store references for the text data
    canvas = Canvas(window, bg="#FFFFFF", height=1200, width=1920, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    # Initialize the canvas data dictionary to store references to widgets
    canvas.data = {}

    # Load the background image using Pillow (PIL)
    image_path = r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\kit\Profile\assets\frame0\booking_bg.png"  # Path to your image
    img = Image.open(image_path)
    img = img.resize((1920, 1200))  # Resize to fit window size

    # Apply Gaussian blur with a radius of 10 (you can adjust this value)
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=2))

    # Resize the blurred image to fit the window size
    blurred_img = blurred_img.resize((1920, 1200))
    bg_image = ImageTk.PhotoImage(blurred_img)

    # Create a Canvas widget to display the background image
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    # Fetch and display admin username
    username = get_admin_username()
    welcome_text = f"Welcome {username}" if username else "Welcome Admin"
    # Title text with simulated layering/border effect
    canvas.create_text(962, 202, text=welcome_text, font=("Red Hat Display Medium", 60), fill="#000000",
                       anchor="center")
    canvas.create_text(960, 200, text=welcome_text, font=("Red Hat Display Medium", 60), fill="#FFFFFF",
                       anchor="center")

    # Render visualizations for a default time range
    chart1_path, chart2_path = render_visualizations(canvas)

    # Dropdown for time range
    time_options = ["1 Day", "1 Week", "1 Month", "YTD", "All Time"]
    time_range = Combobox(window, values=time_options, state="readonly", font=("Red Hat Display Medium", 16))
    time_range.set("All Time")
    time_range.place(x=820, y=400)
    time_range.bind("<<ComboboxSelected>>", lambda e: render_visualizations(canvas, time_range.get()))

    # Generate PDF Button
    chart1_path, chart2_path = render_visualizations(canvas)
    Button(window, text="Download Report", command=lambda: generate_pdf(chart1_path, chart2_path), bg="blue",
           fg="white", font=("Red Hat Display Medium", 20, "bold")).place(x=860, y=990)

    create_header(window, canvas)

    # Show the window
    window.mainloop()


if __name__ == "__main__":
    main_window()
