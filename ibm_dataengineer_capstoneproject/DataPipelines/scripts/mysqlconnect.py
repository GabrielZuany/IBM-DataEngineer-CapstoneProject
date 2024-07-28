# My solution
from sqlalchemy import create_engine, text
import pandas as pd

# connect to database
engine = create_engine('mysql+pymysql://root:root@localhost:3306/sales')

# create table
SQL = """CREATE TABLE IF NOT EXISTS products(
rowid int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
product varchar(255) NOT NULL,
category varchar(255) NOT NULL
)"""
cursor = engine.connect()
cursor.execute(text(SQL))
cursor.commit()
print("Table created")

# insert data
SQL = """INSERT INTO products(product,category)
	 VALUES
	 ("Television","Electronics"),
	 ("Laptop","Electronics"),
	 ("Mobile","Electronics")
	 """
cursor.execute(text(SQL))
cursor.commit()
print("Data inserted")

# query data
SQL = "SELECT * FROM products"
result = pd.read_sql(SQL, engine)
print(result)

# close connection
cursor.close()
engine.dispose()

# ----------------------

# IBM SOLUTION

# This program requires the python module mysql-connector-python to be installed.
# Install it using the below command
# pip3 install mysql-connector-python

# import mysql.connector

# connect to database
# You can get the Hostname and Password from the connection information section of Mysql 
# connection = mysql.connector.connect(user='root', password='<replace with your Mysql password>',host='<replace with your Mysql hostname>',database='sales')

# create cursor
# cursor = connection.cursor()

# create table
# SQL = """CREATE TABLE IF NOT EXISTS products(
# rowid int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
# product varchar(255) NOT NULL,
# category varchar(255) NOT NULL
# )"""
# cursor.execute(SQL)
# print("Table created")

# insert data
# SQL = """INSERT INTO products(product,category)
# 	 VALUES
# 	 ("Television","Electronics"),
# 	 ("Laptop","Electronics"),
# 	 ("Mobile","Electronics")
# 	 """
# cursor.execute(SQL)
# connection.commit()

# query data
# SQL = "SELECT * FROM products"
# cursor.execute(SQL)
# for row in cursor.fetchall():
# 	print(row)

# close connection
# connection.close()
