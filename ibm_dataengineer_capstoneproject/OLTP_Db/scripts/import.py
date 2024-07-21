import os
import uuid
import pandas as pd
from sqlalchemy import create_engine

csv = pd.read_csv('oltpdata.csv')
csv.columns = ['product_id', 'customer_id', 'price', 'quantity', 'timestamp']
csv['id'] = [uuid.uuid4() for _ in range(len(csv.index))]
csv = csv[['id', 'product_id', 'customer_id', 'price', 'quantity', 'timestamp']]
csv.to_csv('oltpdata_transformed.csv', index=False, header=False)

# os.system('docker cp oltpdata_transformed.csv ibm_project_mysql:/oltpdata_transformed.csv')
# os.system('docker exec -i ibm_project_mysql mysql -u root -proot -e "use oltp_db; LOAD DATA LOCAL INFILE \'/path/to/oltpdata_transformed.csv\' INTO TABLE sales_data FIELDS TERMINATED BY \',\' LINES TERMINATED BY \'\\n\' (id, product_id, customer_id, price, quantity, timestamp);"')

engine = create_engine('mysql+pymysql://root:root@localhost:3306/oltp_db')
csv.to_sql('sales_data', con=engine, if_exists='replace', index=False)