import sqlite3
import pandas as pd

def load_log_file(path: str) -> pd.DataFrame:
    con = sqlite3.connect(path)
    df = pd.read_sql_query("""
        SELECT  *
        FROM    messages m
        JOIN    topics t
        ON      m.topic_id = t.id
    """, con)
    return df

def main():
    df = load_log_file("data/manual/state.tlog")
    print(df["message"][21])
    

if __name__ == "__main__":
    main()
