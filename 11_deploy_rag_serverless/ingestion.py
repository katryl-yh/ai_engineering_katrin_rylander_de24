from backend.constants import VECTOR_DATABASE_PATH, DATA_PATH
from backend.data_models import Article
import lancedb
from pathlib import Path
import time

def setup_vector_db(path):
    # creates the folder knowledge_base if it does not exist
    Path(path).mkdir(exist_ok=True)
    vector_db = lancedb.connect(uri=path)
    vector_db.create_table("articles", schema=Article, exist_ok=True)

    return vector_db

def ingest_docs_to_vector_db(table):
    for filepath in DATA_PATH.glob("*.txt"):
        # try common text encodings, otherwise decode bytes with replacement
        content = None
        for enc in ("utf-8", "utf-8-sig", "cp1252"):
            try:
                with open(filepath, "r", encoding=enc) as file:
                    content = file.read()
                break
            except UnicodeDecodeError:
                print(enc)
                continue

        if content is None:
            # last resort: read raw bytes and decode with replacement to avoid errors
            with open(filepath, "rb") as f:
                content = f.read().decode("utf-8", errors="replace")

        doc_id = filepath.stem
        table.delete(f"doc_id = '{doc_id}'")  # avoid duplicates

        table.add(
            [
                {
                    "doc_id": doc_id,
                    "filepath": str(filepath),
                    "filename": filepath.stem,
                    "content": content,
                }
            ]
        )

        print(table.to_pandas().shape)
        print(table.to_pandas()["filename"])
        time.sleep(20)

if __name__=="__main__":
    vector_db = setup_vector_db(VECTOR_DATABASE_PATH)

    ingest_docs_to_vector_db(vector_db["articles"]) # check possiblity to use dlt to ingest docs to lancedb