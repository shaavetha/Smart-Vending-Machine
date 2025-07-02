import socket

#function to display products
def display_products(s):
    s.send('VIEW_PRODUCTS,'.encode('utf-8')) #requests product list
    msg = s.recv(4096).decode('utf-8') #receive response
    print(msg) #prints the products

#function to add product to the cart
def add_to_cart(s,product_id,quantity):
    s.send(f'ADD,{product_id},{quantity}'.encode('utf-8'))
    msg = s.recv(4096).decode('utf-8')
    print(msg)

#function to view the cart
def view_cart(s):
    s.send('VIEW_CART,'.encode('utf-8'))
    msg = s.recv(4096).decode('utf-8')
    print(msg)

#function for checkout
def request_checkout(s):
    s.send('CHECKOUT,'.encode('utf-8'))
    msg=s.recv(4096).decode('utf-8')
    print(msg)

#creating a socket and connecting to a server
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5001)) #connect to server at localhost: 5001
msg = s.recv(1024).decode('utf-8') #receives Hello from server message
print(msg)

print("Welcome to the Vending Machine!!!")
#main menu loop
while True:
    print("Choose an option:")
    print("1. View products")
    print("2. Add to Cart")
    print("3. View Cart")
    print("4. Checkout")
    print("5. Exit")

    choice = int(input("Enter your choice: ")) #user choice
    if choice == 1:
        display_products(s) #shows products
    elif choice == 2:
        product_id = int(input("Enter product id: "))
        quantity = int(input("Enter the quantity required: "))
        add_to_cart(s,product_id,quantity) #adds item to cart
    elif choice == 3:
        view_cart(s) #shows cart contents
    elif choice == 4:
        request_checkout(s) #checkout
    elif choice == 5:
        print("Thank you and See you next time!")
        break #exit loop
    else:
        print("Invalid choice. Try Again.")

s.close() #close socket connection
print("Thank you for using the vending machine")