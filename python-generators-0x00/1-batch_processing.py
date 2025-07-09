# 1-batch_processing.py

import sqlite3

def fetch_users_from_db():
    """
    Fetch users from the user_data table in the database.
    """
    connection = sqlite3.connect('your_database.db')  # Replace with your database
    cursor = connection.cursor()
    
    # Fetch users from the database
    cursor.execute("SELECT id, age FROM user_data")
    users = cursor.fetchall()
    
    connection.close()
    
    return [{'id': user[0], 'age': user[1]} for user in users]  # Convert to list of dictionaries

def stream_users_in_batches(batch_size):
    """
    Generator that yields users in batches of size `batch_size`
    """
    users = fetch_users_from_db()  # Fetch users from the database

    for i in range(0, len(users), batch_size):
        yield users[i:i + batch_size]  # Yield one batch of users

def batch_processing(batch_size):
    """
    Processes each batch and prints users over age 25
    """
    for batch in stream_users_in_batches(batch_size):  # Loop 2
        for user in batch:  # Loop 3
            if user['age'] > 25:
                print(f"User ID: {user['id']}, Age: {user['age']}")

# Example usage
if __name__ == "__main__":
    batch_processing(3)  # Process users in batches of 3
       
