# choosing our base docker image as python 
FROM python:3.13.11-slim

# installing python dependencies eg: pands
RUN pip install pandas pyarrow

# working directory inside our container
WORKDIR /app

# copying our necessary files
COPY pipeline.py pipeline.py

# the command that will execute when the container runs
ENTRYPOINT ["python","pipeline.py"]
