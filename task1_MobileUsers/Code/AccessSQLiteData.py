import pandas as pd
from IPython.display import display
from CSVtoSQLite import disk_engine
import _sqlite3

tables = disk_engine.table_names()
limit = "10"

for table in tables:
    df = pd.read_sql_query("SELECT * FROM " + table + " LIMIT " + limit, disk_engine)
    # TODO: Rowcount
    con = _sqlite3.connect("../Database/MobileUserData.db")
    cur = con.cursor()
    print(cur.rowcount(table))
    print(table, " (Rowcount: ", ")")
    display(df)
