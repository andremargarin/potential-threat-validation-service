FROM python:3.7-alpine
WORKDIR /app
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . /app
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.2/wait /wait
RUN chmod +x /wait
CMD /wait && python "src/bootstrap.py"
