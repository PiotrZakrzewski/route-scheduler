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
