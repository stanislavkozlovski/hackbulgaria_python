/*Напишете заявка, която за всеки филм, по-дълъг от 120 минути, извежда заглавие, година, име и адрес на студио.*/
SELECT movie.title, movie.year, studio.name, studio.address
FROM movie
INNER JOIN studio
ON movie.length > 120 AND movie.studioname = studio.name;
/*
Напишете заявка, която извежда името на студиото и имената на актьорите, участвали във филми, произведени от това студио, подредени по име на студио.*/
SELECT movie.studioname, starsin.starname
FROM starsin
INNER JOIN movie
ON movie.title = starsin.movietitle
ORDER BY movie.studioname
/*Напишете заявка, която извежда имената на продуцентите на филмите, в които е играл Harrison Ford.*/
SELECT movieexec.name
FROM movieexec
WHERE movieexec.cert = 
	(SELECT movie.producer
	FROM movie
	INNER JOIN
		(SELECT starsin.movietitle, starsin.movietitle
		FROM starsin
		WHERE starname="Harrison Ford") as hfMovie
	ON hfMovie.movietitle = movie.title);
/*Напишете заявка, която извежда имената на актрисите, играли във филми на MGM*/
SELECT moviestar.name
FROM moviestar
INNER JOIN 
	(SELECT starsin.starname
	FROM starsin
	INNER JOIN
		(SELECT movie.title
		FROM movie
		WHERE movie.studioname = "MGM") as mgmMovie
	ON mgmMovie.title = starsin.movietitle) as actor
ON actor.starname = moviestar.name and moviestar.gender = "F";
/*Напишете заявка, която извежда името на продуцента и имената на филмите, продуцирани от продуцента на ‘Star Wars’.*/
SELECT producer.name, movie.title
FROM movie
INNER JOIN
	(SELECT movieexec.name, movieexec.cert
	FROM movieexec
	INNER JOIN movie
	ON movie.title = "Star Wars" AND movie.producer = movieexec.cert) as producer
WHERE movie.producer = producer.cert;
/*Напишете заявка, която извежда имената на актьорите не участвали в нито един филм*/
SELECT moviestar.name
FROM moviestar
LEFT JOIN starsin ON starsin.starname = moviestar.name
WHERE starsin.starname IS NULL;

SELECT moviestar.name
FROM moviestar
WHERE moviestar.name NOT IN (SELECT DISTINCT starsin.starname FROM starsin);

/* aktiori, adres na studio na film v koito e uchastval*/
SELECT studio_and_names.starname, studio.address
FROM (
	SELECT movie.studioname, movie_.starname
	FROM movie
	INNER JOIN
		(SELECT starsin.starname, starsin.movietitle
		FROM starsin) as movie_
	ON movie.title = movie_.movietitle) as studio_and_names
LEFT JOIN studio
ON studio_and_names.studioname == studio.name;

/*imena na aktiori, rodeni predi 1950 i v filmi predi 2000*/
SELECT DISTINCT star.name
FROM movie
INNER JOIN
	(SELECT DISTINCT moviestar.name, starsin.movietitle
	FROM moviestar
	INNER JOIN (SELECT DISTINCT starsin.starname, starsin.movietitle
				FROM starsin) as starsin
	WHERE moviestar.birthdate < "1950-01-01") as star
ON movie.title = star.movietitle
WHERE movie.year < 2000;
