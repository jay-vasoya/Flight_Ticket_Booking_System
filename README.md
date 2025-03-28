# Flight Ticket Booking System

## Project Description
The **Flight Ticket Booking System** is a Python-based application that allows users to book flight tickets, manage reservations, and view flight details. The system uses a **linked list data structure** to handle ticket management and integrates with a **MySQL database** for persistent storage. It includes functionalities for both users and administrators.

## Features
### User Features:
- **User Registration & Login**
- **Search Flights** based on departure and arrival details
- **Book Tickets** (One-way, Round-trip, Multi-city trips)
- **Select Seat Class** (Economy, Business, First-Class)
- **Payment Processing**
- **View & Cancel Bookings**
- **Download Ticket as PDF**

### Admin Features:
- **Manage Flights** (Add, Update, Delete, View Flights)
- **Manage Users** (View all registered users)
- **Manage Tickets** (View, Search, and Generate Reports)

## Technologies Used
- **Programming Language:** Python
- **Database:** MySQL
- **Data Structure:** Linked List
- **Libraries:**
  - `mysql-connector-python` (Database connectivity)
  - `fpdf` (Generate PDF tickets)
  - `datetime` (Manage booking timestamps)

## Setup

### Configure Database Connection
Edit the `Connection` class in `Flight_Ticket_Booking_System.py` to match your MySQL configuration:
```python
return mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="root",
    password="",
    database="flight_ticket_booking_system"
)
```

### Run the Application
```sh
python Flight_Ticket_Booking_System.py
```

## Usage
- **For Users:**
  - Register/Login
  - Search for flights
  - Book tickets
  - View or cancel bookings
  - Download tickets in PDF format

- **For Admins:**
  - Manage flights & users
  - View all bookings
  - Generate reports

