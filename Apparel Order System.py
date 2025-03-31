import sqlite3
import csv
#   I am creating a shirt class to give a description of what each
#   self class attribute will do. I also put a quantity function to
#   add to the list of shirts you will see later in the code. After
#   through the menu
class Shirts:
    def __init__(self, design, size, color, price, stock):
        self.__size = size
        self.__color = color
        self.__price = price
        self.__stock = stock
        self.__design = design

    def update_stock(self, quantity):
        self.__stock -= quantity

    def is_stock_available(self, quantity):
        return self.__stock >= quantity

    def set_design(self, design):
        self.__design = design

    def set_size(self, size):
        self.__size = size

    def set_color(self, color):
        self.__color = color

    def set_price(self, price):
        self.__price = price

    def set_stock(self, stock):
        self.__stock = stock

    def get_design(self):
        return self.__design

    def get_size(self):
        return self.__size

    def get_color(self):
        return self.__color

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def display_shirts(self):
        print(f"""
                | Size: {self.get_size()}
                | Color: {self.get_color()}
                | Price: ${self.get_price():,.2f}
                | Stock: {self.get_stock()}
                | Design: {self.get_design()}""")

#   For the customer class we wanted to give the NULL value to the ID
#   since we are relying on our inputs for our users. We wanted to use
#   loops to find the correct outputs for the database table."""
class Customer:
    def __init__(self, customer_id=None, name="", email="", address=""):        
        self.__customer_id = customer_id
        self.__name = name
        self.__email = email
        self.__address = address

    def set_customer_id(self, customer_id):
        if not isinstance(customer_id, int) or customer_id <= 0:
            raise ValueError("Customer ID must be a positive integer")
        self.__customer_id = customer_id

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def get_customer_id(self):
        return self.__customer_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_address(self):
        return self.__address

    def display_customer(self):
        return (f"Customer Information:\n"
                f"ID: {self.__customer_id}\n"
                f"Name: {self.__name}\n"
                f"Email: {self.__email}\n"
                f"Address: {self.__address}")


class Order:
    def __init__(self, order_id, customer_id, items, total_price, status, payment_status):
        self.__order_id = order_id
        self.__customer_id = customer_id
        self.__items = items  # List of (tshirt_id, quantity) tuples
        self.__total_price = total_price
        self.__status = status
        self.__payment_status = payment_status

    def set_order_id(self, order_id):
        self.__order_id = order_id

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_items(self, items):
        self.__items = items

    def set_total_price(self, total_price):
        self.__total_price = total_price

    def set_status(self, status):
        self.__status = status

    def set_payment_status(self, payment_status):
        self.__payment_status = payment_status

    def get_order_id(self):
        return self.__order_id

    def get_customer_id(self):
        return self.__customer_id

    def get_items(self):
        return self.__items

    def get_total_price(self):
        return self.__total_price

    def get_status(self):
        return self.__status

    def get_payment_status(self):
        return self.__payment_status

    def add_item(self, tshirt_id, quantity):
        self.__items.append((tshirt_id, quantity)) #This return will either find the stock or will print that there is not enough stock

    def calculate_total(self):
        return sum(tshirt.get_price() * quantity for tshirt, quantity in self.__items) #Just like SQL we put the sum in front and then we multiply the quantity in the loop

    def update_status(self, new_status):
        types_of_status = ["pending", "processing", "shipped", "delivered"] #This will update the status to show the status I based this off of my general manager simulator but I didn't use import random in this one
        if new_status in types_of_status:
            print("Your order status is currently:", new_status)
        else:
            print("Status is unknown")


