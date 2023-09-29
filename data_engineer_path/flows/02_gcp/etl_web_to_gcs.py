from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
import pandas as pd


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read data from web into pandas DataFrame"""
    df = pd.read_csv(
        dataset_url,
        parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'],
    )
    print(df.head(2))
    print(f'columns: {df.dtypes}')
    print(f'rows: {len(df)}')
    return df


@task(log_prints=True)
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(__file__).absolute().parents[2]
    path_data = str(path) + f'/data/raw/{dataset_file}.parquet'
    df.to_parquet(path_data, compression='gzip')
    return path_data


@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to gcs"""
    gcs_block = GcsBucket.load('zoom-gcs')
    gcs_block.upload_from_path(
        from_path=path,
    )
    return


@flow()
def etl_web_to_gcs() -> None:
    """The main ETL function"""
    color = 'yellow'
    year = 2021
    month = 1
    dataset_file = f'{color}_tripdata_{year}-{month:02}.csv.gz'
    compl = f'{color}/{dataset_file}'
    dataset_url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{compl}'

    df = fetch(dataset_url)
    path = write_local(df, dataset_file)
    write_gcs(path)


if __name__ == '__main__':
    etl_web_to_gcs()
