import math
from route_scheduler.types import Coordinates, DistMatrix, Coordinate


def dist_matrix(cords: Coordinates) -> DistMatrix:
    result = []
    for cord1 in cords:
        row = []
        for cord2 in cords:
            dist = euclid_dist(cord1, cord2)
            row.append(dist)
        result.append(row)
    return result


def euclid_dist(cor1: Coordinate, cor2: Coordinate) -> float:
    x_diff = cor1[0] - cor2[0]
    y_diff = cor1[1] - cor2[1]
    x_diff = x_diff ** 2
    y_diff = y_diff ** 2
    dist = math.sqrt(x_diff + y_diff)
    return dist
