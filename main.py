from product import load_inventory
from billing import Bill, PaymentProcessor, ReportGenerator

def main():
    inventory = load_inventory()

    while True:
        print("\n===== SMART RETAIL ORDER MANAGEMENT SYSTEM =====")
        print("1. Display Products")
        print("2. Place Order / Generate Bill")
        print("3. View Low Stock Products")
        print("4. Payment Summary Report")
        print("5. Daily Sales Summary")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            inventory.display_products()

        elif choice == "2":
            customer_name = input("Enter customer name (or leave blank for Walk-in): ").strip()
            bill = Bill(customer_name if customer_name else "Walk-in Customer")

            while True:
                try:
                    pid = int(input("\nEnter Product ID (0 to finish): "))
                    if pid == 0:
                        break

                    product = inventory.get_product(pid)
                    if not product:
                        print("❌ Invalid Product ID")
                        continue

                    quantity = int(input("Enter quantity: "))
                    if quantity <= 0:
                        print("❌ Quantity must be greater than zero")
                        continue

                    bill.add_item(product, quantity)

                except ValueError:
                    print("❌ Please enter valid numeric input")

            if bill.is_empty():
                print("⚠ No items ordered")
            else:
                discount = input("Enter discount % (0 if none): ")
                try:
                    bill.apply_discount(float(discount))
                except ValueError:
                    print("Invalid discount, using 0%")
                
                bill.display_bill()

                # Payment
                print("\nSelect Payment Method:")
                print("1. Cash")
                print("2. Card")
                print("3. UPI")
                method_choice = input("Choice: ")

                total_amount = bill.calculate_total()
                if method_choice == "1":
                    payment_result = PaymentProcessor.process_cash_payment(total_amount)
                elif method_choice == "2":
                    payment_result = PaymentProcessor.process_card_payment(total_amount)
                elif method_choice == "3":
                    payment_result = PaymentProcessor.process_upi_payment(total_amount)
                else:
                    print("Invalid choice, defaulting to Cash")
                    payment_result = PaymentProcessor.process_cash_payment(total_amount)

                print(payment_result["message"])
                if payment_result["success"]:
                    bill.set_payment_info(payment_result["method"])
                    bill.save_to_csv()

        elif choice == "3":
            print("\n----- LOW STOCK PRODUCTS -----")
            found = False
            for product in inventory.low_stock_generator():
                print(f"{product.name} (Stock Left: {product.stock})")
                found = True
            if not found:
                print("All products are sufficiently stocked")

        elif choice == "4":
            ReportGenerator.display_payment_summary()

        elif choice == "5":
            ReportGenerator.display_daily_summary()

        elif choice == "6":
            print("👋 Thank you for using the system!")
            break

        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
