FROM nikolaik/python-nodejs
WORKDIR /userapp
RUN apt-get update -y
RUN apt-get install libdbus-glib-1-dev libdbus-1-dev -y
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR /userapp/ethereum
COPY ./ethereum/package.json ./
RUN npm install
WORKDIR /userapp
COPY . .
CMD ["python3","main.py"]