import sqlite3
import functools
from datetime import datetime # CORRECTED: Changed 'import datetime' to 'from datetime import datetime'
import os       # For checking if database exists
import sys      # For printing to stderr

# Database file name
DATABASE_NAME = 'users.db'

def log_queries(func):
    """
    A decorator that logs the SQL query before executing it.
    It prints the timestamp, function name, and the query.
    """
    @functools.wraps(func) # Preserves the original function's metadata
    def wrapper(*args, **kwargs):
        # Extract the query from the function's arguments.
        # Assuming the query is passed as a keyword argument 'query'
        # or as the first positional argument.
        query = kwargs.get('query')
        if not query and args:
            # Check if the first arg is a string (likely the query)
            if isinstance(args[0], str):
                query = args[0]
            # If the function takes 'conn' as first arg, query might be second
            elif len(args) > 1 and isinstance(args[1], str):
                query = args[1]

        if query:
            # CORRECTED: Changed datetime.datetime.now() to datetime.now()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Log to stderr as per common practice for logs, or stdout if preferred
            print(f"[{timestamp}] INFO: Executing query for '{func.__name__}': {query}", file=sys.stderr)
        else:
            # CORRECTED: Changed datetime.datetime.now() to datetime.now()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] WARNING: Query not found in arguments for '{func.__name__}'", file=sys.stderr)

        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """
    Fetches all users from the database using the given query.
    This function will be decorated by log_queries.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage:
if __name__ == "__main__":
    # Ensure the database is set up before running queries
    if not os.path.exists(DATABASE_NAME):
        print(f"Database {DATABASE_NAME} not found. Please run setup_database.py first.", file=sys.stderr)
        sys.exit(1)

    print("--- Task 0: Logging Database Queries ---")
    # fetch users while logging the query
    users = fetch_all_users(query="SELECT * FROM users")
    print(f"Fetched {len(users)} users.")
    # Print first 3 users for verification
    print("First 3 users:", users[:3])

    print("\n--- Testing another query ---")
    @log_queries
    def fetch_users_by_age(query, min_age):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute(query, (min_age,))
        results = cursor.fetchall()
        conn.close()
        return results

    old_users = fetch_users_by_age(query="SELECT * FROM users WHERE age > ?", min_age=30)
    print(f"Fetched {len(old_users)} users older than 30.")
    print("First 3 older users:", old_users[:3])
