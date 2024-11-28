# Car Rental Management System

## Project Overview  
This project is a comprehensive Car Rental Management System designed to streamline the car rental process for customers and administrators. The system allows users to search for cars, make bookings, and manage rentals efficiently. It also provides admins with tools to oversee bookings, manage car inventory, and handle customer support.  

## Features  
- User Authentication: Secure login for customers and admins.  
- Search and Filter Options: Find cars based on type, seating capacity, rate, and location.  
- Booking Management: Book cars with confirmation windows showing detailed information.  
- Admin Dashboard: Tools for managing cars, bookings, and customer interactions.  
- Interactive GUI: Built using Tkinter, ensuring a user-friendly interface.  
- Database Management: Data is stored in an SQLite3 database, ensuring data integrity.  

## Development Details  

### Authors  
- **Bryan Tey**  
  - Files:  
    - `Car Rental Tkinter Main/chen/buildregister/admindashboard.py`  
    - `Car Rental Tkinter Main/chen/buildregister/support.py`  
    - Folders: `Car Rental Tkinter Main/SearchPage`, `Car Rental Tkinter Main/ConfirmBookingPage`  

- **Lau Zi Chen**  
  - Files:  
    - All remaining files in the `Car Rental Tkinter Main/chen` folder.  

- **Thong Wai Kit**  
  - Folder: `Car Rental Tkinter Main/kit`  

### Technologies Used  
1. **Python**: Primary programming language.  
2. **Tkinter**: For GUI development.  
3. **Tkinter Designer**: Conversion of Figma designs to Tkinter-compatible Python code.  
4. **SQLite3**: Database for storing customer, admin, car, booking, payment, and review information.  
5. **DB Browser for SQLite**: Tool for managing the database schema.  
6. **CustomTkinter** and **Tkcalendar**: Libraries for advanced widgets and date selection.  
7. **Pycharm IDE**: Development environment.  

## How to Run  
1. Clone this repository:  
   ```bash  
   git clone https://github.com/gokuthong/Car-Rental-Tkinter-Project/  
   ```  
2. Ensure you have **Python 3.x** installed.  
3. Install the required libraries:  
   ```bash  
   pip install tkcalendar
   pip install customtkinter
   ```  
4. Navigate to the `Car Rental Tkinter Main` folder.  
5. Run the home page application file:  
   ```bash  
   python Car Rental Tkinter Main/kit/Profile/home_unregistered.py  
   ```  

## Folder Structure  
- `chen/`: Contains core application modules for the login and register pages, admin dashboard, importing and updating car pages, user and admin headers, display cars page, and the main database
- `kit/`: Modules for registered and unregistered users' home pages, reviews page, user and admin booking lists, and profile and modifying profile pages.
- `SearchPage/`: Modules related to the car search functionality.  
- `ConfirmBookingPage/`: Modules for the booking confirmation window.

## Dependencies  
Make sure you have the following Python libraries installed:  
- **tkinter**  
- **tkcalendar**  
- **customtkinter**  
- **sqlite3**  

## Acknowledgments  
We would like to acknowledge the contributions of all team members:  
- Bryan Tey for the admin functionalities, support system, and booking confirmation modules.  
- Lau Zi Chen for the core functionalities and database management.  
- Thong Wai Kit for utility tools.  

## License  
This project is licensed under the MIT License.
