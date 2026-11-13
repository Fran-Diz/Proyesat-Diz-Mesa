# Proyesat-Diz-Mesa

Trabajo Práctico de Programación 1: seguimiento y caracterización de satélites.

El programa lee un catálogo de satélites en formato JSON (datos de CelesTrak), calcula la posición de cada uno en el momento actual con Skyfield y genera estadísticas y gráficos: conteo por grupo y por tipo de órbita, lanzamientos por año, altitudes por grupo, histogramas de altitud e inclinación, satélites sobre una zona geográfica (Bariloche) y el recorrido de la Estación Espacial Internacional (ISS). El análisis se presenta en el notebook `informe.ipynb`.

## Etapas del desarrollo

### Etapa 1: análisis de la población satelital

- Carga del catálogo, cálculo del EPOCH medio y descarte de los objetos con altitud menor a 100 km.
- Identificación de constelaciones y conteo de satélites por grupo.
- Lanzamientos por año.
- Clasificación por tipo de órbita (LEO, MEO, GEO, HEO).
- Satélites más bajos y más altos, y estadísticas de altitud por grupo.
- Satélites sobre la zona de Bariloche.

### Etapa 2: visualización de datos

- Lanzamientos por año, en barras y apiladas (Starlink contra el resto).
- Altitud media por grupo, en escala logarítmica.
- Histogramas de altitudes en órbita baja (bins de 10 y de 50 km) y de todas las altitudes en escala logarítmica.
- Histogramas de inclinaciones de las órbitas (general, Starlink y GPS).
- **Idea propia:** trayectoria de la ISS en las próximas horas y sus pasadas por la zona de Bariloche.

## Integrantes y tareas

**Franco Diz**
- Creó el repositorio y armó el `.gitignore`.
- Agregó los archivos provistos (`funciones_base.py` y `datos/satelites.json`) y actualizó el catálogo de datos.
- `analisis.py`: `en_zona`, `ordenar_por`, `top_n` y `resumen_por_grupo`.
- `graficos.py`: lanzamientos por año (barras y apiladas), histogramas de altitudes, histograma logarítmico e histogramas de inclinaciones.
- `iss_bariloche.py`: búsqueda de la ISS, trayectoria, corte del salto de longitud en 180° y conteo de pasadas por Bariloche.
- Informe: sección 1 (carga de datos).
- README: integrantes, pasos de instalación y descripción de las etapas.

**Lautaro Mesa**
- `catalogo.py`: `leer_satelites`, `anio_lanzamiento`, `grupo`, `contar_por_grupo` y `lanzamientos_por_anio`.
- `satelite.py`: clase `Satelite` y `crear_satelites`.
- `analisis.py`: `contar_por_tipo`, `mas_bajo` y `mas_alto`.
- `graficos.py`: `plot_altura_media_por_grupo`.
- Informe: secciones 2 a 8 (Etapa 1), secciones 9 a 13 (gráficos de la Etapa 2) y sección 14 (la ISS).
- README: versión completa y actualizaciones.

## Estructura del proyecto

```text
├── README.md
├── .gitignore
├── funciones_base.py   provisto: cálculos con Skyfield
├── catalogo.py         lectura del catálogo, grupos y lanzamientos por año
├── satelite.py         clase Satelite y crear_satelites
├── analisis.py         conteos, extremos, ordenamiento, zonas y resúmenes
├── graficos.py         gráficos con Matplotlib (Etapa 2)
├── iss_bariloche.py    trayectoria de la ISS y pasadas por Bariloche (idea propia)
├── informe.ipynb       el informe: importa y usa los módulos
├── datos/
│   └── satelites.json  catálogo provisto por la cátedra
└── salidas/            figuras generadas por graficos.py e iss_bariloche.py
```

## Cómo correr el proyecto

Desde la carpeta del repositorio:

1. Crear el ambiente:

   ```bash
   python3 -m venv .venv
   ```

2. Activarlo (hay que hacerlo en cada terminal nueva):

   ```bash
   source .venv/bin/activate
   ```

   En Windows: `.venv\Scripts\activate`.

3. Instalar las dependencias:

   ```bash
   pip install skyfield numpy matplotlib jupyterlab
   ```

### Abrir el informe

Desde VS Code: abrir la carpeta del proyecto, abrir `informe.ipynb` y elegir el kernel `.venv`. Para regenerar todas las salidas: Restart & Run All.

También se puede abrir desde la terminal, con el ambiente activado:

```bash
python -m jupyterlab
```

### Generar los gráficos

```bash
python graficos.py
python iss_bariloche.py
```

`graficos.py` guarda en `salidas/` los gráficos de la Etapa 2 e `iss_bariloche.py` guarda el de la ISS:

| Archivo | Qué muestra |
|---|---|
| `lanzamientos_por_anio.png` | cantidad de satélites lanzados por año |
| `lanzamientos_apilados.png` | lo mismo, separando Starlink del resto |
| `altura_media_por_grupo.png` | altitud media de cada grupo |
| `histograma_altitudes_10.png` y `histograma_altitudes_50.png` | altitudes entre 200 y 2.000 km, con bins de 10 y de 50 km |
| `histograma_log_altitudes.png` | todas las altitudes, en escala logarítmica |
| `histograma_inclinaciones_general.png`, `_starlink.png` y `_gps.png` | inclinación de las órbitas, general y por grupo |
| `iss_bariloche.png` | trayectoria de la ISS, su posición actual y la zona de Bariloche |

### Probar los módulos por separado

Cada módulo tiene pruebas en su bloque `if __name__ == "__main__":`. Desde la carpeta del repositorio:

```bash
python catalogo.py
python satelite.py
python analisis.py
```

## Notas

- Las posiciones se calculan para el momento en que se corre el código, así que algunos números (por ejemplo, la cantidad de satélites por tipo de órbita o sobre Bariloche) cambian levemente entre corridas.
- Los datos describen la órbita de cada satélite en una fecha (EPOCH): cuanto más lejos de esa fecha se calcula, menos exacta es la posición. Por eso conviene usar el catálogo más reciente.
- Los lanzamientos por año son una estimación: el archivo solo incluye los satélites activos hoy.
- El ambiente `.venv` no se sube al repositorio (está en `.gitignore`).
