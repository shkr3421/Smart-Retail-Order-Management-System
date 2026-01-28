import csv
from datetime import datetime


class Order:
    """
    Handles customer order, billing and saving
    """

    def __init__(self):
        self.cart = {}          # pid : item details
        self.total_amount = 0

    def add_to_cart(self, product, quantity):
        if product.is_stock_available(quantity):
            amount = product.price * quantity

            self.cart[product.pid] = {
                "product": product,
                "quantity": quantity,
                "amount": amount
            }

            product.reduce_stock(quantity)
            self.total_amount += amount
            return True
        else:
            return False

    def is_cart_empty(self):
        return len(self.cart) == 0

    def generate_bill(self):
        print("\n----------- CUSTOMER BILL -----------")
        print("{:<20} {:<10} {:<10}".format(
            "Product", "Qty", "Amount"
        ))
        print("------------------------------------")

        for item in self.cart.values():
            print("{:<20} {:<10} ₹{:<10}".format(
                item["product"].name,
                item["quantity"],
                item["amount"]
            ))

        print("------------------------------------")
        print(f"Total Amount Payable: ₹{self.total_amount}")
        print("------------------------------------")

    def save_order(self, filename="daily_sales.csv"):
        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for item in self.cart.values():
                writer.writerow([
                    date_time,
                    item["product"].pid,
                    item["product"].name,
                    item["quantity"],
                    item["product"].price,
                    item["amount"],
                    self.total_amount
                ])

        print("💾 Order saved successfully.")
