import folium

class NYMap(object):
    
    def __init__(self):
        self.ny = folium.Map(location=[40.693943, -73.985880], default_zoom_start=15)
        
    def feature_by_zip(self, df_zip, feature):
        
        self.ny.choropleth(geo_data="../../data/nyc-zip-codes.geojson",
            data=df_zip,
            columns=['zip', feature],
            key_on='feature.properties.postalCode',
            fill_color='BuPu', fill_opacity=0.7, line_opacity=0.2,
            legend_name=f'Total {feature}')    
        return self.ny

""" Add Marker to Map
    folium.Marker(
        location=[lat, lng],
        popup=f'total: {total}\npositive: {positive}',
        tooltip = k
    ).add_to(ny)
"""