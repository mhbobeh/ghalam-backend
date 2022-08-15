FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV REDIS_HOST redis
ENV REDIS_PORT 6379 

RUN apt-get update
RUN apt-get install -y git curl gnupg binutils libproj-dev gdal-bin gettext supervisor

RUN pip install --no-cache-dir -U pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get remove git -y; apt-get autoremove -y; apt-get clean
ENV C_FORCE_ROOT=1

COPY . /app
RUN rm -rf .git
WORKDIR /app

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]
