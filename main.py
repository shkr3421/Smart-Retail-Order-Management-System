from product import Product, load_inventory
from order import Order
from billing import Bill, PaymentProcessor
from product_file_io import load_inventory_from_file, save_inventory_to_file


def product_menu(inventory):
    while True:
        print("\n--- PRODUCT MANAGEMENT ---")
        print("1. View Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Delete Product")
        print("5. Back")

        try:
            choice = input("Choice: ")

            if choice == "1":
                inventory.display_products()

            elif choice == "2":
                pid = int(input("ID: "))
                name = input("Name: ")
                price = float(input("Price: "))
                stock = int(input("Stock: "))

                inventory.add_product(Product(pid, name, price, stock))
                save_inventory_to_file(inventory)

            elif choice == "3":
                pid = int(input("ID: "))
                stock = int(input("New Stock: "))
                product = inventory.get_product(pid)
                if product:
                    product.stock = stock
                    save_inventory_to_file(inventory)
                else:
                    print("❌ Product not found")

            elif choice == "4":
                pid = int(input("ID: "))
                if pid in inventory.products:
                    del inventory.products[pid]
                    save_inventory_to_file(inventory)
                else:
                    print("❌ Product not found")

            elif choice == "5":
                break

            else:
                print("❌ Invalid choice")

        except ValueError:
            print("❌ Invalid input")
        except Exception as e:
            print("❌ Error:", e)


def order_and_billing_menu(inventory):
    order = Order()

    name = input("Enter customer name (press Enter for Walk-in): ").strip()
    bill = Bill(name if name else "Walk-in Customer")

    while True:
        try:
            pid = int(input("\nEnter Product ID (0 to finish): "))
            if pid == 0:
                break

            product = inventory.get_product(pid)
            if not product:
                print("❌ Invalid Product ID")
                continue

            qty = int(input("Quantity: "))
            if order.add_to_cart(product, qty):
                bill.add_item(product, qty)

        except ValueError:
            print("❌ Enter valid numbers")

    if order.is_empty():
        print("⚠ No items in cart")
        return

    discount = input("Enter discount % (press Enter for none): ").strip()
    if discount:
        try:
            bill.apply_discount(float(discount))
        except ValueError as e:
            print("❌", e)

    bill.display_bill()

    print("\nPayment Method:")
    print("1. Cash")
    print("2. Card")
    print("3. UPI")

    choice = input("Choose payment: ")
    total = bill.calculate_total()

    if choice == "1":
        result = PaymentProcessor.process_cash_payment(total)
    elif choice == "2":
        result = PaymentProcessor.process_card_payment(total)
    elif choice == "3":
        result = PaymentProcessor.process_upi_payment(total)
    else:
        print("❌ Invalid payment option")
        return

    print(result["message"])

    if result.get("success"):
        bill.set_payment_info(result["method"])
        bill.save_to_csv()
        save_inventory_to_file(inventory)


def main():
    try:
        inventory = load_inventory_from_file()

        # ✅ ONLY SOURCE OF DEFAULT PRODUCTS
        if not inventory.products:
            inventory = load_inventory()
            save_inventory_to_file(inventory)

        while True:
            print("\n===== SMART RETAIL SYSTEM =====")
            print("1. Product Management")
            print("2. Place Order & Billing")
            print("3. Low Stock Products")
            print("4. Exit")

            choice = input("Choice: ")

            if choice == "1":
                product_menu(inventory)
            elif choice == "2":
                order_and_billing_menu(inventory)
            elif choice == "3":
                for p in inventory.low_stock_generator():
                    print()
                    print("==== The item which has low quantity left in stocks ====")
                    print("        Product name -",p.name, " , Amount left -", p.stock)
            elif choice == "4":
                print("👋 Thank you, visit again!")
                break
            else:
                print("❌ Invalid option")

    except KeyboardInterrupt:
        print("\n👋 Program terminated by user")
    except Exception as e:
        print("❌ Unexpected error:", e)


if __name__ == "__main__":
    main()
