from pathlib import Path
import duckdb

DATA_PATH = Path(__file__).parent / "data"


def query_duckdb(sql_code: str, parameters=None):
    with duckdb.connect(DATA_PATH / "movies.duckdb") as conn:
        # execute sql code
        cursor = conn.execute(sql_code, parameters=parameters)

        # return df if starting with ...
        if (
            sql_code.strip()
            .lower()
            .startswith(("select", "from", "desc", "pragma", "with"))
        ):
            return cursor.df()
