import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pandas.plotting import register_matplotlib_converters

# Registrar convertidores para evitar advertencias de matplotlib
register_matplotlib_converters()

# Cargar el archivo CSV
df = pd.read_csv('series_de_tiempo_ejemplo.csv', parse_dates=['Date'], index_col='Date')

# Visualizar la serie de tiempo
df['Value'].plot(title='Serie de Tiempo', figsize=(10, 6))
plt.show()

# Crear el modelo ARIMA
model = ARIMA(df['Value'], order=(5, 1, 0))  # Parámetros p=5, d=1, q=0
model_fit = model.fit()

# Predecir los próximos 10 días
forecast = model_fit.forecast(steps=10)

# Mostrar la predicción
print("Predicción para los próximos 10 días:")
print(forecast)

# Visualizar la predicción junto con los datos reales
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Value'], label='Datos Reales')
plt.plot(pd.date_range(df.index[-1], periods=10, freq='D')[1:], forecast, label='Predicción', color='red')
plt.title('Predicción de Serie de Tiempo')
plt.legend()
plt.show()
