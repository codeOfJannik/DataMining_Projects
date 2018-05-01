from CSVtoSQLite import disk_engine
import pandas as pd
import os
import googlemaps
import gmaps

API_KEY = 'AIzaSyB1UnOoMHLj_QhN-ZD-SHjNf1WJVww2LPY'
gm = googlemaps.Client(key='AIzaSyB1UnOoMHLj_QhN-ZD-SHjNf1WJVww2LPY')
gmaps.configure(api_key='AIzaSyB1UnOoMHLj_QhN-ZD-SHjNf1WJVww2LPY')

# Read device_id by events.csv whitout 0 Items
# TODO
# Ausgabe mit doppelten device_id, da unterschiedliche lon & lat.
# Eine divce_id herauspicken und alle events hierfür ausgeben
events_df = pd.read_sql_query("SELECT COUNT(*) AS number,device_id, longitude AS lon, latitude AS lat "
                              "FROM events "
                              "WHERE longitude > 0 and latitude > 0 "
                              "GROUP BY device_id, lon, lat "
                              "ORDER BY device_id", disk_engine)

location = events_df[['lat', 'lon']]

# do geocode for the city
geocode_result = gm.geocode('Japan')[0]

# get the center of the city
center_lat = geocode_result['geometry']['location']['lat']
center_lon = geocode_result['geometry']['location']['lng']
print('center=', center_lat, center_lon)


def drawHeatMap(location, zoom, intensity, radius):
    # setting the data and parameters
    heatmap_layer = gmaps.heatmap_layer(location, dissipating = True)
    heatmap_layer.max_intensity = intensity
    heatmap_layer.point_radius = radius
    # draw the heatmap into a figure
    fig = gmaps.figure()
    fig = gmaps.figure(center = [center_lat,center_lon], zoom_level=zoom)
    fig.add_layer(heatmap_layer)
    return fig


# set up parameters
zoom = 10
intensity = 5
radius = 15

# call the function to draw the heatmap
drawHeatMap(location, zoom, intensity, radius)
