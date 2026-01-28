def add_to_cart(self, product, quantity):
    if product.is_stock_available(quantity):
        if product.pid in self.cart:
            # Update existing entry
            self.cart[product.pid]["quantity"] += quantity
            self.cart[product.pid]["amount"] += product.price * quantity
        else:
            # New entry
            self.cart[product.pid] = {
                "product": product,
                "quantity": quantity,
                "amount": product.price * quantity
            }

        product.reduce_stock(quantity)
        self.total_amount += product.price * quantity
        return True
    else:
        return False
