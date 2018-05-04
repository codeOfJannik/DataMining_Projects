# Feature Extraction

# Welche Merkmale können zur Gender-Age-Prediction benutzt werden?
#   - Installierte Apps je nach Kategorie können (ggf. auch häufig aktive Apps):
#       > Aussagen über Geschlecht liefern (z.B. Car -> Männer, Beauty -> Frauen)
#       > Aussagen über Alter liefern
#           (z.B Sport Apps/Social Media eher jüngere Leute, Baby Apps eher Leute mittleren Alters)
#   - Hersteller des Smartphones
#       > beliebte Marken bei Frauen/Männern
#       > beliebte Marken bei unterschiedlichen Altersgruppen
#   - Häufigkeit der Smartphone Nutzung
#       > junge Nutzer nutzen Smartphone ggf. häufiger ??
#       > junge Nutzer nutzen Smartphone eher mal nachts ??

# Merkmals Vektoren:
# device_id | hersteller | häufigkeit der Nutzung | häufigkeit Nutzung zwischen 23 und 5 uhr | installierte Apps


from CSVtoSQLite import disk_engine
import pandas as pd
import numpy as np

events_df = pd.read_sql("SELECT device_id as device, event_id as event "
                        "FROM events "
                        "WHERE device_id = '9206538029661406976'",
                        disk_engine)
# get all installed Apps during all events of the device
eventIDs = tuple(events_df.event.values)
apps = pd.read_sql("SELECT DISTINCT app_id as app FROM app_events WHERE event_id in " + str(eventIDs), disk_engine)

# get app_labels for each installed app and store them into a dictionary
appLabels = {}
apps['app_Labels'] = np.nan
for index, row in apps.iterrows():
    app_labels = pd.read_sql("SELECT label_id as appLabel FROM app_labels WHERE app_id = "
                             + str(apps['app'][index]), disk_engine)
    appLabels[apps['app'][index]] = set(app_labels['appLabel'].values)
