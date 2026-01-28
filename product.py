class Product:
    """
    Represents a single product in the store
    """

    def __init__(self, pid, name, price, stock):
        if price < 0 or stock < 0:
            raise ValueError("Price and stock must be non-negative")

        self.pid = pid
        self.name = name
        self.price = price
        self.stock = stock

    def is_stock_available(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        return self.stock >= quantity

    def reduce_stock(self, quantity):
        if quantity > self.stock:
            raise ValueError("Insufficient stock")
        self.stock -= quantity


class Inventory:
    """
    Manages all products in the store
    """

    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.pid in self.products:
            raise KeyError("Product ID already exists")
        self.products[product.pid] = product

    def get_product(self, pid):
        return self.products.get(pid)

    def display_products(self):
        if not self.products:
            print("⚠ No products available")
            return

        print("\n{:<5} {:<20} {:<10} {:<10}".format(
            "ID", "Product Name", "Price", "Stock"
        ))
        print("-" * 45)

        for product in self.products.values():
            print("{:<5} {:<20} ₹{:<9} {:<10}".format(
                product.pid,
                product.name,
                product.price,
                product.stock
            ))

    def low_stock_generator(self, limit=10):
        for product in self.products.values():
            if product.stock < limit:
                yield product
