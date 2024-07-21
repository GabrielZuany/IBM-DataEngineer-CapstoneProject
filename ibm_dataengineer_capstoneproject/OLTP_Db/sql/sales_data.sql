CREATE TABLE sales_data(
id varchar(36),
product_id int,
customer_id int,
price double,
quantity int,
`timestamp` timestamp
);

ALTER TABLE sales_data
ADD CONSTRAINT pk_sales_data PRIMARY KEY(id), 
ADD CHECK (price >=0), 
ADD CHECK (quantity >= 0);

ALTER TABLE sales_data 
MODIFY id varchar(36) NOT NULL,
MODIFY id varchar(36) UNIQUE,
MODIFY product_id int NOT NULL,
MODIFY customer_id int NOT NULL,
MODIFY COLUMN `timestamp` DATETIME;

CREATE INDEX ts on sales_data(`timestamp`);