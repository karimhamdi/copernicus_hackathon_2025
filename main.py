import streamlit as st # type: ignore
import pandas as pd # type: ignore
import folium # type: ignore
from streamlit_folium import folium_static # type: ignore
from streamlit_folium import st_folium # type: ignore
from folium.plugins import HeatMap # type: ignore
from folium import plugins # type: ignore
import branca  # type: ignore
from streamlit.components.v1 import html  # type: ignore
import json
import random
import numpy as np#  type: ignore

if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'
if 'open_sidebar' not in st.session_state:
    st.session_state.open_sidebar = False
if 'lat' not in st.session_state:
    st.session_state.lat = None
if 'lng' not in st.session_state:
    st.session_state.lng = None
if 'intensity' not in st.session_state:
    st.session_state.intensity = 0
if 'cur' not in st.session_state:
    st.session_state.cur = 1

st.set_page_config(page_title="Heatmap dies das",
                    page_icon="",
                    layout="wide", 
                    initial_sidebar_state = st.session_state.sidebar_state
                )

#Data:
with open("data_2.json", "r") as file:
    DATA = json.load(file)
lat_array = np.array(DATA["lat"])
lon_array = np.array(DATA["lon"])
intensity_array = np.array(DATA["intensity"])

df = pd.DataFrame(DATA)

#Heatmap:
MIN_ZOOM = 5
MAX_ZOOM=20

heat_map = folium.Map(location=[50, 10], zoom_start=4, min_zoom=MIN_ZOOM, max_zoom=MAX_ZOOM, control_scale=True)

#HeatMap(data, name=None, min_opacity=0.5, max_zoom=18, max_val=1.0, radius=25, blur=15, gradient=None, overlay=True, control=True, show=True)
#!HeatMap(df.values, min_opacity = 0.5, max_val = 1, overlay=True, radius=40, blur=30).add_to(heat_map)

#Tiles:
folium.TileLayer('Esri.WorldImagery').add_to(heat_map)

folium.WmsTileLayer(
    url="https://fbinter.stadt-berlin.de/fb/wms/senstadt/k09_01_1UGlaerm2021?REQUEST=GetCapabilities&SERVICE=wms",
    name="Lärmkarten WMS",
    fmt="image/png",
    transparent=True,
    layers="k09_01_1UGlaerm2021",  
    control=True
).add_to(heat_map)


#folium.TileLayer('cartodb positron').add_to(heat_map)

#Zoom Einschränkung:
heat_map.options['maxBounds'] = [[-200, -200], [200, 200]]

#Slider

#Pop up Window Haus
geo_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[-122.4194, 37.7749], [-122.4394, 37.7849], [-122.4294, 37.7949], [-122.4194, 37.7749]]
                ],
            },
            "properties": {"id": 1, "name": "Segment A", "data": "Sample Data A"},
        },
         {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[-122.4194, 37.7449], [-122.4394, 37.7549], [-122.4294, 37.7649], [-122.4194, 37.7449]]
                ],
            },
            "properties": {"id": 2, "name": "Segment B", "data": "Sample Data B"},
        },

    ],
}

folium.GeoJson(geo_data).add_to(heat_map)

#heat_map.add_child(folium.ClickForMarker(popup="clicked here"))

def get_nearest_intensity(lat, lon):
    distances = np.sqrt((lat_array - lat)**2 + (lon_array - lon)**2)
    nearest_index = np.argmin(distances)
    return intensity_array[nearest_index]


#! Legende not showing: 
colormap = branca.colormap.LinearColormap(
    colors=['blue', 'green', 'yellow', 'orange', 'red'], 
    vmin=0, vmax=50
).to_step(n=5)  

colormap.caption = "Lufttemperatur in Grad Celsius"
heat_map.add_child(colormap)

heat_map.add_child(folium.LatLngPopup())
map_data = st_folium(heat_map, width=1920, height=1080, returned_objects=['last_clicked', 'zoom'])


if map_data and map_data.get('last_clicked'): 
    lat, lng = map_data.get('last_clicked')["lat"],map_data.get('last_clicked')["lng"]
    st.session_state.lat = lat
    st.session_state.lng = lng
    map_data = {'last_clicked': {'lat': 0, 'lng': 0}, 'zoom': map_data['zoom']}

    st.session_state.intesity = get_nearest_intensity(lat, lng)
    
    st.session_state.open_sidebar = True


folium.Popup(f"", max_width=300)

#TODO: WFS, Soundbelastug, Hitze, Air Pollution, 

st.sidebar.header(f"**Deine Lebenserwartung**")
st.sidebar.write(f"**Standort:** Latitude: {st.session_state.lat} Longditude: {st.session_state.lng}")
st.sidebar.write(f"")
st.sidebar.write(f"")
st.sidebar.write(f"")

#print(st.session_state.cur)
#print(st.session_state.sidebar_state)
#print(st.session_state.open_sidebar)

if st.session_state.open_sidebar and st.session_state.cur % 2 != 0 and st.session_state.sidebar_state != 'expanded': 
    st.session_state.sidebar_state = 'expanded'
    st.session_state.cur = st.session_state.cur  +1
    st.rerun()

if st.session_state.open_sidebar == False and st.session_state.cur %2 == 0 and  st.session_state.sidebar_state != 'collapsed':
    st.session_state.sidebar_state = 'collapsed'
    st.session_state.cur = st.session_state.cur +1
    st.rerun()


 
#Map über den ganzen Bildschrim fitten:
st.markdown("""
<style>
    header {visibility: hidden;}

    *{
        padding: 0px;
        margin: 0px;    
        wdith = 100%
        height = 100%;
    }
            
    iframe {
        position: absolute;
        top: -20vh;
        right: -6.2vw;
        width: 100vw;
        height: 102vh;
        border: none;
        z-index: 1;
    }

</style> 
""", unsafe_allow_html=True)


#st_folium(heat_map)
#folium_static(heat_map, width= 0, height = 0)


