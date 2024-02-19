import tkinter as tk
from tkinter import ttk
import mysql.connector


class CatchPriceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Catch Price Results Database")

        # Database connection details
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = ""
        self.db_name = "CatchPrice"

        # Connect to the database and fetch data
        self.connection = mysql.connector.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name
        )
        self.cursor = self.connection.cursor()
        self.fetch_data()
        print('Connected')

        # Initialize Style
        s = ttk.Style()
        # Create Style used by default for all frames
        self.form_frame = ttk.Frame(self.root, style='TFrame')

        self.form_frame.pack(pady=10)

        self.ID_var = tk.StringVar()
        self.Item_var = tk.StringVar()
        self.Brand_var = tk.StringVar()
        self.EntryDate_var = tk.StringVar()
        self.Store_var = tk.StringVar()
        self.Price_var = tk.StringVar()

        ttk.Label(self.form_frame, text="Item:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(self.form_frame, textvariable=self.Item_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Brand:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(self.form_frame, textvariable=self.Brand_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Entry Date:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(self.form_frame, textvariable=self.EntryDate_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Store:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(self.form_frame, textvariable=self.Store_var).grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Price:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(self.form_frame, textvariable=self.Price_var).grid(row=5, column=1, padx=5, pady=5)

        self.navigation_frame = ttk.Frame(self.root)
        self.navigation_frame.pack(pady=10)

        ttk.Button(self.navigation_frame, text="Previous", command=self.show_previous).grid(row=0, column=1, padx=5,
                                                                                            pady=5)
        ttk.Button(self.navigation_frame, text="Next", command=self.show_next).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(self.navigation_frame, text="Add New", command=self.open_new_item_window).grid(row=1, column=0,
                                                                                                  padx=5, pady=5)
        ttk.Button(self.navigation_frame, text="Update", command=self.update_record).grid(row=1, column=1, padx=5,
                                                                                          pady=5)
        ttk.Button(self.navigation_frame, text="Delete", command=self.delete_record).grid(row=1, column=2, padx=5,
                                                                                          pady=5)
        ttk.Button(self.navigation_frame, text="Spare").grid(row=1, column=3, padx=5, pady=5)

        # Initialize the record index
        self.current_record_index = 0
        self.show_record()

    def fetch_data(self):
        # Execute SQL query to fetch data from the Products table
        self.cursor.execute("SELECT * FROM Products")
        self.records = self.cursor.fetchall()

    def show_record(self):
        # Display the current record in the form
        if self.records:
            current_record = self.records[self.current_record_index]
            self.ID_var.set(current_record[0])
            self.Item_var.set(current_record[1])
            self.Brand_var.set(current_record[2])
            self.EntryDate_var.set(current_record[3])
            self.Store_var.set(current_record[4])
            self.Price_var.set(current_record[5])

            # Update the title with the current Item ID
            self.root.title(f"Catch Price Results Database - Item ID: {current_record[0]}")

    def show_previous(self):
        # Show the previous record
        if self.current_record_index > 0:
            self.current_record_index -= 1
            self.show_record()

    def show_next(self):
        # Show the next record
        if self.current_record_index < len(self.records) - 1:
            self.current_record_index += 1
            self.show_record()

    def open_new_item_window(self):
        # New Window to add item
        self.new_item_window = tk.Toplevel(self.root)
        self.new_item_window.title("Add New Item")

        # Widgets to insert new item details
        ttk.Label(self.new_item_window, text="Item:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.item_entry = ttk.Entry(self.new_item_window)
        self.item_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.new_item_window, text="Brand:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.brand_entry = ttk.Entry(self.new_item_window)
        self.brand_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.new_item_window, text="Entry Date:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_date_entry = ttk.Entry(self.new_item_window)
        self.entry_date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.new_item_window, text="Store:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.store_entry = ttk.Entry(self.new_item_window)
        self.store_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.new_item_window, text="Price:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.price_entry = ttk.Entry(self.new_item_window)
        self.price_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(self.new_item_window, text="Save", command=self.save_and_close).grid(row=6, column=1,
                                                                                        padx=5, pady=5)

    def add_new(self):
        new_item = self.item_entry.get()
        new_brand = self.brand_entry.get()
        new_entry_date = self.entry_date_entry.get()
        new_store = self.store_entry.get()
        new_price = self.price_entry.get()

        new_record = (
            new_item,
            new_brand,
            new_entry_date,
            new_store,
            new_price
        )
        self.cursor.execute(
            "INSERT INTO Products (Item, Brand, EntryDate, Store, Price) VALUES (%s, %s, %s, %s, %s)",
            new_record)
        self.connection.commit()

        # Fetch updated data and show the last record
        self.fetch_data()

    def save_and_close(self):
        # Save the data
        self.add_new()

        # Close the window
        self.new_item_window.destroy()

    def update_record(self):
        # Update the current record in the database
        current_record_id = self.ID_var.get()
        updated_record = (
            self.Item_var.get(),
            self.Brand_var.get(),
            self.EntryDate_var.get(),
            self.Store_var.get(),
            self.Price_var.get(),
            current_record_id
        )
        self.cursor.execute(
            "UPDATE Products SET Item=%s, Brand=%s, EntryDate=%s, Store=%s, Price=%s WHERE ID=%s",
            updated_record)
        self.connection.commit()

        # Fetch updated data
        self.fetch_data()

    def delete_record(self):
        # Update the current record in the database
        current_record_id = self.ID_var.get()
        deleted_record = (
            self.Item_var.get(),
            self.Brand_var.get(),
            self.EntryDate_var.get(),
            self.Store_var.get(),
            self.Price_var.get(),
            current_record_id
        )
        self.cursor.execute(
            "ALTER TABLE Products SET Item=%s, Brand=%s, EntryDate=%s, Store=%s, Price=%s WHERE ID=%s",
            deleted_record)
        self.connection.commit()

        # Fetch updated data
        self.fetch_data()


if __name__ == "__main__":
    # Create the main Tkinter window
    root = tk.Tk()

    # Create an instance of the CatchPriceApp class
    app = CatchPriceApp(root)

    # Run the Tkinter event loop
    root.mainloop()
