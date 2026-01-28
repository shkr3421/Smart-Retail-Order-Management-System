# 🛒 Smart Retail Order Management System

**Console-Based Python Application**

---

## Project Overview

The **Smart Retail Order Management System** is a **console-based Python application** designed for small retail stores to manage **products, customer orders, billing, payments, and sales reports** without using any database.

All data is stored using **file handling (CSV files)**, making the system lightweight and easy to maintain.

---

## 🎯 Objectives

* Manage product inventory efficiently
* Process customer orders with stock validation
* Generate bills with tax and discounts
* Handle multiple payment methods
* Persist sales data using files
* Generate daily sales and payment summary reports

---

## ⚙️ Features

### Product Management

* View all products
* Add new products
* Update stock
* Delete products
* Low-stock detection

### Order & Billing

* Add products to cart
* Validate stock availability
* Apply discounts
* Calculate tax and final bill
* Generate formatted bill

### Payment Processing

* Cash payment (with change calculation)
* Card payment (simulation)
* UPI payment (simulation)
* Payment status tracking

### File Handling (No Database)

* Product inventory stored in CSV
* Sales data stored in CSV
* Automatic file creation and updates

### Reports

* **Daily Sales Summary**
* **Payment Method Summary (Cash / Card / UPI)**

---

## Technologies Used

* **Python 3**
* CSV File Handling
* Object-Oriented Programming (OOP)
* Exception Handling
* Modular Programming

---

## 📁 Project Structure

```
Smart-Retail-Order-Management-System/
│
├── main.py                 # Main application & menu
├── product.py              # Product and inventory logic
├── order.py                # Order/cart handling
├── billing.py              # Billing, payment & reports
├── product_file_io.py      # Inventory file handling
│
├── products.csv            # Product inventory data
├── daily_sales.csv         # Sales & billing data
│
└── README.md               # Project documentation
```

---

## 🔄 Application Flow

1. Load product inventory from file
2. User selects menu option
3. Products added to order
4. Bill generated with tax & discount
5. Payment processed
6. Sales data saved to CSV
7. Reports generated from CSV

---

## 📊 Reports Explanation

### Daily Sales Summary

Displays:

* Total bills generated
* Total customers
* Total items sold
* Total revenue
* Total discount given
* Top-selling products

### Payment Summary

Displays:

* Number of payments via Cash, Card, and UPI
* Total amount received via each method
* Total transactions and revenue

---

## File Handling Strategy

* **products.csv**

  * Stores product ID, name, price, stock
* **daily_sales.csv**

  * Stores bill-wise sales data
  * Used for generating reports

No database is used; all persistence is handled using CSV files.

---

## How to Run the Project

```bash
python main.py
```

---

## How to Test the System

1. Place an order and complete payment
2. Check `daily_sales.csv` for new entries
3. View **Daily Sales Summary** from menu
4. View **Payment Summary** from menu

---

## Team Contribution Strategy

* Each module handled by a separate team member

## 📌 Conclusion

The **Smart Retail Order Management System** demonstrates real-world retail workflows using **core Python concepts**.
