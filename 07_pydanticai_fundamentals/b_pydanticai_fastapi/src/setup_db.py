from utils import query_duckdb

query_duckdb("""--sql
    CREATE TABLE IF NOT EXISTS movies (
             title TEXT,
             year INTEGER,
             genre TEXT,
             rating TINYINT
    );
""")