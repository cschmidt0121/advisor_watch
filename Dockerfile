FROM python:3.12-slim AS builder

WORKDIR /src

# Create and "activate" the virtual environment
RUN python3 -m venv /app
ENV PATH=/app/bin:$PATH

# Install the application as normal
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pip install .


FROM python:3.12-slim AS runner

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app


COPY --from=builder /app /app
ENV PATH=/app/bin:$PATH


CMD advisor-watch
