Apparel Order System:

The Apparel Order System is a Python-based project designed to manage the ordering and inventory of T-shirts. The system allows users to browse available apparel, place orders, manage inventory, and export order history to a CSV file.

Features

T-Shirt Inventory Management: Add, update, and delete T-shirts.

Customer Management: Store customer details securely.

Order Processing: Place orders and track order status.

Database Integration: Uses SQLite for data storage.

CSV Export: Generate a CSV file for order history.

User-Friendly Menu: Interactive CLI-based navigation.

Technologies Used

Python (Object-Oriented Programming)

SQLite3 (Database management)

CSV (Exporting order history)

Installation

Prerequisites

Ensure you have Python installed (version 3.x recommended).

Steps

Clone the repository:

git clone https://github.com/your-repo/apparel-order-system.git

Navigate to the project directory:

cd apparel-order-system

Run the script:

python main.py

Usage

Upon running the script, you will be presented with a menu that allows you to:

Browse available T-shirts.

Place an order.

View order history.

Update T-shirt stock.

Add a new T-shirt.

Export order history to CSV.

Exit the program.

Database Schema

The system consists of four main tables:

TShirts: Stores shirt details (design, size, color, price, stock).

Customers: Stores customer information.

Orders: Stores order details, including order status.

OrderItems: Links orders with specific T-shirt items and quantities.

Example Workflow

Start the program.

Choose option 1 to view available T-shirts.

Choose option 2 to place an order by entering customer details and selecting T-shirts.

The system will check stock availability and process the order.

Order details will be stored in the database.

Choose option 6 to export order history to a CSV file.

Future Enhancements

Implement a graphical user interface (GUI).

Add payment processing integration.

Develop a web-based version using Flask or Django.
