import datetime
import random
from sqlalchemy import create_engine, text
import psycopg2
import pandas as pd

# Connect to MySQL
mysql_engine = create_engine('mysql+pymysql://root:root@localhost:3306/sales')
mysql_cursor = mysql_engine.connect()

# Connect to DB2 or PostgreSql
dsn_hostname = 'localhost'
dsn_user='root'
dsn_pwd ='root' 
dsn_port ="5432"
dsn_database ="sales"
pgsql_conn = psycopg2.connect(
   database=dsn_database, 
   user=dsn_user,
   password=dsn_pwd,
   host=dsn_hostname, 
   port= dsn_port
)
pgsql_cursor = pgsql_conn.cursor()

# Find out the last rowid from DB2 data warehouse or PostgreSql data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the IBM DB2 database or PostgreSql.
def get_last_rowid():
	sql = 'SELECT MAX(rowid) FROM "sales"'
	pgsql_cursor.execute(sql)
	row = pgsql_cursor.fetchone()
	return row[0]
last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)


# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.
def get_latest_records(rowid):
	sql = 'SELECT * FROM sales_data WHERE rowid > {0}'.format(rowid)
	result = pd.read_sql(sql, mysql_engine)
	return result
new_records = get_latest_records(last_row_id)
print("New rows on staging datawarehouse = ", len(new_records))

# Insert the additional records from MySQL into DB2 or PostgreSql data warehouse.
# The function insert_records must insert all the records passed to it into the sales_data table in IBM DB2 database or PostgreSql.
def insert_records(records:pd.DataFrame):
	for index, row in records.iterrows():
		sql = f"INSERT INTO sales(rowid,product_id,customer_id,price,quantity,timestamp) \
			VALUES('{row["rowid"]}', '{row["product_id"]}', '{row["customer_id"]}', '{random.randrange(1, 5000)}', '{row["quantity"]}', '{datetime.datetime.now()}')"
		pgsql_cursor.execute(sql)
	pgsql_conn.commit()
	return
insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# disconnect from mysql warehouse
# disconnect from DB2 or PostgreSql data warehouse 
mysql_cursor.close()
mysql_engine.dispose()
pgsql_cursor.close()
pgsql_conn.close()