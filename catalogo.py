import json

GRUPOS = {
    "STARLINK": "Starlink",
    "ONEWEB": "OneWeb",
    "KUIPER": "Kuiper",
    "QIANFAN": "Qianfan",
    "IRIDIUM": "Iridium",
    "GLOBALSTAR": "Globalstar",
    "NAVSTAR": "GPS",
    "BEIDOU": "BeiDou",
}


def leer_satelites(ruta):
    """Lee el archivo JSON y devuelve la lista de registros.

    Si el archivo no existe, imprime un aviso y devuelve una lista vacía.
    """
    try:
        with open(ruta, encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"Aviso: no se encontró el archivo {ruta}")
        return []


def anio_lanzamiento(registro):
    """Devuelve el año de lanzamiento (int) a partir de OBJECT_ID."""
    return int(registro["OBJECT_ID"][:4])


def grupo(nombre):
    """Devuelve el grupo del satélite según cómo empieza su nombre.

    Si no coincide con ningún prefijo, devuelve "Otros".
    """
    for prefijo, nombre_grupo in GRUPOS.items():
        if nombre.startswith(prefijo):
            return nombre_grupo
    return "Otros"


def contar_por_grupo(registros):
    """Devuelve un diccionario {grupo: cantidad de satélites}."""
    conteo = {}
    for registro in registros:
        g = grupo(registro["OBJECT_NAME"])
        conteo[g] = conteo.get(g, 0) + 1
    return conteo


def lanzamientos_por_anio(registros):
    """Devuelve un diccionario {año: cantidad de satélites lanzados ese año}."""
    conteo = {}
    for registro in registros:
        anio = anio_lanzamiento(registro)
        conteo[anio] = conteo.get(anio, 0) + 1
    return conteo


if __name__ == "__main__":
    registros = leer_satelites("datos/satelites.json")
    print(len(registros), "registros")
    iss = [r for r in registros if r["OBJECT_NAME"] == "ISS (ZARYA)"][0]
    print("Año ISS:", anio_lanzamiento(iss))
    print(grupo("STARLINK-1234"), grupo("ISS (ZARYA)"))
    print(contar_por_grupo(registros))
    print(sorted(lanzamientos_por_anio(registros).items())[-5:])
    print(leer_satelites("no_existe.json"))