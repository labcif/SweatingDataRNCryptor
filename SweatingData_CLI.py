import argparse
import base64
import rncryptor
import sqlite3
from datetime import datetime

def log_procedure(message):
    with open("logs.txt", "a") as logfile:
        logfile.write(f"{datetime.now()} - {message}\n")

def decrypt_text(text, key):
    log_procedure("Decrypting text")
    decoded_data = base64.b64decode(text)
    log_procedure("Decoded base64 data")
    try:
        result = rncryptor.decrypt(decoded_data, key)
        log_procedure("Decryption successful")
        return result
    except rncryptor.DecryptionError as e:
        log_procedure(f"Decryption error: {e}")
        return f"Error: {e}"

def decrypt_database(file_path, key, save_path):
    log_procedure("Decrypting database")
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    conn.close()

    decrypted_tables = {}
    for table in tables:
        table_name = table[0]
        log_procedure(f"Decrypting table: {table_name}")
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [row[1] for row in cursor.fetchall()]
        cursor.execute(f"SELECT * FROM {table_name};")
        table_contents = cursor.fetchall()
        conn.close()

        decrypted_rows = []
        for row in table_contents:
            decrypted_row = []
            for cell in row:
                try:
                    decoded_data = base64.b64decode(cell)
                    decrypted_cell = rncryptor.decrypt(decoded_data, key)
                    decrypted_row.append(decrypted_cell)
                except Exception:
                    decrypted_row.append(cell)
            decrypted_rows.append(decrypted_row)
        decrypted_tables[table_name] = {"columns": columns, "rows": decrypted_rows}

    # Save decrypted tables to the new file
    with sqlite3.connect(save_path) as conn:
        cursor = conn.cursor()
        for table_name, data in decrypted_tables.items():
            columns = data["columns"]
            column_defs = ', '.join([f"{column} TEXT" for column in columns])  # Define columns as TEXT type
            cursor.execute(f"CREATE TABLE IF NOT EXISTS decrypted_{table_name} ({column_defs});")
            cursor.executemany(f"INSERT INTO decrypted_{table_name} VALUES ({', '.join(['?']*len(columns))});", data["rows"])
        conn.commit()
    log_procedure("Decrypted database saved successfully")


def main():
    parser = argparse.ArgumentParser(description="SweatingDataRNCryptor CLI")
    parser.add_argument("input", help="Encrypted text or path to the database file")
    parser.add_argument("--output", help="Path to save the decrypted database (optional)")
    parser.add_argument("--key", help="Decryption key", default='178!819?000!226@184)087&161$196/616')
    args = parser.parse_args()

    if args.input.endswith(".db"):
        if args.output:
            decrypt_database(args.input, args.key, args.output)
            print("Decrypted database saved successfully.")
        else:
            print("Error: Missing output file path for database decryption.")
    else:
        decrypted_text = decrypt_text(args.input, args.key)
        print("Decrypted text:")
        print(decrypted_text)

if __name__ == "__main__":
    main()
