import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

from CSVtoSQLite import disk_engine
from PhoneBrandDeviceModel import replaceChineseBrandNames

pd.options.mode.chained_assignment = None  # default='warn'


def initFeatureVector():
    allUsers = pd.read_sql_query("SELECT device_id as device, agegroup FROM gender_age_train LIMIT 2", disk_engine)
    return allUsers


def getDeviceBrands(allUsers):
    phoneBrandDevices = pd.read_sql_query("SELECT device_id, phone_brand FROM phone_brand_device_model", disk_engine)
    phoneBrandDevices = replaceChineseBrandNames(phoneBrandDevices)
    deviceBrandDict = dict(zip(phoneBrandDevices.device_id, phoneBrandDevices.phone_brand))
    allUsers['phoneBrand'] = np.nan
    for index, row in allUsers.iterrows():
        allUsers['phoneBrand'][index] = deviceBrandDict[allUsers['device'][index]]
    return allUsers


def getNumberOfEvents(allUsers):
    eventCount = pd.read_sql(
        "SELECT device_id as device, COUNT(device_id) as eventCount FROM events WHERE device_id IN "
        + str(tuple(allUsers.device.values))
        + " GROUP BY device",
        disk_engine)
    count_dict = dict(zip(eventCount.device, eventCount.eventCount))
    allUsers['numberOfEvents'] = 0
    for index, row in allUsers.iterrows():
        if allUsers['device'][index] in count_dict.keys():
            allUsers['numberOfEvents'][index] = count_dict[allUsers['device'][index]]
    return allUsers


def getInstalledApps(allUsers):
    allAppsLabeled = pd.read_sql("SELECT app_id as app, label_id FROM app_labels ORDER BY app", disk_engine)
    for appCategory in set(allAppsLabeled.label_id):
        allUsers[appCategory] = 0
    appLabelDict = dict(zip(allAppsLabeled.app, allAppsLabeled.label_id))
    events_df = pd.read_sql("SELECT device_id as device, event_id as event "
                            "FROM events " +
                            "WHERE device_id in " + str(tuple(allUsers.device.values)) + " ORDER BY device",
                            disk_engine)
    devices = list(set(events_df.device.values))
    deviceAppsDict = dict.fromkeys(devices)
    for device in devices:
        eventList = events_df.loc[events_df['device'] == device]['event']
        if len(eventList) > 1:
            installedApps = pd.read_sql("SELECT app_id as app FROM app_events WHERE is_installed = 1 AND event_id IN "
                                        + str(tuple(eventList)), disk_engine)
        else:
            installedApps = pd.read_sql("SELECT app_id as app FROM app_events WHERE is_installed = 1 AND event_id == "
                                        + str(list(eventList)[0]), disk_engine)
        for app in installedApps.app:
            allUsers[appLabelDict[app]][allUsers['device'] == device] += 1

    return allUsers


def encodeBrandNames(allUsers):
    brands = allUsers['phoneBrand']
    labelEncoder = LabelEncoder()
    labelEncoder.fit(brands)
    brands_as_int = labelEncoder.transform(brands)
    oneHotEncoder = OneHotEncoder(sparse=False)
    brands_as_int = brands_as_int.reshape(len(brands_as_int), 1)
    brands_encoded = oneHotEncoder.fit_transform(brands_as_int)
    brands_df = pd.DataFrame(columns=labelEncoder.classes_, data=brands_encoded)
    allUsers = allUsers.join(brands_df)
    del allUsers['phoneBrand']

    return allUsers


featureVector = initFeatureVector()
featureVector = getDeviceBrands(featureVector)
featureVector = getNumberOfEvents(featureVector)
featureVector = getInstalledApps(featureVector)
featureVector = encodeBrandNames(featureVector)


# TODO: Varianz kontrollieren, Aufgabe 4 Gender-Age-Group Prediction, Aufgabe 5, Aufgabe 6
