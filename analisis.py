from catalogo import grupo

def contar_por_tipo(satelites):
    """Devuelve {"LEO": n, "MEO": n, "GEO": n, "HEO": n}.
    Las cuatro claves siempre están presentes (en 0 si no hay de ese tipo).  
    """  
    conteo = {"LEO": 0, "MEO": 0, "GEO": 0, "HEO": 0}
    for satelite in satelites:
        conteo[satelite.tipo_orbita()] += 1
    return conteo

def mas_bajo(satelites):
    """Devuelve el objeto Satelite de menor altitud."""
    mas_bajo_actual = satelites[0]
    for satelite in satelites:
        if satelite.altitud_km < mas_bajo_actual.altitud_km:
            mas_bajo_actual = satelite
    return mas_bajo_actual

def mas_alto(satelites):
    """Devuelve el objeto Satelite de mayor altitud."""
    mas_alto_actual = satelites[0]
    for satelite in satelites:
        if satelite.altitud_km > mas_alto_actual.altitud_km:
            mas_alto_actual = satelite
    return mas_alto_actual

def en_zona(satelites, zona):
    """Devuelve una lista de los satélites dentro de la zona."""
    return [s for s in satelites if s.esta_en_zona(zona)]

def ordenar_por(satelites, atributo, descendente=False):
    """Devuelve una lista nueva ordenada por cualquier atributo."""
    return sorted(satelites, key=lambda s: getattr(s, atributo), reverse=descendente)

def top_n(satelites, n, mas_altos=True):
    """Devuelve los n satélites más altos (si mas_altos=True) o más bajos."""
    ordenados = ordenar_por(satelites, "altitud_km", descendente=mas_altos)
    return ordenados[:n]

def resumen_por_grupo(satelites):
    """Devuelve un diccionario con un resumen de las altitudes de cada grupo."""
    por_grupo = {}
    for satelite in satelites:
        g = grupo(satelite.nombre)
        por_grupo.setdefault(g, []).append(satelite.altitud_km)
    
    resumen = {}
    for g, altitudes in por_grupo.items():
        resumen[g] = {
            "cantidad": len(altitudes),
            "minima": min(altitudes),
            "media": sum(altitudes) / len(altitudes),
            "maxima": max(altitudes),
        }
    return resumen

if __name__ == "__main__":
    from datetime import datetime, timezone
    from catalogo import leer_satelites
    from satelite import Satelite, crear_satelites

    registros = leer_satelites("datos/satelites.json")
    satelites = crear_satelites(registros, datetime.now(timezone.utc))

    # Pruebas generales con datos reales
    conteo = contar_por_tipo(satelites)
    print(conteo, "suma:", sum(conteo.values()), "de", len(satelites))
    print("Más bajo:", mas_bajo(satelites))
    print("Más alto:", mas_alto(satelites))

    # Prueba de top_n (más altos y más bajos)
    print("Top 2 más altos:")
    for s in top_n(satelites, 2, mas_altos=True):
        print(" -", s)
    print("Top 2 más bajos:")
    for s in top_n(satelites, 2, mas_altos=False):
        print(" -", s)

    # Prueba de ordenar_por por nombre (texto)
    print("Primeros 2 ordenados por nombre:")
    for s in ordenar_por(satelites, "nombre")[:2]:
        print(" -", s)

    # Prueba de resumen_por_grupo con datos armados a mano
    prueba_grupo = [
        Satelite("STARLINK-1", 0, 0, 400),
        Satelite("STARLINK-2", 0, 0, 600),
    ]
    print("Resumen grupo prueba:", resumen_por_grupo(prueba_grupo))