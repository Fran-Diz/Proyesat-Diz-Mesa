
# Proyesat-Diz-Mesa

   ## Integrantes
   - Franco Diz
   - Lautaro Mesa

   ## Cómo correr el proyecto
   1. Crear el ambiente: `python3 -m venv .venv`
   2. Activarlo: `source .venv/bin/activate`
   3. Instalar: `pip install skyfield numpy jupyter`



Trabajo Práctico de Programación 1: seguimiento y caracterización de satélites.

Lee un catálogo de satélites en formato JSON (datos de CelesTrak), calcula la posición de cada uno en el momento actual con Skyfield y genera estadísticas: conteo por grupo y por tipo de órbita, lanzamientos por año, altitudes por grupo y satélites sobre una zona geográfica (Bariloche). El análisis se presenta en el notebook informe.ipynb. 



# estructura 

├── README.md
├── .gitignore
├── funciones_base.py   provisto: cálculos con Skyfield
├── catalogo.py         lectura del catálogo, grupos y lanzamientos por año
├── satelite.py         clase Satelite y crear_satelites
├── analisis.py         conteos, extremos, ordenamiento, zonas y resúmenes
├── informe.ipynb       el informe: importa y usa los módulos
└── datos/
    └── satelites.json  provisto: 16.710 satélites 

   

## Integrantes y tareas

**Franco Diz**
- Creó el repositorio y armó el `.gitignore`.
- Agregó los archivos provistos (`funciones_base.py` y `datos/satelites.json`).
- `analisis.py`: `en_zona`, `ordenar_por`, `top_n` y `resumen_por_grupo`.
- Informe: sección 1 (carga de datos).
- README: integrantes y pasos de instalación.

**Lautaro Mesa**
- `catalogo.py`: `leer_satelites`, `anio_lanzamiento`, `grupo`, `contar_por_grupo` y `lanzamientos_por_anio`.
- `satelite.py`: clase `Satelite` y `crear_satelites`.
- `analisis.py`: `contar_por_tipo`, `mas_bajo` y `mas_alto`.
- Informe: secciones 2 a 8 (grupos, lanzamientos por año, tipos de órbita, extremos, comparación de grupos, Bariloche y conclusiones).

# Cómo correr el proyecto 

1. crear el ambiente:

   python3 -m venv .venv 

2. Activarlo (hay que hacerlo en cada terminal nueva): 

   source .venv/bin/activate 

3. Instalar las dependencias:

   pip install skyfield numpy matplotlib jupyterlab

# abribr el informe 

Desde VS Code: abrir la carpeta del proyecto, abrir informe.ipynb y elegir el kernel .venv


# Probar los módulos por separado

Cada módulo tiene pruebas en su bloque if __name__ == "__main__":. Desde la carpeta del repositorio: 

python catalogo.py
python satelite.py
python analisis.py




