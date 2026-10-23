FROM python:3.13-slim-bookworm@sha256:e32be0e55814a08977501ca863271d9bd02443710db8f2afaf8372e2c4508530

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    FLASK_APP=campuseats

WORKDIR /app

RUN groupadd --gid 10001 campuseats \
    && useradd --uid 10001 --gid campuseats --create-home campuseats

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY --chown=campuseats:campuseats src/ ./src/
COPY --chown=campuseats:campuseats docker/entrypoint.py ./docker/entrypoint.py

USER campuseats

EXPOSE 5000

ENTRYPOINT ["python", "/app/docker/entrypoint.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "campuseats:create_app()"]
