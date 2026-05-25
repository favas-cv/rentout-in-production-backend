FROM backend-base

WORKDIR /app

COPY . .

COPY docker/django/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]