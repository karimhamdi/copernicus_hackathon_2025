import streamlit as st # type: ignore
import pandas as pd # type: ignore
import folium # type: ignore
from streamlit_folium import folium_static # type: ignore
from streamlit_folium import st_folium # type: ignore
from folium.plugins import HeatMap # type: ignore
from folium import plugins # type: ignore
import branca  # type: ignore
from streamlit.components.v1 import html  # type: ignore


if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'
if 'open_sidebar' not in st.session_state:
    st.session_state.open_sidebar = True


st.set_page_config(page_title="Heatmap dies das",
                    page_icon="",
                    layout="wide", 
                    initial_sidebar_state = st.session_state.sidebar_state
                )

#Data:
DATA = {
    "lat": [52.5200, 48.8566, 40.7128, 34.0522, 35.6895],
    "lon": [13.4050, 2.3522, -74.0060, -118.2437, 139.6917],
    "intensity": [10, 20, 30, 40, 50]
}
df = pd.DataFrame(DATA)

#Heatmap:
MIN_ZOOM = 2
MAX_ZOOM=20

heat_map = folium.Map(location=[50, 10], zoom_start=4, min_zoom=MIN_ZOOM, max_zoom=MAX_ZOOM, control_scale=True)

#HeatMap(data, name=None, min_opacity=0.5, max_zoom=18, max_val=1.0, radius=25, blur=15, gradient=None, overlay=True, control=True, show=True)
HeatMap(df.values).add_to(heat_map)

#Google Maps:
folium.TileLayer(
    tiles="https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
    attr="Google Maps",
    name="Geodudes Maps",
    max_zoom=MAX_ZOOM,
    min_zoom = MIN_ZOOM,
    subdomains=["mt0", "mt1", "mt2", "mt3"],
).add_to(heat_map)


#Legende: 
colormap = branca.colormap.LinearColormap(
    colors=['blue', 'green', 'yellow', 'orange', 'red'], 
    vmin=0, vmax=50
).to_step(n=5)  

colormap.caption = "Lufttemperatur in Grad Celsius"
colormap.add_to(heat_map)


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
heat_map.add_child(folium.LatLngPopup())
map_data = st_folium(heat_map, width=1920, height=1080, returned_objects=['last_clicked'])

if map_data and map_data.get('last_clicked'):
    lat, lng = map_data.get('last_clicked')["lat"],map_data.get('last_clicked')["lng"]
    print(f"Location lat:{lat},long:{lng}")


folium.Popup(f"TEST", max_width=300)
st.sidebar.title("TEST")
st.sidebar.write("TEST")
st.sidebar.text_input("TEST")

if st.session_state.open_sidebar:
    st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'expanded'
    st.session_state.open_sidebar = False
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
        top: -21vh;
        right: -6.2vw;
        width: 100vw;
        height: 100vh;
        border: none;
        z-index: 1;
    }

</style> 
""", unsafe_allow_html=True)


#st_folium(heat_map)



