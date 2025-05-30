import os
import pandas as pd
from dotenv import load_dotenv
from geopy.geocoders import GoogleV3
from geopy.extra.rate_limiter import RateLimiter
import folium
import re

# Cargar variables del archivo .env
load_dotenv()
api_key = os.getenv("GOOGLE_MAPS_API_KEY")

def procesar_datos_paste():
    """Procesa el archivo paste.txt y extrae las casillas con sus direcciones"""
    
    # Datos directos del paste.txt (las 53 casillas válidas)
    casillas_data = [
        {"seccion": "356", "domicilio": "calle tungsteno, sin número, colonia san pedro 400, san pedro garza garcía, código postal 66210, san pedro garza garcía, nuevo león."},
        {"seccion": "357", "domicilio": "calle antimonio, número 422, colonia san pedro 400, san pedro garza garcía, código postal 66210, san pedro garza garcía, nuevo león."},
        {"seccion": "358", "domicilio": "calle uranio, número 606, colonia san pedro 400, san pedro garza garcía, código postal 66210, san pedro garza garcía, nuevo león."},
        {"seccion": "359", "domicilio": "calle plan de guadalupe, sin número, colonia revolución, san pedro garza garcía, código postal 66219, san pedro garza garcía, nuevo león."},
        {"seccion": "360", "domicilio": "calle nicéforo zambrano, sin número, colonia vista montaña, san pedro garza garcía, código postal 66216, san pedro garza garcía, nuevo león."},
        {"seccion": "361", "domicilio": "calle alejandro vi, sin número, colonia el obispo, san pedro garza garcía, código postal 66214, san pedro garza garcía, nuevo león."},
        {"seccion": "362", "domicilio": "calle corregidora, sin número, colonia el obispo, san pedro garza garcía, código postal 66214, san pedro garza garcía, nuevo león."},
        {"seccion": "363", "domicilio": "calle antonio díaz soto y gama, número 400, colonia vista montaña, san pedro garza garcía, código postal 66216, san pedro garza garcía, nuevo león."},
        {"seccion": "364", "domicilio": "calle josé vivanco norte, sin número, colonia vista montaña, san pedro garza garcía, código postal 66216, san pedro garza garcía, nuevo león."},
        {"seccion": "365", "domicilio": "calle felipe ángeles, sin número, colonia revolución, san pedro garza garcía, código postal 66219, san pedro garza garcía, nuevo león."},
        {"seccion": "366", "domicilio": "calle cobalto, sin número, colonia san pedro 400, san pedro garza garcía, código postal 66210, san pedro garza garcía, nuevo león."},
        {"seccion": "367", "domicilio": "calle platino, sin número, colonia san pedro 400, san pedro garza garcía, código postal 66210, san pedro garza garcía, nuevo león."},
        {"seccion": "368", "domicilio": "calle oro, sin número, colonia unidad san pedro, san pedro garza garcía, código postal 66215, san pedro garza garcía, nuevo león."},
        {"seccion": "369", "domicilio": "calle modesto arreola, sin número, colonia los pinos, san pedro garza garcía, código postal 66239, san pedro garza garcía, nuevo león."},
        {"seccion": "370", "domicilio": "calle plan del río, número 261, colonia lucio blanco, san pedro garza garcía, código postal 66218, san pedro garza garcía, nuevo león."},
        {"seccion": "372", "domicilio": "calle 5 de mayo, sin número, colonia los sauces, san pedro garza garcía, código postal 66230, san pedro garza garcía, nuevo león."},
        {"seccion": "373", "domicilio": "calle los rayones, número 504, colonia los sauces, san pedro garza garcía, código postal 66230, san pedro garza garcía, nuevo león."},
        {"seccion": "374", "domicilio": "calle abasolo, número 201 sur, colonia centro, san pedro garza garcía, código postal 66230, san pedro garza garcía, nuevo león."},
        {"seccion": "375", "domicilio": "calle ignacio altamirano, sin número, colonia prados de la sierra, san pedro garza garcía, código postal 66230, san pedro garza garcía, nuevo león."},
        {"seccion": "376", "domicilio": "avenida josé vasconcelos, número 324 poniente, colonia centro, san pedro garza garcía, código postal 66230, san pedro garza garcía, nuevo león."},
        {"seccion": "377", "domicilio": "calle corregidora, sin número, colonia rincón colonial, san pedro garza garcía, código postal 66230, san pedro garza garcía, nuevo león."},
        {"seccion": "378", "domicilio": "calle benito juárez, número 108 norte, colonia centro, san pedro garza garcía, código postal 66230, san pedro garza garcía, nuevo león."},
        {"seccion": "379", "domicilio": "calle reforma, sin número, colonia centro, san pedro garza garcía, código postal 66230, san pedro garza garcía, nuevo león."},
        {"seccion": "380", "domicilio": "calle porfirio díaz, sin número, colonia centro, san pedro garza garcía, código postal 66230, san pedro garza garcía, nuevo león."},
        {"seccion": "381", "domicilio": "calle hermenegildo galeana, número 1207, colonia palo blanco, san pedro garza garcía, código postal 66236, san pedro garza garcía, nuevo león."},
        {"seccion": "383", "domicilio": "calle río mississippi, número 470 poniente, colonia del valle, san pedro garza garcía, código postal 66220, san pedro garza garcía, nuevo león."},
        {"seccion": "384", "domicilio": "calle río amazonas, número 202 poniente, colonia del valle, san pedro garza garcía, código postal 66220, san pedro garza garcía, nuevo león."},
        {"seccion": "385", "domicilio": "avenida fuentes del valle, número 201 poniente, colonia fuentes del valle, san pedro garza garcía, código postal 66220, san pedro garza garcía, nuevo león."},
        {"seccion": "386", "domicilio": "calle vía valeria, número 301, colonia fuentes del valle, san pedro garza garcía, código postal 66220, san pedro garza garcía, nuevo león."},
        {"seccion": "387", "domicilio": "calle río nazas, sin número, colonia valle oriente, san pedro garza garcía, código postal 66220, san pedro garza garcía, nuevo león."},
        {"seccion": "389", "domicilio": "avenida real san agustín, número 100, colonia san agustín campestre, san pedro garza garcía, código postal 66270, san pedro garza garcía, nuevo león."},
        {"seccion": "390", "domicilio": "avenida batallón de san patricio, número 110, colonia residencial san agustín, san pedro garza garcía, código postal 66260, san pedro garza garcía, nuevo león."},
        {"seccion": "391", "domicilio": "calle montes himalaya, sin número, residencial san agustín, san pedro garza garcía, código postal 66260, san pedro garza garcía, nuevo león."},
        {"seccion": "392", "domicilio": "calle río pantepec, sin número, colonia valle de santa engracia, san pedro garza garcía, código postal 66260, san pedro garza garcía, nuevo león."},
        {"seccion": "393", "domicilio": "calle río pánuco, número 449, colonia del valle, san pedro garza garcía, código postal 66220, san pedro garza garcía, nuevo león."},
        {"seccion": "394", "domicilio": "calle vía corso poniente, sin número, colonia fuentes del valle, san pedro garza garcía, código postal 66220, san pedro garza garcía, nuevo león."},
        {"seccion": "395", "domicilio": "calle río moctezuma, sin número, colonia del valle, san pedro garza garcía, código postal 66220, san pedro garza garcía, nuevo león."},
        {"seccion": "396", "domicilio": "avenida gómez morín, número 410, colonia del valle, san pedro garza garcía, código postal 66220, san pedro garza garcía, nuevo león."},
        {"seccion": "397", "domicilio": "avenida la sierra, número 12, colonia sierra madre, san pedro garza garcía, código postal 66250, san pedro garza garcía, nuevo león."},
        {"seccion": "398", "domicilio": "calle bosques del olivo, sin número, colonia bosques del valle segundo sector, san pedro garza garcía, código postal 66220, san pedro garza garcía, nuevo león."},
        {"seccion": "399", "domicilio": "calle río balsas, número 120 sur, colonia del valle, san pedro garza garcía, código postal 66220, san pedro garza garcía, nuevo león."},
        {"seccion": "400", "domicilio": "avenida josé vasconcelos, número 445, colonia del valle, san pedro garza garcía, código postal 66220, san pedro garza garcía, nuevo león."},
        {"seccion": "401", "domicilio": "calle emilio carranza, sin número, colonia centro, san pedro garza garcía, código postal 66230, san pedro garza garcía, nuevo león."},
        {"seccion": "402", "domicilio": "calle san felipe de jesús, sin número, colonia la cima, san pedro garza garcía, código postal 66230, san pedro garza garcía, nuevo león."},
        {"seccion": "403", "domicilio": "calle hermenegildo galeana, sin número, colonia palo blanco, san pedro garza garcía, código postal 66236, san pedro garza garcía, nuevo león."},
        {"seccion": "404", "domicilio": "calle hermenegildo galeana, sin número, colonia palo blanco, san pedro garza garcía, código postal 66236, san pedro garza garcía, nuevo león."},
        {"seccion": "405", "domicilio": "calzada del rosario, número 99, colonia hacienda el rosario, san pedro garza garcía, código postal 66247, san pedro garza garcía, nuevo león."},
        {"seccion": "406", "domicilio": "avenida josé vasconcelos, número 2214 oriente, colonia tampiquito, san pedro garza garcía, código postal 66240, san pedro garza garcía, nuevo león."},
        {"seccion": "407", "domicilio": "calle plutarco elías calles, número 419, colonia tampiquito, san pedro garza garcía, código postal 66240, san pedro garza garcía, nuevo león."},
        {"seccion": "409", "domicilio": "avenida manuel gómez morín, número 1000 sur, colonia carrizalejo, san pedro garza garcía, código postal 66254, san pedro garza garcía, nuevo león."},
        {"seccion": "410", "domicilio": "calle sócrates, sin número, residencial chipinque tercer sector, san pedro garza garcía, código postal 66297, san pedro garza garcía, nuevo león."},
        {"seccion": "413", "domicilio": "privada herradura, sin número, colonia lomas del valle, san pedro garza garcía, código postal 66256, san pedro garza garcía, nuevo león."},
        {"seccion": "416", "domicilio": "calle perseverancia, número 100, colonia balcones del valle, san pedro garza garcía, código postal 66288, san pedro garza garcía, nuevo león."}
    ]
    
    return pd.DataFrame(casillas_data)

