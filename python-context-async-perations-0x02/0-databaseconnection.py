import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection  # this will be assigned to the `as` variable
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

# Example usage:
if __name__ == "__main__":
    with DatabaseConnection("example.db") as conn:
        cursor = conn.cursor()

        # OPTIONAL: setup for testing (creates table + inserts dummy data if not exists)
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            age INTEGER
                        )''')
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 25))
        conn.commit()

        # Perform SELECT query
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()

        # Print the results
        for row in results:
            print(row)
