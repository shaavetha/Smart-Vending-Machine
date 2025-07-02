# Smart-Vending-Machine

A Python based client-server vending machine system with a graphical user interface and SQLite integration. This project started with basic functions, evolved through modular OOP using classes and objects, then expanded into a client-server architecture using sockets, followed by SQLite database integration, and ultimately developed into a fully integrated database-backed GUI version.

# Overview

This project simulates a real-world vending machine using:
- Socket programming for client-server communication
- SQLite for data storage
- Tkinter for a simple graphical user interface (GUI)
- OOP to structure functionality into reusable classes

You can also view the evolution of the code from the function-based prototype to the final production-ready version.

# Technologies Used

- Python
- socket communication (Client-Server Model)
- sqlite3 (Database)
- Tkinter (GUI)
- OOP (Classes, methods)
- File I/O (.txt)

# File structure

 - CW2_week_6_7.py #Initial function-based prototype for vending machine
 - class.py #OOP version of the vending machine
 - client.py #Text-based client
 - server.py #Text based server
 - SQL.py #reusable database logic
 - sqlserver.py #Final server with SQLite integration (performs database operations using logic from SQL.py)
 - gui.py #Final client with GUI using Tkinter
 - vending_machine.db #SQLite database file for storing inventory and transactions
 - inventory.txt #Used in early versions for stock managment (before database was integration)
 - transactions.txt #Used in early versions for recording sales (before database was integration)
 - README.md #Project overview and instructions

# Project Evolution

| Phase            | Key Files              | Description                                  |
|------------------|------------------------|----------------------------------------------|
| 🧪 Week 1-2       | CW2_week_6_7.py       | Function-based prototype, uses .txt files  |
| 🧱 OOP Structure  | class.py             | Introduces class-based logic (Product, Cart) |
| 🧑‍💻 Week 4        | client.py, server.py | Adds socket-based text (client/server)    |
| 🗃 SQLite Added    | sqlserver.py, SQL.py | Server reads/writes to vending_machine.db  |
| 🖱 GUI Added       | gui.py               | GUI-based client using Tkinter               |
