    # FROM python:3.13.3-slim

    # WORKDIR /sge

    # ENV PYTHONDONTWRITEBYTECODE 1
    # ENV PYTHONUNBUFFERED 1

# RUN apt update && apt -y install cron && apt -y install nano
    # RUN apt update

    # COPY . .

    # RUN pip install --upgrade pip
    # RUN pip install -r requirements.txt

# COPY ./cron /etc/cron.d/cron
# RUN chmod 0644 /etc/cron.d/cron
# RUN crontab /etc/cron.d/cron

    # EXPOSE 8000

# CMD cron ; python manage.py migrate && python manage.py runserver 0.0.0.0:8000
    # CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000



#dockerfile para produçao no easypanel

FROM python:3.13.3-slim

WORKDIR /sge

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalação de dependências para Debian Trixie (Dezembro/2025)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD python manage.py migrate --noinput && \
    gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 app.wsgi:application

