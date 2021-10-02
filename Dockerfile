FROM nikolaik/python-nodejs
WORKDIR /userapp
RUN apt-get update -y
RUN apt-get install libdbus-glib-1-dev libdbus-1-dev -y
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR /userapp/chatApp/run
CMD ["python3","main.py"]
