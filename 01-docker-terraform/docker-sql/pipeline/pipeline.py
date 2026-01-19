import sys 
import pandas as pd

print("arguments",sys.argv)

day = int(sys.argv[1])
print(f"Running pipeline for day {day}")

data = {
    "A" : [1,2],
    "B" : [3,4]
}

df = pd.DataFrame(data)
print(df.head())

df.to_parquet(f"output_day_{sys.argv[1]}.parquet")
