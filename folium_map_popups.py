import pandas as pd
import folium

INPUT_CSV = "hometown_locations_geocoded.csv"
OUTPUT_HTML = "hometown_map_popups.html"

# Your Mapbox basemap tiles (style tiles URL)
TILES = (
    "https://api.mapbox.com/styles/v1/kaitlynglenn/"
    "cmm8g8rce00aq01sccthr6vc4/tiles/256/{z}/{x}/{y}@2x"
    "?access_token=pk.eyJ1Ijoia2FpdGx5bmdsZW5uIiwiYSI6ImNtbThueWdwZjEyaDEyd3E1cDhkZjhoMnYifQ.KG8EF_s3FmZuL2rS_tAHTQ"
)

# Marker styles by Type (edit to match your exact Type values)
STYLE_BY_TYPE = {
    "School":      {"color": "red",    "icon": "pencil", "prefix": "fa"},
    "Restaurant":    {"color": "green",  "icon": "utensils",   "prefix": "fa"},
    "Beach":     {"color": "blue",   "icon": "water",    "prefix": "fa"},
    "Shopping Mall":  {"color": "purple", "icon": "shopping-bag", "prefix": "fa"},
    "Store":      {"color": "pink", "icon": "shopping-bag",  "prefix": "fa"},
    "Bar":      {"color": "darkgreen", "icon": "glass-whiskey",  "prefix": "fa"},
    "Hotel":      {"color": "lightblue", "icon": "hotel",  "prefix": "fa"},
    "Movie Theater":      {"color": "orange", "icon": "film",  "prefix": "fa"},
}
DEFAULT_STYLE = {"color": "cadetblue", "icon": "map-marker", "prefix": "fa"}

df = pd.read_csv(INPUT_CSV, engine="python")

print("TYPES IN CSV:", sorted(df["Type"].dropna().unique()))
# keep only rows with coords
df = df.dropna(subset=["latitude", "longitude"]).copy()

# center map on mean coords
m = folium.Map(
    location=[df["latitude"].mean(), df["longitude"].mean()],
    zoom_start=11,
    tiles=None
)

# add basemap
folium.TileLayer(
    tiles=TILES,
    attr="© Mapbox © OpenStreetMap",
    name="Custom Mapbox Style",
    overlay=False,
    control=True
).add_to(m)

# optional: layer groups by Type
groups = {}
for t in df["Type"].fillna("Other").unique():
    groups[t] = folium.FeatureGroup(name=str(t), show=True)
    groups[t].add_to(m)

def build_popup_html(name, desc, img_url):
    # basic HTML escaping for safety
    name = "" if pd.isna(name) else str(name)
    desc = "" if pd.isna(desc) else str(desc)
    img_url = "" if pd.isna(img_url) else str(img_url).strip()

    # embed image if url exists
    img_html = ""
    if img_url.lower().startswith("http"):
        img_html = f"""
        <div style="margin-top:8px;">
          <img src="{img_url}" style="width: 100%; max-width: 260px; border-radius: 10px;" />
        </div>
        """

    html = f"""
    <div style="width: 280px;">
      <h4 style="margin:0 0 6px 0;">{name}</h4>
      <div style="font-size: 13px; line-height: 1.3;">{desc}</div>
      {img_html}
    </div>
    """
    return html

for _, row in df.iterrows():
    name = row.get("Name", "")
    loc_type = row.get("Type", "Other")
    desc = row.get("Description", "")
    img_url = row.get("Image_URL", "")

    style = STYLE_BY_TYPE.get(str(loc_type), DEFAULT_STYLE)

    popup_html = build_popup_html(name, desc, img_url)

    marker = folium.Marker(
        location=[float(row["latitude"]), float(row["longitude"])],
        tooltip=f"{name}",
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color=style["color"], icon=style["icon"], prefix=style["prefix"]),
    )

    groups.get(loc_type, groups[list(groups.keys())[0]]).add_child(marker)

folium.LayerControl(collapsed=False).add_to(m)

m.save(OUTPUT_HTML)
print(f"Saved: {OUTPUT_HTML}")