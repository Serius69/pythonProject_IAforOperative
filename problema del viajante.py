import itertools
import random

# Distancias entre las ciudades (ejemplo con 4 ciudades)
distancias = {
    ('A', 'B'): 10,
    ('A', 'C'): 15,
    ('A', 'D'): 20,
    ('B', 'C'): 35,
    ('B', 'D'): 25,
    ('C', 'D'): 30
}

# Funcion para calcular la distancia total de una ruta
def calcular_distancia(ruta, distancias):
    distancia_total = 0
    for i in range(len(ruta) - 1):
        distancia_total += distancias.get((ruta[i], ruta[i+1]), distancias.get((ruta[i+1], ruta[i]), float('inf')))
    # Volver a la ciudad de origen
    distancia_total += distancias.get((ruta[-1], ruta[0]), distancias.get((ruta[0], ruta[-1]), float('inf')))
    return distancia_total

# Lista de ciudades
ciudades = ['A', 'B', 'C', 'D']

# Número de iteraciones para la búsqueda aleatoria
iteraciones = 1000

# Búsqueda aleatoria de la mejor ruta
mejor_ruta = None
mejor_distancia = float('inf')

for _ in range(iteraciones):
    ruta_aleatoria = random.sample(ciudades, len(ciudades))
    distancia = calcular_distancia(ruta_aleatoria, distancias)
    if distancia < mejor_distancia:
        mejor_distancia = distancia
        mejor_ruta = ruta_aleatoria

# Mostrar el resultado
print(f"La mejor ruta encontrada es: {mejor_ruta} con una distancia de {mejor_distancia} unidades.")
