FROM python:3.10.4

RUN mkdir /app
WORKDIR /app
RUN git clone https://github.com/gittiecat/BB99.git .

RUN pip install -r /app/resources/requirements.txt

CMD [ "python", "src/main.py"]
