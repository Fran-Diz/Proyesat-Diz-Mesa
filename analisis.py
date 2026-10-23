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


if __name__ == "__main__":
    from datetime import datetime, timezone
    from catalogo import leer_satelites
    from satelite import Satelite, crear_satelites

    registros = leer_satelites("Datos/satelites.json")
    satelites = crear_satelites(registros, datetime.now(timezone.utc))
    conteo = contar_por_tipo(satelites)
    print(conteo, "suma:", sum(conteo.values()), "de", len(satelites))
    print("Más bajo:", mas_bajo(satelites))
    print("Más alto:", mas_alto(satelites))
    print(contar_por_tipo([]))
    print(contar_por_tipo([Satelite("x", 0, 0, 400), Satelite("y", 0, 0, 36000)]))