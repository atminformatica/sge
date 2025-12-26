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
# Usando 3.12 para evitar bugs do Debian Trixie/Python 3.13
FROM python:3.12-slim
WORKDIR /sge
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Expõe a porta 8000
EXPOSE 8000

# Comando final (ajuste 'app' para o nome da sua pasta de settings)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app.wsgi:application"]
