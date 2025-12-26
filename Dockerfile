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

# Variáveis de ambiente para garantir logs limpos no Easypanel
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# INSTALAÇÃO DE DEPENDÊNCIAS GRÁFICAS E DE SISTEMA
# Necessárias para pycairo, reportlab, xhtml2pdf e lxml
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /sge

# Otimização de Cache: Instala dependências antes de copiar o código
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn whitenoise

# Copia o restante dos arquivos do Linux Mint para o Container
COPY . .

# Coleta de arquivos estáticos (essencial para o CSS do Django aparecer)
# Certifique-se de ter o WhiteNoise configurado no settings.py
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Comando para iniciar o servidor Gunicorn
# Confirme se sua pasta com settings.py/wsgi.py se chama realmente 'app'
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app.wsgi:application"]
