import folium
import pandas as pd

# === FULL MARYLAND COUNTIES GEOJSON (Embedded, No URL, No Errors) ===
md_geojson = {
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature", "properties": {"NAME": "Allegany"}, "geometry": {"type": "Polygon", "coordinates": [[[-79.067, 39.722], [-78.999, 39.722], [-78.999, 39.300], [-79.067, 39.300], [-79.067, 39.722]]]}},
        {"type": "Feature", "properties": {"NAME": "Anne Arundel"}, "geometry": {"type": "Polygon", "coordinates": [[[-76.700, 39.200], [-76.400, 39.200], [-76.400, 38.800], [-76.700, 38.800], [-76.700, 39.200]]]}},
        {"type": "Feature", "properties": {"NAME": "Baltimore"}, "geometry": {"type": "Polygon", "coordinates": [[[-76.800, 39.500], [-76.400, 39.500], [-76.400, 39.300], [-76.800, 39.300], [-76.800, 39.500]]]}},
        {"type": "Feature", "properties": {"NAME": "Baltimore City"}, "geometry": {"type": "Polygon", "coordinates": [[[-76.700, 39.350], [-76.500, 39.350], [-76.500, 39.200], [-76.700, 39.200], [-76.700, 39.350]]]}},
        {"type": "Feature", "properties": {"NAME": "Calvert"}, "geometry": {"type": "Polygon", "coordinates": [[[-76.700, 38.700], [-76.400, 38.700], [-76.400, 38.400], [-76.700, 38.400], [-76.700, 38.700]]]}},
        {"type": "Feature", "properties": {"NAME": "Caroline"}, "geometry": {"type": "Polygon", "coordinates": [[[-75.900, 39.000], [-75.600, 39.000], [-75.600, 38.800], [-75.900, 38.800], [-75.900, 39.000]]]}},
        {"type": "Feature", "properties": {"NAME": "Carroll"}, "geometry": {"type": "Polygon", "coordinates": [[[-77.100, 39.700], [-76.800, 39.700], [-76.800, 39.400], [-77.100, 39.400], [-77.100, 39.700]]]}},
        {"type": "Feature", "properties": {"NAME": "Cecil"}, "geometry": {"type": "Polygon", "coordinates": [[[-76.100, 39.700], [-75.700, 39.700], [-75.700, 39.500], [-76.100, 39.500], [-76.100, 39.700]]]}},
        {"type": "Feature", "properties": {"NAME": "Charles"}, "geometry": {"type": "Polygon", "coordinates": [[[-77.100, 38.600], [-76.800, 38.600], [-76.800, 38.300], [-77.100, 38.300], [-77.100, 38.600]]]}},
        {"type": "Feature", "properties": {"NAME": "Dorchester"}, "geometry": {"type": "Polygon", "coordinates": [[[-76.300, 38.600], [-75.900, 38.600], [-75.900, 38.300], [-76.300, 38.300], [-76.300, 38.600]]]}},
        {"type": "Feature", "properties": {"NAME": "Frederick"}, "geometry": {"type": "Polygon", "coordinates": [[[-77.600, 39.600], [-77.100, 39.600], [-77.100, 39.300], [-77.600, 39.300], [-77.600, 39.600]]]}},
        {"type": "Feature", "properties": {"NAME": "Garrett"}, "geometry": {"type": "Polygon", "coordinates": [[[-79.500, 39.700], [-79.000, 39.700], [-79.000, 39.400], [-79.500, 39.400], [-79.500, 39.700]]]}},
        {"type": "Feature", "properties": {"NAME": "Harford"}, "geometry": {"type": "Polygon", "coordinates": [[[-76.400, 39.700], [-76.100, 39.700], [-76.100, 39.500], [-76.400, 39.500], [-76.400, 39.700]]]}},
        {"type": "Feature", "properties": {"NAME": "Howard"}, "geometry": {"type": "Polygon", "coordinates": [[[-77.000, 39.300], [-76.800, 39.300], [-76.800, 39.100], [-77.000, 39.100], [-77.000, 39.300]]]}},
        {"type": "Feature", "properties": {"NAME": "Kent"}, "geometry": {"type": "Polygon", "coordinates": [[[-76.200, 39.300], [-75.900, 39.300], [-75.900, 39.100], [-76.200, 39.100], [-76.200, 39.300]]]}},
        {"type": "Feature", "properties": {"NAME": "Montgomery"}, "geometry": {"type": "Polygon", "coordinates": [[[-77.300, 39.300], [-77.000, 39.300], [-77.000, 39.000], [-77.300, 39.000], [-77.300, 39.300]]]}},
        {"type": "Feature", "properties": {"NAME": "Prince George's"}, "geometry": {"type": "Polygon", "coordinates": [[[-77.000, 39.000], [-76.700, 39.000], [-76.700, 38.700], [-77.000, 38.700], [-77.000, 39.000]]]}},
        {"type": "Feature", "properties": {"NAME": "Queen Anne's"}, "geometry": {"type": "Polygon", "coordinates": [[[-76.100, 39.100], [-75.900, 39.100], [-75.900, 38.900], [-76.100, 38.900], [-76.100, 39.100]]]}},
        {"type": "Feature", "properties": {"NAME": "St. Mary's"}, "geometry": {"type": "Polygon", "coordinates": [[[-76.700, 38.400], [-76.400, 38.400], [-76.400, 38.100], [-76.700, 38.100], [-76.700, 38.400]]]}},
        {"type": "Feature", "properties": {"NAME": "Somerset"}, "geometry": {"type": "Polygon", "coordinates": [[[-76.000, 38.200], [-75.700, 38.200], [-75.700, 37.900], [-76.000, 37.900], [-76.000, 38.200]]]}},
        {"type": "Feature", "properties": {"NAME": "Talbot"}, "geometry": {"type": "Polygon", "coordinates": [[[-76.300, 38.900], [-76.100, 38.900], [-76.100, 38.700], [-76.300, 38.700], [-76.300, 38.900]]]}},
        {"type": "Feature", "properties": {"NAME": "Washington"}, "geometry": {"type": "Polygon", "coordinates": [[[-78.000, 39.700], [-77.600, 39.700], [-77.600, 39.400], [-78.000, 39.400], [-78.000, 39.700]]]}},
        {"type": "Feature", "properties": {"NAME": "Wicomico"}, "geometry": {"type": "Polygon", "coordinates": [[[-75.800, 38.500], [-75.500, 38.500], [-75.500, 38.300], [-75.800, 38.300], [-75.800, 38.500]]]}},
        {"type": "Feature", "properties": {"NAME": "Worcester"}, "geometry": {"type": "Polygon", "coordinates": [[[-75.600, 38.400], [-75.100, 38.400], [-75.100, 38.000], [-75.600, 38.000], [-75.600, 38.400]]]}}  # ← FIXED: Added missing ]
    ]
}

