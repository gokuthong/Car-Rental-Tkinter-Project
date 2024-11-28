# Car Rental Management System

## Project Overview  
This project is a comprehensive **Car Rental Management System** designed to streamline the car rental process for customers and administrators. The system allows users to search for cars, make bookings, and manage rentals efficiently. It also provides admins with tools to oversee bookings, manage car inventory, and handle customer support.  

## Features  
- **User Authentication**: Secure login for customers and admins.  
- **Search and Filter Options**: Find cars based on type, seating capacity, rate, and location.  
- **Booking Management**: Book cars with confirmation windows showing detailed information.  
- **Admin Dashboard**: Tools for managing cars, bookings, and customer interactions.  
- **Interactive GUI**: Built using Tkinter, ensuring a user-friendly interface.  
- **Database Management**: Data is stored in an SQLite3 database, ensuring data integrity.  

## Development Details  

### Authors  
- **Bryan Tey**  
  - Files:  
    - `Car Rental Tkinter Main/chen/buildregister/admindashboard.py`  
    - `Car Rental Tkinter Main/chen/buildregister/support.py`  
    - Folders: `Car Rental Tkinter Main/SearchPage`, `Car Rental Tkinter Main/ConfirmBookingPage`  
  - **Role**: Developed the admin dashboard functionalities, support system, and the booking confirmation modules. Bryan also played a key role in linking all components of the project together by integrating the backend functionality with the front-end user interface.

- **Lau Zi Chen**  
  - Files:  
    - All remaining files in the `Car Rental Tkinter Main/chen` folder.  
  - **Role**: Developed the core functionalities of the application, including the login and registration pages, the car import and update pages, the car display page, as well as managing the database integration for the car, booking, and user data.

- **Thong Wai Kit**  
  - Folder: `Car Rental Tkinter Main/kit`  
  - **Role**: Developed modules related to the home page, user profiles, user and admin headers, booking lists, reviews page, and profile modification functionalities. Wai Kit also worked on the booking list and profile views for both registered and unregistered users.

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
- **chen/**: Contains core application modules for the login and register pages, admin dashboard, importing and updating car pages, user and admin headers, display cars page, and the main database.
- **kit/**: Modules for registered and unregistered users' home pages, reviews page, user and admin booking lists, and profile and modifying profile pages.
- **SearchPage/**: Modules related to the car search functionality.  
- **ConfirmBookingPage/**: Modules for the booking confirmation window.

## Database Management  
The main database used in this system is located at:  
- `Car Rental Tkinter Main/chen/buildregister/customer_registration.db`

This SQLite database is central to the operation of the Car Rental Management System. All relevant data, including customer information, booking details, car inventory, and admin records, are stored within this database.  

### Collaborative Development of the Database  
All team members contributed to the creation and structuring of the database:

- **Bryan Tey**: Assisted with the integration of the database into the system, ensuring data is correctly handled between the frontend and backend, particularly for admin-related tasks.
- **Lau Zi Chen**: Focused on the design and structure of the database, ensuring that all tables (such as customers, cars, bookings, and payments) were properly defined and related. Lau also worked on populating the database with initial data and queries.
- **Thong Wai Kit**: Contributed to ensuring that the database supports all necessary functionality related to user profiles, bookings, and reviews.

By working together, we ensured that the database design supports efficient data management and retrieval across all components of the system, from user sign-ups and car searches to booking confirmations and admin tools.

## Dependencies  
Make sure you have the following Python libraries installed:  
- **tkinter**  
- **tkcalendar**  
- **customtkinter**  
- **sqlite3**  

## Acknowledgments  
We would like to acknowledge the contributions of all team members:  
- **Bryan Tey** for the development of admin dashboard functionalities, the support system, and the booking confirmation modules. Bryan also linked all the files together in the back end, ensuring seamless interaction between the system's components.  
- **Lau Zi Chen** for developing the core functionalities, including the login and registration processes, car import and update pages, and managing the database integration.  
- **Thong Wai Kit** for designing and developing the user-facing features such as the home page, user profiles, booking list, payment, and review system.

## License  
This project is licensed under the MIT License.
