
CREATE TABLE "softCartFactSales"
(
    id INT PRIMARY KEY NOT NULL UNIQUE,
    item_id INT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES "softCartDimItem"(id),
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES "softCartDimCategory"(id),
    country_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES "softCartDimCountry"(id),
    sold_value DECIMAL(10, 2) NOT NULL,
    date_id INT NOT NULL,
    FOREIGN KEY (date_id) REFERENCES "softCartDimDate"(id)
);
CREATE INDEX idx_softCartFactSales_category_id ON "softCartFactSales"(category_id);
CREATE INDEX idx_softCartFactSales_country_id ON "softCartFactSales"(country_id);



