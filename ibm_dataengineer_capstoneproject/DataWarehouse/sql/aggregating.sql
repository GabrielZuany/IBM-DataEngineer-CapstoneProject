-- grouping sets
select 
	cn."country_name" as country,
	ct."category_name" as category,
	sum(sf."sold_value") as total_amount
from "softCartFactSales" sf
join "softCartDimCountry" cn on cn.id = sf.country_id 
join "softCartDimCategory" ct on ct.id = sf.category_id 
group by grouping sets(
	(country,category)
);

-- rollup
select 
	cn."country_name" as country,
	dt."year",
	sum(sf."sold_value") as total_amount
from "softCartFactSales" sf
join "softCartDimCountry" cn on cn.id = sf.country_id 
join "softCartDimDate" dt on dt.id = sf.date_id 
group by rollup(country,category);

-- cube 
select 
	cn."country_name" as country,
	dt."year",
	round(avg(sf."sold_value"), 2) as total_amount
from "softCartFactSales" sf
join "softCartDimCountry" cn on cn.id = sf.country_id 
join "softCartDimDate" dt on dt.id = sf.date_id 
group by cube(country,year);

-- CREATE TABLE "MQTSalesPerCountry" as 
CREATE view "ViewSalesPerCountry" as 
select 
    cn."country_name" as country,
    round(sum(sf."sold_value"), 2) as total_amount
from "softCartFactSales" sf
join "softCartDimCountry" cn on cn.id = sf.country_id
group by country;
