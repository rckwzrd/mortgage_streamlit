FROM python:3.8-slim

WORKDIR /usr/app/src

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./

CMD ["sh", "-c", "streamlit run --server.port 8000 /usr/app/src/main.py"]