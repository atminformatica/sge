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

# Utilizando a versão estável do Python 3.13 de 2025
FROM python:3.13-slim

# Definir o diretório de trabalho
WORKDIR /sge

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalação de dependências do sistema
# O PostgreSQL exige bibliotecas cliente para o adaptador 'psycopg2' ou 'psycopg'
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Atualizar pip e instalar dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Instalar o Gunicorn (servidor de produção)
RUN pip install --no-cache-dir gunicorn

# Copiar o restante do código do projeto
COPY . .

# Coletar arquivos estáticos (essencial para produção)
# Certifique-se de que STATIC_ROOT está configurado no seu settings.py
# RUN python manage.py collectstatic --noinput

# Porta interna do container
EXPOSE 8000

# Comando de execução usando Gunicorn para estabilidade e performance
# Substitua 'seu_projeto' pelo nome da pasta que contém o arquivo wsgi.py
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "app.wsgi:application"]

