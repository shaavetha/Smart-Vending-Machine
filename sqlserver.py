import socket
from SQL import initialize_db, connect_to_db

#initialize the database
initialize_db()

def load_inventory_from_db():
    #load product inventory from the database
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT ID, name, price, stock FROM products")
    products = cursor.fetchall()
    cursor.close() #close the cursor
    connection.close() #close the connection
    return products

def update_inventory_in_db(product_id, quantity):
    #updates the stock of a product in the database
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Products SET stock = stock - ? WHERE ID = ?",
        (quantity, product_id)
    )
    connection.commit() #saves the changes
    cursor.close()
    connection.close()

def save_transaction_in_db(cart):
    #saves transaction details into the db
    connection = connect_to_db()
    cursor = connection.cursor()
    for item in cart:
        cursor.execute(
            "INSERT INTO transactions (ID, quantity, totalPrice) VALUES (?, ?, ?)",
            (item['id'], item['quantity'], item['price'] * item['quantity'])
        )
    connection.commit()
    cursor.close()
    connection.close()

def get_product_list():
    #retrieves the list of products and formats it as a string
    products = load_inventory_from_db()
    result = "Available Products:\n"
    for product in products:
        result += f"{product[0]}, {product[1]}, ${product[2]}, Stock: {product[3]}\n"
    return result

def process_checkout(cart):
    #updating inventory and saving the transaction
    for item in cart:
        update_inventory_in_db(item['id'], item['quantity'])
    save_transaction_in_db(cart)
    return "Your order has been processed."

def handle_client(client_socket):
    #handles the client requests and manages the shopping cart
    cart = []
    while True:
        request = client_socket.recv(1024).decode('utf-8').split(',')
        if not request:
            break

        if request[0] == 'VIEW_PRODUCTS':
            products = get_product_list()
            client_socket.send(products.encode('utf-8'))
        elif request[0] == 'ADD':
            """try:
                product_id = int(request[1])
                quantity = int(request[2])
                cart.append({'id': product_id, 'quantity': quantity, 'price': 0})
                result = f"Added {quantity} of product {product_id} to cart."
            except (ValueError, IndexError):
                result = "Invalid input. Use: ADD,<product_id>,<quantity>"
            client_socket.send(result.encode('utf-8'))"""
            product_id = int(request[1])
            quantity = int(request[2])
            cart.append({'id': product_id, 'quantity': quantity})
            result = f"Added {quantity} of product {product_id} to cart."
            client_socket.send(result.encode('utf-8'))
        elif request[0] == 'VIEW_CART':
            cart_contents = "Cart:\n" + "\n".join([f"Product ID: {item['id']}, Quantity: {item['quantity']}" for item in cart])
            client_socket.send(cart_contents.encode('utf-8'))
        elif request[0] == 'CHECKOUT':
            result = process_checkout(cart)
            cart.clear()
            client_socket.send(result.encode('utf-8'))
        elif request[0] == 'EXIT':
            client_socket.send("Goodbye!".encode('utf-8'))
            break
        else:
            client_socket.send("Unknown command.".encode('utf-8'))
    client_socket.close()

#set up server socket for listening to incoming connections from the client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 5000))
s.listen(5)
print("Waiting for connections...")

while True:
    conn, addr = s.accept() #accepts the new client connection
    print(f"Connected by {addr}")
    conn.send("Welcome to the Vending Machine server!".encode('utf-8'))
    handle_client(conn) #handles requests from the connected server

s.close()
#close the socket when done
