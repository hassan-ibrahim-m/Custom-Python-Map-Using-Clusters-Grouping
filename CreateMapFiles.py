import folium
import os
import pandas as pd
import json
from folium.plugins import MarkerCluster

df_sites = pd.read_csv('allData-sites.csv')
df_links = pd.read_csv('allData-links.csv')

m = folium.Map(location=[26.8976, 31.2006], zoom_start=7)
mCluster1 = MarkerCluster(name="one").add_to(m)
mCluster2 = MarkerCluster(name="two").add_to(m)
mCluster3 = MarkerCluster(name="three").add_to(m)
mCluster4 = MarkerCluster(name="four").add_to(m)
mCluster5 = MarkerCluster(name="five").add_to(m)
mCluster6 = MarkerCluster(name="six").add_to(m)
mCluster7 = MarkerCluster(name="seven").add_to(m)
mCluster8 = MarkerCluster(name="eight").add_to(m)
mCluster9 = MarkerCluster(name="nine").add_to(m)
mCluster10 = MarkerCluster(name="ten").add_to(m)
tooltip = "Click to see details"
html = ""
#####################################################
for indx, row in df_sites.iterrows():
    print(indx)
    # The Tooltip
    op = df_sites.iloc[indx]['operator']
    name = df_sites.iloc[indx]['site']
    long = df_sites.iloc[indx]['long']
    lat = df_sites.iloc[indx]['lat']
    gov = df_sites.iloc[indx]['gov']
    html = f"""
    <h5> Site Code: {name} </h4>
    <h5> Longitude: {long} </h4>
    <h5> Latitude: {lat} </h4>
    <h5> Operator: {op} </h4>
    <h5> Governorate: {gov} </h4>
    """

    # The Markers
    iframe1 = folium.IFrame(html, width=180 + 20, height=190 + 20)
    popup1 = folium.Popup(iframe1, max_width=650)
    icon1 = folium.features.CustomIcon('tower.png', icon_size=(30, 30))

    # The Icons   
    op = df_sites.iloc[indx]['operator']
    color = ""

    if op == 1:
        icon1 = folium.features.CustomIcon('tower.png', icon_size=(30, 30))
        icon2 = folium.features.CustomIcon('tower.png', icon_size=(30, 30))
    elif op == 2:
        icon1 = folium.features.CustomIcon('tower.png', icon_size=(30, 30))
        icon2 = folium.features.CustomIcon('tower.png', icon_size=(30, 30))
    elif op == 3:
        icon1 = folium.features.CustomIcon('tower.png', icon_size=(30, 20))
        icon2 = folium.features.CustomIcon('tower.png', icon_size=(30, 30))
    else:
        icon1 = folium.features.CustomIcon('tower.png', icon_size=(30, 30))
        icon2 = folium.features.CustomIcon('tower.png', icon_size=(30, 30))

    marker1 = folium.Marker(location=[df_sites.iloc[indx]['lat'], df_sites.iloc[indx]['long']], tooltip=tooltip,
                            popup=popup1, icon=icon1)

    if indx <= 3000:
        mCluster1.add_child(marker1)
    elif 3000 < indx <= 6000:
        mCluster2.add_child(marker1)
    elif 6000 < indx <= 9000:
        mCluster3.add_child(marker1)
    elif 9000 < indx <= 12000:
        mCluster4.add_child(marker1)
    elif 12000 < indx <= 15000:
        mCluster5.add_child(marker1)
    elif 15000 < indx <= 18000:
        mCluster6.add_child(marker1)
    elif 18000 < indx <= 21000:
        mCluster7.add_child(marker1)
    elif 21000 < indx <= 24000:
        mCluster8.add_child(marker1)
    elif 24000 < indx <= 28000:
        mCluster9.add_child(marker1)
    else:
        mCluster10.add_child(marker1)
###########################################
    # the Walk
for indx, row in df_links.iterrows():
    print(indx)

    bw = df_links.iloc[indx]['bw']
    freqBand = df_links.iloc[indx]['freqBand']
    html3 = f"""
        <h5> Band width: {bw} </h4>
        <h5> Frequency Band: {freqBand} </h4>
        """
    tooltip = "Click to see details"
    iframe3 = folium.IFrame(html3, width=150 + 20, height=70 + 20)
    popup3 = folium.Popup(iframe3, max_width=650)
    w = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"color": "#228B22", "stroke-width": 1},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        df_links.iloc[indx]['longA'],
                        df_links.iloc[indx]['latA']
                    ],
                    [
                        df_links.iloc[indx]['longB'],
                        df_links.iloc[indx]['latB']
                    ]
                ]
            }
        }]
    }

    op = df_links.iloc[indx]['operator']

    if op == 1:
        w['features'][0]['properties']['color'] = '#E90021'
    elif op == 2:
        w['features'][0]['properties']['color'] = '#FF5A01'
    elif op == 3:
        w['features'][0]['properties']['color'] = '#71A543'
    else:
        w['features'][0]['properties']['color'] = '#963E94'

    w['features'][0]['properties']['stroke-width'] = df_links.iloc[indx]['bw'] / 10
    style_function = lambda x: {
        'weight': x['properties']['stroke-width'],
        'color': x['properties']['color']
    }
    y = json.dumps(w)
    walkData = os.path.join(y)
    geo = folium.GeoJson(walkData, style_function=style_function, name='walk')


    if indx <= 3000:
        mCluster1.add_child(geo)
    elif 3000 < indx <= 6000:
        mCluster2.add_child(geo)
    elif 6000 < indx <= 9000:
        mCluster3.add_child(geo)
    elif 9000 < indx <= 12000:
        mCluster4.add_child(geo)
    elif 12000 < indx <= 15000:
        mCluster5.add_child(geo)
    elif 15000 < indx <= 18000:
        mCluster6.add_child(geo)
    elif 18000 < indx <= 21000:
        mCluster7.add_child(geo)
    elif 21000 < indx <= 24000:
        mCluster8.add_child(geo)
    elif 24000 < indx <= 28000:
        mCluster9.add_child(geo)
    else:
        mCluster10.add_child(geo)
    toolLong = (float(df_links.iloc[indx]['longA']) + float(df_links.iloc[indx]['longB'])) / 2.0
    toolLat = (float(df_links.iloc[indx]['latA']) + float(df_links.iloc[indx]['latB'])) / 2.0

    icon3 = folium.features.CustomIcon('add.png', icon_size=(15, 15))
    marker3 = folium.Marker(location=[toolLat, toolLong], tooltip=tooltip,
                            popup=popup3, icon=icon3)

    mCluster10.add_child(marker3)

folium.LayerControl().add_to(m)
# Saving the HTML
m.save("SitesMap.html")




print('finished')
