import streamlit as st # type: ignore
import pandas as pd # type: ignore
import folium # type: ignore
from streamlit_folium import folium_static # type: ignore
from folium.plugins import HeatMap # type: ignore


st.set_page_config(page_title="Heatmap dies das",
                    page_icon="",
                    layout="wide", 
                    initial_sidebar_state="collapsed"
                )
DATA = {
    "lat": [52.5200, 48.8566, 40.7128, 34.0522, 35.6895],
    "lon": [13.4050, 2.3522, -74.0060, -118.2437, 139.6917],
    "intensity": [10, 20, 30, 40, 50]
}
df = pd.DataFrame(DATA)

MIN_ZOOM = 3
MAX_ZOOM=14

heat_map = folium.Map(location=[50, 10], zoom_start=4, min_zoom=MIN_ZOOM, max_zoom=MAX_ZOOM)

HeatMap(df.values).add_to(heat_map)
folium.TileLayer(
    tiles="https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
    attr="Google Maps",
    name="Geodudes Maps",
    max_zoom=MAX_ZOOM,
    min_zoom = MIN_ZOOM,
    subdomains=["mt0", "mt1", "mt2", "mt3"],
).add_to(heat_map)


southwest = [40, -130]  
northeast = [60, 10]    

heat_map.fit_bounds(southwest, northeast)

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
        top: -18.5vh;
        right: -5.5vw;
        width: 100vw;
        height: 100vh;
        border: none;
        z-index: 1;
    }
</style>
""", unsafe_allow_html=True)


folium_static(heat_map)
