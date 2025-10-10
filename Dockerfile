FROM python:3.13-slim

#Versionhandling
ARG VERSION
ENV APP_VERSION=$VERSION
LABEL org.opencontainers.image.version=$VERSION

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

COPY .github/scripts/start.sh /app/start.sh

RUN chmod +x /app/start.sh

EXPOSE 8000

ENTRYPOINT ["/app/start.sh"]
