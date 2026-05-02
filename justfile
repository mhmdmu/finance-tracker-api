container_name := "finance-tracker"
db_user := "mhmd"
db_name := "finances"

default:
    @just --list

# Start the DB if it exists, otherwise create it
db:
    @docker start {{container_name}} 2>/dev/null || just db-create

db-create:
    docker run --name {{container_name}} \
      -e POSTGRES_PASSWORD=password \
      -e POSTGRES_USER={{db_user}} \
      -e POSTGRES_DB={{db_name}} \
      -p 8888:5432 \
      -v $(pwd)/migrations:/docker-entrypoint-initdb.d:ro \
      -d postgres:latest

# Data wipe only DB
db-reset:
    -docker rm -f {{container_name}}
    @just db-create
    @echo "Database has been wiped and re-initialized."

db-shell:
    docker exec -it {{container_name}} psql -U {{db_user}} -d {{db_name}}

run: db
    uvicorn app.main:app --reload
