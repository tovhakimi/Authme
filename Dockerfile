FROM python:3.12.7-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for.sh /wait-for.sh
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for.sh /wait-for-it.sh
CMD ["/wait-for.sh"]