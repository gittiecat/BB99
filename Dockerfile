FROM python:3.10.4
ADD . /app
RUN pip install -r /app/resources/requirements.txt
WORKDIR "/app"
CMD [ "python", "src/main.py"]
