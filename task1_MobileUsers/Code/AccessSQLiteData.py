import pandas as pd
from IPython.display import display
from CSVtoSQLite import disk_engine

tables = disk_engine.table_names()
limit = "10"

for table in tables:
    df = pd.read_sql_query("SELECT * FROM " + table + " LIMIT " + limit, disk_engine)
    countDf = pd.read_sql_query("SELECT COUNT(*) FROM " + table, disk_engine)
    print(table, " (Rowcount:", countDf['COUNT(*)'][0], ")")
    display(df)

