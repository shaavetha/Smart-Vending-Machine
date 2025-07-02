import socket
from CW2_week_6_7 import add_to_cart, view_cart, save_inventory

#initialize empty shopping cart
cart = {}

def load_inventory():
    #loading product inventory from the text file into a list of dictionaries
    product_inventory = []
    with open('/Users/shaavetha/Documents/CST1510/CW2/inventory.txt', 'r') as file:
        for line in file:
            id, name, price, stock = line.strip().split(',')
            product = {
                "id":int(id), "name":name, "price":float(price), "stock":int(stock)
            }
            product_inventory.append(product)
    return product_inventory

#load the inventory into memory
inventory = load_inventory()

def get_product_list(inventory):
    #formatted string of all products in the inventory
    product_list = ""
    for product in inventory:
        product_list += f"ID: {product['id']}, Name: {product['name']}, Price: ${product['price']}, Stock: {product['stock']}\n"
    return product_list

#process checkout and update stock
def process_checkout(cart):
    for product_id, cart_item in cart.items():
        product = find_product_by_id(product_id, inventory)
        if not product:
            return f"Checkout failed: Invalid product id {product_id}"
        if product['stock'] >= cart_item['quantity']:
            product['stock'] -= cart_item['quantity']
        else:
            return f"Checkout failed: Insufficient stock for product ID {product_id}"

    save_inventory(inventory) #save updated stock
    return "Checkout successful\n"

def save_transaction(cart):
    #save transaction details into the file
    with open('/Users/shaavetha/Documents/CST1510/CW2/transactions.txt', 'a') as file:
        for product_id in cart:
            info = cart[product_id]
            total_price = info['quantity']*info['price']
            file.write(f"{product_id}, {info['name']}, {info['quantity']}, {total_price}\n")
        print("Transaction saved")

def find_product_by_id(product_id, inventory):
    for product in inventory:
        if product['id'] == product_id:
            return product
    return None

def add_to_cart(product_id, quantity, inventory):
    product = find_product_by_id(product_id, inventory) #finding the specified product

    if not product:
        return "Invalid product id" #error handling

    if product['stock'] >= quantity:
        if product_id in cart:
            cart[product_id]['quantity'] += quantity
        else:
            cart[product_id] = {
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity
            }
        product['stock'] -= quantity
        return f"Added {quantity} of {product['name']} to the cart"
    else:
        return "Not enough stock available"

#handles client requests over socket connection
def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024).decode('utf-8').split(',') #receive and decode request
        if request[0] == 'VIEW_PRODUCTS':
            products = get_product_list(inventory) #get list of products
            print(f"Sending products: {products}")
            client_socket.send(products.encode('utf-8')) #sends products back
        elif request[0] == 'ADD':
            print(f"Received request: {request}")
            result = add_to_cart(int(request[1]), int(request[2]), inventory) #adds to th ecart
            client_socket.send(result.encode('utf-8')) #sends results back
        elif request[0] == 'VIEW_CART':
            cart_contents = view_cart(cart) #get current contents of the cart
            client_socket.send(cart_contents.encode('utf-8')) #send cart contents back
        elif request[0] == 'CHECKOUT':
            result = process_checkout(cart) # process checkout for items in the cart
            client_socket.send(result.encode('utf-8')) #sends results back

#sets up server socket for listening to incoming connections
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost',5001))
s.listen(5)
print("Waiting for connection")

while True:
    conn, addr = s.accept() #accept new connection from client
    print(f"Connected by {addr}")
    conn.send("Hello from server".encode('utf-8')) #sends greeting message to client
    handle_client(conn) #handle requests from connected client

s.close()
#closes server socket when it is done