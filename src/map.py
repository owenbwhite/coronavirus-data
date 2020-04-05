class NYMap(object):
    
    def __init__(self):
        self.ny = folium.Map(location=[40.693943, -73.985880], default_zoom_start=15)
        
    def tests_by_zip(self):
        self.ny.choropleth(geo_data="../../data/nyc-zip-codes.geojson",
            data=df,
            columns=['zip', 'positives'],
            key_on='feature.properties.postalCode',
            fill_color='BuPu', fill_opacity=0.7, line_opacity=0.2,
            legend_name='Total Tests')    
        return self.ny
ny = NYMap()
ny.tests_by_zip()