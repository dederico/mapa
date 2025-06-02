import os
from flask import Flask, send_file, render_template_string, jsonify
import pandas as pd
import json

app = Flask(__name__)

@app.route("/")
def mapa_nuevo():
    """Servir el nuevo mapa index2.html"""
    try:
        return send_file("index2.html")
    except FileNotFoundError:
        return """
        <h1>❌ Mapa no encontrado</h1>
        <p>El archivo <code>index2.html</code> no existe.</p>
        <p>Ejecuta primero <code>python mapa_nuevo.py</code> para generar el mapa.</p>
        <hr>
        <h3>Pasos:</h3>
        <ol>
            <li>Asegúrate de tener tu <code>.env</code> con la API key de Google Maps</li>
            <li>Ejecuta: <code>python mapa_nuevo.py</code></li>
            <li>Luego ejecuta: <code>python app_nuevo.py</code></li>
        </ol>
        """, 404

@app.route("/datos")
def mostrar_datos():
    """Mostrar información sobre las casillas procesadas"""
    try:
        import pandas as pd
        df = pd.read_csv("casillas_nuevas_geolocalizadas.csv")
        
        html = """
        <h1>📊 Datos de Casillas</h1>
        
        <h2>Estadísticas</h2>
        <ul>
            <li><strong>Total de casillas:</strong> {total}</li>
            <li><strong>Geocodificadas exitosamente:</strong> {exitosas}</li>
            <li><strong>Fallidas:</strong> {fallidas}</li>
            <li><strong>Porcentaje de éxito:</strong> {porcentaje:.1f}%</li>
        </ul>
        
        <h2>Casillas por Colonia</h2>
        <ul>
        """.format(
            total=len(df),
            exitosas=len(df.dropna(subset=["lat", "lon"])),
            fallidas=len(df) - len(df.dropna(subset=["lat", "lon"])),
            porcentaje=(len(df.dropna(subset=["lat", "lon"]))/len(df)*100) if len(df) > 0 else 0
        )
        
        # Contar por colonia
        colonias = {}
        for _, row in df.iterrows():
            domicilio = str(row['domicilio']).lower()
            if 'colonia' in domicilio:
                try:
                    colonia_part = domicilio.split('colonia')[1].split(',')[0].strip()
                    if colonia_part not in colonias:
                        colonias[colonia_part] = 0
                    colonias[colonia_part] += 1
                except:
                    pass
        
        for colonia, count in sorted(colonias.items()):
            html += f"<li><strong>{colonia.title()}:</strong> {count} casillas</li>"
        
        html += """
        </ul>
        
        <p><a href="/">← Volver al mapa</a></p>
        """
        
        return html
        
    except FileNotFoundError:
        return """
        <h1>❌ Datos no encontrados</h1>
        <p>El archivo <code>casillas_nuevas_geolocalizadas.csv</code> no existe.</p>
        <p>Ejecuta primero <code>python mapa_nuevo.py</code> para generar los datos.</p>
        """, 404

@app.route("/health")
def health_check():
    """Endpoint de salud"""
    return {
        "status": "ok",
        "message": "Servidor funcionando correctamente",
        "mapa_disponible": os.path.exists("index2.html"),
        "datos_disponibles": os.path.exists("casillas_nuevas_geolocalizadas.csv")
    }

# Agregar estas rutas al final de tu app_nuevo.py existente, antes del if __name__ == "__main__":

@app.route("/tabla")
def tabla_casillas():
    """Mostrar tabla de casillas"""
    try:
        return send_file("tabla.html")
    except FileNotFoundError:
        return """
        <h1>❌ Tabla no encontrada</h1>
        <p>El archivo <code>tabla.html</code> no existe.</p>
        <p>Crea el archivo tabla.html en la misma carpeta.</p>
        """, 404

@app.route("/api/casillas-json")
def casillas_json():
    """API para obtener casillas como JSON para la tabla"""
    try:
        import pandas as pd
        import json
        
        # Cargar desde el CSV que ya genera mapa_nuevo.py
        df = pd.read_csv("casillas_nuevas_geolocalizadas.csv")
        
        # Procesar datos para la tabla
        casillas = []
        for _, row in df.iterrows():
            # Extraer colonia del domicilio
            domicilio = str(row['domicilio']).lower()
            colonia = "Sin especificar"
            if 'colonia ' in domicilio:
                inicio = domicilio.find('colonia ') + 8
                fin = domicilio.find(',', inicio)
                if fin != -1:
                    colonia = domicilio[inicio:fin].strip().title()
            
            # Extraer código postal
            codigo_postal = "Sin especificar"
            if 'código postal ' in domicilio:
                inicio = domicilio.find('código postal ') + 14
                fin = domicilio.find(',', inicio)
                if fin != -1:
                    codigo_postal = domicilio[inicio:fin].strip()
            
            casilla = {
                "seccion": row['seccion'],
                "domicilio": row['domicilio'],
                "colonia": colonia,
                "codigo_postal": codigo_postal,
                "lat": row.get('lat'),
                "lon": row.get('lon')
            }
            casillas.append(casilla)
        
        return jsonify({
            "success": True,
            "total": len(casillas),
            "casillas": casillas
        })
        
    except FileNotFoundError:
        return jsonify({
            "success": False,
            "error": "Archivo de casillas no encontrado. Ejecuta primero python mapa_nuevo.py"
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error: {str(e)}"
        }), 500

@app.route("/api/buscar/<seccion>")
def buscar_seccion(seccion):
    """API para buscar una sección específica"""
    try:
        import pandas as pd
        df = pd.read_csv("casillas_nuevas_geolocalizadas.csv")
        
        # Buscar la sección
        casilla = df[df['seccion'] == seccion]
        
        if not casilla.empty:
            row = casilla.iloc[0]
            
            # Extraer colonia
            domicilio = str(row['domicilio']).lower()
            colonia = "Sin especificar"
            if 'colonia ' in domicilio:
                inicio = domicilio.find('colonia ') + 8
                fin = domicilio.find(',', inicio)
                if fin != -1:
                    colonia = domicilio[inicio:fin].strip().title()
            
            return jsonify({
                "success": True,
                "casilla": {
                    "seccion": row['seccion'],
                    "domicilio": row['domicilio'],
                    "colonia": colonia,
                    "lat": row.get('lat'),
                    "lon": row.get('lon')
                }
            })
        else:
            secciones_disponibles = sorted(df['seccion'].unique())
            return jsonify({
                "success": False,
                "error": f"Sección {seccion} no encontrada",
                "secciones_disponibles": secciones_disponibles.tolist()
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    

@app.route("/ayuda")
def presentacion_ayuda():
    """Servir la presentación de la nueva estructura territorial"""
    try:
        return send_file("ayuda.html")
    except FileNotFoundError:
        return """
        <h1>❌ Presentación no encontrada</h1>
        <p>El archivo <code>ayuda.html</code> no existe en el directorio.</p>
        <p><a href="/">← Volver al inicio</a></p>
        """, 404 
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print("🚀 Iniciando servidor Flask...")
    print(f"📍 Mapa disponible en: http://localhost:{port}/")
    print(f"📊 Datos disponibles en: http://localhost:{port}/datos")
    print(f"❤️ Health check en: http://localhost:{port}/health")
    
    app.run(host="0.0.0.0", port=port, debug=True)