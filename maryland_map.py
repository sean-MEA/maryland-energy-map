import folium
import requests
import pandas as pd

# Load Maryland counties GeoJSON
geojson_url = 'https://raw.githubusercontent.com/frankrowe/maryland-geojson/master/md-counties.geojson'
try:
    geo_data = requests.get(geojson_url).json()
    print("GeoJSON loaded from URL.")
except Exception as e:
    print(f"GeoJSON URL failed: {e}. Using fallback.")
    # Fallback minimal map
    geo_data = {"type": "FeatureCollection", "features": []}

# === 5 REGIONS WITH COUNTIES ===
regions = {
    1: {"name": "Baltimore City", "counties": ["Baltimore City"], "color": "red"},
    2: {"name": "Central Region", "counties": ["Montgomery", "Howard", "Carroll", "Baltimore", "Harford", "Cecil"], "color": "orange"},
    3: {"name": "Eastern Shore", "counties": ["Kent", "Queen Anne's", "Caroline", "Talbot", "Dorchester", "Wicomico", "Somerset", "Worcester"], "color": "blue"},
    4: {"name": "Southern Region", "counties": ["Anne Arundel", "Prince George's", "Charles", "St. Mary's", "Calvert"], "color": "pink"},
    5: {"name": "Western Region", "counties": ["Frederick", "Washington", "Allegany", "Garrett"], "color": "green"}
}

# Fix county names to match GeoJSON
county_name_fix = {
    "Queen Anne's": "Queen Anne's",
    "Prince George's": "Prince George's",
    "St. Mary's": "St. Mary's"
}

# === FULL GRANTEES DATA (FY23–FY25 + FY26 placeholder) ===
# Replace with your full list — this is a starter
grantees = {
    1: [
        {'FY': '25', 'Org': 'Civic Works', 'Amount': '$261,423', 'Project': 'Residential Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '25', 'Org': 'Green & Healthy Homes', 'Amount': '$156,854', 'Project': 'Whole Home Upgrades', 'Areas': 'Baltimore City'},
        # ... add all Region 1
        {'FY': '26', 'Org': 'Applications Open', 'Amount': '$25M Total', 'Project': 'Solar & Efficiency', 'Areas': 'Baltimore City'}
    ],
    2: [
        {'FY': '25', 'Org': 'Building Change, Inc.', 'Amount': '$951,872', 'Project': 'Retrofits', 'Areas': 'Central Region'},
        # ... add all
        {'FY': '26', 'Org': 'TBD', 'Amount': 'Pending', 'Project': 'Equity Upgrades', 'Areas': 'Central Region'}
    ],
    3: [
        {'FY': '25', 'Org': 'Choptank Electric', 'Amount': '$340,757', 'Project': 'Retrofits', 'Areas': 'Eastern Region'},
        {'FY': '26', 'Org': 'TBD', 'Amount': 'Pending', 'Project': 'Solar Access', 'Areas': 'Eastern Region'}
    ],
    4: [
        {'FY': '25', 'Org': 'Arundel CDS', 'Amount': '$80,000', 'Project': 'Upgrades', 'Areas': 'Anne Arundel'},
        {'FY': '26', 'Org': 'TBD', 'Amount': 'Pending', 'Project': 'Efficiency', 'Areas': 'Southern Region'}
    ],
    5: [
        {'FY': '25', 'Org': 'Frederick County', 'Amount': '$523,998', 'Project': 'Retrofits', 'Areas': 'Frederick'},
        {'FY': '26', 'Org': 'TBD', 'Amount': 'Pending', 'Project': 'Upgrades', 'Areas': 'Western Region'}
    ]
}

# Popup function
def get_popup(region_id):
    df = pd.DataFrame(grantees.get(region_id, []))
    if df.empty:
        return f'<h4>No grantees in Region {region_id}</h4>'
    html = df.to_html(index=False, escape=False, classes='grantee-table')
    return f'<h4>Region {region_id}: {regions[region_id]["name"]}</h4>{html}'

# Create map
m = folium.Map(location=[39.0458, -76.6413], zoom_start=8, tiles='CartoDB positron')

# === MERGED REGION LAYERS (Shaded by Color) ===
region_features = []
for rid, info in regions.items():
    merged_coords = []
    for county in info["counties"]:
        fixed_name = county_name_fix.get(county, county)
        for feature in geo_data['features']:
            if feature['properties'].get('NAME') == fixed_name:
                coords = feature['geometry']['coordinates']
                merged_coords.extend(coords if feature['geometry']['type'] == 'MultiPolygon' else [coords])
    if merged_coords:
        region_features.append({
            "type": "Feature",
            "properties": {"name": info["name"], "region": rid},
            "geometry": {"type": "MultiPolygon", "coordinates": [merged_coords]}
        })

# Add merged regions
folium.GeoJson(
    {"type": "FeatureCollection", "features": region_features},
    style_function=lambda f: {
        'fillColor': regions[f['properties']['region']]['color'],
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.7
    },
    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Region:']),
    popup=folium.Popup(max_width=600)
).add_to(m)

# === INDIVIDUAL COUNTIES (Faint lines + click for same popup) ===
for feature in geo_data['features']:
    county_name = feature['properties'].get('NAME', '')
    region_id = next((rid for rid, info in regions.items() if county_name in info["counties"]), 0)
    if region_id:
        popup_html = get_popup(region_id)
        folium.GeoJson(
            feature,
            style_function=lambda x: {'fillOpacity': 0, 'color': 'gray', 'weight': 0.5},
            tooltip=folium.GeoJsonTooltip(fields=['NAME'], aliases=['County:']),
            popup=folium.Popup(popup_html, max_width=600)
        ).add_to(m)

# === LEGEND ===
legend_html = '''
<div style="position: fixed; bottom: 50px; right: 50px; width: 160px; height: 170px; 
     background:white; border:2px solid grey; z-index:9999; font-size:14px; padding:10px;">
 <b>Regions</b><br>
 <i style="background:red; width:18px; height:18px; float:left; margin-right:8px;"></i>1: Baltimore City<br>
 <i style="background:orange; width:18px; height:18px; float:left; margin-right:8px;"></i>2: Central<br>
 <i style="background:blue; width:18px; height:18px; float:left; margin-right:8px;"></i>3: Eastern Shore<br>
 <i style="background:pink; width:18px; height:18px; float:left; margin-right:8px;"></i>4: Southern<br>
 <i style="background:green; width:18px; height:18px; float:left; margin-right:8px;"></i>5: Western
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Save
m.save('maryland_regions_map.html')
print("Map generated successfully!")
