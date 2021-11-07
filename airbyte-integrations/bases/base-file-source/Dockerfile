FROM python:3.7-slim as base

WORKDIR /airbyte/base_file_source_code
COPY base_file_source ./base_file_source
COPY setup.py ./
RUN pip install .

LABEL io.airbyte.version=0.0.2
LABEL io.airbyte.name=airbyte/integration-base-file-source
