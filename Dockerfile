FROM python:latest

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFERED 1

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY  ./src  src
COPY ./app_entrypoint.sh /src
CMD [ "./app_entrypoint.sh" ]