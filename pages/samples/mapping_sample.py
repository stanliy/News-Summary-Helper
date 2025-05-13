import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

def run():
    st.markdown("# Mapping Demo")
    st.write("Demo of st.pydeck_chart to show geospatial data.")

    @st.cache_data
    def from_data_file(filename):
        url = f"http://raw.githubusercontent.com/streamlit/example-data/master/hello/v1/{filename}"
        return pd.read_json(url)

    try:
        ALL_LAYERS = {
            "Bike Rentals": pdk.Layer(
                "HexagonLayer",
                data=from_data_file("bike_rental_stats.json"),
                get_position=["lon", "lat"],
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                extruded=True,
            ),
            "Bart Stop Exits": pdk.Layer(
                "ScatterplotLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_color=[200, 30, 0, 160],
                get_radius="[exits]",
                radius_scale=0.05,
            )
        }

        st.sidebar.markdown("### Map Layers")
        selected_layers = [
            layer for name, layer in ALL_LAYERS.items() if st.sidebar.checkbox(name, True)
        ]

        if selected_layers:
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": 37.76,
                    "longitude": -122.4,
                    "zoom": 11,
                    "pitch": 50,
                },
                layers=selected_layers,
            ))
        else:
            st.error("Please select at least one layer.")
    except URLError as e:
        st.error("Connection error: %s" % e.reason)