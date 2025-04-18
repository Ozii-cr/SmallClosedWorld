FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends  \
       adduser \
       curl \
    && addgroup --system django \
    && adduser --system --ingroup django django \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the application code into the container
COPY . .

# Change ownership of the application files
RUN chown -R django:django /app/

# Switch to non-root user
USER django

# Expose the port the app runs on
EXPOSE 8000

# Make sure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
