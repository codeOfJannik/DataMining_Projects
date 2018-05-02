import gmaps
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

from CSVtoSQLite import disk_engine

API_KEY = 'AIzaSyB1UnOoMHLj_QhN-ZD-SHjNf1WJVww2LPY'
gmaps.configure(api_key='AIzaSyB1UnOoMHLj_QhN-ZD-SHjNf1WJVww2LPY')

# Eine divce_id herauspicken: 9221586026451102237
events_df = pd.read_sql_query("SELECT COUNT(*) AS number, device_id, longitude AS lon, latitude AS lat "
                              "FROM events "
                              "WHERE longitude > 0 and latitude > 0  and device_id = '9206538029661406976' "
                              "GROUP BY device_id, lon, lat "
                              "ORDER BY device_id", disk_engine
                              )
locations = events_df[['lat', 'lon']]
weights = events_df['number']
print(locations)

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
    km = 1
    epsilon = km / 6371.008

    # Compute DBSCAN
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(X))
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    print(labels)

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


clusterGeoData()
