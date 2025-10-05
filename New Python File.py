import re
import json
import webbrowser
import pandas as pd
import os

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
HTML_FILE = "highlighted_map.html"
GEOJSON_FILE = "highlighted_points.geojson"

# -------------------------------------------------------------------
# Read the HTML
# -------------------------------------------------------------------
print("Reading HTML file...")
with open(HTML_FILE, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# -------------------------------------------------------------------
# Parse Folium circle marker definitions
# Folium produces JS like:
#   L.circleMarker([49.25, -123.1], {"radius": 8, ...}).addTo(...);
#   var popup_xxx = L.popup(...).setContent("Value: 30");
# -------------------------------------------------------------------
print("Extracting coordinates and values...")
pattern = re.compile(
    r"L\.circleMarker\(\s*\[([0-9\.\-]+),\s*([0-9\.\-]+)\].*?"
    r"L\.popup\(\).*?setContent\(\"Value:\s*([0-9\.]+)\"\)",
    re.S
)
matches = pattern.findall(html)

if not matches:
    print("No markers found. Double-check that the HTML came from the Folium script I wrote.")
    exit()

print(f"Found {len(matches)} markers.")

# -------------------------------------------------------------------
# Convert to DataFrame
# -------------------------------------------------------------------
df = pd.DataFrame(matches, columns=["lat", "lon", "value"])
df = df.astype(float)

# -------------------------------------------------------------------
# Build GeoJSON
# -------------------------------------------------------------------
features = []
for _, row in df.iterrows():
    features.append({
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [row.lon, row.lat]},
        "properties": {"value": row.value}
    })

geo = {"type": "FeatureCollection", "features": features}

with open(GEOJSON_FILE, "w", encoding="utf-8") as f:
    json.dump(geo, f)

print(f"GeoJSON written to {GEOJSON_FILE}")

# -------------------------------------------------------------------
# Open viewer (Kepler.gl)
# -------------------------------------------------------------------
print("Opening Kepler.gl — upload highlighted_points.geojson when prompted.")
webbrowser.open("https://kepler.gl/")
