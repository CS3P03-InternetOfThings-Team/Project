FROM python:3.10

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
COPY . . 

EXPOSE 8080
COPY ./.backend.env /app/.env
CMD ["uvicorn", "src.backend.app:app", "--host", "0.0.0.0","--port", "8080"]
