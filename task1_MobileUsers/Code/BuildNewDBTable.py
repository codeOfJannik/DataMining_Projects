from CSVtoSQLite import disk_engine
import pandas as pd

initTable = pd.read_sql_query("SELECT event_id, app_id FROM app_events WHERE is_active = 1 and app_id IN "
                              "(SELECT app_id FROM app_labels WHERE label_id IN "
                              "(SELECT label_id as label FROM app_labels WHERE app_id IN "
                              "(SELECT app_id FROM app_events WHERE is_active = 1) and label_id IN "
                              "(SELECT label_id FROM label_categories WHERE category != 'unknown')"
                              " GROUP BY label ORDER BY COUNT(label_id) DESC LIMIT 150))", disk_engine)
deviceIdsByAppID = pd.read_sql_query("SELECT device_id, event_id FROM events WHERE event_id IN "
                                     "(SELECT event_id FROM app_events WHERE is_active = 1)", disk_engine)
newTable = pd.merge(initTable, deviceIdsByAppID, 'inner', 'event_id')
appLabelsByAppId = pd.read_sql_query("SELECT app_id, label_id FROM app_labels WHERE app_id IN "
                                     "(SELECT app_id FROM app_events WHERE is_active = 1)", disk_engine)
newTable2 = pd.merge(newTable, appLabelsByAppId, 'inner', 'app_id')
newTable2.to_sql(name="device_app_events", con=disk_engine, if_exists='replace', chunksize=20000)

allAppsLabeled = pd.read_sql("SELECT app_id as app, label_id FROM app_labels WHERE label_id IN "
                             "(SELECT label_id as label FROM app_labels WHERE app_id IN "
                             "(SELECT app_id FROM app_events WHERE is_active = 1) and label_id IN "
                             "(SELECT label_id FROM label_categories WHERE category != 'unknown')"
                             " GROUP BY label ORDER BY COUNT(label_id) DESC LIMIT 150)", disk_engine)


def getDeviceCountForAppcat(appCategory):
    category = pd.read_sql_query("SELECT device_id, COUNT(device_id) as " + appCategory +
                                 " FROM device_app_events WHERE label_id = " + appCategory +
                                 " GROUP BY device_id", disk_engine)
    category.set_index('device_id', inplace=True)
    return category
