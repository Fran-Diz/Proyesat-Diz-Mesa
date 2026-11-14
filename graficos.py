import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from catalogo import leer_satelites, lanzamientos_por_anio, grupo

def _configurar_estilo(ax, xlabel, ylabel, titulo, xlim=None):
    """Función auxiliar interna para aplicar formato común a los gráficos."""
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    if xlim:
        ax.set_xlim(xlim)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

def plot_lanzamientos_por_anio(lanzamientos_dict, anio_min=1990, anio_max=2026, ruta_guardado=None):
    """Genera un gráfico de barras simple con los lanzamientos por año."""
    anios = sorted(lanzamientos_dict.keys())
    cantidades = [lanzamientos_dict[anio] for anio in anios]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(anios, cantidades, color='steelblue')
    
    _configurar_estilo(ax, "Año", "Cantidad de satélites lanzados", 
                         "Lanzamientos de satélites por año", (anio_min - 1, anio_max + 1))
    
    fig.tight_layout()
    
    if ruta_guardado:
        Path(ruta_guardado).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(ruta_guardado)
        plt.close(fig)
    else:
        plt.show()

def plot_lanzamientos_apilados(dict1, dict2, label1="Starlink", label2="Resto", 
                                anio_min=1990, anio_max=2026, ruta_guardado=None):
    """
    Recibe dos diccionarios {año: cantidad} y dibuja barras apiladas,
    completando con 0 los años faltantes en cada diccionario.
    """
    anios_unicos = sorted(set(dict1.keys()) | set(dict2.keys()))
    
    vals1 = [dict1.get(anio, 0) for anio in anios_unicos]
    vals2 = [dict2.get(anio, 0) for anio in anios_unicos]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(anios_unicos, vals1, label=label1, color='tab:blue')
    ax.bar(anios_unicos, vals2, bottom=vals1, label=label2, color='tab:orange')
    
    ax.legend()
    _configurar_estilo(ax, "Año", "Cantidad de satélites lanzados", 
                         "Lanzamientos por año: Starlink vs Resto", (anio_min - 1, anio_max + 1))
    
    fig.tight_layout()
    
    if ruta_guardado:
        Path(ruta_guardado).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(ruta_guardado)
        plt.close(fig)
    else:
        plt.show()

def plot_altura_media_por_grupo(resumen, ruta_guardado=None):
    """
    Dibuja barras con la altitud media de cada grupo.

    Recibe lo que devuelve resumen_por_grupo: {grupo: {"media": ..., ...}}.
    Los grupos se ordenan de menor a mayor altitud media.
    """
    pares = sorted((datos["media"], g) for g, datos in resumen.items())
    grupos = [g for media, g in pares]
    medias = [media for media, g in pares]

    fig, ax = plt.subplots(figsize=(10, 5))
    barras = ax.bar(grupos, medias, color='steelblue')
    ax.set_yscale("log")
    ax.bar_label(barras, fmt="%.0f")

    _configurar_estilo(ax, "Grupo", "Altitud media (km, escala logarítmica)",
                       "Altitud media por grupo")

    fig.tight_layout()

    if ruta_guardado:
        Path(ruta_guardado).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(ruta_guardado)
        plt.close(fig)
    else:
        plt.show()

def plot_histograma_altitudes(altitudes, ancho_bin, ruta_guardado=None):
    """
    Genera un histograma de altitudes entre 200 y 2000 km con el ancho de bin indicado.
    Los valores fuera de ese rango son ignorados por los bins especificados.
    """
    bins = np.arange(200, 2000 + ancho_bin, ancho_bin)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(altitudes, bins=bins, color='steelblue', edgecolor='black', alpha=0.8)
    
    _configurar_estilo(ax, "Altitud (km)", "Cantidad de satélites",
                       f"Histograma de altitudes (ancho_bin = {ancho_bin} km)", (200, 2000))
    
    fig.tight_layout()
    
    if ruta_guardado:
        Path(ruta_guardado).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(ruta_guardado)
        plt.close(fig)
    else:
        plt.show()

