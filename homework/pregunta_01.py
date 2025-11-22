"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
from pathlib import Path

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    # Crear directorio de salida si no existe
    output_dir = Path("files/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Leer el archivo CSV con separador de punto y coma
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", index_col=0)
        
    # Limpiar espacios en blanco al inicio y final de todas las celdas de texto
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    
    # Convertir todo el texto a minúsculas
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.lower()

    # Eliminar caracteres especiales y limpiar formatos
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.replace('_', ' ', regex=False)
        df[col] = df[col].str.replace('-', ' ', regex=False)
        df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
        df[col] = df[col].str.replace('$', '', regex=False)
        df[col] = df[col].str.replace(',', '', regex=False)
        df[col] = df[col].str.replace('.00', '', regex=False)
        df[col] = df[col].str.strip()

    # Limpiar columnas numéricas
    #-- monto_del_credito
    df['monto_del_credito'] = df['monto_del_credito'].astype(float)
    #-- comuna_ciudadano
    df['comuna_ciudadano'] = df['comuna_ciudadano'].astype(int)

    # fecha_de_beneficio
    fecha1 = pd.to_datetime(df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce")
    fecha2 = pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
    df["fecha_de_beneficio"] = fecha1.fillna(fecha2)

    # Eliminar filas completamente duplicadas
    df = df.drop_duplicates()

    # Eliminar filas donde hay valores NaN
    df = df.dropna()

    # Resetear el índice
    df = df.reset_index(drop=True)

    # Guardar el archivo
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";",index=False)