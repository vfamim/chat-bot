docker run -it \
  -e POSTGRES_USER="vfamim" \
  -e POSTGRES_PASSWORD="poli2103" \
  -e POSTGRES_DB="ny_taxi" \
  -e POSTGRES_HOST_AUTH_METHOD=trust \
  -v /$(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5433:5433 \
  --network=pg-network \
  --name pg-database \
  postgres:13

docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4

# create a network
docker network create pg-network

# python command
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
python ingest_data.py \
  --user=vfamim \
  --password=poli2103 \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table-name=yellow_taxi_trips \
  --url=${URL}

docker build -t taxi_ingest:v001 .

docker run taxi_ingest:v001 \
  --user=vfamim \
  --password=poli2103 \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table-name=yellow_taxi_trips \
  --url=${url}

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
  --user=vfamim \
  --password=poli2103 \
  --host=pg-database \
  --port=8001 \
  --db=ny_taxi \
  --table-name=yellow_taxi_trips \
  --url=${url}

docker run -it \
  -e POSTGRES_USER="vfamim" \
  -e POSTGRES_PASSWORD="poli2103" \
  -e POSTGRES_DB="ny_taxi" \
  -e POSTGRES_HOST_AUTH_METHOD=trust \
  -v /$(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