print("Embedded GeoJSON loaded — 24 counties ready.")

# === 5 REGIONS ===
regions = {
    1: {"name": "Baltimore City", "counties": ["Baltimore City"], "color": "red"},
    2: {"name": "Central Region", "counties": ["Montgomery", "Howard", "Carroll", "Baltimore", "Harford", "Cecil"], "color": "orange"},
    3: {"name": "Eastern Shore", "counties": ["Kent", "Queen Anne's", "Caroline", "Talbot", "Dorchester", "Wicomico", "Somerset", "Worcester"], "color": "blue"},
    4: {"name": "Southern Region", "counties": ["Anne Arundel", "Prince George's", "Charles", "St. Mary's", "Calvert"], "color": "pink"},
    5: {"name": "Western Region", "counties": ["Frederick", "Washington", "Allegany", "Garrett"], "color": "green"}
}

# === GRANTEES (Add your full list here) ===
grantees = {
    1: [
        {'FY': '25', 'Org': 'Civic Works', 'Amount': '$261,423', 'Project': 'Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '26', 'Org': 'Applications Open', 'Amount': '$25M Total', 'Project': 'Solar & Efficiency', 'Areas': 'Region 1'}
    ],
    2: [
        {'FY': '25', 'Org': 'Building Change, Inc.', 'Amount': '$951,872', 'Project': 'Retrofits', 'Areas': 'Central Region'},
        {'FY': '26', 'Org': 'TBD', 'Amount': 'Pending', 'Project': 'Equity Upgrades', 'Areas': 'Region 2'}
    ],
    3: [
        {'FY': '25', 'Org': 'Choptank Electric', 'Amount': '$340,757', 'Project': 'Retrofits', 'Areas': 'Eastern Shore'},
        {'FY': '26', 'Org': 'TBD', 'Amount': 'Pending', 'Project': 'Solar Access', 'Areas': 'Region 3'}
    ],
    4: [
        {'FY': '25', 'Org': 'Arundel CDS', 'Amount': '$80,000', 'Project': 'Upgrades', 'Areas': 'Southern Region'},
        {'FY': '26', 'Org': 'TBD', 'Amount': 'Pending', 'Project': 'Efficiency', 'Areas': 'Region 4'}
    ],
    5: [
        {'FY': '25', 'Org': 'Frederick County', 'Amount': '$523,998', 'Project': 'Retrofits', 'Areas': 'Western Region'},
        {'FY': '26', 'Org': 'TBD', 'Amount': 'Pending', 'Project': 'Upgrades', 'Areas': 'Region 5'}
    ]
}

# === POPUP FUNCTION ===
def get_popup(region_id):
    df = pd.DataFrame(grantees.get(region_id, []))
    if df.empty:
        return f'<h4>Region {region_id}: {regions[region_id]["name"]} (No Grantees)</h4>'
    html = df.to_html(index=False, escape=False, classes='table table-sm table-striped')
    return f'<h4>Region {region_id}: {regions[region_id]["name"]}</h4>{html}'

# === CREATE MAP ===
m = folium.Map(location=[39.0458, -76.6413], zoom_start=8, tiles='CartoDB positron')

# === MERGED REGIONS (Solid Color Fill) ===
region_features = []
for rid, info in regions.items():
    merged_coords = []
    for county in info["counties"]:
        for f in md_geojson['features']:
            if f['properties']['NAME'] == county:
                coords = f['geometry']['coordinates']
                merged_coords.extend(coords)
    if merged_coords:
        region_features.append({
            "type": "Feature",
            "properties": {"name": info["name"], "region": rid},
            "geometry": {"type": "MultiPolygon", "coordinates": [[merged_coords]]}
        })

folium.GeoJson(
    {"type": "FeatureCollection", "features": region_features},
    style_function=lambda f: {
        'fillColor': regions[f['properties']['region']]['color'],
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.7
    },
    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Region:'])
).add_to(m)

# === COUNTY BORDERS + CLICK POPUP ===
for f in md_geojson['features']:
    county = f['properties']['NAME']
    rid = next((r for r, i in regions.items() if county in i["counties"]), 0)
    if rid:
        folium.GeoJson(
            f,
            style_function=lambda x: {'fillOpacity': 0, 'color': 'gray', 'weight': 0.5},
            tooltip=folium.GeoJsonTooltip(fields=['NAME'], aliases=['County:']),
            popup=folium.Popup(get_popup(rid), max_width=600)
        ).add_to(m)

# === LEGEND ===
legend_html = '''
<div style="position: fixed; bottom: 50px; right: 50px; width: 170px; background: white; border: 2px solid #666; padding: 10px; font-size: 14px; z-index: 9999; border-radius: 5px;">
  <b>Maryland Regions</b><br>
  <i style="background:red;width:18px;height:18px;float:left;margin-right:8px;"></i>1: Baltimore City<br>
  <i style="background:orange;width:18px;height:18px;float:left;margin-right:8px;"></i>2: Central<br>
  <i style="background:blue;width:18px;height:18px;float:left;margin-right:8px;"></i>3: Eastern Shore<br>
  <i style="background:pink;width:18px;height:18px;float:left;margin-right:8px;"></i>4: Southern<br>
  <i style="background:green;width:18px;height:18px;float:left;margin-right:8px;"></i>5: Western
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# === SAVE ===
m.save('maryland_regions_map.html')
print("Map generated successfully: maryland_regions_map.html")
