#E-commerce Cart System

# ---------------- Product Class ----------------
class Product:
    def __init__(self, name, price, sku):
        self.name = name
        self.price = price
        self._sku = sku   # encapsulation

    def __str__(self):
        return f"{self.name} (₹{self.price:.2f})"

    def __eq__(self, other):
        return self._sku == other._sku if isinstance(other, Product) else False


# ---------------- Cart Class ----------------
class Cart:
    def __init__(self):
        self.items = []   # composition: list of Product objects

    def add_item(self, product):
        self.items.append(product)

    def remove_item(self, product):
        if product in self.items:
            self.items.remove(product)

    def total_cost(self, discount=0):
        subtotal = sum(item.price for item in self.items)
        if discount > 0:
            subtotal -= subtotal * (discount / 100)
        return subtotal

    @staticmethod
    def calculate_tax(amount, tax_rate=0.05):
        """Static method to calculate tax."""
        return amount * tax_rate

    # Dunder methods
    def __len__(self):
        return len(self.items)

    def __add__(self, other):
        """Merge two carts."""
        if isinstance(other, Cart):
            new_cart = Cart()
            new_cart.items = self.items + other.items
            return new_cart
        return NotImplemented

    def __getitem__(self, index):
        return self.items[index]

    def __contains__(self, product):
        return product in self.items

    def __str__(self):
        if not self.items:
            return "Cart is empty."
        return "\n".join([f"{i+1}. {item}" for i, item in enumerate(self.items)])


# ---------------- User Class ----------------
class User:
    def __init__(self, username, email):
        self.username = username
        self._email = email
        self.cart = Cart()   # composition

    def __str__(self):
        return f"User: {self.username} | Email: {self._email}"


# ---------------- Order Class ----------------
class Order:
    def __init__(self, user, cart):
        self.user = user
        self.cart = cart
        self.status = "Pending"

    def checkout(self, discount=0, tax_rate=0.05):
        subtotal = self.cart.total_cost(discount)
        tax = Cart.calculate_tax(subtotal, tax_rate)
        total = subtotal + tax
        self.status = "Completed"
        return {"subtotal": subtotal, "tax": tax, "total": total}

    def __str__(self):
        return f"Order for {self.user.username} | Status: {self.status}"


# ---------------- Example Usage ----------------
if __name__ == "__main__":
    # Products
    p1 = Product("Laptop", 50000, "SKU101")
    p2 = Product("Phone", 25000, "SKU102")
    p3 = Product("Headphones", 3000, "SKU103")

    # User
    u1 = User("Alice", "alice@example.com")

    # Add items to cart
    u1.cart.add_item(p1)
    u1.cart.add_item(p2)

    print("🛒 Cart Contents:")
    print(u1.cart)

    # Check dunder methods
    print("\nCart length:", len(u1.cart))
    print("Is Laptop in cart?", p1 in u1.cart)
    print("First item:", u1.cart[0])

    # Another cart
    cart2 = Cart()
    cart2.add_item(p3)

    merged_cart = u1.cart + cart2
    print("\nMerged Cart:")
    print(merged_cart)

    # Checkout
    order = Order(u1, merged_cart)
    summary = order.checkout(discount=10, tax_rate=0.18)
    print("\n💳 Checkout Summary:")
    print(summary)
    print(order)

