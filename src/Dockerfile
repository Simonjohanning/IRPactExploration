FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./*.py .
COPY ./resources/scripts ./resources/scripts
COPY ./resources/PVact.jar ./resources/
CMD echo "This is a test."