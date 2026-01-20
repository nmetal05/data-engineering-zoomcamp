# choosing our base docker image as python 
FROM python:3.13.11-slim

# copying the uv binary to the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# working directory inside our container
WORKDIR /code

# adding the venv to PATH
ENV PATH="/code/.venv/bin:$PATH"

# copying dependency files 
COPY "pyproject.toml" "uv.lock" ".python-version" ./

# installing dependencies we set up in host env in uv.lock
RUN uv sync --locked

# copying our necessary python code files
COPY ingest_data.py ingest_data.py

# the command that will execute when the container runs
ENTRYPOINT ["python","ingest_data.py"]
