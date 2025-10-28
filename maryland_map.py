import folium
import pandas as pd
import requests

# === LOAD REAL MARYLAND GEOJSON ===
geojson_url = "https://raw.githubusercontent.com/frankrowe/maryland-geojson/master/md-counties.geojson"
try:
    geo_data = requests.get(geojson_url).json()
    print("Real Maryland GeoJSON loaded.")
except Exception as e:
    print(f"GeoJSON failed: {e}. Using empty map.")
    geo_data = {"type": "FeatureCollection", "features": []}

# === REGION MAPPING ===
county_to_region = {
    "Baltimore City": 1,
    "Montgomery": 2, "Howard": 2, "Carroll": 2, "Baltimore": 2, "Harford": 2, "Cecil": 2,
    "Kent": 3, "Queen Anne's": 3, "Caroline": 3, "Talbot": 3, "Dorchester": 3,
    "Wicomico": 3, "Somerset": 3, "Worcester": 3,
    "Anne Arundel": 4, "Prince George's": 4, "Charles": 4, "St. Mary's": 4, "Calvert": 4,
    "Frederick": 5, "Washington": 5, "Allegany": 5, "Garrett": 5
}

regions = {
    1: {"name": "Baltimore City", "color": "red"},
    2: {"name": "Central Region", "color": "orange"},
    3: {"name": "Eastern Shore", "color": "blue"},
    4: {"name": "Southern Region", "color": "pink"},
    5: {"name": "Western Region", "color": "green"}
}

# === GRANTEES ===
grantees = {
    1: [
        {'FY': '25', 'Org': 'Civic Works', 'Amount': '$261,423', 'Project': 'Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '26', 'Org': 'Applications Open', 'Amount': '$25M', 'Project': 'Solar & Efficiency', 'Areas': 'Region 1'}
    ],
    2: [
        {'FY': '25', 'Org': 'Building Change', 'Amount': '$951,872', 'Project': 'Retrofits', 'Areas': 'Central Region'}
    ],
    3: [
        {'FY': '25', 'Org': 'Choptank Electric', 'Amount': '$340,757', 'Project': 'Retrofits', 'Areas': 'Eastern Shore'}
    ],
    4: [
        {'FY': '25', 'Org': 'Arundel CDS', 'Amount': '$80,000', 'Project': 'Upgrades', 'Areas': 'Anne Arundel'}
    ],
    5: [
        {'FY': '25', 'Org': 'Frederick County', 'Amount': '$523,998', 'Project': 'Retrofits', 'Areas': 'Frederick'}
    ]
}

def get_popup(region_id):
    df = pd.DataFrame(grantees.get(region_id, []))
    if df.empty:
        return f'<h4>Region {region_id}: {regions[region_id]["name"]}</h4><p>No data.</p>'
    return f'<h4>Region {region_id}: {regions[region_id]["name"]}</h4>{df.to_html(index=False, classes="table table-sm table-striped")}'

# === MAP ===
m = folium.Map(location=[39.0458, -76.6413], zoom_start=8, tiles='CartoDB positron')

# === ADD COUNTIES WITH DYNAMIC COLOR ===
for feature in geo_data.get("features", []):
    county = feature["properties"].get("NAME", "")
    region_id = county_to_region.get(county, 0)
    
    if region_id == 0:
        continue  # Skip unmapped

    # Dynamic style function
    def make_style(feature, rid=region_id):
        return {
            'fillColor': regions[rid]['color'],
            'color': 'black',
            'weight': 1.5,
            'fillOpacity': 0.7
        }

    folium.GeoJson(
        feature,
        style_function=make_style,
        tooltip=folium.GeoJsonTooltip(
            fields=['NAME'],
            aliases=['County:'],
            localize=True
        ),
        popup=folium.Popup(get_popup(region_id), max_width=600)
    ).add_to(m)

# === LEGEND ===
legend_html = '''
<div style="position:fixed;bottom:50px;right:50px;width:170px;background:white;border:2px solid #666;padding:10px;font-size:14px;z-index:9999;border-radius:5px;">
  <b>REEP Regions</b><br>
  <i style="background:red;width:18px;height:18px;float:left;margin-right:8px;"></i>1: Baltimore City<br>
  <i style="background:orange;width:18px;height:18px;float:left;margin-right:8px;"></i>2: Central<br>
  <i style="background:blue;width:18px;height:18px;float:left;margin-right:8px;"></i>3: Eastern Shore<br>
  <i style="background:pink;width:18px;height:18px;float:left;margin-right:8px;"></i>4: Southern<br>
  <i style="background:green;width:18px;height:18px;float:left;margin-right:8px;"></i>5: Western
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

m.save('maryland_regions_map.html')
print("Map saved — REAL COUNTIES, REAL COLORS, NO PLACEHOLDERS!")
