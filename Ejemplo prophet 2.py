import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Cargar los datos desde un archivo CSV
df = pd.read_csv('data.csv')

# Renombrar las columnas a 'ds' (fecha) y 'y' (valor)
df.rename(columns={'fecha': 'ds', 'valor': 'y'}, inplace=True)

# Crear el modelo Prophet
model = Prophet()

# Ajustar el modelo con los datos
model.fit(df)

# Hacer predicciones para el futuro
future = model.make_future_dataframe(periods=365)  # 365 días en el futuro
forecast = model.predict(future)

# Mostrar las gráficas de las predicciones
fig1 = model.plot(forecast)
plt.show()

# Mostrar los componentes de la predicción
fig2 = model.plot_components(forecast)
plt.show()

# Mostrar las primeras filas del DataFrame de predicción en la consola
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())

