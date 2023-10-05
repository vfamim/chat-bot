from sqlalchemy import create_engine
from pathlib import Path
from prefect import task, flow
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector
from datetime import timedelta
from glob import glob
import os
import pandas as pd


@task(
    log_prints=True,
    tags=['extract'],
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(days=1),
)
def extract_data(url: str):
    # path
    project_path = Path(__file__).absolute().parents[2]
    csv_path = str(project_path) + '/data/external/'
    if url.endswith('.csv.gz'):
        csv_name = 'yellow_tripdata_2021-01.csv.gz'
    else:
        csv_name = 'output.csv'
    csv_full_path = os.path.join(csv_path, csv_name)
    os.system(f'wget {url} -O {os.path.join(csv_full_path)}')
    df_iter = pd.read_csv(
        csv_full_path,
        parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'],
        # date_format='%Y-%m-%d %H:%M:%S',
        chunksize=1000,
        iterator=True,
    )
    df = next(df_iter)
    return df


@task(log_prints=True)
def transform_data(df):
    passenger_count = df['passenger_count'].isin([0]).sum()
    missing_count = df['passenger_count'].isin([0]).sum()
    print(f'pre: missing passenger count: {passenger_count}')
    df = df[df['passenger_count'] != 0]
    print(f'post: missing passenger count: {missing_count}')
    return df


@task(log_prints=True, retries=3)
def load_data(table_name, df):
    connection_block = SqlAlchemyConnector.load('sqlalchemy-zoom')
    with connection_block.get_connection(begin=False) as engine:
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
        df.to_sql(name=table_name, con=engine, if_exists='append')


@flow(name='Subflow', log_prints=True)
def log_subflow(table_name: str):
    print(f'Logging subflow for: {table_name}')


@flow(name='Ingest Data')
def main_flow(table_name: str = 'yellow_taxi_trips'):
    csv_url = 'https://github.com/datatalksclub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'
    log_subflow(table_name)
    raw_data = extract_data(csv_url)
    data = transform_data(raw_data)
    load_data(table_name, data)


if __name__ == '__main__':
    main_flow(table_name='yellow_trips')