class DatabaseHandler:
    def __init__(self, db_name="tshirt_store.db"):
        self.db_name = db_name
        self.connection = None  # This will connect to the database and make sure the connection is NULL before starting 
        self.cursor = None # This will make sure the cursor is NULL before starting

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name) # I was able to use the template made from my toolbox and able to apply this just change a few names 
            self.cursor = self.connection.cursor()
            print("Connected to the database successfully.") # This will print out the message that the database is connected
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")

    def disconnect(self):
        if self.connection: #This will disconnect the database and print out the message that the database is disconnected
            self.connection.close()
            print("Disconnected from the database.")

    def create_tables(self):
        try: #This will create the tables for the database and print out the message that the tables are created 
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS TShirts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    design TEXT NOT NULL,
                    size TEXT NOT NULL,
                    color TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    address TEXT NOT NULL
                )
            """)  #The most important part of the table is the primary key and the foreign key and making sure they are not NULL, because there are no errors that will display
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    total_price REAL NOT NULL,
                    status TEXT NOT NULL,
                    payment_status TEXT NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES Customers(id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS OrderItems (
                    order_id INTEGER NOT NULL,
                    tshirt_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES Orders(id),
                    FOREIGN KEY (tshirt_id) REFERENCES TShirts(id)
                )
            """)
            self.connection.commit()  # This will commit the connection to the database and also the transaction
            print("Tables created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def insert_tshirt(self, tshirt):
        try: #For insert tshirt we are going to insert the tshirt into the database and print out the message that the tshirt is inserted
            query = """
                INSERT INTO TShirts (design, size, color, price, stock)
                VALUES (?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (tshirt.get_design(), tshirt.get_size(), tshirt.get_color(), tshirt.get_price(), tshirt.get_stock()))  #We are using all of our attributes to insert the tshirt which why we used getters ans setters
            self.connection.commit()
            print("T-shirt inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting T-shirt: {e}")

    def insert_customer(self, customer):
        try:
            query = """
                INSERT INTO Customers (name, email, address)
                VALUES (?, ?, ?)
            """
            self.cursor.execute(query, (customer.get_name(), customer.get_email(), customer.get_address()))
            self.connection.commit()
            customer.set_customer_id(self.cursor.lastrowid)  #We are using all of our attributes from the customer class and Set the customer_id after insertion
            print("Customer inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting customer: {e}")

    def insert_order(self, order):
        try:
            query = """
                INSERT INTO Orders (customer_id, total_price, status, payment_status)
                VALUES (?, ?, ?, ?)
            """
            self.cursor.execute(query, (order.get_customer_id(), order.get_total_price(), order.get_status(), order.get_payment_status()))
            self.connection.commit()
            order.set_order_id(self.cursor.lastrowid)#Now using the attributes from the order class
            print("Order inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting order: {e}")

    def insert_order_item(self, order_id, tshirt_id, quantity):
        try:
            query = """
                INSERT INTO OrderItems (order_id, tshirt_id, quantity)
                VALUES (?, ?, ?)
            """
            self.cursor.execute(query, (order_id, tshirt_id, quantity))
            self.connection.commit()
            print("Order item inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting order item: {e}")

    def get_tshirts(self):
        try:
            query = "SELECT * FROM TShirts"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving T-shirts: {e}")
            return []

    def get_customers(self):
        try:
            query = "SELECT * FROM Customers"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving customers: {e}")
            return []

    def get_customer(self, customer_id):
        try:
            query = "SELECT * FROM Customers WHERE id = ?"
            self.cursor.execute(query, (customer_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving customer: {e}")
            return []

    def get_orders(self):
        try:
            query = "SELECT * FROM Orders"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving orders: {e}")
            return []

    def get_order_items(self, order_id):
        try:#For this query we are using the SELECT Statement for SQL and using JOIN statement combine the two tables in order for the SELECT statement to recognize the tables
            query = """
                SELECT TShirts.design, TShirts.size, TShirts.color, OrderItems.quantity 
                FROM OrderItems
                JOIN TShirts ON OrderItems.tshirt_id = TShirts.id 
                WHERE OrderItems.order_id = ?
            """
            self.cursor.execute(query, (order_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving order items: {e}")
            return []

    def update_tshirt_stock(self, tshirt_id, new_stock):
        try:  #For this query we are using the UPDATE Statement for SQL and using the WHERE statement to update the stock of the TShirts
            query = "UPDATE TShirts SET stock = ? WHERE id = ?"
            self.cursor.execute(query, (new_stock, tshirt_id))
            self.connection.commit()
            print("T-shirt stock updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating T-shirt stock: {e}")

    def delete_tshirt(self, tshirt_id):
        try:
            query = "DELETE FROM TShirts WHERE id = ?"
            self.cursor.execute(query, (tshirt_id,))
            self.connection.commit()
            print("T-shirt deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting T-shirt: {e}")


def add_sample_tshirts(db_handler):
    sample_tshirts = [
        Shirts("Design A", "M", "Red", 19.99, 50), #Just like in the business manager simulator I am adding the sample tshirts to the database, I added different sizes, colors, price, and stock
        Shirts("Design B", "L", "Blue", 24.99, 30),
        Shirts("Design C", "S", "Green", 15.99, 20),
        Shirts("Design D", "XL", "Black", 29.99, 10),
    ]

    for tshirt in sample_tshirts: #This for loop will insert the sample T-Shirts into the database and confirm it with a message
        db_handler.insert_tshirt(tshirt)
    print("The cool T-shirts were added!!!.")


def create_csv_file(db_handler): #This function will create a CSV file for the order history and will print out the message that the CSV file is created
    orders = db_handler.get_orders()
    if not orders:
        print("No orders found to export.")
        return

    order_items = db_handler.get_order_items(orders[0][0])  # This will be the order items and it wants the first 
    csv_file = open("order_history.csv", "w", newline="") #This will open the CSV file and write the order history to the CSV file
    csv_writer = csv.writer(csv_file) 
    csv_writer.writerow(["Order ID", "Customer Name", "Total Price", "Status", "Payment Status"]) # This will write the order ID, Customer Name, Total Price, Status, and Payment Status to the CSV file and it will make it look clean

    for order in orders:
        customer_name = db_handler.get_customer(order[1])[0][1]  
        csv_writer.writerow([order[0], customer_name, order[2], order[3], order[4]])

        # Write order items
        items = db_handler.get_order_items(order[0]) # This will write the order items to the CSV file it must be in the same order as the order history
        for item in items:
            csv_writer.writerow(["", "", "", "", f"{item[0]} - {item[1]} {item[2]} ({item[3]} units)"]) # This will write the order items to the CSV file it must be in the same direction as the order history history

    csv_file.close()
    print("Order history saved to 'order_history.csv'.")
    print("CSV file created successfully.")


def main(): #This is where the main menu will be displayed and the user will be able to choose the options and here we will be able to organize the code and put loops in order to run correctly
    db_handler = DatabaseHandler()
    db_handler.connect()
    db_handler.create_tables()

    # Add sample T-shirts to the database (only once)
    add_sample_tshirts(db_handler)

    while True:
        print("\n----T-Shirt Store Menu ----------------") #The menu that you will see when you start it up 
        print("1. Browse T-Shirts")
        print("2. Place an Order")
        print("3. View Order History")
        print("4. Update T-Shirt Stocks")
        print("5. Add T-Shirt")
        print("6. Export Order History to CSV")
        print("7. Exit")

        option = input("Enter an option in the menu: ")

        if option == "1": #This will show what happens when the user chooses option 1 and will display the T-Shirts color, size and more
            tshirts = db_handler.get_tshirts()
            if tshirts:
                print("\nAvailable T-Shirts:")
                for tshirt in tshirts:
                    print(f"""ID: {tshirt[0]}, 
                          Design: {tshirt[1]}, 
                          Size: {tshirt[2]}, 
                          Color: {tshirt[3]}, 
                          Price: ${tshirt[4]:.2f}, 
                          Stock: {tshirt[5]}""")
            else:
                print("There are no T-Shirts available.")

        elif option == "2":
            customer_name = input("Enter your name: ")
            customer_email = input("Enter your email: ")
            customer_address = input("Enter your address: ")

            customer = Customer(name=customer_name, email=customer_email, address=customer_address)
            db_handler.insert_customer(customer)
            customer_id = customer.get_customer_id()

            tshirts = db_handler.get_tshirts()
            if tshirts:
                print("\nAvailable T-Shirts:")
                for tshirt in tshirts:
                    print(f"ID: {tshirt[0]}, Design: {tshirt[1]}, Size: {tshirt[2]}, Color: {tshirt[3]}, Price: ${tshirt[4]:.2f}, Stock: {tshirt[5]}")

                order_items = [] #Order Items for  this customer in the order list
                while True:
                    tshirt_id = input("Enter T-Shirt ID (or 'quit' to finish): ")
                    if tshirt_id.lower() == "quit":
                        break
                    quantity = int(input("Enter the quantity: "))

                    tshirt_found = False #This will show the message that the T-Shirt is not found and will print out the message
                    for tshirt in tshirts:
                        if tshirt[0] == int(tshirt_id):
                            tshirt_found = True
                            if tshirt[5] >= quantity: #This will show the message that the stock is insufficient and will print out the message and add the quantity to the order
                                order_items.append((tshirt[0], quantity))
                                db_handler.update_tshirt_stock(tshirt[0], tshirt[5] - quantity)
                                print(f"Added {quantity} x {tshirt[1]} to your order.")
                            else:
                                print("Insufficient stock.")
                            break
                    if not tshirt_found:
                        print("T-Shirt not found.")

                if order_items: # This will calculate the total price by using sum like SQL and then multiply by its quantity
                    total_price = 0
                    for tshirt_id, quantity in order_items:
                        tshirt = next(tshirt for tshirt in tshirts if tshirt[0] == tshirt_id)
                        total_price += tshirt[4] * quantity

                    order = Order(order_id=None, 
                                  customer_id=customer_id, 
                                  items=order_items, 
                                  total_price=total_price, 
                                  status="pending", 
                                  payment_status="unpaid")
                    db_handler.insert_order(order)
                    order_id = order.get_order_id() #Authorizing the order to be inserted into the database

                    for tshirt_id, quantity in order_items:
                        db_handler.insert_order_item(order_id, tshirt_id, quantity)
                    print(f"Your order has been placed. Total: ${total_price:.2f}")
                else:
                    print("NO ITEMS ADDED!!!.") #If nothing happens then this message will be displayed
            else:
                print("No T-Shirts available to order.")

        elif option == "3":
            customer_email = input("Enter your email to view orders: ")  #Ask the user to enter the email you really can enter anything but it will not show anything
            customers = db_handler.get_customers()
            customer_found = False #Verify to see if the customer is found
            for customer in customers:
                if customer[2] == customer_email: #Make sure the emails match, so the program can move forward
                    customer_found = True
                    orders = db_handler.get_orders()
                    if orders: #All this will do is print out the order and make it look organized
                        print(f"\nOrders for {customer[1]}:")
                        for order in orders:
                            if order[1] == customer[0]:
                                print(f"""Order ID: {order[0]}, 
                                      Total: ${order[2]:.2f}, 
                                      Status: {order[3]}, 
                                      Payment Status: {order[4]}""")
                                items = db_handler.get_order_items(order[0])
                                if items:
                                    print("Items:")
                                    for item in items:
                                        print(f"""- {item[0]} 
                                              ({item[1]}, 
                                              {item[2]}), 
                                              Quantity: {item[3]}""")
                    else:
                        print("No orders found.")
                    break
            if not customer_found:
                print("Customer not found.")

        elif option == "4": #A lot of option 4 & 5 is input heavy and will ask the user to input the information
            tshirt_id = input("Enter T-Shirt ID to update stock: ")
            new_stock = int(input("Enter the new stock quantity: "))
            db_handler.update_tshirt_stock(tshirt_id, new_stock)

        elif option == "5":
            design = input("Enter T-Shirt design: ")
            size = input("Enter T-Shirt size (S, M, L, XL): ")
            color = input("Enter T-Shirt color: ")
            price = float(input("Enter T-Shirt price: "))
            stock = int(input("Enter T-Shirt stock: "))

            new_tshirt = Shirts(design, size, color, price, stock)
            db_handler.insert_tshirt(new_tshirt)
            print("T-Shirt added successfully.")

        elif option == "6":#This will export the order history to a CSV file and will print out the message that the CSV file is created
            # Export order history to CSV
            create_csv_file(db_handler)

        elif option == "7": #This will exit the program and will print out the message that the program is exiting
            print("Exiting program now.")
            db_handler.disconnect()
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
