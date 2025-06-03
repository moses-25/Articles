import os
from db.connection import get_connection

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema = f.read()
    cursor.executescript(schema)
    
    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()