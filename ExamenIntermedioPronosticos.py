import pandas as pd
import numpy as np

# Leer datos del archivo Excel
# Asegúrate de reemplazar 'ruta_del_archivo.xlsx' con la ruta real de tu archivo Excel
df = pd.read_excel('ruta_del_archivo.xlsx')

# Verificar que las columnas necesarias existen
required_columns = ['Mes', '2018', '2019', '2021', '2022']
if not all(column in df.columns for column in required_columns):
    raise ValueError("El archivo Excel no contiene todas las columnas necesarias")

# Promedio móvil simple (4 años: 2018, 2019, 2021, 2022)
df['Promedio_Movil_Simple'] = df[['2018', '2019', '2021', '2022']].mean(axis=1)

# Promedio móvil ponderado (usamos ponderaciones: 0.1 para 2018, 0.2 para 2019, 0.3 para 2021 y 0.4 para 2022)
weights = [0.1, 0.2, 0.3, 0.4]
df['Promedio_Movil_Ponderado'] = df[['2018', '2019', '2021', '2022']].dot(weights)

# Suavizamiento exponencial simple (alpha = 0.3)
alpha = 0.3
df['Suavizamiento_Exponencial'] = df['2022'].ewm(alpha=alpha, adjust=False).mean()

# Mostrar resultados
print(df[['Mes', 'Promedio_Movil_Simple', 'Promedio_Movil_Ponderado', 'Suavizamiento_Exponencial']])

# Guardar resultados en un nuevo archivo Excel
# Asegúrate de reemplazar 'resultados_pronostico.xlsx' con el nombre que desees para tu archivo de salida
df.to_excel('resultados_pronostico.xlsx', index=False)

print("Los resultados han sido guardados en 'resultados_pronostico.xlsx'")