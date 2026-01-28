from product import load_inventory
from order import Order
from billing import ReportGenerator


def main():
    inventory = load_inventory()

    while True:
        print("\n===== SMART RETAIL ORDER MANAGEMENT SYSTEM =====")
        print("1. Display Products")
        print("2. Place Order")
        print("3. View Low Stock Products")
        print("4. Payment Summary")
        print("5. Daily Sales Summary")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            inventory.display_products()

        elif choice == "2":
            order = Order()

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

                    order.add_to_cart(product, quantity)

                except ValueError:
                    print("❌ Please enter valid numeric input")

            if order.is_cart_empty():
                print("⚠ No items in cart")
            else:
                if order.generate_bill():
                    order.save_order()

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
            date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            if date_input:
                ReportGenerator.display_daily_summary(date_input)
            else:
                ReportGenerator.display_daily_summary()

        elif choice == "6":
            print("👋 Thank you for using the system!")
            break

        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()

