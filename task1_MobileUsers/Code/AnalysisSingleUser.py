from CSVtoSQLite import disk_engine
import pandas as pd
import gmaps

API_KEY = 'AIzaSyB1UnOoMHLj_QhN-ZD-SHjNf1WJVww2LPY'
gmaps.configure(api_key='AIzaSyB1UnOoMHLj_QhN-ZD-SHjNf1WJVww2LPY')

# Eine divce_id herauspicken: 9221586026451102237
events_df = pd.read_sql_query("SELECT COUNT(*) AS number, device_id, longitude AS lon, latitude AS lat "
                              "FROM events "
                              "WHERE longitude > 0 and latitude > 0 and device_id = '9221586026451102237' "
                              "GROUP BY device_id, lon, lat "
                              "ORDER BY device_id", disk_engine
                              )

location = events_df[['lat', 'lon']]
weights = events_df['number']

def drawHeatMap(location, weights, zoom, intensity, radius):
    # setting the data and parameters
    heatmap_layer = gmaps.heatmap_layer(location, weights=weights, dissipating=True)
    heatmap_layer.max_intensity = intensity
    heatmap_layer.point_radius = radius

    # draw the heatmap into a figure
    fig = gmaps.figure()
    fig.add_layer(heatmap_layer)
    return fig


# set up parameters
zoom = 10
intensity = 10
radius = 15

# call the function to draw the heatmap
drawHeatMap(location, weights, zoom, intensity, radius)
