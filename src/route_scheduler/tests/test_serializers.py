import json
from route_scheduler.serializers import deserialize_task, serialize_result


test_msg = b'{"coordinates":[[1,0],[0,1]], "start":0, "cars":1}'
expected = {"coordinates": [(1, 0), (0, 1)], "start": 0, "cars": 1}


def test_deserialize_task_basic():
    assert deserialize_task(test_msg) == expected


expected_res = '{"visiting_order": [0, 1, 2, 0], "length": 200, "objective": 200}'


def test_serialize_result_basic():
    route = ([0, 1, 2, 0], 200, 200)
    # use json.loads to prevent failing on str comparison due to ordering
    assert json.loads(serialize_result(route)) == json.loads(expected_res)
