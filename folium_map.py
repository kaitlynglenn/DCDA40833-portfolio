import folium

# ----- Mapbox tile URL -----
TILES = (
    "https://api.mapbox.com/styles/v1/kaitlynglenn/"
    "cmm8g8rce00aq01sccthr6vc4/tiles/256/{z}/{x}/{y}@2x"
    "?access_token=pk.eyJ1Ijoia2FpdGx5bmdsZW5uIiwiYSI6ImNtbThueWdwZjEyaDEyd3E1cDhkZjhoMnYifQ.KG8EF_s3FmZuL2rS_tAHTQ"
)

# ----- Create map -----
m = folium.Map(
    location=[33.6846, -117.8265],  # Irvine-ish center
    zoom_start=11,
    tiles=None
)

# ----- Add Mapbox basemap -----
folium.TileLayer(
    tiles=TILES,
    attr="© Mapbox © OpenStreetMap",
    name="Custom Mapbox Style",
    overlay=False,
    control=True
).add_to(m)

# ----- Save map -----
m.save("mapbox_folium_map.html")

print("Map saved as mapbox_folium_map.html")