FROM python:3.10.4-slim-bullseye
WORKDIR /base/
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY run.sh .
COPY ./app /base/app
ENV PYTHONPATH=/base
RUN chmod +x /base/run.sh
CMD ["/base/run.sh"]

