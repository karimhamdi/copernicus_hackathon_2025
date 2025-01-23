import streamlit as st # type: ignore
import pandas as pd # type: ignore
import folium # type: ignore
from streamlit_folium import folium_static # type: ignore
from folium.plugins import HeatMap # type: ignore

st.title("Heatmap")


DATA = {
    "lat": [52.5200, 48.8566, 40.7128, 34.0522, 35.6895],
    "lon": [13.4050, 2.3522, -74.0060, -118.2437, 139.6917],
    "intensity": [10, 20, 30, 40, 50]
}
df = pd.DataFrame(DATA)


heat_map = folium.Map(location=[20, 0], zoom_start=2)
HeatMap(df.values).add_to(heat_map)


folium_static(heat_map)
