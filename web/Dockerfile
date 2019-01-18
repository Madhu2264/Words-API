FROM ubuntu:latest
MAINTAINER Madhurika Joshi "madhu2264@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
WORKDIR app
COPY * /app/
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]