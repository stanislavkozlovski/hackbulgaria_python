/*Напишете заявка, която извежда имена на случителите и общата стойност на покупките им.*/
SELECT employees.firstname, employees.lastname, customer.price
FROM
	(SELECT SUM(customer.unitprice) as price, customer.id
	FROM 
		(SELECT SUM([order details].unitprice) as unitprice, orders.employeeid as id
		FROM orders
		JOIN [order details]
		ON orders.orderid = [order details].orderid
		GROUP BY customerid) as customer
	GROUP BY customer.id) as customer
JOIN employees
ON employees.employeeid = customer.id;

/*Изведете 10-те най-скъпи продукта.*/
SELECT products.unitprice
FROM products
ORDER BY products.unitprice DESC
LIMIT 10;

/*Напишете заявка, която извежда броят на всички продукти спрямо техните категории.*/
SELECT categories.categoryname, product.productCount
FROM
	(SELECT COUNT(products.productid) as productCount, products.categoryid
	FROM products
	GROUP BY products.categoryid) as product
JOIN categories
ON categories.categoryid = product.categoryid;

/*Изведете най-поръчваните 5 продукта.*/
SELECT products.productname
FROM
	(SELECT COUNT([order details].orderid), [order details].productid
	FROM [order details]
	GROUP BY [order details].productid
	ORDER BY COUNT([order details].orderid) DESC
	LIMIT 5) as topProduct
JOIN products
ON products.productid = topProduct.productid;

/*Изведете описанията на регионите на служителите с най-много поръчки.*/
SELECT region.regiondescription
FROM
	(SELECT DISTINCT territories.regionid
	FROM
		(SELECT employeeterritories.employeeid, employeeterritories.territoryid
		FROM
			(SELECT employees.employeeid
			FROM
				(SELECT orders.employeeid
				FROM orders
				GROUP BY orders.employeeid
				ORDER BY COUNT(orders.orderid) DESC
				LIMIT 1) as maxOrder
			JOIN employees
			ON employees.employeeid = maxOrder.employeeid) as maxEmployee
		JOIN employeeterritories
		ON employeeterritories.employeeid = maxEmployee.employeeid) as employeeterritories
	JOIN territories
	ON territories.territoryid = employeeterritories.territoryid) as employeeregion
JOIN region
ON region.regionid = employeeregion.regionid;
