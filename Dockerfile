FROM python:3.8.13

LABEL project="SOP-Web-backend"
COPY . /
WORKDIR /
EXPOSE 5000

RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
