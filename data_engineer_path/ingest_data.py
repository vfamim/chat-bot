from sqlalchemy import create_engine
from pathlib import Path
from prefect import task, flow
from time import time
import os
import pandas as pd
import argparse


# @task(log_prints=True, retries=3)
def ingest_data(user, password, host, port, db, table_name, url):
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    # path
    project_path = Path(__file__).absolute().parents[1]
    csv_path = str(project_path) + '/data/external/' + csv_name
    # connect
    postgres_url = f'postgresql://{user}:{password}@{host}:{port}/{db}'
    engine = create_engine(postgres_url)

    df_iter = pd.read_csv(
        csv_path,
        parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'],
        # date_format='%Y-%m-%d %H:%M:%S',
        chunksize=1000,
        iterator=True,
    )
    df = next(df_iter)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    while True:
        try:
            t_start = time()

            df = next(df_iter)
            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print(
                'inserted another chunk, took %.3f second(s)'
                % (t_end - t_start)
            )

        except StopIteration:
            print('Finished ingesting data into postgres database')
            break


if __name__ == '__main__':
    user = 'vfamim'
    password = 'poli2103'
    host = 'localhost'
    port = '5433'
    db = 'ny_taxi'
    table_name = 'yellow_taxi_trips'
    csv_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'

    ingest_data(user, password, host, port, db, table_name, csv_url)
