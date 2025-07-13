import time
import sqlite3
import functools

# In-memory cache
query_cache = {}

# Decorator to manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("example.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query from kwargs or args
        query = kwargs.get("query")
        if query in query_cache:
            print("🔁 Returning cached result.")
            return query_cache[query]

        # Run function and cache result
        result = func(*args, **kwargs)
        query_cache[query] = result
        print("✅ Query executed and cached.")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# ---- Execution ----

# First call caches the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call returns cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

print(users_again)
