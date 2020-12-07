
FROM python:latest

RUN pip install --upgrade pip

RUN apt-get update \
&& apt-get install -y openssl

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]