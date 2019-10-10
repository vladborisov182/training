FROM python:3.7

# Install Python and Package Libraries
RUN apt-get update && apt-get install -qq -y \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

RUN pip install pipenv
