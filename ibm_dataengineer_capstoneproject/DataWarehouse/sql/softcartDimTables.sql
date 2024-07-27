CREATE TABLE "softCartDimDate"
(
    id INT PRIMARY KEY NOT NULL UNIQUE,
    date DATE NOT NULL,
    day INT CHECK (day BETWEEN 1 AND 31),
    month INT CHECK (month BETWEEN 1 AND 12),
    year INT CHECK (year BETWEEN 1900 AND 2100),
    month_name VARCHAR(20) CHECK (month_name IN ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')),
    quarter INT CHECK (quarter BETWEEN 1 AND 4)
);

CREATE TABLE "softCartDimCategory"
(
    id INT PRIMARY KEY NOT NULL UNIQUE,
    category_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE "softCartDimCountry"
(
    id INT PRIMARY KEY NOT NULL UNIQUE,
    country_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE "softCartDimItem"
(
    id INT PRIMARY KEY NOT NULL UNIQUE,
    item_name VARCHAR(50) NOT NULL UNIQUE,
    price DECIMAL(10, 2) NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES "softCartDimCategory"(id),
    country_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES "softCartDimCountry"(id)
);
CREATE INDEX idx_softCartDimItem_category_id ON "softCartDimItem"(category_id);
CREATE INDEX idx_softCartDimItem_country_id ON "softCartDimItem"(country_id);

-----------------------------------

