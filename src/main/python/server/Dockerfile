FROM python
WORKDIR /code
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

#FROM nginx

#COPY /nginx.conf /etc/nginx/conf.d/default.conf

#EXPOSE 5000
CMD ["python", "main.py"]