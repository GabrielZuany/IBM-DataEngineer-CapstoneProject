import psycopg2 as pg
import os
import pandas as pd
import random
import faker

SOURCE = os.path.join(os.path.dirname(__file__), '../source')
conn = pg.connect(database="softcart", user="root", password="root", host="localhost", port="5432")
cur = conn.cursor()

def create_faker():
    fake = faker.Faker()
    num_rows = 100
    data = []
    for _ in range(num_rows):
        item = {
            "id": _ + 1,
            "item_name": fake.unique.word(), 
            "price": round(random.uniform(1.00, 2500.00), 2),
            "category_id": random.randint(1, 5),  
            "country_id": random.randint(1, 56) 
        }
        data.append(item)
    df = pd.DataFrame(data)
    df.to_csv(f'{SOURCE}/DimItem.csv', index=False)

def insert_categories():
    categories = pd.read_csv(os.path.join(SOURCE, 'DimCategory.csv'))
    for i, row in categories.iterrows():
        cur.execute('INSERT INTO "softCartDimCategory" (id, category_name) VALUES (%s, %s)', (row['categoryid'], row['category']))
    conn.commit()

def insert_countries():
    countries = pd.read_csv(os.path.join(SOURCE, 'DimCountry.csv'))
    for i, row in countries.iterrows():
        cur.execute('INSERT INTO "softCartDimCountry" (id, country_name) VALUES (%s, %s)', (row['countryid'], row['country']))
    conn.commit()

def insert_dates():
    dates = pd.read_csv(os.path.join(SOURCE, 'DimDate.csv'))
    for i, row in dates.iterrows():
        cur.execute(f'INSERT INTO "softCartDimDate" (id, date, day, month, year, month_name, quarter) VALUES ({row["dateid"]}, \'{row["date"]}\', {row["Day"]}, {row["Month"]}, {row["Year"]}, \'{row["Monthname"]}\', {row["Quarter"]})')
    conn.commit()

def insert_items():
    items = pd.read_csv(os.path.join(SOURCE, 'DimItem.csv'))
    for i, row in items.iterrows():
        cur.execute(f'INSERT INTO "softCartDimItem" (id, item_name, price, category_id, country_id) VALUES ({row["itemid"]}, \'{row["itemname"]}\', {row["price"]}, {row["categoryid"]}, {row["countryid"]})')
    conn.commit()

def insert_sales():
    sales = pd.read_csv(os.path.join(SOURCE, 'FactSales.csv'))
    for i, row in sales.iterrows():
        response = cur.execute(f'SELECT "id" FROM "softCartDimItem" WHERE category_id = {row["categoryid"]} LIMIT 1')
        itemid = cur.fetchone()
        itemid = itemid[0] if itemid else 0
        cur.execute(f'INSERT INTO "softCartFactSales" (id, item_id, date_id, country_id, category_id, sold_value) VALUES ({row['orderid']}, {itemid}, {row['dateid']}, {row['countryid']}, {row['categoryid']}, {row['amount']})')
    conn.commit()

if __name__ == "__main__":
    create_faker()
    insert_categories()
    insert_countries()
    insert_dates()
    insert_items()
    insert_sales()
    cur.close()
    conn.close()