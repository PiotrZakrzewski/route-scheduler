# Route Scheduler Micro-service
This microservice communicates via RabbitMQ with producers providing `Tasks` of format
```javascript
{
    "coordinates": [[INT, INT], [INT, INT]], // array of X,Y tuples
    "start": INT, // home depot to start the journey with
    "cars": INT,  // number of vehicles to be used
    "tid": INT // ID that will be reused in the result message
}
```
and subscribers which can expect results of the route planning in the following format:
```javascript
{
    "length": INT,
    "visiting_order": [INT, INT, INT],
    "tid": INT,
    "objective": INT
}
```
The tasks are expected in queue `coordinates` and the results of successful tasks are pushed to `results`. The repo contains two helper utils to help interact with the microservice:
- `utils/push-coordinates.py` will push two tasks into the queue
- `utils/test-consumer.py` will start listening on the results queue and print new results
See further sections for info on how to install/test/start the entire application.

## Design
The route_scheduler microservice is implemented as a single python3 package with a `__main__.py` file being its entry point for starting its main and only process.
The process depends on RabbitMQ server, config (user, pwd, host) can be changed by setting environment variables, which is a good starting point for a dockerized process and is also a common practice for many dockerized services still.
The microservice is highly decoupled from other components, any task producer or multiple producers can supply tasks to it as long as they adhere to the task format and use globally unique task ids so that they can identify their own results and not interfere with results from other producers.
With this architecture it is also easy to scale up the microservice horizontally. As long as popping items from the RabbitMQ is guaranteed to be atomic, multiple instances of the microservice will share the load equally.

Bonus objectives implemented: docker-compose and (partially, as it is very basic) logging

### Limitations, Exclusions and Future Work
- The task consumer in the microservice reads the queue in a blocking way. With more time I would consider an async flow.
- Only unit-tests are present, mostly quite basic happy path cases. With more time I would write integration tests for the consumer itself with a mocked RabbitMQ connection.
- Number of cars (or vehicles) is not fully supported yet
- Logging is minimal, it only logs out errors on parsing or processing messages. More debug and info logs are necessary to make it closer to being production ready
- The docker file for the microservice is very simple and naive. One improvement would be to use a builder to build the package and pass it to a runtime container as to avoid shipping build dependancies.
- Package manifest (setup.py) can be improved by excluding test files.


## Setup
Create Python env
```bash
python3 -m venv env
```
activate the env
```bash
source env/bin/activate
```
install dependancies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```
Install pre-commit hooks
```bash
pre-commit install
```

## Run tests
After installing dev deps you do
```bash
pytest route_scheduler/
```
It will discover and run all unit tests.

## Build Package
You can build the package with
```bash
python setup.py sdist bdist_wheel
```
## Running the application
For a simple end to end test run
```bash
# will recreate the virtual env!
./example.sh
```
Start up the rabbitMQ server and the application itself with docker-compose
```bash
docker-compose up
```
start a consumer util to read outputs
```bash
python utils/test-consumer.py
```
push some coordinates into the queue
```bash
python utils/push-coordinates.py
```
