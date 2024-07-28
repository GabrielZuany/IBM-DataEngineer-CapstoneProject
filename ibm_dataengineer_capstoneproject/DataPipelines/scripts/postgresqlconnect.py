# This program requires the python module ibm-db to be installed.
# Install it using the below command
# python3 -m pip install psycopg2

import pandas as pd
import psycopg2

dsn_hostname = 'localhost'
dsn_user='root'
dsn_pwd ='root' 
dsn_port ="5432"
dsn_database ="sales"

conn = psycopg2.connect(
   database=dsn_database, 
   user=dsn_user,
   password=dsn_pwd,
   host=dsn_hostname, 
   port= dsn_port
)
cursor = conn.cursor()

def insert_products():
   # create table
   SQL = """CREATE TABLE IF NOT EXISTS products(rowid INTEGER PRIMARY KEY NOT NULL,product varchar(255) NOT NULL,category varchar(255) NOT NULL)"""
   cursor.execute(SQL)
   print("Table created")

   # insert data
   cursor.execute("INSERT INTO  products(rowid,product,category) VALUES(1,'Television','Electronics')");
   cursor.execute("INSERT INTO  products(rowid,product,category) VALUES(2,'Laptop','Electronics')");
   cursor.execute("INSERT INTO products(rowid,product,category) VALUES(3,'Mobile','Electronics')");
   conn.commit()

   # insert list of Records
   # list_ofrecords =[(5,'Mobile','Electronics'),(6,'Mobile','Electronics')]
   # cursor = conn.cursor()
   # for row in list_ofrecords:
   #    SQL="INSERT INTO products(rowid,product,category) values(%s,%s,%s)" 
   #    cursor.execute(SQL,row);
   #    conn.commit()

def insert_sales():
   # rowid,product_id,customer_id,price,quantity,timestamp
   SQL = """CREATE TABLE IF NOT EXISTS sales(
   rowid INTEGER PRIMARY KEY NOT NULL,
   product_id INTEGER NOT NULL,
   customer_id INTEGER NOT NULL,
   price FLOAT NOT NULL,
   quantity INTEGER NOT NULL,
   timestamp TIMESTAMP NOT NULL
   )"""
   cursor.execute(SQL)
   conn.commit()
   print("Table created")

   dataset = pd.read_csv('sales.csv')
   for index, row in dataset.iterrows():
      cursor.execute("INSERT INTO sales(rowid,product_id,customer_id,price,quantity,timestamp) VALUES(%s,%s,%s,%s,%s,%s)", \
                     (row['rowid'],row['product_id'],row['customer_id'],row['price'],row['quantity'],row['timestamp']))
   conn.commit()

if __name__ == "__main__":
   insert_products()
   insert_sales()
   print("Data inserted")

   # query data
   SQL = "SELECT * FROM products"
   cursor.execute(SQL)
   result = cursor.fetchall()
   for row in result:
      print(row)

   SQL = "SELECT * FROM sales"
   cursor.execute(SQL)
   result = cursor.fetchall()
   for row in result:
      print(row)

   cursor.close()
   conn.close()