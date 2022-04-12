FROM python:3.7-alpine3.14
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-m", "bot"]