import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA

# Cargar los datos históricos del tipo de cambio del dólar
df = pd.read_csv('dolar_bolivia.csv', parse_dates=['Date'], index_col='Date')

# Visualizar la serie de tiempo
df['Exchange Rate'].plot(title='Tipo de Cambio del Dólar en Bolivia', figsize=(10, 6))
plt.show()

# Descomposición de la serie de tiempo
decomposition = seasonal_decompose(df['Exchange Rate'], model='additive', period=30)
decomposition.plot()
plt.show()

# Crear y ajustar el modelo ARIMA
model = ARIMA(df['Exchange Rate'], order=(5, 1, 0))
model_fit = model.fit()

# Predecir los próximos valores
forecast = model_fit.forecast(steps=30)
print(forecast)

# Visualizar la predicción
plt.plot(df.index, df['Exchange Rate'], label='Datos Reales')
plt.plot(pd.date_range(df.index[-1], periods=30, freq='D')[1:], forecast, label='Predicción', color='red')
plt.title('Predicción del Tipo de Cambio del Dólar en Bolivia')
plt.legend()
plt.show()
