# 🛒 Smart Retail Order Management System

A **console-based Python application** designed for small retail stores to manage  
**products, inventory, orders, billing, payments, and sales reports** without using any database.

This project follows a **modular, team-based design**, where each functionality is handled in a separate file.

---

## 📌 Features

### ✅ Product Management
- View product catalogue
- Add new products
- Update product stock
- Delete products
- Low-stock product alerts

### ✅ Order Management
- Add products to cart
- Validate stock availability
- Prevent invalid quantities

### ✅ Billing System
- Generate detailed customer bill
- Apply discounts and tax (GST)
- Multiple payment methods:
  - Cash
  - Card
  - UPI
- Final payable amount calculation

### ✅ File Handling (No Database)
- Products stored in `products.csv`
- Sales data stored in `daily_sales.csv`
- Data persists across program runs

### ✅ Reports
- Daily sales summary
- Payment method summary
- Top-selling products

### ✅ Exception Handling
- Invalid user inputs
- File read/write errors
- Safe program termination using `KeyboardInterrupt`



