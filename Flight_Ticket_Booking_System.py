import mysql.connector
from datetime import date, datetime
from fpdf import FPDF

class Connection:

    def connect_to_db():
            try:
                return mysql.connector.connect(
                    host="127.0.0.1",
                    port=3307,
                    user="root",
                    password="",
                    database="flight_ticket_booking_system"
                )
            except mysql.connector.Error as err:
                print(f"Error connecting to database: {err}")
                return None

class Ticket_node:

    def __init__(self, user_id , flight_number , booking_date , booking_time , seat_class , seat_number , ticket_status, price):
        self.user_id = user_id
        self.flight_number = flight_number
        self.booking_date = booking_date
        self.booking_time = booking_time
        self.seat_class = seat_class
        self.seat_number=seat_number
        self.ticket_status= ticket_status
        self.price = price
        self.next = None

class Ticket_linked_list:

    def __init__(self):
        self.head = None

    def add_ticket(self, user_id , flight_number , booking_date , booking_time , seat_class , seat_number , ticket_status, price):
        try:
            new_ticket = Ticket_node(user_id , flight_number , booking_date , booking_time , seat_class , seat_number , ticket_status, price)

            if not self.head:
                self.head = new_ticket
            else:
                current = self.head
                while current.next:  
                    current = current.next
                current.next = new_ticket  
        except Exception as e:
            print(f" Error: {e}")

    def calculate_total(self):
        try:
            total = 0
            current = self.head
            if current is None:
                print("No data available in the linked list.")
                return total
            else:
                while current:
                    total += current.price
                    current = current.next
                return total
        except Exception as e:
            print(f" Error: {e}")
            return 0
        
    def clear_LL(self):
        try:
            self.head = None 
            print("Tickets added to database successfully & list cleared!")
        except Exception as e:
            print(f" Error: {e}")
            
    def data_add_LL_to_DataBase(self):
        conn = Connection.connect_to_db()
        cur = conn.cursor(dictionary=True)
        ticket_ids=[]
        
        current = self.head
        if not current:
            print("No tickets booked.")
            return
        
        while current:
            try:
                query = "INSERT INTO tickets (user_id, flight_number, booking_date, booking_time, seat_class, price, seat_number, ticket_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

                cur.execute(query, (current.user_id, current.flight_number, current.booking_date,current.booking_time, current.seat_class, current.price,current.seat_number, current.ticket_status))
                
                conn.commit() 
                id=cur.lastrowid
                ticket_ids.append(id)
                
            except Exception as e:
                print(f"Error inserting ticket: {e}")
                conn.rollback()  
            
            current = current.next  
        
        self.head = None 
        print("Tickets added to database successfully & list cleared!")
        for i in ticket_ids:

            query = "SELECT * FROM tickets WHERE ticket_id = %s"

            cur.execute(query, (i,))
            data = cur.fetchall()
            try:
                if data:
                    for row in data:
                        self.generate_pdf(row['ticket_id'])
                else:
                    print("No tickets found for the user.")

            except Exception as e:
                print(f"Error generating PDF: {e}")

        conn.close()
        
    def generate_pdf(self,ticket_id):

        try:
            conn = Connection.connect_to_db()
            cursor = conn.cursor(dictionary=True)

            query = "SELECT * FROM tickets WHERE ticket_id = %s"
            cursor.execute(query, (ticket_id,))
            booked_tickets = cursor.fetchone()

            if booked_tickets:
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(200, 10, "Flight Ticket", ln=True, align="C")
                pdf.ln(10)
                pdf.set_font("Arial", size=12)

                try:
                    query = "SELECT * FROM users WHERE user_id = %s"
                    cursor.execute(query, (booked_tickets['user_id'],))
                    user = cursor.fetchone()

                    query = "SELECT * FROM flights WHERE flight_number = %s"
                    cursor.execute(query, (booked_tickets['flight_number'],))
                    flight = cursor.fetchone()

                    pdf.set_fill_color(200, 220, 255)

                    pdf.cell(190, 10, "Ticket Details", ln=True, align="L", fill=True)
                    pdf.cell(190, 8, f"Ticket ID: {booked_tickets['ticket_id']}", ln=True)
                    pdf.cell(190, 8, f"Flight Number: {booked_tickets['flight_number']}", ln=True)
                    pdf.cell(190, 8, f"Booking Date: {booked_tickets['booking_date']} {booked_tickets['booking_time']}", ln=True)
                    pdf.cell(190, 8, f"Seat: {booked_tickets['seat_class']} {booked_tickets['seat_number']}", ln=True)
                    pdf.cell(190, 8, f"Status: {booked_tickets['ticket_status']}", ln=True)
                    pdf.cell(190, 8, f"Price: {booked_tickets['price']} RS.", ln=True)
                    pdf.ln(5)

                    pdf.cell(190, 10, "Passenger Details", ln=True, align="L", fill=True)
                    pdf.cell(190, 8, f"Name: {user['user_name']}", ln=True)
                    pdf.cell(190, 8, f"Email: {user['email']}", ln=True)
                    pdf.cell(190, 8, f"Phone: {user['phone_number']}", ln=True)
                    pdf.cell(190, 8, f"Passport: {user['passport_number']}", ln=True)
                    pdf.cell(190, 8, f"Address: {user['address']}", ln=True)

                    pdf.ln(5)

                    pdf.cell(190, 10, "Flight Details", ln=True, align="L", fill=True)
                    pdf.cell(190, 8, f"Flight Name: {flight['flight_name']}", ln=True)
                    pdf.cell(190, 8, f"Departure: {flight['departure_location']} ({flight['departure_airport']})", ln=True)
                    pdf.cell(190, 8, f"Arrival: {flight['arrival_location']} ({flight['arrival_airport']})", ln=True)
                    pdf.cell(190, 8, f"Departure Time: {flight['departure_date']} {flight['departure_time']}", ln=True)
                    pdf.cell(190, 8, f"Arrival Time: {flight['arrival_date']} {flight['arrival_time']}", ln=True)
                    pdf.cell(190, 8, f"Duration: {flight['duration']}", ln=True)
                    pdf.ln(10)
                
                except Exception as e:
                    print("Error processing ticket details:", str(e))

                pdf_output = f"Flight_Ticket_{ticket_id}.pdf"
                pdf.output(pdf_output)
                print(f"PDF generated successfully: {pdf_output}")

            else:
                print("No ticket found")

        except Exception as e:
            print("Error fetching booked tickets:", str(e))

        finally:
            cursor.close()
            conn.close()
                
