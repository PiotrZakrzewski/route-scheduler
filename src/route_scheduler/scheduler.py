from ortools.constraint_solver import routing_enums_pb2, pywrapcp
from route_scheduler.types import Route, Coordinates, DistMatrix
from route_scheduler.utils import dist_matrix


def find_routes(cords: Coordinates, start: int, cars: int) -> Route:
    d_mat = dist_matrix(cords)
    return _optimize_route(d_mat, start, cars)


def _optimize_route(d_mat: DistMatrix, start: int, cars: int) -> Route:
    manager = pywrapcp.RoutingIndexManager(len(d_mat), cars, start)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index: int, to_index: int) -> int:
        """Returns the distance between the two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return d_mat[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    solution = routing.SolveWithParameters(search_parameters)
    return _format_solution(manager, routing, solution)


def _format_solution(manager, routing, solution) -> Route:
    obj = solution.ObjectiveValue()
    visiting_order = []
    index = routing.Start(0)
    route_distance = 0
    while not routing.IsEnd(index):
        visiting_order.append(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    visiting_order.append(manager.IndexToNode(index))
    return visiting_order, obj, route_distance
