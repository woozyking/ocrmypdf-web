# Build stage
FROM python:3.10-slim-bullseye as base

FROM base as build-stage

# Base dependencies
RUN apt-get -y update && \
    apt-get -y install --no-install-recommends \
        icc-profiles-free \
        libxml2 \
        pngquant \
        zlib1g

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock ./

# Install dependencies (OCRmyPDF and the web frontend ones)
RUN pip install --no-cache-dir pipenv && pipenv install --system --deploy

# Copy the source code to the container
COPY app.py ./

# Application stage
FROM base

# Install latest ghostscript and tesseract-ocr
RUN apt-get -y update && \
    apt-get -y install --no-install-recommends \
        tesseract-ocr \
        ghostscript && \
        rm -rf /var/lib/apt/lists/*

# Copy only the necessary files from the build stage
COPY --from=build-stage /usr/local/lib/ /usr/local/lib/
COPY --from=build-stage /usr/local/bin/ /usr/local/bin/
COPY --from=build-stage /app.py /app.py

# Expose the port for the Flask server
EXPOSE 8080

# Launch the Flask server
CMD ["python", "app.py"]
