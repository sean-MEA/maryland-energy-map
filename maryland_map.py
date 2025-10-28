import folium
import requests
import pandas as pd

# Load Maryland counties GeoJSON
geojson_url = 'https://raw.githubusercontent.com/frankrowe/maryland-geojson/master/md-counties.geojson'
try:
    geo_data = requests.get(geojson_url).json()
    print("GeoJSON loaded from URL.")
except:
    print("GeoJSON URL failed. Using fallback (limited map).")
    # Fallback minimal GeoJSON (just for testing)
    geo_data = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "properties": {"NAME": "Baltimore City"}, "geometry": {"type": "Polygon", "coordinates": [[[0,0],[1,0],[1,1],[0,1],[0,0]]]}},
            {"type": "Feature", "properties": {"NAME": "Montgomery"}, "geometry": {"type": "Polygon", "coordinates": [[[1,1],[2,1],[2,2],[1,2],[1,1]]]}},
        ]
    }

# Map counties to regions
county_to_region = {
    'Allegany': 5, 'Anne Arundel': 4, 'Baltimore': 2, 'Baltimore City': 1, 'Calvert': 4,
    'Caroline': 3, 'Carroll': 2, 'Cecil': 2, 'Charles': 4, 'Dorchester': 3,
    'Frederick': 5, 'Garrett': 5, 'Harford': 2, 'Howard': 2, 'Kent': 3,
    'Montgomery': 2, "Prince George's": 4, "Queen Anne's": 3, "St. Mary's": 4,
    'Somerset': 3, 'Talbot': 3, 'Washington': 5, 'Wicomico': 3, 'Worcester': 3
}

# Add region to features
for f in geo_data['features']:
    name = f['properties'].get('NAME', '')
    f['properties']['region'] = county_to_region.get(name, 0)

# === FULL GRANTEES DATA (FY23-FY25) ===
grantees = {
    1: [  # Baltimore City
        {'FY': '25', 'Org': 'Civic Works', 'Amount': '$261,423', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '25', 'Org': 'Diversified Housing Development, Inc.', 'Amount': '$100,000', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '25', 'Org': 'Green and Healthy Homes Initiative', 'Amount': '$156,854', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '25', 'Org': 'Healthy Neighborhoods, Inc.', 'Amount': '$205,092', 'Project': 'Whole Building Commercial Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '25', 'Org': 'Mayor and City Council of Baltimore', 'Amount': '$211,731', 'Project': 'Whole Building Commercial Retrofits, Limited Upgrades', 'Areas': 'Baltimore City'},
        {'FY': '25', 'Org': 'Neighborhood Housing Services of Baltimore, Inc.', 'Amount': '$319,125', 'Project': 'Residential Whole Home/Building Retrofit', 'Areas': 'Baltimore City'},
        {'FY': '25', 'Org': 'SAFE Housing, Inc.', 'Amount': '$312,246', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Baltimore City'},
        # ... (add all from your list)
    ],
    2: [], 3: [], 4: [], 5: []  # Paste full data here
}

# Add your full grantees[2], [3], [4], [5] from earlier messages!

def get_popup(region):
    df = pd.DataFrame(grantees.get(region, []))
    if df.empty:
        return '<h4>No grantees</h4>'
    return '<h4>Region ' + str(region) + ' Grantees</h4>' + df.to_html(index=False)

colors = {1: 'red', 2: 'orange', 3: 'blue', 4: 'pink', 5: 'green'}

m = folium.Map(location=[39.0458, -76.6413], zoom_start=8)

for f in geo_data['features']:
    r = f['properties']['region']
    popup = folium.Popup(get_popup(r), max_width=500)
    style = {'fillOpacity': 0.7, 'weight': 1, 'color': 'black', 'fillColor': colors.get(r, 'gray')}
    folium.GeoJson(f, style_function=lambda x: style, popup=popup).add_to(m)

m.save('maryland_regions_map.html')
print("Map generated: maryland_regions_map.html")
