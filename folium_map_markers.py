import pandas as pd
import folium

# ---- FILES ----
INPUT_CSV = "hometown_locations_geocoded.csv"
OUTPUT_HTML = "hometown_map_with_markers.html"

# ---- MAPBOX BASEMAP (your style tiles) ----
TILES = (
    "https://api.mapbox.com/styles/v1/kaitlynglenn/"
    "cmm8g8rce00aq01sccthr6vc4/tiles/256/{z}/{x}/{y}@2x"
    "?access_token=pk.eyJ1Ijoia2FpdGx5bmdsZW5uIiwiYSI6ImNtbThueWdwZjEyaDEyd3E1cDhkZjhoMnYifQ.KG8EF_s3FmZuL2rS_tAHTQ"
)

# ---- LOAD DATA ----
df = pd.read_csv(INPUT_CSV, engine="python")

# Safety: drop rows without coordinates
df = df.dropna(subset=["latitude", "longitude"]).copy()

# ---- STYLE RULES BY TYPE ----
# You can edit these based on your class categories
STYLE_BY_TYPE = {
    "Food":      {"color": "red",    "icon": "utensils", "prefix": "fa"},
    "Coffee":    {"color": "green",  "icon": "coffee",   "prefix": "fa"},
    "Beach":     {"color": "blue",   "icon": "water",    "prefix": "fa"},
    "Shopping":  {"color": "purple", "icon": "shopping-bag", "prefix": "fa"},
    "Park":      {"color": "darkgreen", "icon": "tree",  "prefix": "fa"},
    "School":    {"color": "orange", "icon": "graduation-cap", "prefix": "fa"},
}

DEFAULT_STYLE = {"color": "cadetblue", "icon": "map-marker", "prefix": "fa"}

# ---- CENTER MAP ON YOUR DATA ----
center_lat = df["latitude"].mean()
center_lon = df["longitude"].mean()

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=11,
    tiles=None
)

# Add basemap
folium.TileLayer(
    tiles=TILES,
    attr="© Mapbox © OpenStreetMap",
    name="Custom Mapbox Style",
    overlay=False,
    control=True
).add_to(m)

# Optional: group markers by type so you can toggle layers
groups = {}
for t in df["Type"].fillna("Other").unique():
    groups[t] = folium.FeatureGroup(name=str(t), show=True)
    groups[t].add_to(m)

# ---- ADD MARKERS ----
for _, row in df.iterrows():
    name = str(row.get("Name", ""))
    address = str(row.get("Address", ""))
    loc_type = str(row.get("Type", "Other"))
    desc = str(row.get("Description", ""))
    img = str(row.get("Image_URL", "")).strip()

    style = STYLE_BY_TYPE.get(loc_type, DEFAULT_STYLE)

    # Build popup HTML
    popup_html = f"""
    <div style="width: 260px;">
      <h4 style="margin:0 0 6px 0;">{name}</h4>
      <div><b>Type:</b> {loc_type}</div>
      <div><b>Address:</b> {address}</div>
      <div style="margin-top:6px;">{desc}</div>
    """

    if img and img.lower().startswith("http"):
        popup_html += f'<div style="margin-top:8px;"><a href="{img}" target="_blank">Image link</a></div>'

    popup_html += "</div>"

    marker = folium.Marker(
        location=[float(row["latitude"]), float(row["longitude"])],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{name} ({loc_type})",
        icon=folium.Icon(color=style["color"], icon=style["icon"], prefix=style["prefix"]),
    )

    # Add to the right layer
    groups.get(loc_type, groups[list(groups.keys())[0]]).add_child(marker)

# Layer toggle
folium.LayerControl(collapsed=False).add_to(m)

# Save
m.save(OUTPUT_HTML)
print(f"Saved map: {OUTPUT_HTML}")