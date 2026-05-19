FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=local-enterprise-demo

WORKDIR /app

COPY agent-api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY agent-api/app ./app
COPY guardrails ./guardrails

RUN useradd --create-home --shell /usr/sbin/nologin platform && chown -R platform:platform /app
USER platform

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
