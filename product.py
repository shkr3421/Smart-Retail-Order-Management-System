<<<<<<< HEAD
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
=======

class Product:

    #Represents a single product in the store
    

    def __init__(self, pid, name, price, stock):
        self.pid = pid          # Product ID
        self.name = name        # Product name
        self.price = price      # Price per unit
        self.stock = stock      # Available stock

    def is_stock_available(self, quantity):
        
        #Checks if required quantity is available
        #It is called from Main file before adding items to cart
        
        return self.stock >= quantity

    def reduce_stock(self, quantity):
    
        #It is called from Main file after adding items to a cart
        self.stock -= quantity


class Inventory:
    
    #Manages all products in the store
    

    def __init__(self):
        self.products = {}      # Dictionary to store products

    def add_product(self, product):
        
        # Adds a product to inventory
        
        self.products[product.pid] = product

    def get_product(self, pid):
        
        # Returns product object using product ID
        
        return self.products.get(pid)

    def display_products(self):
    
        # Displays all products , it is called from the Main
        
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
    
        # Generator that yields products with stock below limit
    
        for product in self.products.values():
            if product.stock < limit:
                yield product



def load_inventory():
    
    # Creates inventory and loads initial products
    #it is first call method to load the initial products to the inventory
    
    inventory = Inventory()

    inventory.add_product(Product(101, "Rice", 60, 50))
    inventory.add_product(Product(102, "Sugar", 45, 30))
    inventory.add_product(Product(103, "Oil", 150, 20))
    inventory.add_product(Product(104, "Wheat Flour", 55, 25))
    inventory.add_product(Product(105, "Tea Powder", 220, 15))
    inventory.add_product(Product(106, "Soap", 35, 40))
    inventory.add_product(Product(107, "Shampoo", 120, 8))
    inventory.add_product(Product(108, "Toothpaste", 90, 18))
    inventory.add_product(Product(109, "Toothbrush", 40, 35))
    inventory.add_product(Product(110, "Milk Packet", 28, 60))
    inventory.add_product(Product(111, "Curd", 35, 22))
    inventory.add_product(Product(112, "Biscuits", 20, 70))
    inventory.add_product(Product(113, "Chocolate", 50, 45))
    inventory.add_product(Product(114, "Notebook", 60, 30))
    inventory.add_product(Product(115, "Pen", 10, 100))
    inventory.add_product(Product(116, "Detergent", 95, 28))
    inventory.add_product(Product(117, "Hand Sanitizer", 65, 12))

    return inventory
# inventory = load_inventory()
# inventory.display_products()

# product = inventory.get_product(107)
# if product.is_stock_available(2):
#     product.reduce_stock(2)
# inventory.display_products()
>>>>>>> debdffbe654320b2f4216b01be5355a9601135ed
