FROM nikolaik/python-nodejs
WORKDIR /userapp
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY ./package.json ./package.json
COPY . .
CMD ["python3","chatApp/run/main.py"]