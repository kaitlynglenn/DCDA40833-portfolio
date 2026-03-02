import os
import urllib.parse
import requests
import pandas as pd

INPUT_CSV = "hometown_locations.csv"
OUTPUT_CSV = "hometown_locations_geocoded.csv"
ADDRESS_COLUMN = "Address"  # <-- change if your column name is different

access_token = "pk.eyJ1Ijoia2FpdGx5bmdsZW5uIiwiYSI6ImNtbThueWdwZjEyaDEyd3E1cDhkZjhoMnYifQ.KG8EF_s3FmZuL2rS_tAHTQ"
if not access_token:
    raise ValueError('Missing token. In terminal run: export MAPBOX_ACCESS_TOKEN="pk_..."')

print("Loaded token: YES")  # doesn't print the token
df = pd.read_csv(INPUT_CSV, engine="python")
print("Columns:", list(df.columns))
print("Rows/Cols:", df.shape)

if ADDRESS_COLUMN not in df.columns:
    raise ValueError(f"Address column '{ADDRESS_COLUMN}' not found.")

def geocode(address: str):
    q = urllib.parse.quote(str(address))
    url = f"https://api.mapbox.com/search/geocode/v6/forward?q={q}&access_token={access_token}"

    r = requests.get(url, timeout=20)
    print("Status:", r.status_code, "| address:", address)

    if r.status_code != 200:
        print("Response (first 200 chars):", r.text[:200])
        return None, None

    data = r.json()
    features = data.get("features", [])
    if not features:
        print("NO MATCH")
        return None, None

    coords = features[0].get("geometry", {}).get("coordinates")
    print("MATCH coords:", coords)

    lon, lat = coords[0], coords[1]
    return lat, lon

lats, lons = [], []

for idx, addr in enumerate(df[ADDRESS_COLUMN].tolist()):
    # print only first 5 for debugging
    if idx < 5:
        print("\n--- Geocoding row", idx, "---")

    lat, lon = geocode(addr)
    lats.append(lat)
    lons.append(lon)

df["latitude"] = lats
df["longitude"] = lons

print("\nPreview with coords:")
print(df[[ADDRESS_COLUMN, "latitude", "longitude"]].head(10))

df.to_csv(OUTPUT_CSV, index=False)
print("\nSaved:", OUTPUT_CSV)