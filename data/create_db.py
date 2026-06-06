import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def run_sql_script(db_path: str, sql_file: str):
    """
    Run an SQL script file to initialize or populate a database.
    """
    with open(sql_file, "r", encoding="utf-8") as f:
        sql_script = f.read()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.executescript(sql_script)
        conn.commit()
        print(f"Executed {sql_file} on {db_path}")
    except sqlite3.Error as e:
        print(f"Error executing {sql_file} on {db_path}: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    # Databases with schema + import scripts (all inside data/)
    dbs = [
        {
            "db_path": os.getenv("EMBDRAG_DATABASE", "data/embdrag.db"),
            "schema": "data/db.sql",
            "import": "data/db_import.sql",
        },
        {
            "db_path": os.getenv("SQLRAG_DATABASE", "data/sqlrag.db"),
            "schema": "data/sqlrag_db.sql",
            "import": "data/sqlrag_import.sql",
        },
    ]

    for db in dbs:
        print(f"Using database path: {db['db_path']}")
        run_sql_script(db["db_path"], db["schema"])   # create schema
        run_sql_script(db["db_path"], db["import"])   # import data
