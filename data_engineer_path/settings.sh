docker run -it \
  -e POSTGRES_USER="vfamim" \
  -e POSTGRES_PASSWORD="poli2103" \
  -e POSTGRES_DB="ny_taxi" \
  -e POSTGRES_HOST_AUTH_METHOD=trust \
  -v /$(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 8001:5432 \
  postgres:13