class Admin:

    def __init__(self):
        pass
           
    def add_flight(self):
        conn = Connection.connect_to_db()

        if not conn:
            print("Database connection failed.")
            return
        
        try:
            cursor = conn.cursor()
            
            flight_number = input("Enter Flight Number (e.g., AI101): ")
            flight_name = input("Enter Flight Name: ")
            departure_location = input("Enter Departure Location: ")
            arrival_location = input("Enter Arrival Location: ")
            departure_airport = input("Enter Departure Airport: ")
            arrival_airport = input("Enter Arrival Airport: ")
            departure_date = input("Enter Departure Date (YYYY-MM-DD): ")
            departure_time = input("Enter Departure Time (HH:MM:SS): ")
            arrival_date = input("Enter Arrival Date (YYYY-MM-DD): ")
            arrival_time = input("Enter Arrival Time (HH:MM:SS): ")
            duration = input("Enter Flight Duration (e.g., 2h 30m): ")
            flight_type = input("Enter Flight Type (Domestic/International): ")
            total_seats = int(input("Enter Total Seats: "))

            economy_seat = total_seats-20
            business_seat = 10
            first_class_seat = 10
            economy_price = float(input("Enter Economy Ticket Price: "))
            business_price = float(input("Enter Business Ticket Price: "))
            first_class_price = float(input("Enter First Class Ticket Price: "))
            
            available_seats = total_seats 

            query = "INSERT INTO flights (flight_number, flight_name, departure_location, arrival_location, departure_airport,arrival_airport,departure_date, departure_time, arrival_date, arrival_time, duration, flight_type, total_seats, available_seats, economy_seats, business_seats, first_class_seats, economy_price, business_price, first_class_price, status)VALUES (%s, %s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Scheduled')"
            
            cursor.execute(query, (flight_number, flight_name, departure_location, arrival_location,departure_airport,arrival_airport, departure_date, departure_time, arrival_date, arrival_time, duration, flight_type,total_seats, available_seats, economy_seat, business_seat, first_class_seat, economy_price, business_price, first_class_price))
            
            conn.commit()
            print("Flight added successfully!")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

        finally:
            cursor.close()
            conn.close()
  
    def view_all_flights(self):
        conn = Connection.connect_to_db()
        if not conn:
            print("Database connection failed.")
            return

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM flights"
            cursor.execute(query)
            rows = cursor.fetchall()

            if not rows:
                print("No flights available.")
                return

            def format_row(label, value, width=60):
                return f"| {label.ljust(25)} {str(value).rjust(width - 30)} |"

            box_width = 70
            border = "+" + "-" * (box_width - 2) + "+"

            for flight in rows:
                print(border)
                print(f"| {'FLIGHT DETAILS'.center(box_width - 4)} |")
                print(border)
                print(format_row("Flight Number:", flight['flight_number']))
                print(format_row("Flight Name:", flight['flight_name']))
                print(format_row("Departure Location:", flight['departure_location']))
                print(format_row("Departure Date & Time:", f"{flight['departure_date']} at {flight['departure_time']}"))
                print(format_row("Departure Airport:", flight['departure_airport']))
                print(format_row("Arrival Location:", flight['arrival_location']))
                print(format_row("Arrival Date & Time:", f"{flight['arrival_date']} at {flight['arrival_time']}"))
                print(format_row("Arrival Airport:", flight['arrival_airport']))
                print(format_row("Duration:", flight['duration']))
                print(format_row("Flight Type:", flight['flight_type']))
                print(format_row("Economy Seats:", f"{flight['economy_seats']} | ₹{flight['economy_price']}"))
                print(format_row("Business Seats:", f"{flight['business_seats']} | ₹{flight['business_price']}"))
                print(format_row("First Class Seats:", f"{flight['first_class_seats']} | ₹{flight['first_class_price']}"))
                print(format_row("Total Seats:", flight['total_seats']))
                print(format_row("Available Seats:", flight['available_seats']))
                print(format_row("Status:", flight['status']))
                print(border)
                print("\n")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

        finally:
            cursor.close()
            conn.close()

    def update_flight(self):
        conn = Connection.connect_to_db()
        if not conn:
            print("Database connection failed.")
            return
        
        try:
            cursor = conn.cursor()
            self.view_all_flights()
            flight_number = input("Enter Flight Number to Update: ")

            query_check = "SELECT * FROM flights WHERE flight_number = %s"
            cursor.execute(query_check, (flight_number,))
            row = cursor.fetchone()

            if row is None:
                print("Flight number not found.")
                return

            print("\nUpdating Flight Details...\n")

            flight_name = input("Enter New Flight Name: ")
            dep_location = input("Enter New Departure Location: ")
            arr_location = input("Enter New Arrival Location: ")
            dep_airport= input("Enter New Departure Airport: ")
            arr_airport = input("Enter New Arrival Airport: ")
            departure_date = input("Enter New Departure Date (YYYY-MM-DD): ")
            departure_time = input("Enter New Departure Time (HH:MM:SS): ")
            arrival_date = input("Enter New Arrival Date (YYYY-MM-DD): ")
            arrival_time = input("Enter New Arrival Time (HH:MM:SS): ")
            duration = input("Enter New Flight Duration (e.g., 2h 30m): ")
            flight_type = input("Enter New Flight Type (Domestic/International): ")
            total_seats = int(input("Enter New Total Seats: "))

            economy_seats = total_seats-20
            business_seats = 10
            first_class_seats = 10
            economy_price = float(input("Enter New Economy Ticket Price: "))
            business_price = float(input("Enter New Business Ticket Price: "))
            first_class_price = float(input("Enter New First Class Ticket Price: "))
            status = input("Enter status('Scheduled', 'Delayed', 'Cancelled') : ")
            available_seats = total_seats  

            query_update = "UPDATE flights SET flight_name = %s, departure_location = %s, arrival_location = %s, departure_airport = %s, arrival_airport = %s, departure_date = %s, departure_time = %s, arrival_date = %s, arrival_time = %s, duration = %s, flight_type = %s, total_seats = %s, available_seats = %s, economy_seats = %s, business_seats = %s, first_class_seats = %s, economy_price = %s, business_price = %s, first_class_price = %s,status =%sWHERE flight_number = %s"
            
            cursor.execute(query_update, (flight_name, dep_location, arr_location, dep_airport,arr_airport,departure_date, departure_time, arrival_date, arrival_time, duration, flight_type, total_seats, available_seats, economy_seats, business_seats, first_class_seats, economy_price, business_price, first_class_price,status, flight_number))
            
            conn.commit()
            print("Flight updated successfully!")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

        finally:
            cursor.close()
            conn.close()

    def delete_flight(self):
        conn = Connection.connect_to_db()
        if not conn:
            print("Database connection failed.")
            return

        try:
            cursor = conn.cursor()
            self.view_all_flights()

            flight_number = input("Enter Flight Number to Delete: ")

            query = "SELECT * FROM flights WHERE flight_number = %s"
            cursor.execute(query, (flight_number,))
            row = cursor.fetchone()

            if row is None:
                print("Flight number not found.")
                return

            confirm = input(f"Are you sure you want to delete flight {flight_number}? (yes/no): ")
            if confirm.lower() != 'yes':
                print("Deletion canceled.")
                return

            delete_query = "DELETE FROM flights WHERE flight_number = %s"
            cursor.execute(delete_query, (flight_number,))
            conn.commit()

            print(f"Flight {flight_number} deleted successfully!")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

        finally:
            cursor.close()
            conn.close()

    def display_all_tickets(self):
        try:
            conn = Connection.connect_to_db()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM tickets"
            cursor.execute(query)
            rows = cursor.fetchall()

            if not rows:
                print("No tickets found.")
                return

            def format_row(label, value, width=50):
                return f"| {label.ljust(25)} : {str(value).ljust(width - 30)} |"

            box_width = 80
            border = "+" + "-" * (box_width - 2) + "+"

            for row in rows:

                cursor.execute("SELECT * FROM users WHERE user_id = %s", (row['user_id'],))
                user = cursor.fetchone()

                cursor.execute("SELECT * FROM flights WHERE flight_number = %s", (row['flight_number'],))
                flight = cursor.fetchone()

                print("=" * box_width)
                print(f"{'✈ FLIGHT TICKET'.center(box_width)}")
                print("=" * box_width)

                print(format_row("Passenger Name", user['user_name']))
                print(format_row("Passport Number", user['passport_number']))
                print(format_row("Phone Number", user['phone_number']))
                print(format_row("Email", user['email']))
                print("-" * box_width)

                print(format_row("Flight Name", flight['flight_name']))
                print(format_row("Flight Number", row['flight_number']))
                print(format_row("Departure Location", flight['departure_location']))
                print(format_row("Arrival Location", flight['arrival_location']))
                print(format_row("Departure Airport", flight['departure_airport']))
                print(format_row("Arrival Airport", flight['arrival_airport']))
                print("-" * box_width)

                print(format_row("Departure Date", flight['departure_date']))
                print(format_row("Departure Time", flight['departure_time']))
                print(format_row("Arrival Date", flight['arrival_date']))
                print(format_row("Arrival Time", flight['arrival_time']))
                print(format_row("Duration", flight['duration']))
                print("-" * box_width)

                print(format_row("Seat Class", row['seat_class']))
                print(format_row("Seat Number", row['seat_number']))
                print(format_row("Ticket Status", row['ticket_status']))
                print(format_row("Price", f"₹{row['price']}"))
                print("-" * box_width)

                print(format_row("Flight Type", flight['flight_type']))
                print(format_row("Flight Status", flight['status']))
                print("=" * box_width)
                print("\n")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def display_tickets(self, ticket_id):
        try:
            conn = Connection.connect_to_db()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM tickets WHERE ticket_id = %s"
            cursor.execute(query, (ticket_id,))
            row = cursor.fetchone()

            if not row:
                print(" No ticket found.")
                return

            query = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(query, (row['user_id'],))
            user = cursor.fetchone()

            query = "SELECT * FROM flights WHERE flight_number = %s"
            cursor.execute(query, (row['flight_number'],))
            flight = cursor.fetchone()

            def format_row(label, value, width=50):
                return f"| {label.ljust(25)} : {str(value).ljust(width - 30)} |"

            box_width = 80
            border = "+" + "-" * (box_width - 2) + "+"

            print("=" * box_width)
            print(f"{'✈ FLIGHT TICKET'.center(box_width)}")
            print("=" * box_width)

            print(format_row("Passenger Name", user['user_name']))
            print(format_row("Passport Number", user['passport_number']))
            print(format_row("Phone Number", user['phone_number']))
            print(format_row("Email", user['email']))
            print("-" * box_width)

            print(format_row("Flight Name", flight['flight_name']))
            print(format_row("Flight Number", row['flight_number']))
            print(format_row("Departure Location", flight['departure_location']))
            print(format_row("Arrival Location", flight['arrival_location']))
            print(format_row("Departure Airport", flight['departure_airport']))
            print(format_row("Arrival Airport", flight['arrival_airport']))
            print("-" * box_width)

            print(format_row("Departure Date", flight['departure_date']))
            print(format_row("Departure Time", flight['departure_time']))
            print(format_row("Arrival Date", flight['arrival_date']))
            print(format_row("Arrival Time", flight['arrival_time']))
            print(format_row("Duration", flight['duration']))
            print("-" * box_width)

            print(format_row("Seat Class", row['seat_class']))
            print(format_row("Seat Number", row['seat_number']))
            print(format_row("Ticket Status", row['ticket_status']))
            print(format_row("Price", f"₹{row['price']}"))
            print("-" * box_width)

            print(format_row("Flight Type", flight['flight_type']))
            print(format_row("Flight Status", flight['status']))
            print("=" * box_width)
            print("\n")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

    def search_ticket(self):
        conn = Connection.connect_to_db()
        if not conn:
            print("Database connection failed.")
            return

        try:
            cursor = conn.cursor(dictionary=True)

            while True:
                print("=" * 60)
                print("|" + " " * 20 + " SEARCH TICKET OPTIONS" + " " * 18 + "|")
                print("=" * 60)
                print("|  1. Search by Ticket Number                   |")
                print("|  2. Search by User ID                         |")
                print("|  3. Search by Flight Number                   |")
                print("|  4. Search by Booking Date                    |")
                print("|  5. Search by Booking Time                    |")
                print("|  6. Search by Seat Class ('Economy', 'Business', 'First') |")
                print("|  7. Search by Seat Number                     |")
                print("|  8. Search by Ticket Price                    |")
                print("|  9. Search by Ticket Status ('Confirmed', 'Canceled') |")
                print("| 10. Back to Main Menu                         |")
                print("=" * 60)

                try:
                    choice = int(input("| Enter Choice: "))

                except ValueError:
                    print("Invalid input! Please enter a number.")
                    continue

                if choice == 1:

                    ticket_id = int(input("Enter your Ticket Number: "))
                    self.display_tickets(ticket_id)     

                elif choice == 2:

                    user_id = input("Enter your User ID: ")
                    query = "SELECT * FROM tickets WHERE user_id = %s"
                    cursor.execute(query, (user_id,))
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            self.display_tickets(row['ticket_id'])
                    else:
                        print("No tickets found")

                elif choice == 3:

                    flight_number = input("Enter your Flight Number: ")
                    query = "SELECT * FROM tickets WHERE flight_number = %s"
                    cursor.execute(query, (flight_number,))
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            self.display_tickets(row['ticket_id'])
                    else:
                        print("No tickets found")

                elif choice == 4:

                    booking_date = input("Enter your Booking Date (YYYY-MM-DD): ")
                    query = "SELECT * FROM tickets WHERE booking_date = %s"
                    cursor.execute(query, (booking_date,))
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            self.display_tickets(row['ticket_id'])
                    else:
                        print("No tickets found")  

                elif choice == 5:

                    booking_time = input("Enter your Booking Time (HH:MM:SS): ")
                    query = "SELECT * FROM tickets WHERE booking_time = %s"
                    cursor.execute(query, (booking_time,))
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            self.display_tickets(row['ticket_id'])
                    else:
                        print("No tickets found")    

                elif choice == 6:

                    flight_number = input("Enter your Flight Number: ")
                    seat_class = input(" Enter seat class ('Economy','Business','First class')")
                    query = "SELECT * FROM tickets WHERE seat_class = %s AND flight_number = %s"
                    cursor.execute(query, (seat_class,flight_number,))
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            self.display_tickets(row['ticket_id'])
                    else:
                        print("No tickets found")    

                elif choice == 7:

                    flight_number = input("Enter your Flight Number: ")
                    seat_number= input("Enter your seat number ")
                    query = "SELECT * FROM tickets WHERE seat_number = %s AND flight_number = %s"
                    cursor.execute(query, (seat_number,flight_number,))
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            self.display_tickets(row['ticket_id'])
                    else:
                        print("No tickets found")

                elif choice == 8:

                    min_price = float(input("Enter Minimum Price: "))
                    max_price = float(input("Enter Maximum Price: "))
                    query = "SELECT * FROM tickets WHERE price BETWEEN %s AND %s"
                    cursor.execute(query, (min_price, max_price))
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            self.display_tickets(row['ticket_id'])
                    else:
                        print("No tickets found")                  

                elif choice == 9:

                    ticket_status = input("Enter your ticket status ('Confirmed','Canceld') ")
                    query = "SELECT * FROM tickets WHERE ticket_status = %s"
                    cursor.execute(query, (ticket_status,))
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            self.display_tickets(row['ticket_id'])
                    else:
                        print("No tickets found")

                elif choice == 10:
                    print("Returning to Main Menu...")
                    break

                else:
                    print("Invalid choice! Please enter a valid option.")
                    continue

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

        finally:
            cursor.close()
            conn.close()

    def display_all_users(self):
        conn = Connection.connect_to_db()
        if not conn:
            print("Database connection failed.")
            return

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users"
            cursor.execute(query)
            rows = cursor.fetchall()

            if not rows:
                print("⚠ No users found.")
                return

            def format_row(label, value, width=60):
                return f"| {label.ljust(20)} : {str(value).ljust(width - 25)} |"

            box_width = 80
            border = "+" + "-" * (box_width - 2) + "+"

            print("=" * box_width)
            print(f"{'All Registered Users'.center(box_width)}")
            print("=" * box_width)

            for row in rows:
                print(border)
                print(f"| {'USER PROFILE'.center(box_width - 4)} |")
                print(border)
                print(format_row("User ID", row['user_id']))
                print(format_row("Name", row['user_name']))
                print(format_row("Email", row['email']))
                print(format_row("Phone", row['phone_number']))
                print(format_row("Address", row['address']))
                print(format_row("Passport", row['passport_number'] if row['passport_number'] else 'N/A'))
                print(format_row("Gender", row['gender']))
                print(border)
                print("\n")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

        finally:
            cursor.close()
            conn.close()

    def display_user_details(self, user_id):
        conn = Connection.connect_to_db()
        if not conn:
            print("Database connection failed.")
            return

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()

            if not row:
                print(f"User with ID {user_id} not found.")
                return

            def format_row(label, value, width=60):
                return f"| {label.ljust(20)} : {str(value).ljust(width - 25)} |"

            box_width = 80
            border = "+" + "-" * (box_width - 2) + "+"

            print(border)
            print(f"| {'USER DETAILS'.center(box_width - 4)} |")
            print(border)
            print(format_row("User ID", row['user_id']))
            print(format_row("Name", row['user_name']))
            print(format_row("Email", row['email']))
            print(format_row("Phone", row['phone_number']))
            print(format_row("Address", row['address']))
            print(format_row("Passport", row['passport_number'] if row['passport_number'] else 'N/A'))
            print(format_row("Gender", row['gender']))
            print(border)
            print("\n")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

        finally:
            cursor.close()
            conn.close()
 
    def search_user(self):
        conn = Connection.connect_to_db()
        if not conn:
            print("Database connection failed.")
            return

        try:
            cursor = conn.cursor(dictionary=True)
            while True:
                print("=" * 60)
                print("|" + " " * 18 + " SEARCH USER DETAILS" + " " * 19 + "|")
                print("=" * 60)
                print("|  1.  Search by User ID                           |")
                print("|  2.  Search by User Name                         |")
                print("|  3.  Search by Email                             |")
                print("|  4.  Search by Phone Number                      |")
                print("|  5.  Search by Passport Number                   |")
                print("|  6.  Search by Gender                            |")
                print("|  7.  Search by Address                           |")
                print("|  8.  Back to Main Menu                           |")
                print("=" * 60)

                choice = input("| Enter your choice: ")

                if choice == "1": 

                    user_id = input("Enter User ID: ")
                    self.display_user_details(user_id)

                elif choice == "2":

                    user_name = input("Enter User Name: ")
                    query = "SELECT * FROM users WHERE user_name = %s"
                    cursor.execute(query, (user_name,))
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            self.display_user_details(row["user_id"])
                    else:
                        print("User not found.")

                elif choice == "3":

                    email = input("Enter Email: ")
                    query = "SELECT * FROM users WHERE email = %s"
                    cursor.execute(query, (email,))
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            self.display_user_details(row["user_id"])
                    else:
                        print("User not found.")

                elif choice == "4":

                    phone_number = input("Enter Phone Number: ")
                    query = "SELECT * FROM users WHERE phone_number = %s"
                    cursor.execute(query, (phone_number,))
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            self.display_user_details(row["user_id"])
                    else:
                        print("User not found.")

                elif choice == "5":

                    passport_number = input("Enter Passport Number: ")
                    query = "SELECT * FROM users WHERE passport_number = %s"
                    cursor.execute(query, (passport_number,))
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            self.display_user_details(row["user_id"])
                    else:
                        print("User not found.")
                
                elif choice == "6":

                    gender= input("Enter Gender: ")
                    query = "SELECT * FROM users WHERE gender = %s"
                    cursor.execute(query, (gender,))
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            self.display_user_details(row["user_id"])
                    else:
                        print("User not found.")
                    
                elif choice == "7":

                    address = input("Enter Address: ")
                    query = "SELECT * FROM users WHERE address = %s"
                    cursor.execute(query, (address,))
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            self.display_user_details(row["user_id"])
                    else:
                        print("User not found.")

                elif choice == "8":
                    break

                else:
                    print("Invalid choice. Please choose a valid option.")
    

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

        finally:
            cursor.close()
            conn.close()

