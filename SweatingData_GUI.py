import tkinter as tk
import base64
import rncryptor
from tkinter import filedialog, messagebox
from tkinter import ttk
import sqlite3
import os
from datetime import datetime

def main():
    def log_procedure(message):
            with open("logs.txt", "a") as logfile:
                logfile.write(f"{datetime.now()} - {message}\n")

    def decrypt_text():
        log_procedure("Decrypting text")
        text1 = textbox1.get("1.0", "end-1c")
        log_procedure("Retrieved text from input box")

        decoded_data = base64.b64decode(text1)
        log_procedure("Decoded base64 data")

        if key_entry.get().strip():
            password = f"{key_entry.get().strip()}"
            print(password)
        else:
            password = '178!819?000!226@184)087&161$196/616'
        log_procedure("Using decryption password")

        try:
            result = rncryptor.decrypt(decoded_data, password)
            log_procedure("Decryption successful")
        except rncryptor.DecryptionError as e:
            log_procedure(f"Decryption error: {e}")
            print("Error:", e)

        output_box.delete("1.0", "end")
        log_procedure("Cleared output box")
        output_box.insert("1.0", result)
        log_procedure("Inserted decrypted text into output box")

    def get_file_path():
        file_path = filedialog.askopenfilename()
        database_entry.delete(0, tk.END)
        database_entry.insert(0, file_path)
        save_database_entry()

    def display_tables():
        log_procedure("Displaying tables")
        file_path = database_entry.get()
        log_procedure(f"Retrieved database file path: {file_path}")

        conn = sqlite3.connect(file_path)
        log_procedure("Connected to database")

        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        log_procedure("Executed query to fetch table names")
        
        tables = cursor.fetchall()
        conn.close()
        log_procedure("Closed database connection")

        for table in tables:
            table_name = table[0]
            listbox.insert(tk.END, table_name)
            log_procedure(f"Inserted table name '{table_name}' into listbox")


    def save_decrypted_database(save_path, table_contents, column_names, selected_table):
        log_procedure("Saving decrypted database")
        with sqlite3.connect(save_path) as conn:
            log_procedure("Connected to SQLite database")
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {selected_table} ({', '.join(column_names)});")
            log_procedure(f"Created table {selected_table}")
            for row in table_contents:
                decrypted_row = []
                for cell in row:
                    # Check if cell is base64 encoded
                    try:
                        decoded_data = base64.b64decode(cell)
                        password = '178!819?000!226@184)087&161$196/616'
                        decrypted_cell = rncryptor.decrypt(decoded_data, password)
                        decrypted_row.append(decrypted_cell)
                    except Exception:
                        decrypted_row.append(cell)
                cursor.execute(f"INSERT INTO {selected_table} VALUES ({', '.join(['?']*len(row))})", decrypted_row)
            conn.commit()
            log_procedure("Database saved successfully")
        messagebox.showinfo("Decrypted Database Saved", f"The decrypted database has been saved to:\n{save_path}")


    def display_table_contents():
        log_procedure("Displaying table contents")
        selected_table = listbox.get(tk.ACTIVE)
        log_procedure(f"Selected table: {selected_table}")
        
        if not selected_table:
            log_procedure("No table selected. Display error message.")
            messagebox.showerror("Error", "Please select a table.")
            return
        
        file_path = database_entry.get()
        log_procedure(f"Database file path: {file_path}")
        
        conn = sqlite3.connect(file_path)
        log_procedure("Connected to the database")
        
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {selected_table};")
        log_procedure("Executed SQL query to fetch table contents")
        
        table_contents = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        log_procedure("Fetched table contents and column names")
        
        conn.close()
        log_procedure("Closed database connection")
        
        # Clear previous contents
        for child in table_treeview.get_children():
            table_treeview.delete(child)
        log_procedure("Cleared previous contents from table treeview")
        
        # Update column headings
        table_treeview['columns'] = column_names
        for col in column_names:
            table_treeview.heading(col, text=col)
        log_procedure("Updated column headings")
        
        if key_entry.get().strip():
            password = key_entry.get().strip()
        else:
            password = '178!819?000!226@184)087&161$196/616'

        # Insert new data
        for row in table_contents:
            decoded_row = []
            for cell in row:
                try:
                    decoded_data = base64.b64decode(cell)
                    decrypted_cell = rncryptor.decrypt(decoded_data, password)
                    decoded_row.append(decrypted_cell)
                    # Add cell with blue foreground color
                    table_treeview.insert('', 'end', values=[f"Decrypted: {decrypted_cell}"], tags='blue_text')
                    log_procedure("Inserted decrypted cell with blue foreground color")
                except Exception:
                    decoded_row.append(cell)
            table_treeview.insert('', 'end', values=decoded_row)
        log_procedure("Inserted new data into table treeview")

        # Configure tag for blue text
        table_treeview.tag_configure('blue_text', foreground='blue')
        log_procedure("Configured tag for blue text")

        # Ask user for save path for decrypted database
        save_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database", "*.db")])
        if save_path:
            log_procedure(f"User selected save path for decrypted database: {save_path}")
            # Save decrypted database to the new file
            save_decrypted_database(save_path, table_contents, column_names, selected_table)
            log_procedure("Decrypted database saved successfully")

    def save_key(event=None):
        with open("key.txt", "w") as file:
            file.write(key_entry.get())

    def load_key():
        try:
            with open("key.txt", "r") as file:
                key_entry.delete(0, tk.END)
                key_entry.insert(0, file.read())
        except FileNotFoundError:
            pass

    def save_database_entry():
        entry_text = database_entry.get()
        with open("database_entry.txt", "w") as f:
            f.write(entry_text)

    def load_database_entry():
        if os.path.exists("database_entry.txt"):
            with open("database_entry.txt", "r") as f:
                entry_text = f.read()
                database_entry.insert(tk.END, entry_text)

    # Create main window
    root = tk.Tk()
    root.title("SweatingDataRNCryptor GUI")
    root.geometry("1024x768")

    top_frame = tk.Frame(root,)
    top_frame.pack(fill=tk.X, side=tk.TOP)

    bot_frame = tk.Frame(root)
    bot_frame.pack(fill=tk.X, side=tk.BOTTOM)

    textbox_frame = tk.Frame(bot_frame)
    textbox_frame.pack(fill=tk.X, expand=True, side=tk.TOP)

    textbox_top_frame = tk.Frame(textbox_frame)
    textbox_top_frame.pack(fill=tk.X, expand=True, side=tk.TOP)

    left_frame = tk.Frame(textbox_frame)
    left_frame.pack(fill=tk.X, expand=True, side=tk.LEFT)

    right_frame = tk.Frame(textbox_frame)
    right_frame.pack(fill=tk.X, expand=True, side=tk.RIGHT)

    button_frame = tk.Frame(bot_frame)
    button_frame.pack(side=tk.BOTTOM, padx=10, pady=5)

    top_top_frame = tk.Frame(top_frame)
    top_top_frame.pack(fill=tk.X, expand=True, side=tk.TOP)


    file_database_frame = tk.Frame(top_top_frame)
    file_database_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, anchor='s')

    title_frame = tk.Frame(file_database_frame)
    title_frame.pack(side=tk.TOP)
    label = tk.Label(title_frame, text="SweatingDataRNCryptor GUI", font=("Arial", 18, "bold"))
    label.pack(padx=10, pady=5, side=tk.TOP)
    file_database_frame3 = tk.Frame(file_database_frame)
    file_database_frame3.pack(fill=tk.X, side=tk.BOTTOM)
    file_database_frame4 = tk.Frame(file_database_frame)
    file_database_frame4.pack(fill=tk.X, side=tk.BOTTOM)
    file_database_frame2 = tk.Frame(file_database_frame)
    file_database_frame2.pack(fill=tk.X, side=tk.BOTTOM)

    label3 = tk.Label(file_database_frame4, text="Insert key:")
    label3.pack(side=tk.LEFT, padx=5, pady=5)
    key_entry = tk.Entry(file_database_frame4)
    key_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5, pady=5)
    key_entry.bind("<FocusOut>", save_key)  # Bind the <FocusOut> event to the save_key function
    load_key()

    label = tk.Label(file_database_frame2, text="Select File Containing Database:*")
    label.pack(side=tk.LEFT, padx=5, pady=5)
    browse_button = tk.Button(file_database_frame2, text="Browse", command=get_file_path)
    browse_button.pack(side=tk.RIGHT, padx=5, pady=5)
    display_button = tk.Button(file_database_frame2, text="Display Tables", command=display_tables)
    display_button.pack(side=tk.RIGHT, padx=5, pady=5)
    database_entry = tk.Entry(file_database_frame2)
    database_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5, pady=5)
    load_database_entry()

    database_view_frame = tk.Frame(top_top_frame)
    database_view_frame.pack( side=tk.RIGHT)
    listbox = tk.Listbox(database_view_frame)
    listbox.pack()
    view_button = tk.Button(database_view_frame, text="View Table Contents", command=display_table_contents)
    view_button.pack()

    database_table_frame = tk.Frame(top_frame)
    database_table_frame.pack(fill=tk.X, expand=True, side=tk.BOTTOM)
    table_treeview = ttk.Treeview(root, show='headings')
    table_treeview.pack(fill=tk.BOTH, expand=True)

    entry_text_label = tk.Label(left_frame, text="Encrypted Data:")
    entry_text_label.pack(side=tk.TOP, anchor="w")
    textbox1 = tk.Text(left_frame, font=("Arial", 14), height='2', width='3')
    textbox1.pack(side=tk.BOTTOM, padx=10, pady=5, fill="x", expand=True)
    entry_text_label = tk.Label(right_frame, text="Decrypted Data:")
    entry_text_label.pack(side=tk.TOP, anchor="w")
    output_box = tk.Text(right_frame, font=("Arial", 14), height='2', width='3')
    output_box.pack(side=tk.BOTTOM, padx=10, pady=5, fill="x", expand=True)

    concat_button = tk.Button(button_frame, text="Decrypt", command=decrypt_text)
    concat_button.pack()

    root.mainloop()

if __name__ == '__main__':
    main()
    
