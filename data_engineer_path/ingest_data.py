#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import argparse
from sqlalchemy import create_engine
from time import time
from pathlib import Path


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    # the backup file could be gzipped
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
    project_path = Path(__file__).parent
    csv_file_name = csv_name
    csv_path = str(project_path) + '/data/external/'
    full_path = csv_path + csv_file_name
    print(full_path)
    eng = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    os.system(f'wget {url} -O {full_path}')
    # load csv
    df_iter = pd.read_csv(
        full_path,
        parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'],
        date_format='%Y-%m-%d %H:%M:%S',
        chunksize=1000,
        iterator=True,
    )
    df = next(df_iter)
    df.head(n=0).to_sql(name=table_name, con=eng, if_exists='append')

    while True:
        t_start = time()
        df = next(df_iter)
        df.to_sql(name=table_name, con=eng, if_exists='append')
        t_end = time()
        print('inserted another chunk, took %.3f second' % (t_end - t_start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name postgres')
    parser.add_argument('--password', required=True, help='password postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument(
        '--db', required=True, help='database name for postgres'
    )
    parser.add_argument(
        '--table-name', required=True, help='name of the table'
    )
    parser.add_argument('--url', required=True, help='url of the csv file')
    args = parser.parse_args()

    main(args)
