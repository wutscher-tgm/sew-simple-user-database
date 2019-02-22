FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
COPY . /app
#COPY /nginx.conf /etc/nginx/conf.d/default.conf
#CMD ["uwsgi", "--http", "0.0.0.0:8000", "--wsgi-file", "wsgi.py", "-s", "/tmp/yourapplication.sock"]
#CMD ["uwsgi", "--http", "0.0.0.0:8000", "--manage-script-name", "--mount", "/=main:app"]
#FROM nginx


#EXPOSE 5000
#CMD ["python", "main.py"]