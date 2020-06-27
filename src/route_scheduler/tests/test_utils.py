from route_scheduler.utils import euclid_dist, dist_matrix
from pytest import approx

tolerance = 1e-3


def test_euclid_basic():
    cord1 = 1, 0
    cord2 = 1, 0
    assert euclid_dist(cord1, cord2) == approx(0.0, rel=tolerance)
    cord1 = 1, 0
    cord2 = 0, 1
    assert euclid_dist(cord1, cord2) == approx(1.414, rel=tolerance)
    cord1 = 12, 39
    cord2 = 80, 90
    assert euclid_dist(cord1, cord2) == approx(85.0, rel=tolerance)


def test_dist_matrix():
    c1 = 1, 0
    c2 = 0, 1
    cords = [c1, c2]
    d_mat = dist_matrix(cords)
    assert d_mat[0][0] == approx(0.0, rel=tolerance)
    assert d_mat[0][1] == approx(1.414, rel=tolerance)
    assert d_mat[1][1] == approx(0.0, rel=tolerance)
    assert d_mat[1][0] == approx(1.414, rel=tolerance)
