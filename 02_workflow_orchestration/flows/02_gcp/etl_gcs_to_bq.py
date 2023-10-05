from pathlib import Path
from prefect import flow, task
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
import pandas as pd


def local_path():
    """Absolute path of the project"""
    path = Path(__file__).absolute().parents[2]
    return str(path)


@flow()
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f'{color}_tripdata_{year}-{month:02}.csv.gz.parquet'
    gcs_block = GcsBucket.load('zoom-gcs')
    gcs_block.get_directory(
        from_path=gcs_path, local_path=local_path() + '/data/'
    )
    return Path(local_path() + '/data/' + gcs_path)


@task(retries=3)
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    print(
        f"pre: missing pessenger count: {df['passenger_count'].isna().sum()}"
    )
    df['passenger_count'].fillna(0)
    print(
        f"post: missing pessenger count: {df['passenger_count'].isna().sum()}"
    )
    return df


@task()
def write_BQ(df: pd.DataFrame) -> None:
    """Write DataFrame to Big Query"""
    gcp_credential_block = GcpCredentials.load('zoom-gcp-creds')
    df.to_gbq(
        destination_table='dezoomcamp.rides',
        project_id='iconic-era-400201',
        credentials=gcp_credential_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists='append',
    )


@flow()
def etl_gcs_to_bq():
    """Main ETL flow to load data into Big Query"""
    color = 'yellow'
    year = 2021
    month = 1

    path = extract_from_gcs(color, year, month)
    df = transform(path)
    write_BQ(df)


if __name__ == '__main__':
    etl_gcs_to_bq()
from pathlib import Path
from prefect import flow, task
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
import pandas as pd


def local_path():
    """Absolute path of the project"""
    path = Path(__file__).absolute().parents[2]
    return str(path)


@flow()
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f'{color}_tripdata_{year}-{month:02}.csv.gz.parquet'
    gcs_block = GcsBucket.load('zoom-gcs')
    gcs_block.get_directory(
        from_path=gcs_path, local_path=local_path() + '/data/'
    )
    return Path(local_path() + '/data/' + gcs_path)


@task(retries=3)
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    print(
        f"pre: missing pessenger count: {df['passenger_count'].isna().sum()}"
    )
    df['passenger_count'].fillna(0)
    print(
        f"post: missing pessenger count: {df['passenger_count'].isna().sum()}"
    )
    return df


@task()
def write_BQ(df: pd.DataFrame) -> None:
    """Write DataFrame to Big Query"""
    gcp_credential_block = GcpCredentials.load('zoom-gcp-creds')
    df.to_gbq(
        destination_table='dezoomcamp.rides',
        project_id='iconic-era-400201',
        credentials=gcp_credential_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists='append',
    )


@flow()
def etl_gcs_to_bq():
    """Main ETL flow to load data into Big Query"""
    color = 'yellow'
    year = 2021
    month = 1

    path = extract_from_gcs(color, year, month)
    df = transform(path)
    write_BQ(df)


if __name__ == '__main__':
    etl_gcs_to_bq()
