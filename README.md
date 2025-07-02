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

# How to Run

Required Files:
- gui.py
- sqlserver.py
- SQL.py
- vending_machine.db

These 4 files must be in the same folder.

Setup Instructions:
- Ensure Python is installed
- The sqlserver.py file and the gui.py file need to be in the same directory as the SQL.py file as it contains necessary functions used by sqlserver.py
- Open two separate cmd windows or terminal windows
- On the first window, navigate to the directory ‘sqlserver.py’ is in
- Run the prompt:
             python sqlserver.py
- On the second window, navigate to where ‘gui.py’ is in
- Run the prompt: 
       python gui.py

**sqlserver.py should be run first and then gui.py**

# Data Handling
Old versions:
  Uses inventory.txt and transactions.txt for storage and logging
Final version:
  All inventory and transactions are stored in vending_machine.db (SQLite database)
  SQL operations are handled by functions in SQL.py


# Testing Older Versions

To explore development progress:
Uncomment the line '#menu' and run CW2_week_6_7.py to see function-based vending logic
Run class.py to test class-based design
Run client.py and server.py in two terminals to try the basic socket model (text-based, no database)

*These versions use inventory.txt and transactions.txt, not the .db file.*
 
 


