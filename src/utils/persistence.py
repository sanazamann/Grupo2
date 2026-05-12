import json

def guardar_json(datos, archivo):

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def cargar_json(archivo):

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)

        return datos

    except FileNotFoundError:
        return []


def guardar_csv(df, archivo):

    df.to_csv(archivo, index=False, encoding="utf-8")