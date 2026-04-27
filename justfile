default:
    @just --list

test:
    pytest --no-header --tb=line -ra

run: db
    uvicorn app.main:app --reload

# DB docker commands
db-create:
  docker run --name finance-tracker \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_USER=mhmd \
    -e POSTGRES_DB=finances \
    -p 8888:5432 \
    -v $(pwd)/migrations:/docker-entrypoint-initdb.d:ro \
    -d postgres:latest

db:
  docker start finance-tracker

db-stop:
  docker stop finance-tracker

db-restart: db-stop db
  @echo "DB restarted"

db-reset:
  docker rm -f finance-tracker
  docker volume prune -f
  just db-create
