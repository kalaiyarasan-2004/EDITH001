FROM python:3.10-slim

WORKDIR /app

COPY . /app

COPY req.txt /app/
RUN pip install --no-cache-dir -r req.txt


ENV NAME myenv

CMD ["python", "chatbot5.py"]
