FROM python:3.12-slim

WORKDIR /app

COPY . /app

ARG SECRET_KEY
ENV SECRET_KEY=${SECRET_KEY}

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manager.py", "run"]
