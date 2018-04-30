from CSVtoSQLite import disk_engine
import pandas as pd

# Read device_id by events.csv whitout 0 Items
# TODO
# Ausgabe mit doppelten device_id, da unterschiedliche lon & lat.
# Eine divce_id herauspicken und alle events hierfür ausgeben
events_df = pd.read_sql_query("SELECT COUNT(*) AS number,device_id, longitude AS lon, latitude AS lat "
                              "FROM events "
                              "WHERE longitude > 0 and latitude > 0 "
                              "GROUP BY device_id, lon, lat "
                              "ORDER BY device_id", disk_engine)

print(events_df)
