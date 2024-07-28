# Restore the database

# Copy the dump.sql file to the container
docker cp dump.sql ibm_project_mysql:/tmp/dump.sql

# Enter the container and restore the database
docker exec -it ibm_project_mysql /bin/bash
mysql -u root -p sales < /tmp/dump.sql