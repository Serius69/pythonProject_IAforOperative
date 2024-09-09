from ortools.constraint_solver import pywrapcp, routing_enums_pb2

def create_data_model():
    """Crear los datos para el problema."""
    data = {}
    # Matriz de distancias (Ejemplo con 6 ubicaciones: depósito y 5 clientes)
    data['distance_matrix'] = [
        [0, 29, 20, 21, 16, 31],
        [29, 0, 15, 29, 28, 40],
        [20, 15, 0, 15, 14, 25],
        [21, 29, 15, 0, 13, 40],
        [16, 28, 14, 13, 0, 35],
        [31, 40, 25, 40, 35, 0],
    ]
    # Capacidad del vehículo
    data['vehicle_capacities'] = [100]
    # Demandas en cada ubicación
    data['demands'] = [0, 10, 20, 10, 20, 30]
    # Número de vehículos
    data['num_vehicles'] = 1
    # Depósito inicial (central de distribución)
    data['depot'] = 0
    return data

def print_solution(manager, routing, solution):
    """Imprimir la solución."""
    print('Objetivo: {} unidades de distancia'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Ruta del vehículo 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    print('Distancia total de la ruta: {} unidades de distancia'.format(route_distance))

def main():
    """Resolviendo el problema de ruteo de vehículos."""
    # Crea el modelo de datos
    data = create_data_model()

    # Crea el gestor de índices
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Crea el modelo de ruteo
    routing = pywrapcp.RoutingModel(manager)

    # Función de costo: distancia entre ubicaciones
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Restricciones de capacidad
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # Sin capacidad de sobrecarga
        data['vehicle_capacities'],  # Capacidad del vehículo
        True,  # La demanda debe ser menor o igual a la capacidad
        'Capacity'
    )

    # Parámetros de búsqueda
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Resolver el problema
    solution = routing.SolveWithParameters(search_parameters)

    # Imprimir la solución
    if solution:
        print_solution(manager, routing, solution)

if __name__ == '__main__':
    main()
