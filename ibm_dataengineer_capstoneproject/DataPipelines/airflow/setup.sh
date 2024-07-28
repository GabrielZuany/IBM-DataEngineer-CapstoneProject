mkdir dags plugins logs
chown 50000:0 dags plugins logs
docker compose up airflow-init
docker compose up

# submit a dag
# docker cp dag.py airflow-airflow-webserver-1:/opt/airflow/dags 
# docker exec airflow-airflow-webserver-1 ls /opt/airflow/dags/data
# docker exec airflow-airflow-webserver-1 cat /opt/airflow/dags/data/transformed_data.txt