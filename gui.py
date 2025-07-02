import tkinter as tk
from tkinter import messagebox
import socket

class VendingMachine:
    def __init__(self, master):
        self.master = master
        self.master.title("Vending Machine")
        self.products = {}

        #connect to the server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('localhost', 5000))
        msg = self.s.recv(1024).decode('utf-8')
        print(msg)

        self.create_main_window() #set up the main window user interface

    def create_main_window(self):
        #creates the main interface for the vending machine
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(padx=10, pady=10)

        self.product_frame = tk.Frame(self.main_frame)
        self.product_frame.pack()

        #button for refreshing products
        refresh_button = tk.Button(self.main_frame, text="Refresh Products", command=self.display_products)
        refresh_button.pack(pady=5)

        #button for viewing cart
        cart_button = tk.Button(self.main_frame, text="View Cart", command=self.view_cart)
        cart_button.pack(pady=5)

        #button for checking out
        checkout_button = tk.Button(self.main_frame, text="Checkout", command=self.request_checkout)
        checkout_button.pack(pady=5)

        self.display_products() #displays initial list of products

    def display_products(self):
        for widget in self.product_frame.winfo_children():
            widget.destroy() #clears previous product entries

        self.s.send('VIEW_PRODUCTS,'.encode('utf-8'))
        msg = self.s.recv(4096).decode('utf-8')
        products = msg.split('\n')[1:-1]

        self.products.clear()
        for product in products:
            id, name, price, stock = product.split(', ')
            self.products[id] = name
            frame = tk.Frame(self.product_frame)
            frame.pack(pady=5)

            label = tk.Label(frame, text=f"{name} - {price} - Stock: {stock.split(': ')[1]}")
            label.pack(side=tk.LEFT)

            entry = tk.Entry(frame, width=5)
            entry.insert(0, "1")
            entry.pack(side=tk.LEFT, padx=5)

            button = tk.Button(frame, text="Add to Cart", command=lambda i=id, e=entry: self.add_to_cart(i, e.get()))
            button.pack(side=tk.LEFT, padx=5)

    def add_to_cart(self, product_id, quantity):
        #sends requests to add a product to the cart
        self.s.send(f'ADD,{product_id},{quantity}'.encode('utf-8'))
        msg = self.s.recv(4096).decode('utf-8')
        product_name = self.products.get(product_id, "Unknown Product")
        messagebox.showinfo("Cart Update", f"{product_name} has been added to cart.\n\n{msg}")

    def view_cart(self):
        #displays the contents of the cart
        self.s.send('VIEW_CART,'.encode('utf-8'))
        msg = self.s.recv(4096).decode('utf-8')

        cart_window = tk.Toplevel(self.master)
        cart_window.title("Shopping Cart")
        cart_window.geometry("400x300")

        cart_frame = tk.Frame(cart_window)
        cart_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(cart_frame)
        scrollbar = tk.Scrollbar(cart_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas) #creates a scrollable frame

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        cart_items = msg.split('\n')[1:-1]
        #cart items in scrollable frame
        if cart_items:
            for item in cart_items:
                product_id, quantity = item.split(', ')
                product_id = product_id.split(': ')[1]
                quantity = quantity.split(': ')[1]
                product_name = self.products.get(product_id, f"Unknown Product (ID: {product_id})")
                item_label = tk.Label(scrollable_frame, text=f"{product_name} - Quantity: {quantity}")
                item_label.pack(pady=2)
        else:
            empty_label = tk.Label(scrollable_frame, text="Your cart is empty.")
            empty_label.pack(pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def request_checkout(self):
        #sends checkout request
        self.s.send('CHECKOUT,'.encode('utf-8'))
        msg = self.s.recv(4096).decode('utf-8')
        messagebox.showinfo("Checkout", msg)
        self.display_products() #refresh product list after checking out

    def __del__(self):
        self.s.send('EXIT,'.encode('utf-8'))
        self.s.close()

root = tk.Tk()
app = VendingMachine(root) #creates the instance
root.mainloop() #starts the main Tkinter loop
