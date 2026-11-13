import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from datetime import datetime, timezone
from pathlib import Path

from catalogo import leer_satelites
from funciones_base import (
    crear_objeto_skyfield,
    obtener_posicion,
    obtener_trayectoria
)

# Zona de Bariloche exportable para ser importada desde otros lados del proyecto
BARILOCHE = (-76.30, -46.13, -66.30, -36.13)

def buscar_iss(registros):
    """
    Busca el registro exacto de la ISS utilizando su NORAD_CAT_ID oficial (25544),
    evitando coincidencias erróneas por texto parcial en el nombre.
    """
    for reg in registros:
        norad_id = reg.get('NORAD_CAT_ID') or reg.get('norad_cat_id')
        if norad_id == 25544 or str(norad_id) == '25544':
            print(f"Objeto encontrado por NORAD ID: {reg.get('OBJECT_NAME', 'ISS')}")
            return reg
            
    print("Aviso: No se encontró por ID 25544, buscando por nombre exacto...")
    for reg in registros:
        nombre = reg.get('OBJECT_NAME', reg.get('name', '')).upper()
        if nombre.strip() == 'ISS (ZARYA)' or nombre.strip() == 'ISS':
            return reg
            
    return None

def cortar_saltos_longitud(lons, lats, umbral=180):
    """
    Inserta un NaN cuando la longitud salta de +180 a -180 
    para evitar que Matplotlib dibuje una línea cruzando todo el mapa.
    """
    lons_corte = []
    lats_corte = []
    
    for i in range(len(lons)):
        if i > 0 and abs(lons[i] - lons[i - 1]) > umbral:
            lons_corte.append(np.nan)
            lats_corte.append(np.nan)
        lons_corte.append(lons[i])
        lats_corte.append(lats[i])
        
    return np.array(lons_corte), np.array(lats_corte)

def evaluar_zona_bariloche(lats, lons, zona=BARILOCHE):
    """
    Recibe los arrays de latitudes y longitudes de la trayectoria y la zona geográfica.
    Calcula la cantidad total de minutos dentro de la zona y cuántas 'pasadas' realizó
    (contando como pasada cada ingreso desde el exterior hacia el interior).
    """
    lon_min, lat_min, lon_max, lat_max = zona
    
    minutos_dentro = 0
    pasadas = 0
    dentro_anterior = False
    
    for lat, lon in zip(lats, lons):
        actual_dentro = (lon_min <= lon <= lon_max) and (lat_min <= lat <= lat_max)
        
        if actual_dentro:
            minutos_dentro += 1
            if not dentro_anterior:
                pasadas += 1
                
        dentro_anterior = actual_dentro
        
    return minutos_dentro, pasadas

def procesar_datos_iss(ruta_json="datos/satelites.json", horas=4):
    """
    Procesa los datos del catálogo, calcula la posición actual, la trayectoria,
    los días transcurridos desde el EPOCH y evalúa el paso por la zona de Bariloche.
    """
    registros = leer_satelites(ruta_json)
    reg_iss = buscar_iss(registros)
    
    if not reg_iss:
        print("Error: No se encontró la ISS en el catálogo.")
        return None

    obj_iss = crear_objeto_skyfield(reg_iss)
    momento_actual = datetime.now(timezone.utc)
    
    # Posición actual y trayectoria
    lat_act, lon_act, alt_act = obtener_posicion(obj_iss, momento_actual)
    lats, lons, alts = obtener_trayectoria(obj_iss, momento_actual, horas=horas, paso_min=1)

    # Evaluación del paso por Bariloche
    minutos_zona, num_pasadas = evaluar_zona_bariloche(lats, lons, BARILOCHE)

    # Cálculo exacto de días transcurridos desde el EPOCH
    dias_transcurridos = None
    if 'EPOCH' in reg_iss:
        epoch_str = reg_iss['EPOCH']
        epoch_dt = datetime.fromisoformat(epoch_str.replace('Z', '+00:00'))
        if epoch_dt.tzinfo is None:
            epoch_dt = epoch_dt.replace(tzinfo=timezone.utc)
        dias_transcurridos = (momento_actual - epoch_dt).days

    return {
        "registro": reg_iss,
        "lat_act": lat_act,
        "lon_act": lon_act,
        "alt_act": alt_act,
        "lats": lats,
        "lons": lons,
        "alts": alts,
        "dias_transcurridos": dias_transcurridos,
        "minutos_zona": minutos_zona,
        "num_pasadas": num_pasadas
    }

def plotear_trayectoria_iss(datos, ruta_guardado="salidas/iss_bariloche.png"):
    """
    Recibe el diccionario de datos y genera el gráfico de la trayectoria,
    la posición actual y la zona de Bariloche.
    """
    if not datos:
        print("No hay datos disponibles para graficar.")
        return

    lats = datos["lats"]
    lons = datos["lons"]
    lat_act = datos["lat_act"]
    lon_act = datos["lon_act"]
    dias = datos["dias_transcurridos"]

    lons_graf, lats_graf = cortar_saltos_longitud(lons, lats)

    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(lons_graf, lats_graf, color='tab:blue', label='Trayectoria propagada', linewidth=1.5)
    ax.scatter([lon_act], [lat_act], color='red', zorder=5, label='Posición Actual')

    rect = Rectangle(
        (BARILOCHE[0], BARILOCHE[1]), 
        BARILOCHE[2] - BARILOCHE[0], 
        BARILOCHE[3] - BARILOCHE[1],
        linewidth=1.5, edgecolor='tab:orange', facecolor='tab:orange', alpha=0.3, label='Zona Bariloche'
    )
    ax.add_patch(rect)

    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_xlabel("Longitud (°)")
    ax.set_ylabel("Latitud (°)")
    
    titulo = "Seguimiento de la ISS y zona de Bariloche"
    if dias is not None:
        titulo += f" (Datos a {dias} días del Epoch)"
    ax.set_title(titulo)
    
    ax.legend(loc='lower left')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    fig.tight_layout()
    
    if ruta_guardado:
        Path(ruta_guardado).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(ruta_guardado)
        plt.close(fig)
        print(f"Gráfico guardado en {ruta_guardado}")
    else:
        plt.show()

if __name__ == "__main__":
    datos_iss = procesar_datos_iss(horas=4)
    if datos_iss:
        print(f"Posición actual -> Lat: {datos_iss['lat_act']:.2f}°, Lon: {datos_iss['lon_act']:.2f}°, Alt: {datos_iss['alt_act']:.2f} km")
        print(f"Minutos en Bariloche: {datos_iss['minutos_zona']} | Pasadas: {datos_iss['num_pasadas']}")
        if datos_iss['dias_transcurridos'] is not None:
            print(f"Aviso: Han transcurrido {datos_iss['dias_transcurridos']} días desde el epoch del catálogo.")
        plotear_trayectoria_iss(datos_iss)