class User:

    def __init__(self):
        self.current_date = date.today()
        self.current_time = datetime.now().time()
        self.login=0
        self.a=Admin()
        self.ticket_LL=Ticket_linked_list()

    def display_user_details(self):
        if not self.login:
            print("You are not logged in.")
            return

        conn = Connection.connect_to_db()
        if not conn:
            print("Database connection failed.")
            return

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            user = cursor.fetchone()

            if not user:
                print("User details not found.")
                return

            def format_row(label, value, width=60):
                return f"| {label.ljust(20)} : {str(value).ljust(width - 25)} |"

            box_width = 80
            border = "+" + "-" * (box_width - 2) + "+"

            print(border)
            print(f"| {'USER PROFILE'.center(box_width - 4)} |")
            print(border)
            print(format_row("User ID", user['user_id']))
            print(format_row("Name", user['user_name']))
            print(format_row("Email", user['email']))
            print(format_row("Address", user['address']))
            print(format_row("Phone", user['phone_number']))
            print(format_row("Passport", user['passport_number'] if user['passport_number'] else 'N/A'))
            print(format_row("Gender", user['gender']))
            print(border)
            print("\n")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

        finally:
            cursor.close()
            conn.close()

    def search_flight_details(self):
        conn = Connection.connect_to_db()
        if not conn:
            print("Database connection failed.")
            return
        try:
            cursor = conn.cursor(dictionary=True)
            while True:
                print("=" * 65)
                print("|" + " " * 20 + "  SEARCH FLIGHT DETAILS" + " " * 22 + "|")
                print("=" * 65)
                print("|  1.  Search by Flight Number                   |")
                print("|  2.  Search by Flight Name                     |")
                print("|  3.  Search by Departure Location              |")
                print("|  4.  Search by Arrival Location                |")
                print("|  5.  Search by Departure Airport               |")
                print("|  6.  Search by Arrival Airport                 |")
                print("|  7.  Search by Departure Date                  |")
                print("|  8.  Search by Departure Time                  |")
                print("|  9.  Search by Arrival Date                    |")
                print("| 10.  Search by Arrival Time                    |")
                print("| 11.  Search by Flight Duration                 |")
                print("| 12.  Search by Flight Type                     |")
                print("| 13.  Search by Flight Status                   |")
                print("| 14.  Search by Flight Price                    |")
                print("| 15.  Back to Main Menu                         |")
                print("=" * 65)

                choice = input("| Enter your choice: ") 

                if choice == '1':

                    flight_number = input("Enter flight number: ")
                    self.display_flights(flight_number)

                elif choice == '2':

                    flight_name = input("Enter flight name: ")
                    query = "SELECT * FROM flights WHERE flight_name = %s AND departure_date > %s AND departure_time > %s"
                    cursor.execute(query, (flight_name, self.current_date , self.current_time))
                    flights = cursor.fetchall()
                    if flights:
                        for flight in flights:
                            self.display_flights(flight['flight_number'])
                    else:
                        print("No flights found with the given name.")

                elif choice == '3':

                    departure_location = input("Enter flight departure location: ")
                    query = "SELECT * FROM flights WHERE departure_location = %s AND departure_date > %s AND departure_time > %s"
                    cursor.execute(query, (departure_location , self.current_date , self.current_time))
                    flights = cursor.fetchall()
                    if flights:
                        for flight in flights:
                            self.display_flights(flight['flight_number'])
                    else:
                        print("No flights found with the given departure location.")

                elif choice == '4':

                    arrival_location = input("Enter flight arrival location: ")
                    query = "SELECT * FROM flights WHERE arrival_location = %s AND departure_date > %s AND departure_time > %s"
                    cursor.execute(query, (arrival_location , self.current_date , self.current_time))
                    flights = cursor.fetchall()
                    if flights:
                        for flight in flights:
                            self.display_flights(flight['flight_number'])
                    else:
                        print("No flights found with the given arrival location.")

                elif choice == '5':

                    departure_airport = input("Enter flight departure airport: ")
                    query = "SELECT * FROM flights WHERE departure_airport = %s AND departure_date > %s AND departure_time > %s"
                    cursor.execute(query, (departure_airport, self.current_date , self.current_time))
                    flights = cursor.fetchall()
                    if flights:
                        for flight in flights:
                            self.display_flights(flight['flight_number'])
                    else:
                        print("No flights found with the given departure airport.")

                elif choice == '6':

                    arrival_airport = input("Enter flight arrival airport: ")
                    query = "SELECT * FROM flights WHERE arrival_airport = %s AND departure_date > %s AND departure_time > %s"
                    cursor.execute(query, (arrival_airport , self.current_date , self.current_time))
                    flights = cursor.fetchall()
                    if flights:
                        for flight in flights:
                            self.display_flights(flight['flight_number'])
                    else:
                        print("No flights found with the given arrival airport.")

                elif choice == '7':

                    departure_date = input("Enter flight departure date (YYYY-MM-DD): ")
                    query = "SELECT * FROM flights WHERE departure_date = %s AND departure_date > %s AND departure_time > %s"
                    cursor.execute(query, (departure_date , self.current_date , self.current_time))
                    flights = cursor.fetchall()
                    if flights:
                        for flight in flights:
                            self.display_flights(flight['flight_number'])
                    else:
                        print("No flights found with the given departure date.")

                elif choice == '8':

                    departure_time = input("Enter flight departure time (HH:MM:SS): ")
                    query = "SELECT * FROM flights WHERE departure_time = %s AND departure_date > %s AND departure_time > %s"
                    cursor.execute(query, (departure_time , self.current_date , self.current_time))
                    flights = cursor.fetchall()
                    if flights:
                        for flight in flights:
                            self.display_flights(flight['flight_number'])
                    else:
                        print("No flights found with the given departure time.")

                elif choice == '9':

                    arrival_date = input("Enter flight arrival date (YYYY-MM-DD): ")
                    query = "SELECT * FROM flights WHERE arrival_date = %s AND departure_date > %s AND departure_time > %s"
                    cursor.execute(query, (arrival_date , self.current_date , self.current_time))
                    flights = cursor.fetchall()
                    if flights:
                        for flight in flights:
                            self.display_flights(flight['flight_number'])
                    else:
                        print("No flights found with the given arrival date.")

                elif choice == '10':

                    arrival_time = input("Enter flight arrival time (HH:MM:SS): ")
                    query = "SELECT * FROM flights WHERE arrival_time = %s AND departure_date > %s AND departure_time > %s"
                    cursor.execute(query, (arrival_time, self.current_date , self.current_time))
                    flights = cursor.fetchall()
                    if flights:
                        for flight in flights:
                            self.display_flights(flight['flight_number'])
                    else:
                        print("No flights found with the given arrival time.")

                elif choice == '11':

                    duration = input("Enter flight duration (Ex: 02h 30m): ")
                    query = "SELECT * FROM flights WHERE duration = %s AND departure_date > %s AND departure_time > %s"
                    cursor.execute(query, (duration , self.current_date , self.current_time))
                    flights = cursor.fetchall()
                    if flights:
                        for flight in flights:
                            self.display_flights(flight['flight_number'])
                    else:
                        print("No flights found with the given duration.")

                elif choice == '12':

                    flight_type = input("Enter flight type (Ex: Domestic ,International): ")
                    query = "SELECT * FROM flights WHERE flight_type = %s AND departure_date > %s AND departure_time > %s"
                    cursor.execute(query, (flight_type, self.current_date , self.current_time))
                    flights = cursor.fetchall()
                    if flights:
                        for flight in flights:
                            self.display_flights(flight['flight_number'])
                    else:
                        print("No flights found with the given flight type.")

                elif choice == '13':

                    status = input("Enter flight status (Ex: 'Scheduled', 'Delayed', 'Cancelled') : ")
                    query = "SELECT * FROM flights WHERE status = %s AND departure_date > %s AND departure_time > %s"
                    cursor.execute(query, (status , self.current_date , self.current_time))
                    flights = cursor.fetchall()
                    if flights:
                        for flight in flights:
                            self.display_flights(flight['flight_number'])
                    else:
                        print("No flights found with the given status.")

                elif choice == '14':

                    print("1. Search by echonomy seat price")
                    print("2. Search by business seat price")
                    print("3. Search by first class seat price")

                    choice = input("Enter your choice: ")

                    if choice == '1':

                        price = input("Enter economy seat price: ")
                        query = "SELECT * FROM flights WHERE economy_price = %s AND departure_date > %s AND departure_time > %s"
                        cursor.execute(query, (price , self.current_date , self.current_time))
                        flights = cursor.fetchall()
                        if flights:
                            for flight in flights:
                                self.display_flights(flight['flight_number'])
                        else:
                            print("No flights found with the given economy seat price.")

                    elif choice == '2':

                        price = input("Enter business seat price: ")
                        query = "SELECT * FROM flights WHERE business_price = %s AND departure_date > %s AND departure_time > %s"
                        cursor.execute(query, (price , self.current_date , self.current_time))
                        flights = cursor.fetchall()
                        if flights:
                            for flight in flights:
                                self.display_flights(flight['flight_number'])
                        else:
                            print("No flights found with the given business seat price.")

                    elif choice == '3':

                        price = input("Enter first class seat price: ")
                        query = "SELECT * FROM flights WHERE first_class_price = %s AND departure_date > %s AND departure_time > %s"
                        cursor.execute(query, (price , self.current_date , self.current_time))
                        flights = cursor.fetchall()
                        if flights:
                            for flight in flights:
                                self.display_flights(flight['flight_number'])
                        else:
                            print("No flights found with the given first class seat price.")

                    else:
                        print("Invalid choice.")

                elif choice == '15':
                    print("back to main menu")
                    break

                else:
                    print("Invalid choice.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            cursor.close()
            conn.close()
                    
    def display_flights(self, flight_number):
        conn = Connection.connect_to_db()
        if not conn:
            print("Database connection failed.")
            return

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM flights WHERE flight_number = %s"
            cursor.execute(query, (flight_number,))
            flight = cursor.fetchone() 

            if not flight:
                print("No flight found with the given flight number.")
                return

            def format_row(label, value, width=70):
                return f"| {label.ljust(22)} : {str(value).ljust(width - 27)} |"

            box_width = 80
            border = "+" + "-" * (box_width - 2) + "+"

            print(border)
            print(f"| {'FLIGHT DETAILS'.center(box_width - 4)} |")
            print(border)
            print(format_row("Flight Number", flight['flight_number']))
            print(format_row("Flight Name", flight['flight_name']))
            print(format_row("Departure Location", flight['departure_location']))
            print(format_row("Arrival Location", flight['arrival_location']))
            print(format_row("Departure Airport", flight['departure_airport']))
            print(format_row("Arrival Airport", flight['arrival_airport']))
            print(format_row("Departure Date", flight['departure_date']))
            print(format_row("Departure Time", flight['departure_time']))
            print(format_row("Arrival Date", flight['arrival_date']))
            print(format_row("Arrival Time", flight['arrival_time']))
            print(format_row("Duration", flight['duration']))
            print(format_row("Flight Type", flight['flight_type']))
            print(format_row("Status", flight['status']))
            print(format_row("Economy Price", f"₹{flight['economy_price']}"))
            print(format_row("Business Price", f"₹{flight['business_price']}"))
            print(format_row("First Class Price", f"₹{flight['first_class_price']}"))
            print(border)
            print("\n")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")

        finally:
            cursor.close()
            conn.close()

    def seat_class(self,row,flight_number,seat_type,first_ticket_price=0,booktype=1):
        conn = Connection.connect_to_db()
        cursor = conn.cursor()
        try:
            if seat_type == "1":

                seat_typee='Economy'
                if row['economy_seats'] > 0:
                    try:    

                        query = "SELECT total_seats FROM flights WHERE flight_number = %s AND departure_date > %s AND departure_time > %s"
                        cursor.execute(query, (flight_number,self.current_date,self.current_time,))
                        all_total_seats = cursor.fetchone()
                        
                        query = "SELECT seat_number FROM tickets WHERE flight_number = %s AND seat_class = %s AND ticket_status = %s "
                        cursor.execute(query, (flight_number, seat_typee,'Confirmed',))
                        booked_seats = {seat[0] for seat in cursor.fetchall()} 

                        total_seats = [f"{chr(67 + i // 10)}{i % 10 + 1}" for i in range(int(all_total_seats[0]) - 20)]

                        available_seats = [seat for seat in total_seats if seat not in booked_seats]

                        print("Available seats:", available_seats)
                        seat_number= input("Enter seat number: ")
                        if (seat_number in available_seats) and (seat_number not in booked_seats):

                            print("Economy class ticket price is ",row['economy_price'])
                            print("Do you want to book this ticket? (yes/no): ")
                            book = input()
                            if book == "yes":
                                try:

                                    if booktype==1:

                                        pay=self.payment((row['economy_price']),booktype)
                                        if pay:
                                            query = "UPDATE flights SET available_seats = available_seats - 1, economy_seats = economy_seats - 1 WHERE flight_number = %s"
                                            cursor.execute(query, (flight_number,))
                                            conn.commit()
                                            self.ticket_LL.add_ticket(self.user_id,flight_number,self.current_date,self.current_time,seat_typee,seat_number,'Confirmed',row['economy_price'])
                                            print("Ticket booked successfully")                              
                                            self.ticket_LL.data_add_LL_to_DataBase()
                                            return True
                                        
                                    elif booktype==2:

                                        pay= self.payment(row['economy_price']+first_ticket_price,booktype)
                                        if pay:
                                            query = "UPDATE flights SET available_seats = available_seats - 1, economy_seats = economy_seats - 1 WHERE flight_number = %s"
                                            cursor.execute(query, (flight_number,))
                                            conn.commit()
                                            self.ticket_LL.add_ticket(self.user_id,flight_number,self.current_date,self.current_time,seat_typee,seat_number,'Confirmed',row['economy_price'])
                                            print("Ticket booked successfully")
                                            self.ticket_LL.data_add_LL_to_DataBase()
                                            return True
                                        
                                except Exception as e:
                                    print("Error during payment or booking:", str(e))

                            else:
                                print("Payment failed")

                        else:
                            print("Booking cancelled")

                    except Exception as e:
                        print("Error while fetching or processing seat data:", str(e))
                        
                else:
                    print("No seats available")

            elif seat_type =="2":

                seat_typee='Business'
                if row['business_seats'] > 0:
                    try:

                        query = "SELECT seat_number FROM tickets WHERE flight_number = %s AND seat_class = %s AND ticket_status = %s "
                        cursor.execute(query, (flight_number, seat_typee,'Confirmed',))
                        booked_seats = {seat[0] for seat in cursor.fetchall()} 

                        total_seats = [f"{chr(66 + i // 10)}{i % 10 + 1}" for i in range(10)]

                        available_seats = [seat for seat in total_seats if seat not in booked_seats]

                        print("Available seats:", available_seats)
                        seat_number= input("Enter seat number: ")
                        if (seat_number in available_seats) and (seat_number not in booked_seats):

                            print("Business class ticket price is ",row['business_price'])
                            print("Do you want to book this ticket? (yes/no): ")
                            book = input()
                            if book == "yes":
                                try:

                                    if booktype==1:

                                        pay=self.payment(row['business_price'],booktype)
                                        if pay:
                                            query = "UPDATE flights SET available_seats = available_seats - 1 , business_seats = business_seats - 1 WHERE flight_number = %s"
                                            cursor.execute(query, (flight_number,))
                                            conn.commit()
                                            self.ticket_LL.add_ticket(self.user_id,flight_number,self.current_date,self.current_time,seat_typee,seat_number,'Confirmed',row['business_price'])
                                            print("Ticket booked successfully")
                                            self.ticket_LL.data_add_LL_to_DataBase()
                                            return True
                                        
                                    elif booktype==2:

                                        pay= self.payment(row['business_price']+first_ticket_price,booktype)
                                        if pay:
                                            query = "UPDATE flights SET available_seats = available_seats - 1 , business_seats = business_seats - 1 WHERE flight_number = %s"
                                            cursor.execute(query, (flight_number,))
                                            conn.commit()
                                            self.ticket_LL.add_ticket(self.user_id,flight_number,self.current_date,self.current_time,seat_typee,seat_number,'Confirmed',row['business_price'])
                                            print("Ticket booked successfully")
                                            self.ticket_LL.data_add_LL_to_DataBase()
                                            return True
                                        
                                except Exception as e:
                                    print("Error during payment or booking:", str(e))   

                            else:
                                print("Payment failed")

                        else:
                            print("Booking cancelled")

                    except Exception as e:
                        print("Error while fetching or processing seat data:", str(e))

                else:
                    print("No seats available")

            elif seat_type == "3":

                seat_typee='First Class'
                if row['first_class_seats'] > 0:
                    try:

                        query = "SELECT seat_number FROM tickets WHERE flight_number = %s AND seat_class = %s AND ticket_status = %s"
                        cursor.execute(query, (flight_number, seat_typee,'Confirmed',))
                        booked_seats = {seat[0] for seat in cursor.fetchall()} 

                        total_seats = [f"{chr(65 + i // 10)}{i % 10 + 1}" for i in range(10)]

                        available_seats = [seat for seat in total_seats if seat not in booked_seats]

                        print("Available seats:", available_seats)
                        seat_number= input("Enter seat number: ")
                        if (seat_number in available_seats) and (seat_number not in booked_seats):
                            print("First class ticket price is ",row['first_class_price'])
                            print("Do you want to book this ticket? (yes/no): ")
                            book = input()
                            if book == "yes":
                                try:

                                    if booktype==1:

                                        pay=self.payment(row['first_class_price'],booktype)
                                        if pay:
                                            query = "UPDATE flights SET available_seats = available_seats - 1 , first_class_seats = first_class_seats - 1 WHERE flight_number = %s"
                                            cursor.execute(query, (flight_number,))
                                            conn.commit()
                                            self.ticket_LL.add_ticket(self.user_id,flight_number,self.current_date,self.current_time,seat_typee,seat_number,'Confirmed',row['first_class_price'])
                                            print("Ticket booked successfully")
                                            self.ticket_LL.data_add_LL_to_DataBase()
                                            return True
                                        
                                    elif  booktype==2:

                                        pay= self.payment(row['first_class_price']+first_ticket_price,booktype)
                                        if pay:
                                            query = "UPDATE flights SET available_seats = available_seats - 1 , first_class_seats = first_class_seats - 1 WHERE flight_number = %s"
                                            cursor.execute(query, (flight_number,))
                                            conn.commit()
                                            self.ticket_LL.add_ticket(self.user_id,flight_number,self.current_date,self.current_time,seat_typee,seat_number,'Confirmed',row['first_class_price'])
                                            print("Ticket booked successfully")
                                            self.ticket_LL.data_add_LL_to_DataBase()
                                            return True
                                        
                                except Exception as e:
                                    print("Error during payment or booking:", str(e))

                            else:
                                print("Payment failed")

                        else:
                            print("Booking cancelled")

                    except Exception as e:
                        print("Error while fetching or processing seat data:", str(e))

                else:
                    print("No seats available")

        except Exception as e:
            print("Unexpected error:", str(e))

        finally:
            cursor.close()
            conn.close()

    def book_ticket(self):
        
        conn = Connection.connect_to_db()
        cursor = conn.cursor(dictionary=True)
        self.booked_ticket=0
        if self.login==0:
            print("Please login first")
            return
        
        else:
            self.booked_seats=0
            Admin.view_all_flights(self)
            
            while True:
                print("+----------------------------------+")
                print("|      Booking Process            |")
                print("|  Select Flight Trip             |")
                print("+----------------------------------+")
                print("|  1. One-Way Trip                |")
                print("|  2. Round-Trip                  |")
                print("|  3. Multi-City Trip             |")
                print("|  4. Back to Main Menu           |")
                print("+----------------------------------+")

                choice = input("Enter your choice: ")

                if choice == "1":
                    
                    from_location = input("Enter from location: ")
                    to_location = input("Enter to location: ")
                    query = "SELECT * FROM flights WHERE departure_location = %s AND arrival_location = %s AND departure_date > %s AND departure_time > %s"
                    cursor.execute(query, (from_location, to_location,self.current_date,self.current_time,))
                    rows = cursor.fetchall()

                    if rows is None:
                        print("From and to locations not found")
                        return False
                    
                    else:
                        print("Flight details:")
                        flight_number_list=[]

                        for row in rows:
                            self.display_flights(row['flight_number'])
                            flight_number_list.append(row['flight_number'])
                        flight_number = input("Enter flight number: ")

                        if flight_number in flight_number_list:
                            query = "SELECT * FROM flights WHERE departure_location = %s AND arrival_location = %s AND flight_number = %s AND departure_date > %s AND departure_time > %s"
                            cursor.execute(query, (from_location,to_location,flight_number,self.current_date, self.current_time))
                            row = cursor.fetchone()

                            if row is None:
                                print("Flight number not found")
                                return False
                            
                            else:
                                print("Flight details:")
                                self.display_flights(row['flight_number'])
                                print("+----------------------------------+")
                                print("|   Please Select Type of Seat     |")
                                print("+----------------------------------+")
                                print("|  1. Economy                      |")
                                print("|  2. Business                     |")
                                print("|  3. First Class                  |")
                                print("+----------------------------------+")

                                seat_type = input("Enter your choice: ")
                                self.seat_class(row,flight_number,seat_type)
                            
                elif choice == "2":

                    from_location = input("Enter from location: ")
                    to_location = input("Enter to location: ")
                    query = "SELECT * FROM flights WHERE departure_location = %s AND arrival_location = %s AND departure_date > %s AND departure_time > %s"
                    cursor.execute(query, (from_location, to_location, self.current_date, self.current_time,))
                    rows = cursor.fetchall()

                    if rows is None:
                        print("From and to locations not found")
                        return False
                    
                    else:
                        print("Flight details:")
                        print("\n")
                        for row in rows:   
                            self.display_flights(row['flight_number'])
                        flight_number1 = input("Enter flight number: ")
                        query = "SELECT * FROM flights WHERE departure_location = %s AND arrival_location = %s AND flight_number = %s AND departure_date > %s AND departure_time > %s"
                        cursor.execute(query, (from_location,to_location,flight_number1 ,self.current_date, self.current_time,))
                        row = cursor.fetchone()

                        if row is None:
                            print("Flight number not found")
                            return False
                        
                        else:
                            self.display_flights(row['flight_number'])
                            print("+----------------------------------+")
                            print("|   Please Select Type of Seat     |")
                            print("+----------------------------------+")
                            print("|  1. Economy                      |")
                            print("|  2. Business                     |")
                            print("|  3. First Class                  |")
                            print("+----------------------------------+")
                            seat_type = input("Enter your choice: ")

                            if seat_type == "1":

                                seat_typee1='Economy'
                                if row['economy_seats'] > 0:
                                    query = "SELECT total_seats FROM flights WHERE flight_number = %s AND departure_date > %s AND departure_time > %s"
                                    cursor.execute(query, (flight_number1, self.current_date, self.current_time,))
                                    all_total_seats = cursor.fetchone()

                                    query = "SELECT seat_number FROM tickets WHERE flight_number = %s AND seat_class = %s AND ticket_status = %s "
                                    cursor.execute(query, (flight_number1, seat_typee1,'Confirmed',))
                                    booked_seats = {seat["seat_number"] for seat in cursor.fetchall()} 

                                    total_seats = [f"{chr(67 + i // 10)}{i % 10 + 1}" for i in range(int(all_total_seats['total_seats']) - 20)]

                                    available_seats = [seat for seat in total_seats if seat not in booked_seats]

                                    print("Available seats:", available_seats)
                                    seat_number= input("Enter seat number: ")
                                    if (seat_number in available_seats) and (seat_number not in booked_seats):

                                        first_ticket_price=row['economy_price']
                                        print("Economy class ticket price is ",first_ticket_price)
                                        print("Do you want to book this ticket? (yes/no): ")
                                        book = input()
                                        if book == "yes":
                                                
                                                query = "UPDATE flights SET available_seats = available_seats - 1, economy_seats = economy_seats - 1 WHERE flight_number = %s"
                                                cursor.execute(query, (flight_number1,))
                                                conn.commit()
                                                self.ticket_LL.add_ticket(self.user_id,flight_number1,self.current_date,self.current_time,seat_typee1,seat_number,'Confirmed',row['economy_price'])
                                                query ="SELECT * FROM flights WHERE departure_location=%s AND arrival_location=%s AND departure_date > %s AND departure_time > %s"
                                                cursor.execute(query,(to_location,from_location, self.current_date, self.current_time,))
                                                rows=cursor.fetchall()

                                                if rows is None:
                                                    print("No flights available on this date")
                                                    return False
                                                
                                                else:
                                                    for row in rows:
                                                        self.display_flights(row['flight_number'])
                                                return_date = input("Enter return date: ")
                                                query= "SELECT * FROM flights WHERE departure_location=%s AND arrival_location=%s AND departure_date=%s AND departure_date > %s AND departure_time > %s"
                                                cursor.execute(query, (to_location,from_location,return_date, self.current_date, self.current_time))
                                                rows = cursor.fetchall()

                                                if rows is None:
                                                    print("No flights available on this date")
                                                    return False
                                                
                                                else:
                                                    print("Available flights on this date:")
                                                    for row in rows:
                                                        self.display_flights(row['flight_number'])
                                                    flight_number2= input("Enter flight number for return ticket: ")
                                                    query = "SELECT * FROM flights WHERE departure_location=%s AND arrival_location=%s AND departure_date=%s AND flight_number=%s AND departure_date > %s AND departure_time > %s"
                                                    cursor.execute(query, (to_location,from_location,return_date,flight_number2, self.current_date, self.current_time,))
                                                    row = cursor.fetchone()

                                                    if row is None:
                                                        print("Flight number not found")
                                                        return False
                                                    
                                                    else:
                                                        self.display_flights(row['flight_number'])
                                                        print("+----------------------------------+")
                                                        print("|   Please Select Type of Seat     |")
                                                        print("+----------------------------------+")
                                                        print("|  1. Economy                      |")
                                                        print("|  2. Business                     |")
                                                        print("|  3. First Class                  |")
                                                        print("+----------------------------------+")
                                                        seat_type = input("Enter your choice: ")
                                                        self.seat_class(row,flight_number2,seat_type,first_ticket_price,2)
                                                                                       
                            elif seat_type == "2":

                                seat_typee1='Business'
                                if row['business_seats'] > 0:
                                    query = "SELECT seat_number FROM tickets WHERE flight_number = %s AND seat_class = %s AND ticket_status = %s"
                                    cursor.execute(query, (flight_number1, seat_typee1,'Confirmed'))
                                    booked_seats = {seat[0] for seat in cursor.fetchall()} 

                                    total_seats = [f"{chr(66 + i // 10)}{i % 10 + 1}" for i in range(10)]

                                    available_seats = [seat for seat in total_seats if seat not in booked_seats]

                                    print("Available seats:", available_seats)
                                    seat_number= input("Enter seat number: ")
                                    if (seat_number in available_seats) and (seat_number not in booked_seats):

                                        first_ticket_price=row['business_price']
                                        print("Business class ticket price is ",first_ticket_price)
                                        print("Do you want to book this ticket? (yes/no): ")
                                        book = input()
                                        if book == "yes":
                                                query = "UPDATE flights SET available_seats = available_seats - 1, Business_seats = Business_seats - 1 WHERE flight_number = %s"
                                                cursor.execute(query, (flight_number1,))
                                                conn.commit()
                                                self.ticket_LL.add_ticket(self.user_id,flight_number1,self.current_date,self.current_time,seat_typee1,seat_number,'Confirmed',row['business_price'])
                                                query ="SELECT * FROM flights WHERE departure_location=%s AND arrival_location=%s AND departure_date > %s AND departure_time > %s"
                                                cursor.execute(query,(to_location,from_location, self.current_date, self.current_time))
                                                rows=cursor.fetchall()

                                                if rows is None:
                                                    print("No flights available on this date")
                                                    return False
                                                else:
                                                    for row in rows:
                                                        self.display_flights(row['flight_number'])
                                                return_date = input("Enter return date: ")
                                                query= "SELECT * FROM flights WHERE departure_location=%s AND arrival_location=%s AND departure_date=%s  AND departure_date > %s AND departure_time > %s"
                                                cursor.execute(query, (to_location,from_location,return_date, self.current_date, self.current_time))
                                                rows = cursor.fetchall()

                                                if rows is None:
                                                    print("No flights available on this date")
                                                    return False
                                                else:
                                                    print("Available flights on this date:")

                                                    for row in rows:
                                                        self.display_flights(row['flight_number'])
                                                    flight_number2= input("Enter flight number for return ticket: ")
                                                    query = "SELECT * FROM flights WHERE departure_location=%s AND arrival_location=%s AND departure_date=%s AND flight_number=%s AND departure_date > %s AND departure_time > %s"
                                                    cursor.execute(query, (to_location,from_location,return_date,flight_number2, self.current_date, self.current_time))
                                                    row = cursor.fetchone()

                                                    if row is None:
                                                        print("Flight number not found")
                                                        return False
                                                    
                                                    else:
                                                        self.display_flights(row['flight_number'])
                                                        print("+----------------------------------+")
                                                        print("|   Please Select Type of Seat     |")
                                                        print("+----------------------------------+")
                                                        print("|  1. Economy                      |")
                                                        print("|  2. Business                     |")
                                                        print("|  3. First Class                  |")
                                                        print("+----------------------------------+")
                                                        seat_type = input("Enter your choice: ")
                                                        self.seat_class(row,flight_number2,seat_type,first_ticket_price,2)
                            
                            elif seat_type == "3":

                                seat_typee1='First Class'
                                if row['first_class_seats'] > 0:
                                    query = "SELECT seat_number FROM tickets WHERE flight_number = %s AND seat_class = %s AND ticket_status = %s"
                                    cursor.execute(query, (flight_number1, seat_typee1,'Confirmed'))
                                    booked_seats = {seat[0] for seat in cursor.fetchall()} 

                                    total_seats = [f"{chr(65 + i // 10)}{i % 10 + 1}" for i in range(10)]

                                    available_seats = [seat for seat in total_seats if seat not in booked_seats]

                                    print("Available seats:", available_seats)
                                    seat_number= input("Enter seat number: ")

                                    if (seat_number in available_seats) and (seat_number not in booked_seats):
                                        first_ticket_price=row['first_class_price']
                                        print("First class ticket price is ",first_ticket_price)
                                        print("Do you want to book this ticket? (yes/no): ")
                                        book = input()
                                        if book == "yes":
                                                
                                                query = "UPDATE flights SET available_seats = available_seats - 1, First_class_seats = First_class_seats - 1 WHERE flight_number = %s"
                                                cursor.execute(query, (flight_number1,))
                                                conn.commit()
                                                self.ticket_LL.add_ticket(self.user_id,flight_number1,self.current_date,self.current_time,seat_typee1,seat_number,'Confirmed',row['first_class_price'])
                                                query ="SELECT * FROM flights WHERE departure_location=%s AND arrival_location=%s AND departure_date > %s AND departure_time > %s"
                                                cursor.execute(query,(to_location,from_location, self.current_date, self.current_time))
                                                rows=cursor.fetchall()

                                                if rows is None:
                                                    print("No flights available on this date")
                                                    return False
                                                
                                                else:
                                                    for row in rows:
                                                        self.display_flights(row['flight_number'])

                                                return_date = input("Enter return date: ")
                                                query= "SELECT * FROM flights WHERE departure_location=%s AND arrival_location=%s AND departure_date=%s AND departure_date > %s AND departure_time > %s"
                                                cursor.execute(query, (to_location,from_location,return_date, self.current_date, self.current_time))
                                                rows = cursor.fetchall()

                                                if rows is None:
                                                    print("No flights available on this date")
                                                    return False
                                                
                                                else:
                                                    print("Available flights on this date:")
                                                    for row in rows:
                                                        self.display_flights(row['flight_number'])
                                                    flight_number2= input("Enter flight number for return ticket: ")
                                                    query = "SELECT * FROM flights WHERE departure_location=%s AND arrival_location=%s AND departure_date=%s AND flight_number=%s AND departure_date > %s AND departure_time > %s"
                                                    cursor.execute(query, (to_location,from_location,return_date,flight_number2, self.current_date, self.current_time))
                                                    row = cursor.fetchone()

                                                    if row is None:
                                                        print("Flight number not found")
                                                        return False
                                                    
                                                    else:
                                                        self.display_flights(row['flight_number'])
                                                        print("+----------------------------------+")
                                                        print("|   Please Select Type of Seat     |")
                                                        print("+----------------------------------+")
                                                        print("|  1. Economy                      |")
                                                        print("|  2. Business                     |")
                                                        print("|  3. First Class                  |")
                                                        print("+----------------------------------+")
                                                        seat_type = input("Enter your choice: ")
                                                        self.seat_class(row,flight_number2,seat_type,first_ticket_price,2)                           
                        
                elif choice == "3":
                    self.multi_city_booking()
                elif choice == "4":
                    break
                else:
                    print("Invalid choice. Please choose a valid option.")

            conn.commit()
            conn.close()
                
    def multi_city_booking(self, flag=0, from_location=None, to_location=None):

        if flag == 0:
            self.conn = Connection.connect_to_db()
            self.cursor = self.conn.cursor(dictionary=True)
            from_location = input("Enter from location: ")
            to_location = input("Enter to location: ")

        query = "SELECT * FROM flights WHERE departure_location = %s AND arrival_location = %s"
        
        if flag == 1:
            query = "SELECT * FROM flights WHERE departure_location = %s AND arrival_location = %s"
            self.cursor.execute(query, (from_location, to_location))
            rows = self.cursor.fetchall()
            if rows:
                print("Available flights on this date:")
                for row in rows:
                    self.display_flights(row['flight_number'])
            else:
                print("No flights available on this date")
                return

            date = input(f"Enter date of travel for {from_location} to {to_location} (in YYYY-MM-DD format): ")
            query = "SELECT * FROM flights WHERE departure_location = %s AND arrival_location = %s AND departure_date = %s"
            self.cursor.execute(query, (from_location, to_location, date))
        else:
            self.cursor.execute(query, (from_location, to_location))

        rows = self.cursor.fetchall()
        
        if not rows:
            print("From and to locations not found")
            return False
        
        print("Flight details:\n")

        for row in rows:
            self.display_flights(row['flight_number'])
        flight_number = input("Enter flight number: ")
        query = "SELECT * FROM flights WHERE departure_location = %s AND arrival_location = %s AND flight_number = %s"
        self.cursor.execute(query, (from_location, to_location, flight_number))
        row = self.cursor.fetchone()

        if not row:
            print("Flight number not found")
            return False

        self.display_flights(row['flight_number'])
        
        print("+----------------------------------+")
        print("|   Please Select Type of Seat     |")
        print("+----------------------------------+")
        print("|  1. Economy                      |")
        print("|  2. Business                     |")
        print("|  3. First Class                  |")
        print("+----------------------------------+")
        seat_type = int(input("Enter your choice: "))

        if seat_type == 1:

            seat_typee = 'Economy'
            connn=Connection.connect_to_db()
            cursor2= connn.cursor()

            if row['economy_seats'] > 0:
                query = "SELECT total_seats FROM flights WHERE flight_number = %s"
                cursor2.execute(query, (flight_number,))
                all_total_seats = cursor2.fetchone()

                query = "SELECT seat_number FROM tickets WHERE flight_number = %s AND seat_class = %s AND ticket_status = %s"
                cursor2.execute(query, (flight_number, seat_typee,'Confirmed'))
                booked_seats = {seat[0] for seat in cursor2.fetchall()} 

                total_seats = [f"{chr(67 + i // 10)}{i % 10 + 1}" for i in range(int(all_total_seats[0]) - 20)]

                available_seats = [seat for seat in total_seats if seat not in booked_seats]
                print("Available seats:", available_seats)
                seat_number= input("Enter seat number: ")

                if (seat_number in available_seats) and (seat_number not in booked_seats):
                    ticket_price = row['economy_price']
                    print("Economy class ticket price is", ticket_price)
                    book = input("Do you want to book this ticket? (yes/no): ")

                    if book.lower() == "yes":
                        query = "UPDATE flights SET available_seats = available_seats - 1, economy_seats = economy_seats - 1 WHERE flight_number = %s"
                        self.cursor.execute(query, (flight_number,))
                        self.conn.commit()
                        self.ticket_LL.add_ticket(self.user_id,flight_number,self.current_date,self.current_time,seat_type,seat_number,'Confirmed',row['economy_price'])

                    else:
                        print("Ticket not booked")

                else:
                    print("No seats available")
        
        elif seat_type == 2:

            seat_typee = 'Business'
            connn=Connection.connect_to_db()
            cursor2= connn.cursor()

            if row['business_seats'] > 0:
                query = "SELECT seat_number FROM tickets WHERE flight_number = %s AND seat_class = %s AND ticket_status = %s"
                cursor2.execute(query, (flight_number, seat_typee,'Confirmed'))
                booked_seats = {seat[0] for seat in cursor2.fetchall()} 

                total_seats = [f"{chr(66 + i // 10)}{i % 10 + 1}" for i in range(10)]

                available_seats = [seat for seat in total_seats if seat not in booked_seats]
                print("Available seats:", available_seats)
                seat_number= input("Enter seat number: ")
                
                if (seat_number in available_seats) and (seat_number not in booked_seats):
                    ticket_price = row['business_price']
                    print("Business class ticket price is", ticket_price)
                    book = input("Do you want to book this ticket? (yes/no): ")

                    if book.lower() == "yes":
                        query = "UPDATE flights SET available_seats = available_seats - 1, business_seats = business_seats - 1 WHERE flight_number = %s"
                        self.cursor.execute(query, (flight_number,))
                        self.conn.commit()
                        self.ticket_LL.add_ticket(self.user_id,flight_number,self.current_date,self.current_time,seat_type,seat_number,'Confirmed',row['business_price'])

                    else:
                        print("Ticket not booked")

                else:
                    print("No seats available")

        elif seat_type == 3:

            seat_typee = 'First Class'
            connn=Connection.connect_to_db()
            cursor2= connn.cursor()

            if row['first_class_seats'] > 0:
                query = "SELECT seat_number FROM tickets WHERE flight_number = %s AND seat_class = %s AND ticket_status = %s"
                cursor2.execute(query, (flight_number, seat_typee,'Confirmed'))
                booked_seats = {seat[0] for seat in cursor2.fetchall()} 

                total_seats = [f"{chr(65 + i // 10)}{i % 10 + 1}" for i in range(10)]

                available_seats = [seat for seat in total_seats if seat not in booked_seats]
                print("Available seats:", available_seats)
                seat_number= input("Enter seat number: ")

                if (seat_number in available_seats) and (seat_number not in booked_seats):
                    ticket_price = row['first_class_price']
                    print("First Class class ticket price is", ticket_price)
                    book = input("Do you want to book this ticket? (yes/no): ")

                    if book.lower() == "yes":
                        query = "UPDATE flights SET available_seats = available_seats - 1, First_class_seats = First_class_seats - 1 WHERE flight_number = %s"
                        self.cursor.execute(query, (flight_number,))
                        self.conn.commit()
                        self.ticket_LL.add_ticket(self.user_id,flight_number,self.current_date,self.current_time,seat_type,seat_number,'Confirmed',row['first_class_price'])

                    else:
                        print("Ticket not booked")

                else:
                    print("No seats available")

        print("If you want to book another flight, press 1. Otherwise, press 0.")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            new_from_location = to_location
            new_to_location = input("Enter your next destination: ")
            self.multi_city_booking(1, new_from_location, new_to_location)

        elif choice == "0":
            amount = self.ticket_LL.calculate_total()
            pay = self.payment(amount, 3)

            if pay:
                print("Ticket booked successfully")
                self.ticket_LL.data_add_LL_to_DataBase()

    def view_booked_tickets(self):

        if self.login == 0:
            print("Please login first")
            return
        
        try:
            conn = Connection.connect_to_db()
            cursor = conn.cursor(dictionary=True)

            def format_row(label, value, width=62):
                 return f"| {label.ljust(20)} : {str(value).ljust(width - 25)} |"
            
            query = "SELECT * FROM tickets WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))
            booked_tickets = cursor.fetchall()

            if booked_tickets:
                for ticket in booked_tickets:
                    try:
                        query = "SELECT * FROM users WHERE user_id = %s"
                        cursor.execute(query, (self.user_id,))
                        user = cursor.fetchone()

                        query = "SELECT * FROM flights WHERE flight_number = %s"
                        cursor.execute(query, (ticket['flight_number'],))
                        flight = cursor.fetchone()

                        if not user or not flight:
                            print("Error retrieving user or flight details")
                            continue

                        print("=" * 70)
                        print(" " * 25 + " FLIGHT TICKET")
                        print("=" * 70)

                        print("| Passenger Details:".ljust(69) + "|")
                        print("|" + "-" * 68 + "|")
                        print(format_row("Name", user['user_name']))
                        print(format_row("Email", user['email']))
                        print(format_row("Phone Number", user['phone_number']))
                        print(format_row("Passport Number", user['passport_number']))
                        print(format_row("Address", user['address']))
                        print(format_row("Gender", user['gender']))
                        print("=" * 70)

                        print("| Ticket Details:".ljust(69) + "|")
                        print("|" + "-" * 68 + "|")
                        print(format_row("User ID", user['user_id']))
                        print(format_row("Flight Number", ticket['flight_number']))
                        print(format_row("Booking Date", ticket['booking_date']))
                        print(format_row("Booking Time", ticket['booking_time']))
                        print(format_row("Seat Class", ticket['seat_class']))
                        print(format_row("Seat Number", ticket['seat_number']))
                        print(format_row("Ticket Status", ticket['ticket_status']))
                        print(format_row("Price", f"₹ {ticket['price']}"))
                        print("=" * 70)

                        print("| Flight Details:".ljust(69) + "|")
                        print("|" + "-" * 68 + "|")
                        print(format_row("Flight Name", flight['flight_name']))
                        print(format_row("Departure From", flight['departure_location']))
                        print(format_row("Arrival To", flight['arrival_location']))
                        print(format_row("Departure Airport", flight['departure_airport']))
                        print(format_row("Arrival Airport", flight['arrival_airport']))
                        print(format_row("Departure Date", flight['departure_date']))
                        print(format_row("Departure Time", flight['departure_time']))
                        print(format_row("Arrival Date", flight['arrival_date']))
                        print(format_row("Arrival Time", flight['arrival_time']))
                        print(format_row("Duration", flight['duration']))
                        print("=" * 70)

                        print("| Additional Details:".ljust(69) + "|")
                        print("|" + "-" * 68 + "|")
                        print(format_row("Flight Type", flight['flight_type']))
                        print(format_row("Flight Status", flight['status']))
                        print("=" * 70 + "\n")

                    except Exception as e:
                        print("Error processing ticket details:", str(e))

            else:
                print("No ticket found")

        except Exception as e:
            print("Error fetching booked tickets:", str(e))

        finally:
            cursor.close()
            conn.close()

    def payment(self,amount,booktype):
        if booktype==1:
            print("Total amount is ",amount)
        elif booktype==2:
            print("Total ticket 1 and 2 price is ",amount)
        elif booktype==3:
            print("Total ticket 1,2 or more price is ",amount)
        print("Payment method:")
        print("1. Cash")
        print("2. Card")
        print("3. Bank Transfer")
        print("4. Cancel")
        choice=input("Enter your choice: ")
        if choice == "1":
            print("Cash payment is accepted")
            return True
        elif choice == "2":
            print("Card payment is accepted")
            return True
        elif choice == "3":
            print("Bank transfer is accepted")
            return True
        elif choice == "4":
            print("payment cancelled")
            return False
        else:
            print("Invalid choice")
                               
    def cancel_ticket(self):
        try:

            if self.login == 1:
                conn = Connection.connect_to_db()
                cursor = conn.cursor(dictionary=True)

                print("Cancel Ticket:")
                query1 = "SELECT * FROM tickets WHERE ticket_status= %s AND user_id= %s"
                cursor.execute(query1, ('Confirmed', self.user_id,))
                rows = cursor.fetchall()
                if rows:

                    ticket_booked = [row['ticket_id'] for row in rows]

                    for i, row in enumerate(rows, start=1):
                        print("+--------------------------------------+")
                        print(f"| Ticket ID    : {row['ticket_id']}           |")
                        print(f"| User ID      : {row['user_id']}             |")
                        print(f"| Flight No.   : {row['flight_number']}       |")
                        print(f"| Booking Date : {row['booking_date']}       |")
                        print(f"| Booking Time : {row['booking_time']}       |")
                        print(f"| Seat Class   : {row['seat_class']}         |")
                        print(f"| Seat Number  : {row['seat_number']}       |")
                        print(f"| Ticket Price : ₹{row['price']}             |")
                        print("+--------------------------------------+")

                    try:
                        choice = int(input("Enter the ticket id you want to cancel: "))
                    except ValueError:
                        print("Invalid input! Please enter a valid ticket ID.")
                        return

                    if choice in ticket_booked:
                        query2 = "UPDATE tickets SET ticket_status = %s WHERE ticket_id = %s"
                        cursor.execute(query2, ('Cancelled', choice,))

                        query3 = "SELECT * FROM tickets WHERE ticket_id = %s"
                        cursor.execute(query3, (choice,))
                        rows = cursor.fetchone()
                        if rows:
                            flight_number = rows['flight_number']
                            seat_class = rows['seat_class']
                            query4 = ''

                            if seat_class == "Economy":
                                query4 = "UPDATE flights SET economy_seats = economy_seats + 1, available_seats = available_seats + 1 WHERE flight_number = %s"
                            elif seat_class == "Business":
                                query4 = "UPDATE flights SET business_seats = business_seats + 1, available_seats = available_seats + 1 WHERE flight_number = %s"
                            elif seat_class == "First Class":
                                query4 = "UPDATE flights SET first_class_seats = first_class_seats + 1, available_seats = available_seats + 1 WHERE flight_number = %s"

                            cursor.execute(query4, (flight_number,))
                            conn.commit()
                            print("Booking cancelled successfully")
                        else:
                            print("You cannot cancel this ticket as it has already departed")
                    else:
                        print("Invalid ticket ID")
                else:
                    print("No bookings found")
            else:
                print("You are not logged in")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            cursor.close()
            conn.close()
                        
    def sign_up(self):

        if self.login == 1:
            print("You are already logged in")
            return

        print("\nSign Up")

        try:
            user_name = input("Enter your username: ")
            password = input("Enter your password: ")
            email = input("Enter your email: ")
            phone_number = input("Enter your phone number: ")
            address = input("Enter your address: ")
            passport_number = input("Enter your passport number: ")
            gender = input("Enter your gender (male/female/other): ")

            conn = Connection.connect_to_db()
            cursor = conn.cursor()

            check_query = "SELECT * FROM users WHERE email = %s OR phone_number = %s"
            cursor.execute(check_query, (email, phone_number))
            if cursor.fetchone():
                print("Email or Phone Number already registered! Try logging in.")
                return

            query = "INSERT INTO users (user_name, password, email, address, phone_number, passport_number, gender) VALUES (%s, %s, %s, %s, %s, %s, %s)"

            cursor.execute(query, (user_name, password, email, address, phone_number, passport_number, gender))
            conn.commit()

            print("Sign Up Successfully!")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

    def sign_in(self):

        if self.login == 1:
            print("You are already logged in")
            return

        try:
            conn = Connection.connect_to_db()
            cursor = conn.cursor(dictionary=True)
            attempts = 3  

            print("\nEnter your details to sign in:")

            for attempt in range(attempts):
                try:

                    user_id = int(input("Enter your user ID: "))
                except ValueError:
                    print("Invalid input! User ID must be a number.")
                    continue  

                password = input("Enter your password: ")

                query = "SELECT * FROM users WHERE user_id = %s AND password = %s"
                cursor.execute(query, (user_id, password))
                row = cursor.fetchone()

                if row:
                    print("Sign In Successfully!\n")
                    self.user_id = row['user_id']
                    self.user_name = row['user_name']
                    self.email = row["email"]
                    self.phone_number = row['phone_number']
                    self.passport_number = row['passport_number']
                    self.gender = row['gender']
                    self.address = row['address']
                    self.login = 1
                    break  
                else:
                    print(f"Invalid user ID or password! Attempts left: {attempts - attempt - 1}")

            else:  
                print("Too many failed attempts! Please try again later.")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            cursor.close()
            conn.close()

    def sign_out(self):
        try:

            if self.login == 1:
                self.login = 0
                print("Sign Out Successfully")

            else:
                print("Please login to sign out")

        except Exception as e:
            print(f"An error occurred: {e}")

    def delete_user_account(self):
        try:

            if self.login == 0:
                print("You are not logged in")

            else:
                conn = Connection.connect_to_db()
                cursor = conn.cursor()
                query = "DELETE FROM users WHERE user_id = %s"
                cursor.execute(query, (self.user_id,))
                conn.commit()
                print("User account deleted successfully")
                self.login = 0

        except Exception as e:
            print(f"An error occurred: {e}")
            
    def update_user_details(self):

        try:
            conn = Connection.connect_to_db()
            cursor = conn.cursor()
            
            if self.login == 1:
                print("\nUpdate Your Details:")

                self.user_name = input("Enter your new username: ")
                self.password = input("Enter your new password: ")  
                self.email = input("Enter your new email: ")
                self.phone_number = input("Enter your new phone number: ")
                self.address = input("Enter your new address: ")
                self.passport_number = input("Enter your new passport number: ")
                self.gender = input("Enter your new gender (male/female/other): ")

                query = "UPDATE users SET user_name = %s, password = %s, email = %s, phone_number = %s, address = %s, passport_number = %s, gender = %s WHERE user_id = %s"
                
                cursor.execute(query, (self.user_name, self.password, self.email, self.phone_number, self.address, self.passport_number, self.gender, self.user_id))
                
                conn.commit()
                print("User details updated successfully!")

            else:
                print("Please login first.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            cursor.close()
            conn.close()

class Main:
    
    def __init__(self):
        self.a=Admin()
        self.u=User()
        self.tl=Ticket_linked_list()

    def menu(self):
        while True:
            try:
                print("=" * 52)
                print("|" + " " * 10 + "✈ FLIGHT TICKET BOOKING SYSTEM" + " " * 10 + "|")
                print("=" * 52)
                print("|" + " " * 50 + "|")
                print("|  1. Admin                                        |")
                print("|  2. User                                         |")
                print("|  3. Exit                                         |")
                print("|" + " " * 50 + "|")
                print("=" * 51)

                choice = input("| Enter Choice: ")

                if choice == "1":
                    admin_id = input("Enter admin id: ")
                    admin_password = input("Enter admin password: ")
                    conn = Connection.connect_to_db()
                    cursor = conn.cursor(dictionary=True)
                    query = "SELECT * FROM admin WHERE admin_id = %s AND password = %s"
                    cursor.execute(query, (admin_id, admin_password))
                    admin = cursor.fetchone()
                    if admin:
                        self.admin_menu()
                    else:
                        print("Invalid admin id or password.")

                elif choice == "2":
                    self.user_menu()

                elif choice == "3":
                    print("| Exiting... Have a great day!                     |")
                    print("=" * 50)
                    break

                else:
                    print("|   Enter a valid choice!                         |")
                    print("=" * 50)

            except Exception as e:
                print(f"|   An error occurred: {e}".ljust(49) + "|")
                print("=" * 50)

    def admin_menu(self):
        while True:
            try:
                print("=" * 50)
                print("|" + " " * 18 + "  ADMIN PANEL" + " " * 17 + "|")
                print("=" * 50)
                print("|  1. Add Flight                                  |")
                print("|  2. Remove Flight                               |")
                print("|  3. Update Flight                               |")
                print("|  4. Show All Flights                            |")
                print("|  5. Find Flight                                 |")
                print("|  6. Show All Tickets                            |")
                print("|  7. Find Ticket                                 |")
                print("|  8. Show All Users                              |")
                print("|  9. Find User                                   |")
                print("| 10. Back to Main Menu                           |")
                print("=" * 50)

                choice1 = input("| Enter Choice: ")

                if choice1 == "1":
                    self.a.add_flight()

                elif choice1 == "2":
                    self.a.delete_flight()

                elif choice1 == "3":
                    self.a.update_flight()

                elif choice1 == "4":
                    self.a.view_all_flights()

                elif choice1 == "5":
                    self.u.search_flight_details()

                elif choice1 == "6":
                    self.a.display_all_tickets()
                    
                elif choice1 == "7":
                    self.a.search_ticket()

                elif choice1 == "8":
                    self.a.display_all_users()

                elif choice1 == "9":
                    self.a.search_user()

                elif choice1 == "10":
                    print("| Returning to Main Menu...                       |")
                    print("=" * 50)
                    break

                else:
                    print("|   Enter a valid choice!                        |")
                    print("=" * 50)

            except ValueError:
                print("|   Invalid input. Please enter a number.        |")
                print("=" * 50)

            except Exception as e:
                print(f"|   An error occurred: {e}".ljust(49) + "|")
                print("=" * 50)
   
    def user_menu(self):
        while True:
            try:
                print("=" * 50)
                print("|" + " " * 18 + "  USER PANEL" + " " * 17 + "|")
                print("=" * 50)
                print("|  1. Search Flight                              |")
                print("|  2. Show All Flights                           |")
                print("|  3. Sign In                                    |")
                print("|  4. Sign Out                                   |")
                print("|  5. Sign Up                                    |")
                print("|  6. Show User Details                          |")
                print("|  7. Delete User Account                        |")
                print("|  8. Book A Ticket                              |")
                print("|  9. Cancel A Ticket                            |")
                print("| 10. Update User Details                        |")
                print("| 11. Show Booked Tickets                        |")
                print("| 12. Back To Main Menu                          |")
                print("=" * 50)

                choice1 = input("| Enter Choice: ")

                if choice1 == "1":
                    self.u.search_flight_details()

                elif choice1 == "2":
                    self.a.view_all_flights()

                elif choice1 == "3":
                    self.u.sign_in()

                elif choice1 == "4":
                    self.u.sign_out()

                elif choice1 == "5":
                    self.u.sign_up()

                elif choice1 == "6":
                    self.u.display_user_details()
                    
                elif choice1 == "7":
                    self.u.delete_user_account()

                elif choice1 == "8":
                    self.u.book_ticket()

                elif choice1 == "9":
                    self.u.cancel_ticket()

                elif choice1 == "10":
                    self.u.update_user_details()

                elif choice1 == "11":
                    self.u.view_booked_tickets()

                elif choice1 == "12":
                    print("| Returning to Main Menu...                      |")
                    print("=" * 50)
                    break

                else:
                    print("|   Enter a valid choice!                        |")
                    print("=" * 50)

            except ValueError:
                print("|   Invalid input. Please enter a number.        |")
                print("=" * 50)

            except Exception as e:
                print(f"|   An error occurred: {e}".ljust(49) + "|")
                print("=" * 50)
        
m = Main()
m.menu()
