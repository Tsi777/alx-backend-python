import sqlite3
import functools
import os
import sys # For printing to stderr

# Database file name
DATABASE_NAME = 'users.db'

# --- Copy with_db_connection from Task 1 ---
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
        return wrapper
# --- End with_db_connection ---

def transactional(func):
    """
    A decorator that ensures a function running a database operation is wrapped
    inside a transaction. If the function raises an error, rollback;
    otherwise, commit the transaction.
    Assumes the decorated function receives a 'conn' object as its first argument.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs): # 'conn' is expected as the first argument
        try:
            # Ensure autocommit is off for explicit transaction control
            # For sqlite3, setting isolation_level to None disables autocommit
            # and allows explicit begin/commit/rollback.
            original_isolation_level = conn.isolation_level
            conn.isolation_level = None # Disable autocommit

            cursor = conn.cursor()
            cursor.execute("BEGIN TRANSACTION") # Start an explicit transaction

            result = func(conn, *args, **kwargs) # Execute the original function

            conn.commit() # Commit if no error occurred
            print(f"Transaction committed for '{func.__name__}'.")
            return result
        except sqlite3.Error as e:
            if conn:
                conn.rollback() # Rollback on database error
            print(f"Transaction rolled back for '{func.__name__}' due to database error: {e}", file=sys.stderr)
            raise # Re-raise the exception
        except Exception as e:
            if conn:
                conn.rollback() # Rollback on any other error
            print(f"Transaction rolled back for '{func.__name__}' due to unexpected error: {e}", file=sys.stderr)
            raise # Re-raise the exception
        finally:
            # Restore original isolation level if it was changed
            if conn:
                conn.isolation_level = original_isolation_level
            pass # The with_db_connection decorator handles closing the connection

    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Updates a user's email. Decorated with connection handling and transactional logic.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"Attempted to update user ID {user_id} email to {new_email}.")
    # Simulate an error for testing rollback (uncomment to test failure)
    # if user_id == 2:
    #     raise ValueError("Simulated error for rollback test!")

@with_db_connection
def get_user_email(conn, user_id):
    """Helper to get user email for verification."""
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

# Example usage:
if __name__ == "__main__":
    # Ensure the database is set up before running operations
    if not os.path.exists(DATABASE_NAME):
        print(f"Database {DATABASE_NAME} not found. Please run setup_database.py first.", file=sys.stderr)
        sys.exit(1)

    print("--- Task 2: Transaction Management ---")

    # Test successful update
    user_id_to_update = 1
    original_email = get_user_email(user_id=user_id_to_update)
    print(f"Original email for user {user_id_to_update}: {original_email}")

    new_email_success = 'Crawford_Cartwright@hotmail.com'
    try:
        update_user_email(user_id=user_id_to_update, new_email=new_email_success)
        updated_email = get_user_email(user_id=user_id_to_update)
        print(f"New email for user {user_id_to_update} after successful update: {updated_email}")
    except Exception as e:
        print(f"Update failed (expected to succeed): {e}", file=sys.stderr)


    print("\n--- Testing Rollback (simulated error) ---")
    user_id_for_rollback = 2
    original_email_rollback = get_user_email(user_id=user_id_for_rollback)
    print(f"Original email for user {user_id_for_rollback}: {original_email_rollback}")

    @with_db_connection
    @transactional
    def update_user_email_and_fail(conn, user_id, new_email):
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
        print(f"Attempted to update user ID {user_id} email to {new_email}.")
        raise ValueError("Simulated error during update to force rollback!") # Simulate an error

    new_email_fail = 'rollback_test@example.com'
    try:
        update_user_email_and_fail(user_id=user_id_for_rollback, new_email=new_email_fail)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    except Exception as e:
        print(f"Caught unexpected error during rollback test: {e}", file=sys.stderr)

    # Verify email was NOT changed due to rollback
    final_email_rollback = get_user_email(user_id=user_id_for_rollback)
    print(f"Email for user {user_id_for_rollback} after rollback attempt: {final_email_rollback}")
    if original_email_rollback == final_email_rollback:
        print("Rollback successful: Email remained unchanged.")
    else:
        print("Rollback FAILED: Email was unexpectedly changed.", file=sys.stderr)
