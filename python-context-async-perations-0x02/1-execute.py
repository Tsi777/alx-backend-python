import sqlite3
class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()  # Return the results directly
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
            print("Connection closed after executing query.")
# Example usage
if __name__ == "__main__":
    # Set up some data for testing (only needs to run once)
    with sqlite3.connect("example.db") as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cur.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [("Charlie", 40), ("Dana", 22)])
        conn.commit()
    # Use ExecuteQuery context manager
    with ExecuteQuery("example.db", "SELECT * FROM users WHERE age > ?", (25,)) as results:
        for row in results:
            print(row)
