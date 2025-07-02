# 2. load_inventory() function
# empty list to hold product inventory
product_inventory = []
def load_inventory():

    with open('/Users/shaavetha/Documents/CST1510/CW2/inventory.txt', 'r') as file:
        #iterate over each line in the file
        for line in file:
            #split the line into individual components
            id, name, price, stock = line.strip().split(',')
            #product dictionary
            product = {
                "id":int(id), "name":name, "price":float(price), "stock":int(stock)
            }
            #append product dictionary to the list
            product_inventory.append(product)
    return product_inventory

#inventory = load_inventory()
#view_products(inventory)


#3. view_products() function
def view_products(inventory):
    print("\nAvailable Products:")
    for product in inventory:
        print(f"ID: {product['id']}, Name:{product['name']}, Price: {product['price']}, Stock: {product['stock']}")




#4. set up cart and add_to_cart function
cart = {}
def add_to_cart(product_id, quantity, inventory):

    found_product = False
    #search for product in inventory using ID
    for product in inventory:
        if product['id']==product_id:
            found_product = True
            # check if enough stock is available
            if product['stock']>= quantity:
                if product_id in cart:
                    #update quantity if it already exists in the cart
                    total = cart[product_id]['quantity'] + quantity
                    #limit to 5 items
                    if total>5:
                        total = 5
                    cart[product_id]['quantity'] = total
                    #decrease stock accordingly
                    product['stock'] = product['stock'] - quantity
                    return f"Quantity updated. {cart[product_id]['quantity']} of{product['name']} in cart"
                else:
                    if quantity >5:
                        quantity = 5
                    cart[product_id] = {'name':product['name'], 'price':product['price'], 'quantity' : quantity}
                    product['stock'] = product['stock'] - quantity
                    return f"Added {quantity} of{product['name']} to the cart\n"
            else:
                return "Not enough stock available"
    if not found_product:
        return "Invalid product id"

#add_to_cart(1, 2, inventory)
#add_to_cart(2, 2, inventory)



def view_cart(cart):
    #check if cart is empty
    if not cart:
        return "\nYour cart is empty\n"
    cart_contents = "\nShopping Cart:\n"
    total_price = 0.0
    total_quantity = 0
    #iterate through each item in the cart
    for product_id in cart:
        info = cart[product_id]
        product_total = info['price']* info['quantity'] #calculate total price for this item
        total_price = total_price + product_total
        total_quantity += info['quantity']
        #append item details as string
        cart_contents += f"{info['name']} - ${info['price']} x {info['quantity']} = ${product_total:.2f}\n"
        cart_contents += f"\n Total Items: {total_quantity} no."
    cart_contents += f"\n Cart total is ${total_price:.2f}\n"
    return cart_contents

#view_cart(cart)



def checkout(inventory):
    print("Cart Contents")
    print(view_cart(cart)) #show current items in the cart before checkout
    confirm = input("Do you want to checkout? (yes/no) ").lower()
    if confirm == "yes":
        save_transactions(cart) #save transaction details to file
        cart.clear() #empty the cart
        print("Checkout Completed. Cart is now cleared")
    else:
        print("Check out cancelled")
        cart.clear()
    save_inventory(inventory) #save updated inventory



def save_inventory(inventory):
    with open('/Users/shaavetha/Documents/CST1510/CW2/inventory.txt', 'w') as file:
        for product in inventory:
            # write each product's details back into the file
            file.write(f"{product['id']},{product['name']},{product['price']},{product['stock']}\n")
    print("Stock updated")



def save_transactions(cart):
    with open('/Users/shaavetha/Documents/CST1510/CW2/transactions.txt', 'a') as file:
        for product_id in cart:
            info = cart[product_id]
            total_price = info['quantity']*info['price'] #calculate total price for this transaction
            #write transaction into the file
            file.write(f"{product_id}, {info['name']}, {info['quantity']}, {total_price}\n")
        print("Transaction saved")


#MAIN FUNCTION
def menu():
    inventory = load_inventory() #load inventory from file
    print("Welcome to the Vending Machine!!!")
    while True: #infinite loop until user decided to exit
        print("Choose an option:")
        print("1. View products")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Checkout")
        print("5. Exit")

        choice = int(input("Enter your choice: ")) #get user input
        if choice == 1:
            view_products(inventory)
        elif choice == 2:
            product_id = int(input("Enter product id: "))
            quantity = int(input("Enter the quantity required: "))
            result = add_to_cart(product_id, quantity, inventory)
            print(result)
        elif choice == 3:
            print(view_cart(cart))
        elif choice == 4:
            checkout(inventory)
        elif choice == 5:
            print("Thank you and See you next time!")
            cart.clear()
            break
#uncomment to run the system when the script is executed
#menu()
