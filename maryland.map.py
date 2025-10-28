import folium
import requests
import pandas as pd

# Load Maryland counties GeoJSON from GitHub
geojson_url = 'https://raw.githubusercontent.com/frankrowe/maryland-geojson/master/md-counties.geojson'
geo_data = requests.get(geojson_url).json()

# Map counties to your defined regions (1-5)
county_to_region = {
    'Allegany': 5,
    'Anne Arundel': 4,
    'Baltimore': 2,  # Baltimore County
    'Baltimore City': 1,
    'Calvert': 4,
    'Caroline': 3,
    'Carroll': 2,
    'Cecil': 2,
    'Charles': 4,
    'Dorchester': 3,
    'Frederick': 5,
    'Garrett': 5,
    'Harford': 2,
    'Howard': 2,
    'Kent': 3,
    'Montgomery': 2,
    'Prince George\'s': 4,
    'Queen Anne\'s': 3,
    'St. Mary\'s': 4,
    'Somerset': 3,
    'Talbot': 3,
    'Washington': 5,
    'Wicomico': 3,
    'Worcester': 3
}

# Add region property to each feature
for feature in geo_data['features']:
    county_name = feature['properties']['NAME']
    feature['properties']['region'] = county_to_region.get(county_name, 0)

# Grantees data compiled from FY23, FY24, FY25 (all entries included)
grantees = {
    1: [  # Baltimore City Region
        {'FY': '25', 'Org': 'Civic Works', 'Amount': '$261,423', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '25', 'Org': 'Diversified Housing Development, Inc.', 'Amount': '$100,000', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '25', 'Org': 'Green and Healthy Homes Initiative', 'Amount': '$156,854', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '25', 'Org': 'Healthy Neighborhoods, Inc.', 'Amount': '$205,092', 'Project': 'Whole Building Commercial Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '25', 'Org': 'Mayor and City Council of Baltimore', 'Amount': '$211,731', 'Project': 'Whole Building Commercial Retrofits, Limited Upgrades to Existing Commercial/Residential Buildings', 'Areas': 'Baltimore City'},
        {'FY': '25', 'Org': 'Neighborhood Housing Services of Baltimore, Inc. (New Applicant)', 'Amount': '$319,125', 'Project': 'Residential Whole Home/Building Retrofit', 'Areas': 'Baltimore City'},
        {'FY': '25', 'Org': 'SAFE Housing, Inc.', 'Amount': '$312,246', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '25', 'Org': 'The Community Action Council of Howard County, Maryland, Inc.', 'Amount': '$100,000', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Howard County'},
        {'FY': '24', 'Org': 'CASA, Inc. (New in FY24)', 'Amount': '$250,000', 'Project': 'Whole Building Commercial Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '24', 'Org': 'Civic Works, Inc.', 'Amount': '$240,000', 'Project': 'Whole Building Commercial Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '24', 'Org': 'Civic Works, Inc.', 'Amount': '$415,141', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '24', 'Org': 'Community Action Council of Howard County, Maryland, Inc.', 'Amount': '$106,126', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '24', 'Org': 'Diversified Housing Development', 'Amount': '$84,901', 'Project': 'Residential Whole Home/Building Retrofit', 'Areas': 'Baltimore City'},
        {'FY': '24', 'Org': 'Green & Healthy Homes Initiative', 'Amount': '$176,169', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '24', 'Org': 'We Care Incorporated D/B/A Feed the Fridge', 'Amount': '$3,300', 'Project': 'Limited Upgrades to Existing Commercial/Residential Buildings', 'Areas': 'Baltimore City'},
        {'FY': '24', 'Org': 'Healthy Neighborhoods, Inc.', 'Amount': '$376,150', 'Project': 'Whole Building Commercial Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '24', 'Org': 'Mayor and City Council of Baltimore', 'Amount': '$281,367', 'Project': 'Limited Upgrades to Existing Commercial/Residential Buildings', 'Areas': 'Baltimore City'},
        {'FY': '24', 'Org': 'Safe Housing, Inc.', 'Amount': '$497,985', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '24', 'Org': 'Sustain Our Future, Inc.', 'Amount': '$493,880', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Baltimore City'},
        {'FY': '24', 'Org': 'Unity Properties, Inc.', 'Amount': '$180,200', 'Project': 'New Construction with Incremental Efficiency Upgrades', 'Areas': 'Baltimore City'},
        {'FY': '24', 'Org': 'Youth Educational Services', 'Amount': '$50,000', 'Project': 'Limited Upgrades to Existing Commercial/Residential Buildings', 'Areas': 'Baltimore City'},
        {'FY': '23', 'Org': 'Community Action Council of Howard County, MD', 'Amount': '$364,586', 'Project': 'Limited energy efficiency upgrades to a former school building', 'Areas': 'Baltimore, Maryland'},
        {'FY': '23', 'Org': 'Civic Works, Inc.', 'Amount': '$488,068', 'Project': 'Energy efficiency services to an estimated 660 homes', 'Areas': 'Baltimore City'},
        {'FY': '23', 'Org': 'Diversified Housing Development, Inc.', 'Amount': '$199,585', 'Project': 'Whole Home/Whole Building upgrades for 40 households', 'Areas': 'Baltimore City'},
        {'FY': '23', 'Org': 'Enterprise Community Development, Inc.', 'Amount': '$126,160', 'Project': 'Incremental costs of energy efficiency upgrades in a multi-family building', 'Areas': 'Baltimore City'},
        {'FY': '23', 'Org': 'Enterprise Community Development, Inc.', 'Amount': '$140,180', 'Project': 'Whole building retrofit to a low-income senior living community', 'Areas': 'Baltimore City'},
        {'FY': '23', 'Org': 'Green & Healthy Homes Initiative, Inc.', 'Amount': '$365,357', 'Project': 'Energy audits and efficiency measures in 32 homes', 'Areas': 'Baltimore City'},
        {'FY': '23', 'Org': 'Govans Ecumenical Development Corporation', 'Amount': '$96,747', 'Project': 'Energy efficiency upgrades to two buildings', 'Areas': 'Baltimore, Maryland'},
        {'FY': '23', 'Org': 'Healthy Neighborhoods, Inc.', 'Amount': '$601,519', 'Project': 'Energy efficiency measures in eight buildings', 'Areas': 'Baltimore City'},
        {'FY': '23', 'Org': 'Mayor and City Council of Baltimore', 'Amount': '$448,331', 'Project': 'Energy efficiency upgrades to seventeen commercial buildings', 'Areas': 'Baltimore City'},
        {'FY': '23', 'Org': 'New Ecology, Inc.', 'Amount': '$60,000', 'Project': 'Sustainability consulting for all-electric upgrades of 5 homes', 'Areas': 'Baltimore City (Cherry Hill neighborhood)'},
        {'FY': '23', 'Org': 'SAFE Housing, Inc.', 'Amount': '$576,118', 'Project': 'Whole Home/Whole Building upgrades in 100 homes', 'Areas': 'Baltimore City'},
        {'FY': '23', 'Org': 'The Community Builders, Inc.', 'Amount': '$213,303', 'Project': 'Whole building retrofit to the Coel Grant Higgs building and Oliver Senior Center', 'Areas': 'Baltimore City'}
    ],
    2: [  # Central Region
        {'FY': '25', 'Org': 'Building Change, Inc.', 'Amount': '$951,872', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Prince George’s County'},
        {'FY': '25', 'Org': 'Civic Works', 'Amount': '$951,872', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Central Region'},
        {'FY': '25', 'Org': 'Diversified Housing Development, Inc.', 'Amount': '$634,582', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Central Region'},
        {'FY': '25', 'Org': 'GREEN SPARK (New Applicant)', 'Amount': '$801,550', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Central Region'},
        {'FY': '25', 'Org': 'Habitat for Humanity Metro Maryland', 'Amount': '$158,646', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Central Region'},
        {'FY': '25', 'Org': 'Rebuilding Together Montgomery County', 'Amount': '$157,630', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Montgomery County'},
        {'FY': '25', 'Org': 'SAFE Housing, Inc.', 'Amount': '$727,659', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Central Region'},
        {'FY': '25', 'Org': 'ZNRG Foundation, Inc. (New Applicant)', 'Amount': '$187,251', 'Project': 'Whole Building Commercial Retrofits', 'Areas': 'Central Region'},
        {'FY': '24', 'Org': 'Building Change, Inc.', 'Amount': '$53,306', 'Project': 'Whole Building Commercial Retrofits', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'Building Change, Inc.', 'Amount': '$886,415', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'CASA, Inc.', 'Amount': '$250,000', 'Project': 'Whole Building Commercial Retrofits', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'Civic Works, Inc.', 'Amount': '$1,034,151', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'Community Action Council of Howard County, Maryland, Inc.', 'Amount': '$531,849', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'Diversified Housing Development', 'Amount': '$1,034,151', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'Enterprise Community Development, Inc.', 'Amount': '$137,937', 'Project': 'New Construction with Incremental Efficiency Upgrades', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'Chinese Culture and Community Service Center, Inc.', 'Amount': '$24,780', 'Project': 'Limited Upgrades to Existing Commercial/Residential Buildings', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'Nourish Now, Inc.', 'Amount': '$34,825', 'Project': 'Limited Upgrades to Existing Commercial/Residential Buildings', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'Rainbow Community Development Center', 'Amount': '$31,530', 'Project': 'Limited Upgrades to Existing Commercial/Residential Buildings', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'We Care Incorporated D/B/A Feed the Fridge', 'Amount': '$19,800', 'Project': 'Limited Upgrades to Existing Commercial/Residential Buildings', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'Habitat for Humanity Metro Maryland', 'Amount': '$110,000', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'Housing Opportunities Commission of Montgomery County', 'Amount': '$435,365', 'Project': 'New Construction with Incremental Efficiency Upgrades-Age Restricted', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'Housing Opportunities Commission of Montgomery County', 'Amount': '$256,060', 'Project': 'New Construction with Incremental Efficiency Upgrades-Non-Age-Restricted', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'Rebuilding Together Montgomery County', 'Amount': '$248,400', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'Safe Housing, Inc.', 'Amount': '$1,705,968', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Central'},
        {'FY': '24', 'Org': 'Sustain Our Future, Inc.', 'Amount': '$905,003', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Central'},
        {'FY': '23', 'Org': 'Building Change, Inc.', 'Amount': '$1,000,000', 'Project': 'Energy audits and efficiency measures in 200 homes', 'Areas': 'Central Region'},
        {'FY': '23', 'Org': 'Choptank Electric Cooperative, Inc.', 'Amount': '$150,000', 'Project': 'Whole home upgrades in 30 homes', 'Areas': 'Cecil County'},
        {'FY': '23', 'Org': 'Civic Works', 'Amount': '$600,000', 'Project': 'Energy efficiency services to 800 homes', 'Areas': 'Central Region'},
        {'FY': '23', 'Org': 'Diversified Housing Development', 'Amount': '$1,400,000', 'Project': 'Whole Home/Whole Building upgrades for 280 households', 'Areas': 'Central Region'},
        {'FY': '23', 'Org': 'Green & Healthy Homes Initiative, Inc.', 'Amount': '$230,000', 'Project': 'Energy audits and efficiency measures in 20 homes', 'Areas': 'Central Region'},
        {'FY': '23', 'Org': 'Rainbow Community Development Center', 'Amount': '$57,860', 'Project': 'Limited refrigeration upgrades in food pantry', 'Areas': 'Montgomery County'},
        {'FY': '23', 'Org': 'Rebuilding Together Montgomery County', 'Amount': '$221,750', 'Project': 'Energy audits and home upgrades for 20 households', 'Areas': 'Montgomery County'},
        {'FY': '23', 'Org': 'SAFE Housing, Inc.', 'Amount': '$3,571,815', 'Project': 'Whole Home/Whole Building upgrades in 650 homes', 'Areas': 'Central Region'}
    ],
    3: [  # Eastern Region
        {'FY': '25', 'Org': 'Choptank Electric Cooperative, Inc.', 'Amount': '$340,757', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Eastern Region'},
        {'FY': '25', 'Org': 'Dorchester County, Maryland (New Applicant)', 'Amount': '$70,671', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Dorchester County'},
        {'FY': '25', 'Org': 'GREEN SPARK (New Applicant)', 'Amount': '$801,550', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Eastern Region'},
        {'FY': '25', 'Org': 'Habitat for Humanity Choptank Inc.', 'Amount': '$125,888', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Eastern Region'},
        {'FY': '25', 'Org': 'Milford Housing Development Corporation (New Applicant)', 'Amount': '$103,237', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Eastern Region'},
        {'FY': '25', 'Org': 'The Community Action Council of Howard County, Maryland, Inc.', 'Amount': '$272,606', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Howard County'},
        {'FY': '24', 'Org': 'Building Change, Inc.', 'Amount': '$214,981', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Eastern'},
        {'FY': '24', 'Org': 'Choptank Electric Cooperative, Inc.', 'Amount': '$214,981', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Eastern'},
        {'FY': '24', 'Org': 'Community Action Council of Howard County, Maryland, Inc.', 'Amount': '$322,472', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Eastern'},
        {'FY': '24', 'Org': 'Habitat for Humanity Choptank Inc.', 'Amount': '$125,888', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Eastern'},
        {'FY': '24', 'Org': 'Habitat for Humanity Choptank, Inc.', 'Amount': '$28,750', 'Project': 'New Construction with Incremental Efficiency Upgrades', 'Areas': 'Eastern'},
        {'FY': '24', 'Org': 'Maryland Rural Development Corporation', 'Amount': '$214,981', 'Project': 'Residential Whole Home/Building Retrofit', 'Areas': 'Eastern'},
        {'FY': '24', 'Org': 'Safe Housing, Inc.', 'Amount': '$243,401', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Eastern'},
        {'FY': '24', 'Org': 'Chesapeake Neighbors', 'Amount': '$25,000', 'Project': 'Whole Building Commercial Retrofits', 'Areas': 'Eastern'},
        {'FY': '23', 'Org': 'Building Change, Inc.', 'Amount': '$233,070', 'Project': 'Energy audits and efficiency measures in 45 homes', 'Areas': 'Eastern Region'},
        {'FY': '23', 'Org': 'Choptank Electric Cooperative, Inc.', 'Amount': '$279,685', 'Project': 'Whole home upgrades in 45 homes', 'Areas': 'Eastern Region'},
        {'FY': '23', 'Org': 'Habitat for Humanity Choptank', 'Amount': '$110,770', 'Project': 'Multiple project types for weatherization and upgrades', 'Areas': 'Dorchester and Talbot Counties'},
        {'FY': '23', 'Org': 'Maryland Rural Development Corporation', 'Amount': '$139,842', 'Project': 'Whole Home/Whole Building upgrades for 20 homes', 'Areas': 'Caroline, Cecil, Kent, Talbot, and Queen Anne’s Counties'},
        {'FY': '23', 'Org': 'County Commissioners of Queen Anne’s County', 'Amount': '$23,500', 'Project': 'Limited upgrades to 10 households', 'Areas': 'Queen Anne’s County'},
        {'FY': '23', 'Org': 'SAFE Housing, Inc.', 'Amount': '$450,130', 'Project': 'Whole Home/Whole Building upgrades in 80 homes', 'Areas': 'Eastern Region'}
    ],
    4: [  # Southern Region
        {'FY': '25', 'Org': 'Arundel Community Development Services, Inc.', 'Amount': '$80,000', 'Project': 'Limited Upgrades to Existing Commercial/Residential Buildings', 'Areas': 'Anne Arundel County'},
        {'FY': '25', 'Org': 'Building Change, Inc.', 'Amount': '$941,968', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Southern Region'},
        {'FY': '25', 'Org': 'Civic Works', 'Amount': '$282,591', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Southern Region'},
        {'FY': '25', 'Org': 'Electrify Equity (New Applicant)', 'Amount': '$100,000', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Southern Region'},
        {'FY': '25', 'Org': 'Garrett County MD Community Action Committee, Inc.', 'Amount': '$235,492', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Garrett County'},
        {'FY': '25', 'Org': 'Housing Authority of Calvert County (New Applicant)', 'Amount': '$100,000', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Calvert County'},
        {'FY': '25', 'Org': 'Housing Options & Planning Enterprises, Inc. (New Applicant)', 'Amount': '$270,586', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Prince George’s County, Southern Maryland'},
        {'FY': '25', 'Org': 'Prince George\'s County Government (New Applicant)', 'Amount': '$204,444', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Prince George’s County'},
        {'FY': '25', 'Org': 'SAFE Housing, Inc.', 'Amount': '$320,112', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Southern Region'},
        {'FY': '25', 'Org': 'Town of North Beach', 'Amount': '$80,000', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'North Beach, Calvert County'},
        {'FY': '25', 'Org': 'United Communities Against Poverty', 'Amount': '$94,198', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Prince George’s County'},
        {'FY': '24', 'Org': 'Building Change, Inc.', 'Amount': '$408,220', 'Project': 'Whole Building Commercial Retrofits', 'Areas': 'Southern'},
        {'FY': '24', 'Org': 'Building Change, Inc.', 'Amount': '$837,064', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Southern'},
        {'FY': '24', 'Org': 'CASA, Inc.', 'Amount': '$250,000', 'Project': 'Whole Building Commercial Retrofits', 'Areas': 'Southern'},
        {'FY': '24', 'Org': 'Civic Works, Inc.', 'Amount': '$386,647', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Southern'},
        {'FY': '24', 'Org': 'Community Action Council of Howard County, Maryland, Inc.', 'Amount': '$100,000', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Southern'},
        {'FY': '24', 'Org': 'Diversified Housing Development', 'Amount': '$732,431', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Southern'},
        {'FY': '24', 'Org': 'Christian Life Center, Inc.', 'Amount': '$16,370', 'Project': 'Limited Upgrades to Existing Commercial/Residential Buildings', 'Areas': 'Southern'},
        {'FY': '24', 'Org': 'College Park United Methodist Church', 'Amount': '$21,830', 'Project': 'Limited Upgrades to Existing Commercial/Residential Buildings', 'Areas': 'Southern'},
        {'FY': '24', 'Org': 'Holy Mountain International Ministries', 'Amount': '$28,170', 'Project': 'Limited Upgrades to Existing Commercial/Residential Buildings', 'Areas': 'Southern'},
        {'FY': '24', 'Org': 'We Care Incorporated D/B/A Feed the Fridge', 'Amount': '$3,300', 'Project': 'Limited Upgrades to Existing Commercial/Residential Buildings', 'Areas': 'Southern'},
        {'FY': '24', 'Org': 'Lighthouse Ministries International Incorporated', 'Amount': '$93,665', 'Project': 'Limited Upgrades to Existing Commercial/Residential Buildings', 'Areas': 'Southern'},
        {'FY': '24', 'Org': 'Habitat for Humanity Metro Maryland', 'Amount': '$225,000', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Southern'},
        {'FY': '23', 'Org': 'Arundel Community Development Services, Inc.', 'Amount': '$150,000', 'Project': 'Comprehensive energy upgrades to 11 homes', 'Areas': 'Anne Arundel County'},
        {'FY': '23', 'Org': 'Building Change, Inc.', 'Amount': '$1,204,613', 'Project': 'Energy audits and efficiency measures in 240 homes', 'Areas': 'Southern Region'},
        {'FY': '23', 'Org': 'Diversified Housing Development', 'Amount': '$1,350,255', 'Project': 'Whole Home/Whole Building upgrades for 260 households', 'Areas': 'Southern Region'},
        {'FY': '23', 'Org': 'Garrett County MD Community Action Committee', 'Amount': '$337,292', 'Project': 'Installation of energy efficiency measures in 45 homes', 'Areas': 'Southern Region'},
        {'FY': '23', 'Org': 'SAFE Housing, Inc.', 'Amount': '$1,827,100', 'Project': 'Whole Home/Whole Building upgrades in 320 homes', 'Areas': 'Southern Region'},
        {'FY': '23', 'Org': 'The Community Builders, Inc.', 'Amount': '$360,339', 'Project': 'Whole building retrofit to the Morris Blum Senior Apartments', 'Areas': 'Annapolis, Maryland'},
        {'FY': '23', 'Org': 'Town of North Beach', 'Amount': '$100,000', 'Project': 'Energy audits and upgrades to 10 homes', 'Areas': 'North Beach'},
        {'FY': '23', 'Org': 'United Communities Against Poverty, Inc.', 'Amount': '$289,761', 'Project': 'Upgrade of 35 homes with energy audits and measures', 'Areas': 'Southern Region'}
    ],
    5: [  # Western Region
        {'FY': '25', 'Org': 'Frederick County Government', 'Amount': '$523,998', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Frederick County'},
        {'FY': '25', 'Org': 'Garrett County MD Community Action Committee, Inc.', 'Amount': '$92,284', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Garrett County'},
        {'FY': '25', 'Org': 'GREEN SPARK (New Applicant)', 'Amount': '$241,208', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Western Region'},
        {'FY': '25', 'Org': 'SAFE Housing, Inc.', 'Amount': '$262,596', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Western Region'},
        {'FY': '25', 'Org': 'Sustain Our Future Foundation INC.', 'Amount': '$153,293', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Western Region'},
        {'FY': '25', 'Org': 'The Community Action Council of Howard County, Maryland, Inc.', 'Amount': '$272,606', 'Project': 'Residential Whole Home/Building Retrofits', 'Areas': 'Howard County'},
        {'FY': '23', 'Org': 'Frederick County Government', 'Amount': '$571,948', 'Project': 'Energy audits and upgrades to 70 homes', 'Areas': 'Frederick County'},
        {'FY': '23', 'Org': 'Garrett County MD Community Action Committee', 'Amount': '$100,000', 'Project': 'Building shell and insulation upgrades in 12 homes', 'Areas': 'Garrett County'},
        {'FY': '23', 'Org': 'SAFE Housing, Inc.', 'Amount': '$933,691', 'Project': 'Whole Home/Whole Building upgrades in 130 homes', 'Areas': 'Western Region'}
    ]
}

# Function to create popup HTML table
def get_popup(region):
    if region == 0:
        return 'Unknown region'
    df = pd.DataFrame(grantees.get(region, []))
    if df.empty:
        return '<h4>No grantees found for this region</h4>'
    html = df.to_html(index=False, escape=False)
    return '<h4>Grantees for Region ' + str(region) + '</h4>' + html

# Color mapping for regions
colors = {1: 'red', 2: 'orange', 3: 'blue', 4: 'pink', 5: 'green'}

# Create the map centered on Maryland
m = folium.Map(location=[39.0458, -76.6413], zoom_start=8, tiles='OpenStreetMap')

# Add each county as a separate GeoJson layer with custom style and popup
for feature in geo_data['features']:
    region = feature['properties']['region']
    popup_html = get_popup(region)
    popup = folium.Popup(popup_html, max_width=500, min_width=300)
    style = {
        'fillOpacity': 0.7,
        'weight': 1,
        'color': 'black',
        'fillColor': colors.get(region, 'gray')
    }
    geo_layer = folium.GeoJson(
        feature,
        style_function=lambda f: style,
        tooltip=folium.GeoJsonTooltip(
            fields=['NAME', 'region'],
            aliases=['County:', 'Region:'],
            localize=True
        )
    )
    geo_layer.add_child(popup)
    geo_layer.add_to(m)

# Save the map to an HTML file
m.save('maryland_regions_map.html')
print('Map saved to maryland_regions_map.html')
