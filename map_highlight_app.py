import folium
import pandas as pd

file = pd.read_csv("combinedfrp.csv")

file["EFPM"] = file["frp"]*10.91

# Example data: list of (lat, lon, value)

# Convert to DataFrame for convenience
df = pd.DataFrame(file, columns=['latitude', 'longitude', 'value'])

# Create base map centered roughly on average coordinates
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=10)

# Normalize color based on value
for _, row in df.iterrows():
    color = 'green' if row['value'] < 40 else 'orange' if row['value'] < 70 else 'red'
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=8,
        popup=f"Value: {row['value']}",
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)

# Save map to file
m.save('highlighted_map.html')
print('Map saved as highlighted_map.html')
