import matplotlib.pyplot as plt
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
        fig.savefig(ruta_guardado)
        plt.close(fig)
    else:
        plt.show()

if __name__ == "__main__":
    # Asegurarse de que la carpeta 'salidas/' exista
    Path("salidas").mkdir(parents=True, exist_ok=True)
    
    registros = leer_satelites("datos/satelites.json")
    
    # 1. Guardar el gráfico de lanzamientos por año
    lanzamientos = lanzamientos_por_anio(registros)
    plot_lanzamientos_por_anio(
        lanzamientos, 
        ruta_guardado="salidas/lanzamientos_por_anio.png"
    )
    
    # 2. Separar Starlink del resto y guardar el gráfico de barras apiladas
    registros_starlink = [r for r in registros if grupo(r["OBJECT_NAME"]) == "Starlink"]
    registros_resto = [r for r in registros if grupo(r["OBJECT_NAME"]) != "Starlink"]
    
    lanzamientos_starlink = lanzamientos_por_anio(registros_starlink)
    lanzamientos_resto = lanzamientos_por_anio(registros_resto)
    
    plot_lanzamientos_apilados(
        lanzamientos_starlink, 
        lanzamientos_resto, 
        ruta_guardado="salidas/lanzamientos_apilados.png"
    )
    
    print("¡Gráficos de la Etapa 2 generados y guardados en salidas/ con éxito!")