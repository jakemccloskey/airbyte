FROM airbyte/integration-base-python:0.1.1

WORKDIR /airbyte/base_file_source_code
COPY base_file_source ./base_file_source
COPY setup.py ./
RUN pip install .

LABEL io.airbyte.version=0.0.1
LABEL io.airbyte.name=airbyte/integration-base-file-source
