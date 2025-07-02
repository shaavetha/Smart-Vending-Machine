import sqlite3

# connecting to sqlite database
def connect_to_db():
    return sqlite3.connect("vending_machine.db")

# initializing to create tables and insert into them
def initialize_db():
    connection = connect_to_db()
    cursor = connection.cursor()

    #products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """)

    #transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transactionID INTEGER PRIMARY KEY AUTOINCREMENT,
        ID INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        totalPrice REAL NOT NULL,
        FOREIGN KEY (ID) REFERENCES products(ID)
    )
    """)
    try:
        cursor.execute("ALTER TABLE transactions ADD COLUMN totalPrice REAL")
    except sqlite3.OperationalError:
        pass

    # insert data into products table
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:  # Only insert if table is empty
        cursor.executemany("""
        INSERT INTO products (name, price, stock)
        VALUES (?, ?, ?)
        """, [
            ('Python Programming eBook',10.99,20),
            ('Photo Editing License',29.99,15),
            ('Study Playlist MP3',5.99,50
),
        ])

    connection.commit()
    cursor.close()
    connection.close()

# view products
def view_products():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT ID, name, price FROM products")
    products = cursor.fetchall()

    result = "Available Products:\n"
    for i in products:
        result += f"{i[0]}, {i[1]}, ${i[2]}\n"

    cursor.close()
    connection.close()
    return result

# add to cart
def add_to_cart(product_id, quantity):
    connection = connect_to_db()
    cursor = connection.cursor()

    # fetch product details
    cursor.execute("SELECT name, price, stock FROM products WHERE ID = ?", (product_id,))
    product = cursor.fetchone()

    if not product:
        cursor.close()
        connection.close()
        return "Product not found."

    product_name, price, stock = product
    if stock < quantity:
        cursor.close()
        connection.close()
        return f"Insufficient stock. Available: {stock}"

    # insert transaction into transactions
    total_price = price * quantity
    cursor.execute(
        "INSERT INTO transactions (ID, quantity, totalPrice) VALUES (?, ?, ?)",
        (product_id, quantity, total_price)
    )

    # update stock in products
    cursor.execute(
        "UPDATE Products SET stock = stock - ? WHERE ID = ?",
        (quantity, product_id)
    )

    connection.commit()
    cursor.close()
    connection.close()
    return f"Added {quantity} {product_name}(s) to the cart."

# view Cart
def view_cart():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT products.name, transactions.quantity, products.price, transactions.totalPrice
    FROM transactions
    JOIN products ON transactions.ID = products.ID
    """)
    cart_items = cursor.fetchall()

    result = "Vending Machine:\n"
    total = 0
    for item in cart_items:
        result += f"{item[0]}, ${item[2]:.2f} x {item[1]} = ${item[3]:.2f}\n"
        total += item[3]

    result += f"                 Total: ${total:.2f}\n"
    cursor.close()
    connection.close()
    return result

# checkout
def checkout():
    connection = connect_to_db()
    cursor = connection.cursor()

    # clear all transactions from transactions
    cursor.execute("DELETE FROM transactions")
    connection.commit()

    cursor.close()
    connection.close()
    return "Thank you for shopping with us! Your cart is now empty."

# main menu
def menu():
    initialize_db()
    while True:
        print("\nWelcome to the Vending Machine!")
        print("1. View Products")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Checkout")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print(view_products())
        elif choice == "2":
            product_id = int(input("Enter the product ID: "))
            quantity = int(input("Enter the quantity: "))
            print(add_to_cart(product_id, quantity))
        elif choice == "3":
            print(view_cart())
        elif choice == "4":
            print(checkout())
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# running the menu
#menu()
