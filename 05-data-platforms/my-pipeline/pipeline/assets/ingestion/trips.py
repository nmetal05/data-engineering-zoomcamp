"""@bruin
name: ingestion.trips
type: python
image: python:3.11
connection: duckdb-default

materialization:
  type: table
  strategy: append

columns:
  - name: pickup_datetime
    type: timestamp
    description: "When the meter was engaged"
  - name: dropoff_datetime
    type: timestamp
    description: "When the meter was disengaged"
@bruin"""

import os
import json
import pandas as pd

def materialize():
    start_date = os.environ["BRUIN_START_DATE"]
    end_date = os.environ["BRUIN_END_DATE"]
    taxi_types = json.loads(os.environ["BRUIN_VARS"]).get("taxi_types", ["yellow"])

    # Generate list of months between start and end dates
    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    months = pd.date_range(start.replace(day=1), end, freq="MS")

    # Fetch parquet files for each taxi type and month
    frames = []
    for taxi_type in taxi_types:
        for month in months:
            url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{month.year}-{month.month:02d}.parquet"
            try:
                df = pd.read_parquet(url)
                df = df.rename(columns={
                    "tpep_pickup_datetime": "pickup_datetime",
                    "tpep_dropoff_datetime": "dropoff_datetime",
                    "lpep_pickup_datetime": "pickup_datetime",
                    "lpep_dropoff_datetime": "dropoff_datetime",
                    "PULocationID": "pickup_location_id",
                    "DOLocationID": "dropoff_location_id",
                })
                frames.append(df)
            except Exception as e:
                print(f"Skipping {url}: {e}")

    final_dataframe = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    for col in final_dataframe.select_dtypes(include=["datetimetz"]).columns:
        final_dataframe[col] = final_dataframe[col].dt.tz_localize(None)

    return final_dataframe
