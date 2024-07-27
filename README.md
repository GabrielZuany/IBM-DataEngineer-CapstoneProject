# IBM-DataEngineer-CapstoneProject

## Environment:
This document introduces you to the data platform architecture of an ecommerce company named SoftCart.

SoftCart uses a hybrid architecture, with some of its databases on premises and some on cloud.

### Tools and Technologies:
- OLTP database - MySQL
- NoSql database - MongoDB
- Production Data warehouse – DB2 on Cloud
- Staging Data warehouse – PostgreSQL
- Big data platform - Hadoop
- Big data analytics platform – Spark
- Business Intelligence Dashboard - IBM Cognos Analytics
- Data Pipelines - Apache Airflow

### Process:
- SoftCart's online presence is primarily through its website, which customers access using a variety of devices like laptops, mobiles and tablets.
- All the catalog data of the products is stored in the MongoDB NoSQL server.
- All the transactional data like inventory and sales are stored in the MySQL database server.
- SoftCart's webserver is driven entirely by these two databases.
- Data is periodically extracted from these two databases and put into the staging data warehouse running on PostgreSQL.
- The production data warehouse is on the cloud instance of IBM DB2 server.
- BI teams connect to the IBM DB2 for operational dashboard creation. IBM Cognos Analytics is used to create dashboards.
- SoftCart uses Hadoop cluster as its big data platform where all the data is collected for analytics purposes.
- Spark is used to analyse the data on the Hadoop cluster.
- To move data between OLTP, NoSQL and the data warehouse, ETL pipelines are used and these run on Apache Airflow.

---

## OLTP database requirements and design

### OLTP database
OLTP database is generally used to handle every day business transactions of an organization like a bank or a super market chain. OLTP databases can be write heavy or may have a balanced read/write load.

### OLTP database requirements:
An OLTP database is expected to handle a huge number of transactions per second. Each transaction usually involves accessing (read/write) a small portion of the database, in other words the payload per transaction is small.

The time taken to execute a transaction usually called latency needs to be very less.

### OLTP database design:
The schema of an OLTP database is higly normalized so as to achieve a very low latency. To further improve the latency an OLTP database stores only the recent data like the last few week's data. They are usually run on storage that is very fast like SSD.

---

## NoSQL Database

You are a data engineer at an e-commerce company. Your company needs you to design a data platform that uses MongoDB as a NoSQL database. You will be using MongoDB to store the e-commerce catalog data.

The basics tasks is import data into a MongoDB database, query data in a MongoDB database, and export data from MongoDB.


---

## Data Warehousing

You are a data engineer hired by an ecommerce company named SoftCart.com . The company retails download only items like E-Books, Movies, Songs etc. The company has international presence and customers from all over the world. The company would like to create a data warehouse so that it can create reports like

- total sales per year per country
- total sales per month per category
- total sales per quarter per country
- total sales per category per country

You will use your data warehousing skills to design and implement a data warehouse for the company.

### What are the differences between a database and a data warehouse? 
A database is any collection of data organized for storage, accessibility, and retrieval. A data warehouse is a type of database the integrates copies of transaction data from disparate source systems and provisions them for analytical use.

The important distinction is that data warehouses are designed to handle analytics required for improving quality and costs in the new healthcare environment. A transactional database, like an EHR, doesn’t lend itself to analytics.

### The High-level Distinction Between Databases and Data Warehouses
What I will refer to as a “database” in this post is one designed to make transactional systems run efficiently. Typically, this type of database is an OLTP (online transaction processing) database. An electronic health record (EHR) system is a great example of an application that runs on an OLTP database. In fact, an OLTP database is typically constrained to a single application.

The important fact is that a transactional database doesn’t lend itself to analytics. To effectively perform analytics, you need a data warehouse. A data warehouse is a database of a different kind: an OLAP (online analytical processing) database. A data warehouse exists as a layer on top of another database or databases (usually OLTP databases). The data warehouse takes the data from all these databases and creates a layer optimized for and dedicated to analytics.

So the short answer to the question I posed above is this: A database designed to handle transactions isn’t designed to handle analytics. It isn’t structured to do analytics well. A data warehouse, on the other hand, is structured to make analytics fast and easy.
aggregation.
It the end, data warehouses can be viewed as an aggregarion of data marts.


#### Note:
- [ERROR] : IBM haven't build a product dataset to be loaded into productsDimTable.
- [ERROR] : FactSales.csv don't have the product_id (or item_id) column to reference the product table. So, i can't know which products were sold. Inconsistant data.