FROM python:3.8.13

LABEL project="SOP-Web-backend"
EXPOSE 5000

RUN pip install -r requirements.txt
