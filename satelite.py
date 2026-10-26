from funciones_base import crear_objeto_skyfield, obtener_posicion


class Satelite:
    """Guarda la posición de un satélite en un instante."""

    def __init__(self, nombre, latitud, longitud, altitud_km):
        """Guarda los cuatro datos como atributos del objeto."""
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.altitud_km = altitud_km

    def tipo_orbita(self):
        """Devuelve "LEO", "MEO", "GEO" o "HEO" según la altitud."""
        if self.altitud_km < 2000:
            return "LEO"
        elif self.altitud_km < 34000:
            return "MEO"
        elif self.altitud_km <= 37000:
            return "GEO"
        else:
            return "HEO"

    def esta_en_zona(self, zona):
        """True si el satélite está dentro de la zona (lon_min, lat_min, lon_max, lat_max).

        El borde cuenta como adentro.
        """
        lon_min, lat_min, lon_max, lat_max = zona
        return (lon_min <= self.longitud <= lon_max
                and lat_min <= self.latitud <= lat_max)

    def __str__(self):
        """Devuelve un texto como 'ISS (ZARYA) | LEO | 419.7 km'."""
        return f"{self.nombre} | {self.tipo_orbita()} | {self.altitud_km:.1f} km"


def crear_satelites(registros, momento):
    """Devuelve una lista de objetos Satelite con su posición en `momento`.

    Descarta los satélites cuya altitud es menor a 100 km (ya cayeron).
    """
    satelites = []
    for registro in registros:
        objeto = crear_objeto_skyfield(registro)
        latitud, longitud, altitud_km = obtener_posicion(objeto, momento)
        if altitud_km >= 100:
            satelites.append(Satelite(registro["OBJECT_NAME"], latitud, longitud, altitud_km))
    return satelites


if __name__ == "__main__":
    from datetime import datetime, timezone
    from catalogo import leer_satelites

    registros = leer_satelites("datos/satelites.json")
    ahora = datetime.now(timezone.utc)
    satelites = crear_satelites(registros, ahora)
    print(len(registros), "registros ->", len(satelites), "satélites")
    iss = [s for s in satelites if s.nombre == "ISS (ZARYA)"][0]
    print(iss)
    print(iss.esta_en_zona((-180, -90, 180, 90)))
    print(Satelite("x", 0, 0, 36000).tipo_orbita(), Satelite("x", 0, 0, 2000).tipo_orbita(),
          Satelite("x", 0, 0, 37000).tipo_orbita(), Satelite("x", 0, 0, 37001).tipo_orbita())