from marshmallow import Schema, fields

coordinate = fields.Tuple((fields.Integer, fields.Integer))


class TaskSchema(Schema):
    cars = fields.Integer()
    start = fields.Integer()
    coordinates = fields.List(coordinate)


task_schema = TaskSchema()


def deserialize_task(raw_json: bytes):
    return task_schema.loads(raw_json.decode())
