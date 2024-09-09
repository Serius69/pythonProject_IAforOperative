import random
import numpy as np
from deap import base, creator, tools, algorithms

# Parámetros del problema
NUM_CIUDADES = 6
CAPACIDAD_VEHICULO = 100

# Matriz de distancias entre ubicaciones
distancias = np.array([
    [0, 29, 20, 21, 16, 31],
    [29, 0, 15, 29, 28, 40],
    [20, 15, 0, 15, 14, 25],
    [21, 29, 15, 0, 13, 40],
    [16, 28, 14, 13, 0, 35],
    [31, 40, 25, 40, 35, 0]
])

# Demandas de cada cliente
demandas = [0, 10, 20, 30, 40, 50]  # El depósito no tiene demanda

# Ventanas de tiempo (mínimo, máximo) para cada cliente
ventanas_de_tiempo = [(0, 5), (1, 3), (2, 7), (4, 9), (6, 12), (5, 10)]

# Función para calcular la distancia total de una ruta, considerando las restricciones de capacidad y tiempo
def calcular_distancia(ruta):
    distancia_total = 0
    capacidad_restante = CAPACIDAD_VEHICULO
    tiempo_actual = 0
    
    for i in range(len(ruta) - 1):
        # Verificar capacidad
        if capacidad_restante < demandas[ruta[i+1]]:
            return float('inf'),  # Penalización por exceder la capacidad
        
        capacidad_restante -= demandas[ruta[i+1]]
        distancia_total += distancias[ruta[i]][ruta[i+1]]
        tiempo_actual += distancias[ruta[i]][ruta[i+1]]  # Suponiendo que la distancia es proporcional al tiempo

        # Verificar ventana de tiempo
        if tiempo_actual < ventanas_de_tiempo[ruta[i+1]][0] or tiempo_actual > ventanas_de_tiempo[ruta[i+1]][1]:
            return float('inf'),  # Penalización por incumplir ventanas de tiempo
    
    # Regreso al depósito
    distancia_total += distancias[ruta[-1]][ruta[0]]
    return distancia_total,

# Configuración del algoritmo genético
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individuo", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Registro de los operadores
toolbox.register("indices", random.sample, range(NUM_CIUDADES), NUM_CIUDADES)
toolbox.register("individuo", tools.initIterate, creator.Individuo, toolbox.indices)
toolbox.register("poblacion", tools.initRepeat, list, toolbox.individuo)

toolbox.register("evaluate", calcular_distancia)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Parámetros del algoritmo
def main():
    random.seed(42)
    
    # Crear la población inicial
    poblacion = toolbox.poblacion(n=100)
    
    # Aplicamos el algoritmo genético
    num_generaciones = 300
    prob_cruce = 0.7
    prob_mutacion = 0.2
    
    # Usamos el algoritmo genético con la población inicial, cruce y mutación
    result, log = algorithms.eaSimple(poblacion, toolbox, cxpb=prob_cruce, mutpb=prob_mutacion, ngen=num_generaciones, verbose=False)
    
    # Encontramos el mejor individuo
    mejor_individuo = tools.selBest(poblacion, 1)[0]
    print("La mejor ruta encontrada es:", mejor_individuo)
    print("Con una distancia de:", calcular_distancia(mejor_individuo)[0])

if __name__ == "__main__":
    main()
