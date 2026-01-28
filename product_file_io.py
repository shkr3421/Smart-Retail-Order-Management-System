import csv
import os
from product import Product, Inventory


def load_inventory_from_file(filename="products.csv"):
    inventory = Inventory()
    try:
        if not os.path.exists(filename):
            return inventory

        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                inventory.add_product(
                    Product(
                        int(row["pid"]),
                        row["name"],
                        float(row["price"]),
                        int(row["stock"])
                    )
                )
    except Exception as e:
        print("❌ Error loading products:", e)

    return inventory


def save_inventory_to_file(inventory, filename="products.csv"):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["pid", "name", "price", "stock"])
            for p in inventory.products.values():
                writer.writerow([p.pid, p.name, p.price, p.stock])
    except Exception as e:
        print("❌ Error saving products:", e)
