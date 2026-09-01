FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir python-telegram-bot==22.8
COPY main.py .
CMD ["python", "main.py"]