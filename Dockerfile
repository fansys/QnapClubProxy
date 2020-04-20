FROM python:3

WORKDIR /app
COPY requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV CDN_HOST 'qnapclub.eu'
ENV CDN_PROTOCOL 'https'

COPY . /app
EXPOSE 80

CMD ["python", "app.py"]