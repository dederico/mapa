# 🗺️ Mapa de Casillas Electorales - San Pedro Garza García

Sistema actualizado para geocodificar y visualizar casillas electorales usando los datos más recientes.

## 📋 Descripción

Este proyecto geocodifica direcciones de casillas electorales en San Pedro Garza García y las visualiza en un mapa interactivo usando:
- **53 casillas** de las secciones 356-417
- API de Google Maps para geocodificación
- Folium para la visualización
- Flask para el servidor web

## 🚀 Instalación

### 1. Clonar repositorio
```bash
git clone <tu-repositorio>
cd <nombre-del-proyecto>
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar API Key de Google Maps
```bash
# Copiar el template
cp .env.template .env

# Editar .env y agregar tu API key
GOOGLE_MAPS_API_KEY="tu-api-key-aqui"
```

> 💡 **Obtener API Key**: Ve a [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials → Create API Key → Habilita "Geocoding API"

## 📍 Uso

### 1. Generar el mapa
```bash
python mapa_nuevo.py
```

Esto hará:
- ✅ Procesar las 53 casillas del archivo `paste.txt`
- 🌍 Geocodificar todas las direcciones
- 💾 Guardar datos en `casillas_nuevas_geolocalizadas.csv`
- 🗺️ Crear mapa interactivo `index2.html`

### 2. Ejecutar servidor web
```bash
python app_nuevo.py
```

### 3. Abrir en navegador
- **Mapa**: http://localhost:5000/
- **Estadísticas**: http://localhost:5000/datos
- **Health Check**: http://localhost:5000/health

## 📊 Datos

### Secciones incluidas
El sistema procesa **53 casillas** de las secciones:
- 356-370 (excepto 371)
- 372-381 (excepto 382)
- 383-387 (excepto 388)
- 389-407 (excepto 408)
- 409-410, 413, 416 (excepto 411, 412, 414, 415, 417)

### Colonias principales
- San Pedro 400
- Vista Montaña  
- Del Valle
- Centro
- Revolución
- Fuentes del Valle
- Y muchas más...

## 🗂️ Estructura de archivos

```
proyecto/
├── mapa_nuevo.py              # 🔄 Script principal de geocodificación
├── app_nuevo.py               # 🌐 Servidor Flask
├── paste.txt                  # 📄 Datos fuente de casillas
├── requirements.txt           # 📦 Dependencias
├── .env.template             # 🔧 Template de configuración
├── .env                      # 🔐 Configuración (no incluido en git)
├── .gitignore               # 🚫 Archivos ignorados
├── README.md                # 📖 Esta documentación
│
├── casillas_nuevas_geolocalizadas.csv  # 📊 Datos procesados
└── index2.html              # 🗺️ Mapa interactivo generado
```

## 🔧 Solución de problemas

### Error de API Key
```
❌ Error: No se encontró GOOGLE_MAPS_API_KEY en el archivo .env
```
**Solución**: Verifica que el archivo `.env` existe y contiene la API key correcta.

### Error de geocodificación
```
⚠️ Error: The provided API key is invalid
```
**Solución**: 
1. Verifica que la API key es correcta
2. Asegúrate de que "Geocoding API" está habilitada en Google Cloud
3. Revisa que no hay restricciones de IP en la API key

### Mapa no se carga
```
❌ Mapa no encontrado
```
**Solución**: Ejecuta `python mapa_nuevo.py` primero para generar `index2.html`

## 📈 Estadísticas típicas

Después de ejecutar el script, normalmente obtienes:
- ✅ **45-50 casillas** geocodificadas exitosamente (~85-95%)
- ❌ **3-8 casillas** que fallan (direcciones ambiguas)
- ⏱️ **Tiempo total**: 2-3 minutos (con rate limiting)

## 🆕 Cambios respecto a la versión anterior

- ✅ **Datos completamente nuevos** de 53 casillas
- ✅ **Archivo de salida independiente** (`index2.html`)
- ✅ **Sin dependencia de Excel** - datos directos en código
- ✅ **Mejor manejo de errores** en geocodificación
- ✅ **Estadísticas más detalladas**
- ✅ **Endpoints adicionales** para monitoreo

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

**🎯 Listo para usar!** Ejecuta `python mapa_nuevo.py` seguido de `python app_nuevo.py` y abre http://localhost:5000