import sqlite3
import random
from datetime import datetime, timedelta

# Connect (or create) SQLite database
conn = sqlite3.connect('blinks.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS blinks (
        user_id TEXT,
        blink_count INTEGER,
        timestamp TEXT
    )
''')

# Clear existing data (optional)
cursor.execute('DELETE FROM blinks')

# Generate random data for 3 users over the last 5 days
users = ['test1@example.com', 'test2@example.com', 'test3@example.com']
base_time = datetime.utcnow()

for user in users:
    for i in range(10):  # 10 records each
        blink_count = random.randint(1, 10)
        # Random timestamp within last 5 days
        random_time = base_time - timedelta(days=random.randint(0, 5), hours=random.randint(0,23), minutes=random.randint(0,59))
        timestamp = random_time.isoformat()
        cursor.execute(
            "INSERT INTO blinks (user_id, blink_count, timestamp) VALUES (?, ?, ?)",
            (user, blink_count, timestamp)
        )

conn.commit()
conn.close()
print("Database 'blinks.db' created and filled with sample data.")
