from prefect import flow, task
from urllib.error import HTTPError, URLError
from prefect_gcp.cloud_storage import GcsBucket
from io import BytesIO
import pandas as pd


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    df = pd.read_parquet(dataset_url)
    print(df.head(2))
    print(f'columns: {df.dtypes}')
    print(f'rows: {len(df)}')
    return df


@task(log_prints=True)
def send_to_gcs_raw(df: pd.DataFrame, dataset_file: str) -> None:
    """Write DataFrame out locally as a parquet file"""
    stream = BytesIO()
    df.to_parquet(stream)
    path_file = '/data/raw/' + dataset_file
    stream.seek(0)
    gcs_block = GcsBucket.load('zoom-gcs')
    gcs_block.upload_from_file_object(
        from_file_object=stream, to_path=path_file
    )
    return


@flow()
def etl_web_to_google(
    color: str = 'yellow',
    months: list[int] = [i if i <= 12 else 0 for i in range(1, 13)],
    year: int = 2023,
):
    """The main ETL function to web, gcs and then to BQ"""
    for month in months:
        try:
            dataset_file = (
                f'{color}_tripdata_{year}-{str(month).zfill(2)}.parquet'
            )
            dataset_url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{dataset_file}'

            df = fetch(dataset_url)
            send_to_gcs_raw(df, dataset_file)
        except HTTPError as e:
            if e.code == 404:
                print(f'File for month {month} not found.')
                break
            else:
                print(f'HTTP ERROR {e.code}: {e.reason}')
        except URLError as e:
            print(f'URL Error: {e.reason}')


if __name__ == '__main__':
    etl_web_to_google()
