FROM python:3.10.4

WORKDIR /app
ARG CACHEBUST
RUN echo "$CACHEBUST"
RUN git clone https://github.com/gittiecat/BB99.git .

RUN pip install -r /app/resources/requirements.txt

CMD [ "python", "-u", "src/main.py"]
