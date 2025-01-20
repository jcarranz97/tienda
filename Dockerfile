FROM python:3
WORKDIR /app
COPY src/requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
