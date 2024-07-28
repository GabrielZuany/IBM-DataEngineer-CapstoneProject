mkdir dags plugins logs
chown 50000:0 dags plugins logs
docker compose up airflow-init
docker compose up