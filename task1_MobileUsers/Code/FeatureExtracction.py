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
#       > ältere Nutzer nutzen Smartphone im Schnitt häufiger (siehe plotEventFrequency)

# Merkmals Vektoren:
# device_id | hersteller | häufigkeit der Nutzung | installierte Apps (| aktive Apps)

from CSVtoSQLite import disk_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def labelAppsPerEvent():
    events_df = pd.read_sql("SELECT device_id as device, event_id as event "
                            "FROM events "
                            "WHERE device_id = '9206538029661406976'",
                            disk_engine)
    # get all installed Apps during all events of the device
    eventIDs = tuple(events_df.event.values)
    apps = pd.read_sql("SELECT DISTINCT app_id as app FROM app_events WHERE event_id in " + str(eventIDs), disk_engine)


def labelAllApps():
    allAppsLabeled = pd.read_sql("SELECT app_id as app, label_id FROM app_labels ORDER BY app", disk_engine)
    appDict = {}
    for app in set(allAppsLabeled['app']):
        appDict[app] = list(allAppsLabeled.loc[allAppsLabeled['app'] == app]['label_id'])

    return appDict


def plotEventFrequency():
    numberOfEvents = pd.read_sql(
        "SELECT device_ID as device, agegroup FROM gender_age_train", disk_engine)
    numberOfEvents['eventCount'] = np.zeros(len(numberOfEvents))
    deviceIds = tuple(numberOfEvents.device.values)
    eventCount = pd.read_sql(
        "SELECT device_id as device, COUNT(device_id) as eventCount FROM events WHERE device_id IN "
        + str(deviceIds)
        + " GROUP BY device",
        disk_engine)
    count_dict = dict(zip(eventCount.device, eventCount.eventCount))

    y = []
    x = set(list(numberOfEvents.agegroup.values))
    plt.xticks(np.arange(12), x, rotation=90)
    plt.yticks(np.arange(0, 220, 20))

    for group in x:
        devices = numberOfEvents.loc[numberOfEvents['agegroup'] == group].device.values
        frequency = 0
        count = 0
        for device in devices:
            if device in count_dict.keys():
                frequency += count_dict[device]
                count += 1
        frequency = frequency / count
        y.append(frequency)

    plt.bar(np.arange(12), y, 0.35)
    plt.grid(True)
    plt.show()

plotEventFrequency()
