/* •Напишете заявка, която за всеки кораб извежда името му, държавата, броя оръдия и годината на пускане (launched).
 */
SELECT ships.name, classes.country, classes.numguns, ships.launched
FROM ships
JOIN classes ON ships.class = classes.class;

/*•Повторете горната заявка като този път включите в резултата и класовете, които нямат кораби, но съществуват кораби със същото име като тяхното.*/
SELECT ships.name, classes.country, classes.numguns, ships.launched
FROM classes
LEFT JOIN ships
ON ships.class = classes.class OR ships.name = classes.class;


/* Напишете заявка, която извежда имената на корабите, участвали в битка от 1942г.*/
SELECT outcomes.ship
FROM outcomes
JOIN
	(SELECT name
	FROM battles
	WHERE date > '1941-12-31' AND date < "1943-1-1") as battle
ON battle.name == outcomes.battle as ship;

/*• За всяка страна изведете имената на корабите, които никога не са участвали в битка.*/
SELECT classes.country, ships.name
FROM classes
JOIN
	(SELECT ships.name, ships.class
	FROM ships
	LEFT JOIN outcomes
	ON ships.name == outcomes.ship
	WHERE outcomes.battle is null) as ships
ON ships.class == classes.class;
