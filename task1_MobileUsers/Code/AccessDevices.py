from CSVtoSQLite import disk_engine
import pandas as pd

genderAgeTrain_df = pd.read_sql_query("SELECT device_id, agegroup FROM gender_age_train", disk_engine)


def countDistinctDevices(genderAgeTrain):
    # Read all distinct devices of gender_age_train
    print("Distinct device_id in gender_age_train.csv:", len(set(genderAgeTrain['device_id'])))

    # Read all distinct devices of events
    events_Devices = pd.read_sql_query("SELECT DISTINCT device_id FROM events", disk_engine)
    print("Distinct device_id in events.csv:", len(events_Devices.index))

    # Combine dataFrames above and count distinct devices
    combinedList = list(events_Devices['device_id'])
    combinedList.extend(genderAgeTrain['device_id'])
    combinedSet = set(combinedList)

    print("Number of different device_id in gender_age_train and events:", len(combinedSet))


countDistinctDevices(genderAgeTrain_df)
