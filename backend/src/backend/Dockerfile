FROM python:3.10 as build

WORKDIR /venv
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt --no-cache-dir --compile && \
  rm /tmp/requirements.txt


FROM python:3.10-slim as runtime

WORKDIR /app
COPY --from=build /venv /venv
COPY . . 

ENV PATH="/venv/bin:$PATH"
RUN pip install -e . --no-cache-dir --compile

EXPOSE 8080
COPY ./.backend.env /app/.env
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0","--port", "8080"]
