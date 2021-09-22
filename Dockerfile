FROM nikolaik/python-nodejs
WORKDIR /userapp
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR /userapp/chatApp/run
CMD ["python3","main.py"]