import sqlite3


def init_db():
    """
    Connects to a database file (or creates it if it doesn't exist)
    and sets up our transactions table.
    """
    # Connects to a file called 'fintech_vault.db'
    conn = sqlite3.connect('fintech_vault.db')
    cursor = conn.cursor()

    # Create a table for transactions if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Commit changes and close the connection securely
    conn.commit()
    conn.close()
    print("Backend Database Initialized Successfully!")


# Run this script directly to create the database file
if __name__ == "__main__":
    init_db()
