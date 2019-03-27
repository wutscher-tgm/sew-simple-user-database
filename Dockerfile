FROM python:3.7

COPY 25224756.jpg /app/25224756.jpg
COPY pp.jpg /app/pp.jpg
COPY requirements.txt /app/requirements.txt
COPY setup.py /app/setup.py
COPY tox.ini /app/tox.ini
COPY src/main/python/server /app/src/main/python/server
COPY src/unittest/python /app/src/unittest/python

WORKDIR /app

RUN pip3 install tox

CMD ['tox']