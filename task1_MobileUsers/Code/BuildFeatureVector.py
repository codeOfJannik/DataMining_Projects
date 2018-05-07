import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from IPython.display import display

from CSVtoSQLite import disk_engine

from PhoneBrandDeviceModel import replaceChineseBrandNames

pd.options.mode.chained_assignment = None  # default='warn'


def initFeatureVector():
    allUsers = pd.read_sql_query("SELECT device_id as device, agegroup"
                                 " FROM gender_age_train"
                                 " WHERE device IN (SELECT DISTINCT device_id FROM events) LIMIT 15", disk_engine)
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
    allAppsLabeled = pd.read_sql("SELECT app_id as app, label_id FROM app_labels WHERE label_id IN "
                                 "(SELECT label_id as label FROM app_labels WHERE app_id IN "
                                 "(SELECT app_id FROM app_events WHERE is_active = 1) and label_id IN "
                                 "(SELECT label_id FROM label_categories WHERE category != 'unknown')"
                                 " GROUP BY label ORDER BY COUNT(label_id) DESC LIMIT 2)", disk_engine)

    for appCategory in set(allAppsLabeled.label_id):
        allUsers[appCategory] = 0
    appLabelDict = dict(zip(allAppsLabeled.app, allAppsLabeled.label_id))

    events_df = pd.read_sql("SELECT device_id as device, event_id as event "
                            "FROM events " +
                            "WHERE device_id in " + str(tuple(allUsers.device.values)) + " ORDER BY device",
                            disk_engine)
    devices = list(set(events_df.device.values))
    app_df = pd.read_sql_query(
        "SELECT app_id as app, event_id as event FROM app_events WHERE is_active = 1 and app_id IN "
        "(SELECT DISTINCT app_id FROM app_labels WHERE label_id IN " + str(tuple(set(allAppsLabeled.label_id))) + ")",
        disk_engine)

    for device in devices:
        eventList = events_df.loc[events_df['device'] == device]['event']
        installedApps = app_df.loc[app_df['event'].isin(eventList)]['app']
        for app in installedApps.values:
            allUsers[appLabelDict[app]][allUsers['device'] == device] += 1

    return allUsers


def getDeviceCountForAppcat(appCategory):
    category = pd.read_sql_query("SELECT device_id as device, COUNT(device_id) as '" + str(appCategory) +
                                 "' FROM device_app_events WHERE label_id = " + str(appCategory) +
                                 " GROUP BY device_id", disk_engine)
    return category


def getActiveApps(allUsers):
    allUsers = allUsers.set_index('device')
    allAppsLabeled = pd.read_sql("SELECT app_id as app, label_id FROM app_labels WHERE label_id IN "
                                 "(SELECT label_id as label FROM app_labels WHERE app_id IN "
                                 "(SELECT app_id FROM app_events WHERE is_active = 1) and label_id IN "
                                 "(SELECT label_id FROM label_categories WHERE category != 'unknown')"
                                 " GROUP BY label ORDER BY COUNT(label_id) DESC LIMIT 2)", disk_engine)
    count = 1
    for appCategory in set(allAppsLabeled.label_id):
        print(count, "/", len(set(allAppsLabeled.label_id)))
        appcat_df = getDeviceCountForAppcat(appCategory)
        allUsers = allUsers.join(appcat_df.set_index('device'))
        count += 1
    return allUsers.fillna(0)


def encodeBrandNames(allUsers):
    brands = allUsers['phoneBrand']
    allUsers = allUsers.reset_index()
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
print("Init finished")
featureVector = getDeviceBrands(featureVector)
print("getDeviceBrands finished")
featureVector = getNumberOfEvents(featureVector)
print("getNumEvents finished")
featureVector = getActiveApps(featureVector)
print("getApps finished")
featureVector = encodeBrandNames(featureVector)
print("encode finished")
print(featureVector)

# TODO: Varianz kontrollieren, Aufgabe 4 Gender-Age-Group Prediction, Aufgabe 5, Aufgabe 6
