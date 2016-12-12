/*   Напишете заявка, която извежда средната скорост на компютрите */
SELECT AVG(PC.speed)
FROM PC;

/*  Напишете заявка, която извежда средния размер на екраните на лаптопите за всеки производител. */
SELECT product.maker, AVG(SCREEN)
FROM laptop
JOIN product
ON product.model == laptop.model
GROUP BY product.maker;

/*Напишете заявка, която извежда средната скорост на лаптопите с цена над 1000.*/
SELECT AVG(laptop.speed)
FROM laptop
WHERE price > 1000;

/*• Напишете заявка, която извежда средната цена на компютрите според различните им hd.*/
SELECT PC.hd, AVG(pc.price)
FROM PC
GROUP BY PC.hd;

/*• Напишете заявка, която извежда средната цена на компютрите за всяка скорост по-голяма от 500.*/
SELECT AVG(pc.price)
FROM PC
WHERE pc.speed > 500;

/*• Напишете заявка, която извежда средната цена на компютрите произведени от производител ‘A’.*/
SELECT AVG(pc.price)
FROM pc
JOIN product
ON pc.model = product.model and product.maker = 'A';

/*• Напишете заявка, която извежда средната цена на компютрите и лаптопите за производител ‘B’*/
SELECT (AVG(laptop.price) + pc.avg)/2
FROM laptop
JOIN product
ON laptop.model = product.model and product.maker = 'B'
JOIN
	(SELECT AVG(pc.price) as avg
	FROM pc
	JOIN product
	ON pc.model = product.model and product.maker = 'B') as pc;
/*• Напишете заявка, която извежда производителите, които са произвели поне по 3 различни модела компютъра. 
Помислете каква заявка можете да напишете за да сте сигурни в отговора, например да изведете за всеки производител, броя различни модели компютри.*/
SELECT product.maker, COUNT(product.maker)
FROM
(SELECT DISTINCT product.model, product.maker
FROM product) as product
GROUP BY product.maker
HAVING COUNT(product.maker) > 2;

/*• Напишете заявка, която извежда производителите на компютрите с най-висока цена.*/
SELECT product.maker
FROM product
WHERE product.model = 
	(SELECT pc.model
	FROM pc
	WHERE price = (SELECT MAX(pc.price)
					FROM pc));
					
/*Напишете заявка, която извежда средния размер на диска на тези компютри произведени от производители, които произвеждат и принтери.*/
SELECT pc.maker, AVG(pc.hd)
FROM
	(SELECT product.maker, pc.hd
	FROM pc
	JOIN product
	ON product.model = pc.model
	JOIN
		(SELECT DISTINCT product.maker
		FROM product
		JOIN printer
		ON product.model == printer.model) as printerMaker
	ON printerMaker.maker = product.maker) as pc
GROUP BY maker;
