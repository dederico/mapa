import os
import pandas as pd
from dotenv import load_dotenv
from geopy.geocoders import GoogleV3
from geopy.extra.rate_limiter import RateLimiter
import folium

# Cargar variables del archivo .env
load_dotenv()
api_key = os.getenv("GOOGLE_MAPS_API_KEY")

# Cargar archivo Excel
df = pd.read_excel("recorrido_casillas_san_pedro.xlsx")

# Crear columna de dirección completa
df["DireccionCompleta"] = df["Domicilio"].astype(str) + ", San Pedro Garza García, Nuevo León, México"

# Configura tu API KEY (mejor usar variable de entorno en producción)
geolocator = GoogleV3(api_key=api_key, timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Geocodificación
df["location"] = df["DireccionCompleta"].apply(geocode)
df["lat"] = df["location"].apply(lambda loc: loc.latitude if loc else None)
df["lon"] = df["location"].apply(lambda loc: loc.longitude if loc else None)

# Guardar como CSV para referencia futura
df.to_csv("casillas_geolocalizadas.csv", index=False)

# Crear mapa con Folium
mapa = folium.Map(location=[25.6579, -100.4026], zoom_start=13)

# Agregar puntos al mapa
for _, row in df.dropna(subset=["lat", "lon"]).iterrows():
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"{row['Ubicación']}<br>{row['Domicilio']}<br>{row['Referencia']}",
        tooltip=row["Ubicación"]
    ).add_to(mapa)

# Guardar HTML
mapa.save("mapa_casillas_san_pedro.html")
print("✅ Mapa guardado como mapa_casillas_san_pedro.html")
