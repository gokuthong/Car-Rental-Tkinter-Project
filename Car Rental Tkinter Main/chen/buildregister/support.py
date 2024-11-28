from tkinter import Tk, Canvas, Button, Label, Frame, Listbox, Scrollbar, messagebox, Toplevel
import webbrowser
from chen.buildregister.header import create_header
from PIL import Image, ImageTk, ImageFilter

def main_window():
    def show_chatbot():
        """Display a chatbot-style FAQ system."""
        # Get the screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Define the chatbot window size
        chatbot_width = 600
        chatbot_height = 800

        # Calculate position to center the window
        x_position = (screen_width // 2) - (chatbot_width // 2)
        y_position = (screen_height // 2) - (chatbot_height // 2)

        # Create the chatbot window
        chatbot_window = Toplevel(window)
        chatbot_window.title("Support Chatbot")
        chatbot_window.geometry(f"{chatbot_width}x{chatbot_height}+{x_position}+{y_position}")
        chatbot_window.configure(bg="#f5f5f5")

        # Chatbot frame
        chatbot_frame = Frame(chatbot_window, bg="#f5f5f5")
        chatbot_frame.place(relwidth=1, relheight=0.9, rely=0.1)

        # Title
        Label(
            chatbot_window,
            text="How can we help you?",
            font=("Red Hat Display Medium", 24),
            bg="#f5f5f5",
        ).pack(pady=10)

        # List of FAQ categories
        categories = ["Booking Issues", "Payment Questions", "Account Help", "Other"]
        faq_data = {
            "Booking Issues": ["How do I modify a booking?", "Can I cancel a booking?"],
            "Payment Questions": ["What payment methods are accepted?", "Why is my payment failing?"],
            "Account Help": ["How do I reset my password?", "How do I update my profile?"],
        }

        def show_faq(category):
            """Show FAQs for a selected category."""
            question_list.delete(0, 'end')
            questions = faq_data.get(category, [])
            if questions:
                for question in questions:
                    question_list.insert('end', question)
            else:
                question_list.insert('end', "Other questions")

        def handle_question_selection(event):
            """Handle FAQ selection or show email option."""
            selected_question = question_list.get(question_list.curselection())

            # Providing answers to the selected questions
            if selected_question == "How do I modify a booking?":
                messagebox.showinfo("FAQ Answer", "If you haven't uploaded an image of payment proof/proceeded with payment, you can modify your booking by clicking on the cart symbol in the header located at the top of the page.")
            elif selected_question == "Can I cancel a booking?":
                messagebox.showinfo("FAQ Answer", "If you haven't uploaded an image of payment proof/proceeded with payment, simply search for a new car and add it to your cart, it will override your current booking. If you've already submitted payment proof/proceeded with payment, you can file a request to cancel your booking by emailing us at carrentalbay@gmail.com with relevant information.")
            elif selected_question == "What payment methods are accepted?":
                messagebox.showinfo("FAQ Answer", "We currently accept Touch n Go e-wallet, Maybank, PayPal, and American Express.")
            elif selected_question == "Why is my payment failing?":
                messagebox.showinfo("FAQ Answer", "Check with your payment provider to ensure your payment meets your personal requirements/spending limits. Payment failure can also be caused by issues like incorrect card details, expired card, or insufficient balance.")
            elif selected_question == "How do I reset my password?":
                messagebox.showinfo("FAQ Answer", "You can reset your password by clicking on the profile icon on the top right of the screen in the header, then clicking on 'Edit Profile', then click on the 'Edit' button and select 'Change Password'. You will then be redirected to a page where you can enter a new password.")
            elif selected_question == "How do I update my profile?":
                messagebox.showinfo("FAQ Answer", "You can update your profile by clicking on the profile icon on the top right of the screen in the header and clicking on 'Edit Profile'. You will then be redirected to a page where you can edit your profile details like username and email.")
            else:
                messagebox.showinfo(
                    "Contact Support",
                    "If your question is not listed, please contact us at carrentalbay@gmail.com.",
                )

        # Dropdown to select category
        category_label = Label(
            chatbot_frame, text="Select a category:", font=("Arial", 14), bg="#f5f5f5"
        )
        category_label.pack(pady=10)

        for category in categories:
            Button(
                chatbot_frame,
                text=category,
                font=("Arial", 12),
                width=20,
                bg="#0078D7",
                fg="white",
                command=lambda c=category: show_faq(c),
            ).pack(pady=5)

        # Listbox to display questions
        question_list = Listbox(chatbot_frame, font=("Arial", 12), height=15, width=50)
        question_list.pack(pady=10)

        # Scrollbar
        scrollbar = Scrollbar(chatbot_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        question_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=question_list.yview)

        question_list.bind("<<ListboxSelect>>", handle_question_selection)

        # Email fallback button
        email_label = Label(
            chatbot_frame,
            text="Still need help? Contact us:",
            font=("Arial", 14),
            bg="#f5f5f5",
        )
        email_label.pack(pady=20)
        Button(
            chatbot_frame,
            text="Email: carrentalbay@gmail.com",
            font=("Arial", 12),
            bg="#0078D7",
            fg="white",
            command=open_gmail,
        ).pack()

    def open_gmail():
        """Open Gmail compose with pre-filled subject and recipient in a browser."""
        recipient = "carrentalbay@gmail.com"
        subject = "Inquiry about Car Rental"

        # Construct the Gmail URL to open compose window
        gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={recipient}&su={subject}"

        # Open Gmail compose window in the default web browser
        webbrowser.open(gmail_url)

    # Initialize the Tkinter window
    window = Tk()
    window.title("Support")
    window.geometry("1920x1200")

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
    canvas = Canvas(window, width=1920, height=1200)
    canvas.pack(fill="both", expand=True)

    # Draw the blurred background image on the canvas
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    # Title text with simulated layering/border effect
    canvas.create_text(
        962, 202, text="Support", font=("Red Hat Display Medium", 80), fill="#000000", anchor="center"
    )
    canvas.create_text(
        960, 200, text="Support", font=("Red Hat Display Medium", 80), fill="#FFFFFF", anchor="center"
    )


    # Add a "Chat with us" button
    Button(
        window,
        text="Chat with us",
        font=("Arial", 16),
        bg="#0078D7",
        fg="white",
        command=show_chatbot,
    ).place(x=860, y=400, width=200, height=50)

    # Import and create header
    create_header(window, canvas)

    # Run the Tkinter event loop
    window.mainloop()


if __name__ == "__main__":
    main_window()