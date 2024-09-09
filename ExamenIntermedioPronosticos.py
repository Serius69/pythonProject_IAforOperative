import pandas as pd
import numpy as np
import os

# Ruta del archivo Excel
excel_file = 'demanda.xlsx'  # Asegúrate de reemplazar esto con la ruta correcta

# Verificar si el archivo existe
if not os.path.exists(excel_file):
    raise FileNotFoundError(f"El archivo '{excel_file}' no existe. Por favor, verifica la ruta.")

try:
    # Leer datos del archivo Excel
    df = pd.read_excel(excel_file)

    print("Columnas en el archivo Excel:")
    print(df.columns.tolist())

    # Convertir los nombres de las columnas a strings
    df.columns = df.columns.astype(str)

    # Verificar que las columnas necesarias existen
    required_columns = ['Mes', '2018', '2019', '2021', '2022']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(
            f"El archivo Excel no contiene las siguientes columnas necesarias: {', '.join(missing_columns)}")

    # Promedio móvil simple (4 años: 2018, 2019, 2021, 2022)
    df['Promedio_Movil_Simple'] = df[['2018', '2019', '2021', '2022']].mean(axis=1)

    # Promedio móvil ponderado (usamos ponderaciones: 0.1 para 2018, 0.2 para 2019, 0.3 para 2021 y 0.4 para 2022)
    weights = [0.1, 0.2, 0.3, 0.4]
    df['Promedio_Movil_Ponderado'] = df[['2018', '2019', '2021', '2022']].dot(weights)

    # Suavizamiento exponencial simple (alpha = 0.3)
    alpha = 0.3
    df['Suavizamiento_Exponencial'] = df['2022'].ewm(alpha=alpha, adjust=False).mean()

    # Mostrar resultados
    print("\nResultados:")
    print(df[['Mes', 'Promedio_Movil_Simple', 'Promedio_Movil_Ponderado', 'Suavizamiento_Exponencial']])

    # Guardar resultados en un nuevo archivo Excel
    output_file = 'resultados_pronostico.xlsx'
    df.to_excel(output_file, index=False)
    print(f"\nLos resultados han sido guardados en '{output_file}'")

except pd.errors.EmptyDataError:
    print(f"El archivo '{excel_file}' está vacío. Por favor, asegúrate de que contiene datos.")
except Exception as e:
    print(f"Ocurrió un error al procesar el archivo: {str(e)}")