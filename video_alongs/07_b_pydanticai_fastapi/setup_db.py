from utils import query_duckdb

query_duckdb("DROP TABLE IF EXISTS movies;")

query_duckdb("""
    CREATE TABLE IF NOT EXISTS movies (
        title STRING,
        year INT,
        genre STRING,
        rating TINYINT       
    );
""")

if __name__ == "__main__":
    print(query_duckdb("DESC;"))