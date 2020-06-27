# Setup
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
# Build Package
You can build the package with
```bash
python setup.py sdist bdist_wheel
```
# Running the application
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
