from route_scheduler.scheduler import find_routes


def test_find_routes_basic():
    result = find_routes([(0, 1), (1, 0)], 0, 1)
    assert result == ([0, 1, 0], 2, 2)