def plot_histograma_log_altitudes(altitudes, num_bins=50, ruta_guardado=None):

    """Histograma de todas las altitudes con el eje X en escala logarítmica."""
    # Filtro de seguridad para evitar errores con ceros o negativos en log10
    altitudes_validas = [a for a in altitudes if a > 0]
    
    bins = np.logspace(np.log10(min(altitudes_validas)), np.log10(max(altitudes_validas)), num_bins)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(altitudes_validas, bins=bins, color='tab:green', edgecolor='black', alpha=0.8)
    ax.set_xscale("log")
    
    _configurar_estilo(ax, "Altitud (km, escala logarítmica)", "Cantidad de satélites",
                       "Histograma logarítmico de todas las altitudes")
    
    fig.tight_layout()
    
    if ruta_guardado:
        Path(ruta_guardado).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(ruta_guardado)
        plt.close(fig)
    else:
        plt.show()

def plot_histograma_inclinaciones(registros, grupo_filtro=None, ruta_guardado=None):
    """
    Histograma de 'INCLINATION' de 0° a 180°, con bins de 1°.
    Permite filtrar opcionalmente por grupo específico.
    """
    if grupo_filtro:
        regs = [r for r in registros if grupo(r["OBJECT_NAME"]) == grupo_filtro and "INCLINATION" in r]
        titulo = f"Histograma de inclinaciones: {grupo_filtro} (0° a 180°)"
    else:
        regs = [r for r in registros if "INCLINATION" in r]
        titulo = "Histograma de inclinaciones (0° a 180°)"
        
    inclinaciones = [r["INCLINATION"] for r in regs]
    bins = np.arange(0, 181, 1)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(inclinaciones, bins=bins, color='tab:orange', edgecolor='black', alpha=0.8)
    
    _configurar_estilo(ax, "Inclinación (°)", "Cantidad de satélites", titulo, (0, 180))
    
    fig.tight_layout()
    
    if ruta_guardado:
        Path(ruta_guardado).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(ruta_guardado)
        plt.close(fig)
    else:
        plt.show()


if __name__ == "__main__":
    registros = leer_satelites("datos/satelites.json")
    
    # 1. Gráfico de lanzamientos por año
    lanzamientos = lanzamientos_por_anio(registros)
    plot_lanzamientos_por_anio(
        lanzamientos, 
        ruta_guardado="salidas/lanzamientos_por_anio.png"
    )
    
    # 2. Gráfico de barras apiladas (Starlink vs Resto)
    registros_starlink = [r for r in registros if grupo(r["OBJECT_NAME"]) == "Starlink"]
    registros_resto = [r for r in registros if grupo(r["OBJECT_NAME"]) != "Starlink"]
    
    lanzamientos_starlink = lanzamientos_por_anio(registros_starlink)
    lanzamientos_resto = lanzamientos_por_anio(registros_resto)
    
    plot_lanzamientos_apilados(
        lanzamientos_starlink, 
        lanzamientos_resto, 
        ruta_guardado="salidas/lanzamientos_apilados.png"
    )
    
    # 3. Altitud media por grupo
    from datetime import datetime, timezone
    from satelite import crear_satelites
    from analisis import resumen_por_grupo

    satelites = crear_satelites(registros, datetime.now(timezone.utc))
    plot_altura_media_por_grupo(
        resumen_por_grupo(satelites),
        ruta_guardado="salidas/altura_media_por_grupo.png"
    )

    # 4. Histogramas de altitudes en órbita baja
    altitudes_totales = [s.altitud_km for s in satelites]
    
    plot_histograma_altitudes(
        altitudes_totales, 
        ancho_bin=10, 
        ruta_guardado="salidas/histograma_altitudes_10.png"
    )
    
    plot_histograma_altitudes(
        altitudes_totales, 
        ancho_bin=50, 
        ruta_guardado="salidas/histograma_altitudes_50.png"
    )

    # 5. Histograma logarítmico de todas las altitudes
    plot_histograma_log_altitudes(
        altitudes_totales,
        num_bins=50,
        ruta_guardado="salidas/histograma_log_altitudes.png"
    )

    # 6. Histograma de inclinaciones (General, Starlink y GPS)
    plot_histograma_inclinaciones(
        registros,
        ruta_guardado="salidas/histograma_inclinaciones_general.png"
    )
    plot_histograma_inclinaciones(
        registros,
        grupo_filtro="Starlink",
        ruta_guardado="salidas/histograma_inclinaciones_starlink.png"
    )
    plot_histograma_inclinaciones(
        registros,
        grupo_filtro="GPS",
        ruta_guardado="salidas/histograma_inclinaciones_gps.png"
    )

    print("¡Todos los gráficos de la Etapa 2 generados y guardados en salidas/ con éxito!")