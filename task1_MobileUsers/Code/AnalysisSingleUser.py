import datetime

import gmaps
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
import random

pd.options.mode.chained_assignment = None  # default='warn'

from CSVtoSQLite import disk_engine

API_KEY = 'AIzaSyB1UnOoMHLj_QhN-ZD-SHjNf1WJVww2LPY'
gmaps.configure(api_key='AIzaSyB1UnOoMHLj_QhN-ZD-SHjNf1WJVww2LPY')

# Eine divce_id herauspicken: 9206538029661406976
events_df = pd.read_sql_query("SELECT COUNT(*) AS number, device_id, longitude AS lon, latitude AS lat "
                              "FROM events "
                              "WHERE longitude > 0 and latitude > 0  and device_id = '9206538029661406976' "
                              "GROUP BY device_id, lon, lat "
                              "ORDER BY device_id", disk_engine
                              )
locations = events_df[['lat', 'lon']]
weights = events_df['number']

# set up parameters
zoom = 10
intensity = 10
radius = 15


def drawHeatMap(location, weight, intensity, radius):
    # setting the data and parameters
    heatmap_layer = gmaps.heatmap_layer(location, weights=weight, dissipating=True)
    heatmap_layer.max_intensity = intensity
    heatmap_layer.point_radius = radius

    # draw the heatmap into a figure
    fig = gmaps.figure()
    fig.add_layer(heatmap_layer)
    return fig


# call the function to draw the heatmap
drawHeatMap(locations, weights, intensity, radius)


def clusterGeoData():
    X = np.array(locations.values)
    # distance in km in which radius points should be in one cluster
    km = 2
    epsilon = km / 6371.008

    # Compute DBSCAN
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(X))
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()
    return labels


clusterLabels = clusterGeoData()


def drawEventsOverTimeGraph(labels):
    # select all events of a single user
    allEvents_df = pd.read_sql(
        "SELECT longitude AS lon, latitude AS lat, timestamp as time "
        "FROM events "
        "WHERE longitude > 0 and latitude > 0  and device_id = '9206538029661406976'"
        "ORDER BY timestamp",
        disk_engine
    )
    # add labels of clustering to every coordinate
    locations_labeled = events_df[['number', 'lat', 'lon']]
    locations_labeled['label'] = labels

    # get the timestamp of the first and last event and calculate the time period between these events
    firstEventTime = allEvents_df.iloc[0, 2]
    lastEventTime = allEvents_df.iloc[len(allEvents_df['time']) - 1, 2]
    firstEventTime = datetime.datetime.strptime(firstEventTime, '%Y-%m-%d %H:%M:%S')
    lastEventTime = datetime.datetime.strptime(lastEventTime, '%Y-%m-%d %H:%M:%S')
    timePeriod = lastEventTime - firstEventTime
    timePeriodInHours = round(timePeriod.total_seconds() / 3600 + 0.5)

    # set up the axis an the headers of the plot
    plt.xticks(np.arange(0, timePeriodInHours + 50, 20))
    plt.xlabel("Time Offset in hours")
    plt.yticks(np.arange(0, len(allEvents_df.index) + 50, 200))
    plt.ylabel("Number of events")
    plt.title("Smartphone Events over time")

    # create a dictionary with: key = coordinate, value = label
    labelDict = {}
    for entry in np.array(locations_labeled[['lat', 'lon', 'label']]):
        cordTuple = (entry[0], entry[1])
        labelDict[cordTuple] = entry[2]

    # number of labels (locations) of the user
    labelCount = len(set(labels))
    # dictionary with different colors for each location
    labelColors = {}
    # lists for correct representation of the plot legend
    scatterList = []
    labelNames = []

    # generate a random color for each label (location) and add to dict/lists above
    i = 0
    while i < labelCount:
        j = 0
        rgb = "#"
        while j < 6:
            rgb += random.choice("0123456789ABCDEF")
            j += 1
        labelColors[i] = rgb
        scatterList.append(Line2D([0], [0], marker='o', color='w', markerfacecolor=rgb, markersize=5))
        labelNames.append("location " + str(i))
        i += 1

    # assign correct label and color to every single event of the user
    allEvents_df['label'] = np.nan
    allEvents_df['color'] = np.nan
    for index, row in allEvents_df.iterrows():
        cordTuple = (row['lat'], row['lon'])
        label = labelDict[cordTuple]
        allEvents_df['label'][index] = label
        allEvents_df['color'][index] = labelColors[label]

    # create a new data frame containing all data needed to plot the graph (x=time offset in hours since first event;
    # y=number of event; c=color of the event, based on label)
    plotData = pd.DataFrame(columns=['x', 'y', 'c'])
    xList = []
    yList = []
    cList = []

    for index, row in allEvents_df.iterrows():
        timeStamp = datetime.datetime.strptime(row['time'], '%Y-%m-%d %H:%M:%S')
        xList.append((timeStamp - firstEventTime).total_seconds() / 3600)
        yList.append(index)
        color = row['color']
        cList.append(color)
    plotData['x'] = xList
    plotData['y'] = yList
    plotData['c'] = cList

    # plot line
    plt.plot(plotData[['x']], plotData[['y']], '-', color="#000000", linewidth=0.5, zorder=1)
    scatterList.append(Line2D([0, 0], [1, 0], linestyle='-', color='#000000'))
    labelNames.append("No location info")

    # plot points
    for index, row in plotData.iterrows():
        plt.scatter(row['x'], row['y'], s=2, marker='o', c=row['c'], zorder=2)

    plt.legend(scatterList, labelNames)
    plt.show()


drawEventsOverTimeGraph(clusterLabels)
