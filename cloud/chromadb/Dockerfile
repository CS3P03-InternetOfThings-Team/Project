FROM python:3.10-slim-bookworm as builder

#RUN apt-get update -qq
#RUN apt-get install python3.10 python3-pip -y --no-install-recommends && rm -rf /var/lib/apt/lists_/*
RUN apt-get update --fix-missing && apt-get install -y --fix-missing build-essential

RUN mkdir /install
WORKDIR /install

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade --prefix="/install" -r requirements.txt

FROM python:3.10-slim-bookworm as final

RUN mkdir /chroma
WORKDIR /chroma

COPY --from=builder /install /usr/local

COPY . /chroma

EXPOSE 8000
RUN apt-get update
RUN apt-get install build-essential -y
RUN pip install --force-reinstall --no-cache-dir chroma-hnswlib
RUN export IS_PERSISTENT=1
CMD ["uvicorn", "chromadb.app:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8000", "--log-config", "log_config.yml"] 