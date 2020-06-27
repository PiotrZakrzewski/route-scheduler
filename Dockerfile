FROM python:3.7

ADD route_scheduler /route_scheduler
ADD setup.py /
ADD requirements.txt /
ADD README.md /
RUN pip install -r requirements.txt
RUN python setup.py sdist bdist_wheel
RUN pip install dist/*whl

CMD [ "python", "-m", "route_scheduler"]
