import folium
import requests
import pandas as pd
import json

# Load Maryland counties GeoJSON
geojson_url = 'https://raw.githubusercontent.com/frankrowe/maryland-geojson/master/md-counties.geojson'
try:
    geo_data = requests.get(geojson_url).json()
except:
    # Fallback if URL fails (minimal for testing)
    geo_data = {"type": "FeatureCollection", "features": []}
    print("Using fallback GeoJSON.")

# Your 5 regions (exact counties)
regions = {
    1: {"name": "Baltimore City", "counties": ["Baltimore City"], "color": "red"},
    2: {"name": "Central (Montgomery, Howard, etc.)", "counties": ["Montgomery", "Howard", "Carroll", "Baltimore", "Harford", "Cecil"], "color": "orange"},
    3: {"name": "Eastern Shore (Kent, Queen Anne's, etc.)", "counties": ["Kent", "Queen Anne's", "Caroline", "Talbot", "Dorchester", "Wicomico", "Somerset", "Worcester"], "color": "blue"},
    4: {"name": "Southern (Anne Arundel, Prince George's, etc.)", "counties": ["Anne Arundel", "Prince George's", "Charles", "St. Mary's", "Calvert"], "color": "pink"},
    5: {"name": "Western (Frederick, Washington, etc.)", "counties": ["Frederick", "Washington", "Allegany", "Garrett"], "color": "green"}
}

# County name mapping (fix for exact matches, e.g., "Prince George's")
county_map = {"Prince George's": "Prince George's", "Queen Anne's": "Queen Anne's", "St. Mary's": "St. Mary's"}

# Full grantees (FY23-FY25 from before + FY26 placeholders)
grantees = {
    1: [  # Baltimore City - Full FY23-25 data (abbrev for space; paste full from earlier)
        {'FY': '25', 'Org': 'Civic Works', 'Amount': '$261,423', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Baltimore City'},
        # ... (add all 30+ from your Region 1 list)
        {'FY': '26', 'Org': 'TBD - Applications Open', 'Amount': 'Up to $25M Total Program', 'Project': 'Solar & Efficiency Upgrades', 'Areas': 'Baltimore City'},
    ],
    2: [  # Central - Full data
        {'FY': '25', 'Org': 'Building Change, Inc.', 'Amount': '$951,872', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Prince George’s County'},
        # ... (add all from Region 2)
        {'FY': '26', 'Org': 'TBD', 'Amount': 'Pending Awards', 'Project': 'Equity Upgrades', 'Areas': 'Central Region'},
    ],
    3: [  # Eastern
        {'FY': '25', 'Org': 'Choptank Electric Cooperative, Inc.', 'Amount': '$340,757', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Eastern Region'},
        # ... (full list)
        {'FY': '26', 'Org': 'TBD', 'Amount': 'Pending', 'Project': 'Solar Access', 'Areas': 'Eastern Region'},
    ],
    4: [  # Southern
        {'FY': '25', 'Org': 'Arundel Community Development Services, Inc.', 'Amount': '$80,000', 'Project': 'Limited Upgrades', 'Areas': 'Anne Arundel County'},
        # ... (full list)
        {'FY': '26', 'Org': 'TBD', 'Amount': 'Pending', 'Project': 'Efficiency & Solar', 'Areas': 'Southern Region'},
    ],
    5: [  # Western
        {'FY': '25', 'Org': 'Frederick County Government', 'Amount': '$523,998', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Frederick County'},
        # ... (full list)
        {'FY': '26', 'Org': 'TBD', 'Amount': 'Pending', 'Project': 'Upgrades', 'Areas': 'Western Region'},
    ]
}

# Function for popup table
def get_popup(region_id):
    df = pd.DataFrame(grantees.get(region_id, []))
    if df.empty:
        return '<h4>No grantees for Region {}</h4>'.format(region_id)
    html = df.to_html(index=False, escape=False, classes='table table-striped')
    return '<h4>Grantees for Region {}: {}</h4>{}'.format(region_id, regions[region_id]["name"], html)

# Create map
m = folium.Map(location=[39.0458, -76.6413], zoom_start=7, tiles='OpenStreetMap')

# Add region layers (merged counties for shading)
region_features = []
for rid, info in regions.items():
    # Find and merge county features
    region_geom = {"type": "MultiPolygon", "coordinates": []}
    region_props = {"name": info["name"], "region": rid}
    for county in info["counties"]:
        mapped_name = county_map.get(county, county)
        for f in geo_data['features']:
            if f['properties']['NAME'] == mapped_name:
                region_geom["coordinates"].append(f['geometry']['coordinates'])
                break
    if region_geom["coordinates"]:
        region_features.append({
            "type": "Feature",
            "properties": region_props,
            "geometry": region_geom
        })

# Add merged region GeoJSON
folium.GeoJson(
    {"type": "FeatureCollection", "features": region_features},
    style_function=lambda f: {
        'fillColor': f['properties']['region_color'],
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.6
    },
    popup=folium.Popup(max_width=600),
    tooltip=folium.GeoJsonTooltip(fields=['name']),
    popup=folium.GeoJsonPopup(fields=['name'])
).add_to(m)

# Add counties for detail (lighter opacity)
for f in geo_data['features']:
    county = f['properties']['NAME']
    rid = next((r for r, info in regions.items() if county in info["counties"]), 0)
    if rid:
        f['properties']['region'] = rid
        f['properties']['region_name'] = regions[rid]['name']
        folium.GeoJson(
            f,
            style_function=lambda x: {'fillOpacity': 0.2, 'color': 'white', 'weight': 0.5},
            tooltip=folium.GeoJsonTooltip(fields=['NAME']),
            popup=folium.Popup(get_popup(rid), max_width=600)
        ).add_to(m)

# Legend
legend_html = '''
<div style="position: fixed; 
     bottom: 50px; right: 50px; width: 150px; height: 120px; 
     background-color: white; border:2px solid grey; z-index:9999; 
     font-size:14px; padding: 10px">
<h4>Regions</h4>
<i style="background:red; width:18px; height:18px; display:inline-block;"></i> Region 1<br>
<i style="background:orange; width:18px; height:18px; display:inline-block;"></i> Region 2<br>
<i style="background:blue; width:18px; height:18px; display:inline-block;"></i> Region 3<br>
<i style="background:pink; width:18px; height:18px; display:inline-block;"></i> Region 4<br>
<i style="background:green; width:18px; height:18px; display:inline-block;"></i> Region 5
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Save
m.save('maryland_regions_map.html')
print('Map saved to maryland_regions_map.html')


