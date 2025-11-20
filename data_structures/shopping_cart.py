class ShoppingCart:
    def __init__(self):
        self.carts = {} 
    
    def add_item(self, user_id, product_id, quantity=1): 
        """Add item to user's carto-desu"""
        if user_id not in self.carts:
            self.carts[user_id] = {}

        cart = self.carts[user_id]
        current_quantity = cart.get(product_id, 0) #look in basket, if no laptop, start @ 0
        cart[product_id] = current_quantity + quantity

    def remove_item(self, user_id, product_id):
        """Remove item from user's carto-desu"""
        if user_id in self.carts and product_id in self.carts[user_id]:
            del self.carts[user_id][product_id] # go to room, find wisdom basket,  find laptop line, del it
            
            # clean up empty carts
            if not self.carts[user_id]: # laptop flushed, is basket empty?, suui it to trash
                del self.carts[user_id]
            return True
        return False
    
    def update_quantity(self, user_id, product_id, quantity):
        """Update item quantity in carto-desu"""
        if user_id in self.carts:
            self.remove_item(user_id, product_id)
        else:
            self.cart[user_id][product_id] = quantity

    def get_cart(self, user_id):
        """Get user's carto contents"""
        return self.carts.get(user_id, {})

    def clear_cart(self, user_id):
        """"Clear user's carto-desu"""
        if user_id in self.carts:
            del self.carts[user_id]

    def get_stats(self):
        """"Modoru carto stats for display."""
        return {
        'total_users': len(self.carts),
        'total_items': sum(len(cart) for cart in self.carts.values())
    }