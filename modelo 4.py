import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt

# Cargar los datos del archivo CSV
df = pd.read_csv('dolar_bolivia.csv')

# Renombrar las columnas para que Prophet pueda trabajar con ellas
df.rename(columns={'Date': 'ds', 'Exchange Rate': 'y'}, inplace=True)

# Crear el modelo Prophet
model = Prophet()
model.fit(df)

# Hacer predicciones para los próximos 30 días
future = model.make_future_dataframe(periods=30)  # Genera fechas futuras
forecast = model.predict(future)  # Hace la predicción

# Visualizar la predicción
model.plot(forecast)
plt.title('Predicción del Tipo de Cambio del Dólar en Bolivia')
plt.show()

# Descomposición de los componentes de la predicción (tendencia, estacionalidad, etc.)
model.plot_components(forecast)
plt.show()
