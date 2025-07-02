class Product():
    #initialize a product with id, name, price, and stock
    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

    #method to update the stock
    def update_stock(self, quantity):
        if self.stock >= quantity:
            self.stock = self.stock - quantity
            return True
        else:
            print("Insufficient stock")
    #string representation of the product
    def __str__(self):
        return (f"Id: {self.id}, Name: {self.name}, Price: {self.price}, Stock: {self.stock}")

#creating instances of Product
product1 = Product(1, "Python Programming eBook", 10.99, 20)
product2 = Product(2,"Photo Editing License",29.99, 15)
product3 = Product(3, "Study Playlist MP3", 5.99, 50)

#print(product1)
#print(product2)
#print(product3)

class Cart():
    #initialize empty cart
    def __init__(self):
        self.items = {} #dictionary to store products and their quantities

    #method to add a product to the cart
    def add_item(self,product,quantity):
        if product.update_stock(quantity):
            if product.id in self.items:
                self.items[product.id]["quantity"] += quantity
            else:
                self.items[product.id] = {"product": product, "quantity":quantity}
                print(f"Added {quantity} of product {product.name} into the cart")
        else:
            print(f"Not enough stock for {product.name}")

    #method to view all the items in the cart and their total price
    def view_items(self):
        total_price = 0
        print("Cart contents:\n")
        for product_id in self.items:
            item = self.items[product_id]
            product = item["product"]
            quantity = item["quantity"]
            product_total = product.price*quantity
            total_price = total_price + product_total
            print(f"{product.name}, Quantity: {quantity}, Total: {product_total}")
        print(f"Total price:${total_price}")

    #method to clear all the items in the cart
    def clear_cart(self):
        self.items.clear()
        print("Cart has been cleared!")

class VendingMachine():
    inventory_file = '/Users/shaavetha/Documents/CST1510/inventory.txt' #path for inventory file
    transaction_file = '/Users/shaavetha/Documents/CST1510/transactions.txt' #path for transaction file
    def __init__(self,inventory_file, transaction_file):
        self.inventory_file = inventory_file
        self.transaction_file = transaction_file
        self.product_inventory = []
        self.cart = Cart()

    #method to load products from inventory file into vending machine's inventory
    def load_inventory(self):
        with open(self.inventory_file, 'r') as file:
            for line in file:
                product_id, name, price, stock = line.strip().split(',')
                product = Product(int(product_id), name, float(price), int(stock)) # create a product instance
                self.product_inventory.append(product)
        print("Inventory loaded!")

    #method to display all products in the inventory
    def view_products(self):
        print("Product Inventory: ")
        for product in self.product_inventory:
            print(product)

    # method to add product and its quantity to the cart
    def add_to_cart(self):
        product_id = int(input("Enter product Id: "))
        quantity = int(input("Enter the quantity: "))

        product = None
        for p in self.product_inventory:
            if p.id == product_id:
                product = p
                break

        if product.stock >= quantity:
            self.cart.add_item(product,quantity)
            product.update_stock(quantity)
            print(f"{quantity} of {product.name} added to the cart.")
        else:
            print(f"Only {product.stock} of {product.name} available")

    #method to view contents of the cart
    def view_cart(self):
        print("cart contents: ")
        self.cart.view_items() #calling method from Cart class to display items

    #method for the checkout process
    def checkout(self):
        print("cart contents: ")
        self.view_cart()
        confirm = input("Do you wish to proceed with the checkout? (yes/no): ").lower()
        if confirm == "yes":
            self.save_transactions()
            self.cart.clear_cart()
            self.save_inventory()
            print("Checkout completed successfully. Cart has been cleared")
        else:
            print("Checkout cancelled.")

    #method to append transaction details into the file after checkout
    def save_transactions(self):
        with open(self.transaction_file, 'a') as file:
            for product_id in self.cart.items.keys():
                item = self.cart.items[product_id]
                product = item["product"]
                quantity = item["quantity"]
                total_price = product.price * quantity
                file.write(f"{product_id},{product.name},{quantity},{total_price}")
        print("Transactions saved successfully")

    #method to save current inventory back into the txt file
    def save_inventory(self):
        with open(self.inventory_file,'w') as file:
            for product in self.product_inventory:
                file.write(f"{product.id},{product.name},{product.price},{product.stock}\n")
        print("Inventory saved")