def main():
    print("🚀 Iniciando procesamiento de nuevas casillas...")
    
    # Obtener datos procesados
    df = procesar_datos_paste()
    print(f"✅ {len(df)} casillas procesadas")
    
    # Crear columna de dirección completa para geocodificación
    df["DireccionCompleta"] = df["domicilio"] + ", San Pedro Garza García, Nuevo León, México"
    
    # Configurar geocodificador
    if not api_key:
        print("❌ Error: No se encontró GOOGLE_MAPS_API_KEY en el archivo .env")
        print("🔧 Crea un archivo .env con tu API key de Google Maps")
        return
    
    geolocator = GoogleV3(api_key=api_key, timeout=10)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    print("🌍 Iniciando geocodificación...")
    
    # Geocodificación con manejo de errores
    locations = []
    lats = []
    lons = []
    
    for idx, direccion in enumerate(df["DireccionCompleta"]):
        try:
            print(f"Geocodificando {idx+1}/{len(df)}: Sección {df.iloc[idx]['seccion']}")
            location = geocode(direccion)
            
            locations.append(location)
            if location:
                lats.append(location.latitude)
                lons.append(location.longitude)
                print(f"  ✅ Encontrada: {location.latitude}, {location.longitude}")
            else:
                lats.append(None)
                lons.append(None)
                print(f"  ❌ No encontrada")
                
        except Exception as e:
            print(f"  ⚠️ Error: {str(e)}")
            locations.append(None)
            lats.append(None)
            lons.append(None)
    
    # Agregar coordenadas al DataFrame
    df["location"] = locations
    df["lat"] = lats
    df["lon"] = lons
    
    # Guardar datos geocodificados
    df.to_csv("casillas_nuevas_geolocalizadas.csv", index=False)
    print("💾 Datos guardados en casillas_nuevas_geolocalizadas.csv")
    
    # Crear mapa
    casillas_validas = df.dropna(subset=["lat", "lon"])
    print(f"📍 {len(casillas_validas)} casillas geocodificadas exitosamente")
    
    if len(casillas_validas) == 0:
        print("❌ No se pudieron geocodificar direcciones. Verifica tu API key.")
        return
    
    # Calcular centro del mapa
    centro_lat = casillas_validas["lat"].mean()
    centro_lon = casillas_validas["lon"].mean()
    
    print(f"🎯 Centro del mapa: {centro_lat:.4f}, {centro_lon:.4f}")
    
    # Crear mapa con Folium
    mapa = folium.Map(
        location=[centro_lat, centro_lon], 
        zoom_start=13,
        tiles='OpenStreetMap',
        prefer_canvas=False
    )
    
    # Agregar marcadores
    for _, row in casillas_validas.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"<b>Sección {row['seccion']}</b><br>{row['domicilio']}",
            tooltip=f"Sección {row['seccion']}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(mapa)
    
    # Guardar nuevo mapa
    mapa.save("index2.html")
    print("🗺️ Nuevo mapa guardado como index2.html")
    
    # Estadísticas finales
    print("\n📊 RESUMEN:")
    print(f"   Total de casillas: {len(df)}")
    print(f"   Geocodificadas: {len(casillas_validas)}")
    print(f"   Fallidas: {len(df) - len(casillas_validas)}")
    print(f"   Éxito: {len(casillas_validas)/len(df)*100:.1f}%")

if __name__ == "__main__":
    main()