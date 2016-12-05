/*Напишете заявка, която извежда имената на актьорите мъже участвали в ‘Terms
of Endearment*/
SELECT starsin.starname
FROM starsin
WHERE starsin.movietitle == "Terms of Endearment";
/*Напишете заявка, която извежда имената на актьорите участвали във филми продуцирани от ‘MGM’през 1995 г.*/
SELECT starsin.starname
FROM starsin, movie
WHERE starsin.movietitle == movie.title AND movie.studioname = "MGM" AND movie.year = 1995;
/*Напишете заявка, която извежда името на президента на ‘MGM’*/
SELECT DISTINCT movieexec.name
FROM movieexec, studio, movie
WHERE studio.name == movie.studioname AND movieexec.cert == movie.producer;
/*Напишете заявка, която извежда имената на всички филми с дължина по-голяма от дължината на филма ‘Gone With the Wind’*/
SELECT *
FROM movie
WHERE movie.length > (
SELECT movie.length FROM movie WHERE movie.title = "Gone With the Wind");
/*Напишете заявка, която извежда имената на тези продукции на стойност по- голяма от ‘Mery Griffin’*/
SELECT movieexec.name
FROM movieexec
WHERE movieexec.networth >
(SELECT movieexec.networth FROM movieexec WHERE movieexec.name = "Merv Griffin");