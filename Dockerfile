FROM python:3.10-alpine3.15
USER nobody
COPY . /rss
WORKDIR /rss
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-m", "bot"]