FROM python:3.8-slim AS base
# We choose python-slim instead of alpine, a buildspeed vs image size tradeoff.

# In case you need base debian dependencies install them here.
# RUN apt-get update && apt-get -y upgrade && apt-get install -y --no-install-recommends \
# #        TODO list depencies here \
#    && apt-get clean && rm -rf /var/lib/apt/lists/*

# --- COMPILE-IMAGE ---
FROM base AS compile-image
ENV DEBIAN_FRONTEND=noninteractive

# Install dev dependencies
RUN apt-get update && apt-get -y upgrade && apt-get install -y --no-install-recommends \
        gcc \
        python3.8-dev && \
        apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade --no-cache-dir setuptools pip
RUN pip install --no-cache-dir pipenv

# Copy source
WORKDIR /code
COPY . /code

# Install packages, including the dev (test) packages.
RUN PIPENV_VENV_IN_PROJECT=1 pipenv --three
RUN pipenv lock
RUN pipenv sync --dev

# Run pytest tests.
# pipenv check fails due to a github connection error. Pipenv check scans for python
# vulnerabilities amongst other things. We might want to debug and fix this:
# RUN PIPENV_PYUP_API_KEY="" pipenv check &&
#RUN pipenv run pytest

# Cleanup test packages. We want to use pipenv uninstall --all-dev but that command is
# broken. See: https://github.com/pypa/pipenv/issues/3722
RUN pipenv --rm && \
    PIPENV_VENV_IN_PROJECT=1 pipenv --three && \
    pipenv sync

# --- BUILD IMAGE ---
FROM base AS build-image
WORKDIR /code

COPY --from=compile-image "/code/inspire_etf_validator.egg-info/" "/code/inspire_etf_validator.egg-info/"
COPY --from=compile-image "/code/inspire_etf_validator" "/code/inspire_etf_validator"
COPY --from=compile-image /code/.venv /code/.venv

# Make sure we use the virtualenv:
ENV PATH="/code/.venv/bin:$PATH"

# Metadata params
ARG BUILD_DATE
ARG VERSION
ARG GIT_COMMIT_HASH

# Metadata
LABEL org.opencontainers.image.authors="William Loosman william.loosman@kadaster.nl" \
      org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.title="inspire-etf-validator" \
      org.opencontainers.image.description="Python wrapper that runs and aggregates the EU inspire ETF validator" \
      org.opencontainers.image.url="https://github.com/PDOK/inspire-etf-validator" \
      org.opencontainers.image.vendor="PDOK" \
      org.opencontainers.image.source="https://github.com/PDOK/inspire-etf-validator" \
      org.opencontainers.image.revision=$GIT_COMMIT_HASH \
      org.opencontainers.image.version=$VERSION

ENTRYPOINT [ "etf" ]
