FROM python:3.12-slim

WORKDIR /app

COPY . /app

ARG SECRET_KEY
ENV SECRET_KEY=${SECRET_KEY}

RUN pip install --no-cache-dir -r requirements.txt
RUN python manager.py init

EXPOSE 8000

CMD ["sh", "-c", "exec uvicorn src.main:app --host 0.0.0.0 --port $(echo $PORT)"]
