from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Toplevel
from PIL import Image, ImageTk

def main_window():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ASUS\PycharmProjects\pythonProject\Car Rental Tkinter Main\kit\Payment\assets\frame0")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = Toplevel()
    window.geometry("600x800")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=800,
        width=600,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    header_img = PhotoImage(file=relative_to_assets("header_img.png"))
    header_image = canvas.create_image(300.0, 36.0, image=header_img)

    canvas.create_text(
        30.0,
        17.0,
        anchor="nw",
        text="Payment Method",
        fill="#FFFFFF",
        font=("Roboto Bold", 32 * -1)
    )

    popup_bg = PhotoImage(file=relative_to_assets("popup_bg.png"))
    popup_image = canvas.create_image(300.0, 436.0, image=popup_bg)

    method_container = PhotoImage(file=relative_to_assets("method_container.png"))
    method_image = canvas.create_image(300.0, 210.0, image=method_container)

    # Load but do not display the QR container and border initially
    qr_container = PhotoImage(file=relative_to_assets("qr_container.png"))
    qr_border = PhotoImage(file=relative_to_assets("qr_border.png"))

    canvas.create_text(
        77.0,
        155.0,
        anchor="nw",
        text="Pick a payment method:",
        fill="#000000",
        font=("Roboto Bold", 24 * -1)
    )

    # Define specific QR code images
    def load_image(path):
        return ImageTk.PhotoImage(Image.open(relative_to_assets(path)).resize((338, 270)))  # Adjust size to fit qr_border

    tng_qr = load_image("tng_qr.jpg")
    maybank_qr = load_image("maybank_qr.jpg")
    paypal_qr = load_image("paypal_qr.jpg")
    american_qr = load_image("american_qr.png")

    # Function to display QR container, border, and the selected QR code image
    def show_qr_code(qr_image):
        canvas.create_image(300.0, 547.0, image=qr_container)
        canvas.create_image(300.0, 547.0, image=qr_border)
        canvas.create_image(300.0, 547.0, image=qr_image)  # Display the selected QR code

    # Buttons for different payment methods
    tng = PhotoImage(file=relative_to_assets("tng.png"))
    button_tng = Button(
        window,
        image=tng,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: show_qr_code(tng_qr),
        relief="flat"
    )
    button_tng.place(x=95.0, y=200.0, width=60.0, height=60.0)

    maybank = PhotoImage(file=relative_to_assets("maybank.png"))
    button_maybank = Button(
        window,
        image=maybank,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: show_qr_code(maybank_qr),
        relief="flat"
    )
    button_maybank.place(x=212.0, y=200.0, width=60.0, height=60.0)

    paypal = PhotoImage(file=relative_to_assets("paypal.png"))
    button_paypal = Button(
        window,
        image=paypal,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: show_qr_code(paypal_qr),
        relief="flat"
    )
    button_paypal.place(x=329.0, y=200.0, width=60.0, height=60.0)

    american_express = PhotoImage(file=relative_to_assets("american_express.png"))
    button_american_express = Button(
        window,
        image=american_express,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: show_qr_code(american_qr),
        relief="flat"
    )
    button_american_express.place(x=446.0, y=198.0, width=60.0, height=60.0)

    window.resizable(False, False)
    window.mainloop()

if __name__ == '__main__':
    main_window()
