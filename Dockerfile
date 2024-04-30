# Use the official Python 3.9 image as a base
FROM python:3.9-slim

# Set environment variables
ENV POETRY_VERSION=1.1.12 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only the poetry files
COPY pyproject.toml poetry.lock /app/

# Set the working directory
WORKDIR /app

# Install dependencies
RUN poetry install --no-dev

# Copy the rest of the application code
COPY . /app

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
