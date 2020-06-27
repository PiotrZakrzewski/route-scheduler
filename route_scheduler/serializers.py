from marshmallow import Schema, fields
from route_scheduler.types import Route

coordinate = fields.Tuple((fields.Integer, fields.Integer))


class TaskSchema(Schema):
    cars = fields.Integer()
    start = fields.Integer()
    coordinates = fields.List(coordinate)
    tid = fields.Integer()


class ResultSchema(Schema):
    visiting_order = fields.List(fields.Integer())
    objective = fields.Integer()
    length = fields.Integer()
    tid = fields.Integer()


task_schema = TaskSchema()
result_schema = ResultSchema()


def deserialize_task(raw_json: bytes):
    return task_schema.loads(raw_json.decode())


def serialize_result(result: Route, task_id: int) -> str:
    v_order, obj, length = result
    result = {
        "visiting_order": v_order,
        "objective": obj,
        "length": length,
        "tid": task_id,
    }
    return result_schema.dumps(result)
