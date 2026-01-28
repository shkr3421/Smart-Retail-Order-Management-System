class Order:
    """
    Handles customer order/cart only
    """

    def __init__(self):
        self.cart = {}   # pid -> {product, quantity}

    def add_to_cart(self, product, quantity):
        try:
            if product.is_stock_available(quantity):
                if product.pid in self.cart:
                    self.cart[product.pid]["quantity"] += quantity
                else:
                    self.cart[product.pid] = {
                        "product": product,
                        "quantity": quantity
                    }
                product.reduce_stock(quantity)
                return True
            else:
                print("❌ Insufficient stock")
                return False
        except Exception as e:
            print("❌ Error adding to cart:", e)
            return False

    def is_empty(self):
        return len(self.cart) == 0
