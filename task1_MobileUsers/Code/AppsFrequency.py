from CSVtoSQLite import disk_engine
import pandas as pd


allAppsLabeled = pd.read_sql("SELECT app_id as app, label_id FROM app_labels WHERE label_id IN "
                             "(SELECT label_id as label FROM app_labels WHERE app_id IN "
                             "(SELECT app_id FROM app_events WHERE is_active = 1) and label_id IN "
                             "(SELECT label_id FROM label_categories WHERE category != 'unknown')"
                             " GROUP BY label ORDER BY COUNT(label_id) DESC LIMIT 150)", disk_engine)

app_df = pd.read_sql_query(
        "SELECT DISTINCT app_id FROM app_labels WHERE label_id IN " + str(tuple(set(allAppsLabeled.label_id))),
        disk_engine)
print(app_df)

apps_df = pd.read_sql_query(
        "SELECT app_id as app, event_id as event FROM app_events WHERE is_active = 1",
        disk_engine)
print(apps_df)
appss_df = pd.read_sql_query(
        "SELECT app_id as app, event_id as event FROM app_events WHERE is_active = 1 and app_id IN "
        "(SELECT DISTINCT app_id FROM app_labels WHERE label_id IN " + str(tuple(set(allAppsLabeled.label_id))) + ")",
        disk_engine)
print(appss_df)