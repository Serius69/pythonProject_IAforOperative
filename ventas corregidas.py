import pandas as pd
import numpy as np

# Cargar los datos desde el archivo CSV
df = pd.read_csv('ventas_con_desfase.csv')

# Reemplazar los ceros con NaN para identificar los valores faltantes
df['ventas'].replace(0, np.nan, inplace=True)

# Calcular la media de los valores adyacentes para rellenar los valores faltantes
df['ventas'].fillna(df['ventas'].mean(), inplace=True)

# Guardar el DataFrame corregido en un nuevo archivo CSV
df.to_csv('ventas_corregidas.csv', index=False)

# Mostrar los primeros registros corregidos en pantalla
print(df.head())
