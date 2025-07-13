import sqlite3
import functools
import os
import sys # For printing to stderr

# Database file name
DATABASE_NAME = 'users.db'

def with_db_connection(func):
    """
    A decorator that automatically handles opening and closing database connections.
    It passes the connection object as the first argument to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            # Pass the connection object as the first argument to the original function
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"Database error in '{func.__name__}': {e}", file=sys.stderr)
            raise # Re-raise the exception to propagate it
        except Exception as e:
            print(f"An unexpected error occurred in '{func.__name__}': {e}", file=sys.stderr)
            raise # Re-raise other exceptions
        finally:
            if conn:
                conn.close()
                # print(f"Connection closed for '{func.__name__}'.") # Optional: for debugging
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetches a user by ID using the provided database connection.
    The connection is handled by the with_db_connection decorator.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Example usage:
if __name__ == "__main__":
    # Ensure the database is set up before running queries
    if not os.path.exists(DATABASE_NAME):
        print(f"Database {DATABASE_NAME} not found. Please run setup_database.py first.", file=sys.stderr)
        sys.exit(1)

    print("--- Task 1: Handle Database Connections ---")

    # Fetch user by ID with automatic connection handling
    print("Fetching user with ID 1:")
    user = get_user_by_id(user_id=1)
    print(user) # Expected: (1, 'Alice Smith', 'alice.smith@example.com', 30)

    print("\nFetching user with ID 5:")
    user2 = get_user_by_id(user_id=5)
    print(user2) # Expected: (5, 'Ethan Hunt', 'ethan.h@example.com', 35)

    print("\nFetching non-existent user with ID 99:")
    user_none = get_user_by_id(user_id=99)
    print(user_none) # Expected: None
