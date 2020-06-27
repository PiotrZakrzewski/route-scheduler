from route_scheduler.serializers import deserialize_task


test_msg = b'{"coordinates":[[1,0],[0,1]], "start":0, "cars":1}'
expected = {"coordinates": [(1, 0), (0, 1)], "start": 0, "cars": 1}


def test_deserialize_task_basic():
    assert deserialize_task(test_msg) == expected
