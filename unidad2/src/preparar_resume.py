"""Prepara el CSV local sin modificar filas ni etiquetas."""

from pathlib import Path

import pandas as pd

RUTA_ORIGEN = Path("data/resume.csv")
RUTA_DESTINO = Path("data/resume_limpio.csv")

COLUMNAS_EXCLUIDAS = [
    "rownames",
    "job_ad_id",
    "firstname",
    "resume_quality",
]


def main():
    if not RUTA_ORIGEN.is_file():
        raise FileNotFoundError(
            f"No se encontró {RUTA_ORIGEN}. "
            "Colocá resume.csv dentro de unidad2/data/."
        )

    datos = pd.read_csv(RUTA_ORIGEN)

    if (
        len(datos) != 4870
        or set(datos["received_callback"].unique()) != {0, 1}
    ):
        raise ValueError("Cantidad de filas o etiquetas inesperadas.")

    preparados = datos.drop(columns=COLUMNAS_EXCLUIDAS)
    preparados.to_csv(RUTA_DESTINO, index=False)

    print(f"Archivo generado: {RUTA_DESTINO}")
    print("Filas y columnas:", preparados.shape)
    print(
        datos.groupby("gender")["received_callback"].agg(["count", "mean"])
    )


if __name__ == "__main__":
    main()
