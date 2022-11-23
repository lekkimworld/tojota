FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./
COPY optional-requirements.txt ./

RUN mkdir -p /usr/src/app/cache
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir -r optional-requirements.txt
COPY . .

CMD [ "python", "./tojota.py" ]

ARG REDIS_URL
ARG TOJOTA_PASSWORD
ARG TOJOTA_USERNAME
ARG TOJOTA_VIN
ENV TOJOTA_TIMEZONE="Europe/Copenhagen"
ENV TOJOTA_PLUGINS="redisqueue"
ENV TOJOTA_VIN="${TOJOTA_VIN}"
ENV TOJOTA_USERNAME="${TOJOTA_USERNAME}"
ENV TOJOTA_PASSWORD="${TOJOTA_PASSWORD}"
ENV REDIS_URL="${REDIS_URL}"
