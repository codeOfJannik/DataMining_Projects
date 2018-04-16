import pandas as pd
from sqlalchemy import create_engine
import os.path

# generate SQLite Database
disk_engine = create_engine('sqlite:///../Database/MobileUserData.db')


# Function to read CSV-files into pandas dataFrames and write into a SQLite Database
def fromCSVtoSQLite(db_Engine):

    resources_path = os.path.join(os.path.dirname(__file__), "../../Resources/GenderAgePrediction/")
    fileNames = ["events.csv",
                 "app_events.csv",
                 "app_labels.csv",
                 "label_categories.csv",
                 "phone_brand_device_model.csv",
                 "gender_age_train.csv",
                 "gender_age_test.csv"
                 ]

    for name in fileNames:
        file = os.path.join(resources_path, name)
        tableName = name[:-4]
        chunkSize = 20000
        index_start = 1
        if tableName in db_Engine.table_names():
            continue
        for df in pd.read_csv(file, chunksize=chunkSize, sep=','):
            df.index += index_start
            df.to_sql(tableName, db_Engine, if_exists='append')
            index_start = df.index[-1] + 1

fromCSVtoSQLite(disk_engine)


