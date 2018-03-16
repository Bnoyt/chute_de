# Simulation de la chute d'un dé à 6 faces
Programme python qui simule la chute en 3D d'un dé à 6 faces

*Ce programme nécessite matlpotlib ou vpython pour fonctionner : F5 pour lancer

* Tous les calculs sont effectués, et ensuite seulement on crée l'animation, pour des questions de performances. En effet, l'animation ne requiert aucune spécification particulière, alors que les calculs peuvent saturer le processeur. Nous avons privilégié la programmation orientée objet, dans un souci de clarté et d'organisation : ceci est un travail de groupe, il était plus simple de tout séparer en classes pour que chacun puisse faire les fonctions qu'il devait faire pendant les vacances, sans se soucier du résultat de celles des autres.

 Notre modélisation semble restranscrire la réalité avec une fidélité acceptable, du moins au début de l'animation. L'évolution quelque peu chaotique du mouvement du cube est fidèle à la réalité.
 Mais il faut cependant soulever 2 problèmes majeurs :
	1) Notre programme est déterministe (aux erreurs de python près): pour un état initial donné, l'état final sera systématiquement le même (et heureusement sinon ça ne serait pas aussi évident à programmer), alors qu'en réalité, l'état final est aléatoire (la distribution des résultats de faces d'un lancer de dé parfaitement équilibré est équiprobable)

	2) On remarquera que le cube à la fin de l'animation ne se stoppe pas sur une face, comme le voudrait la réalité. Notre explication à ce résultat quelque peu inattendu est qu'à cet instant là, la force de réaction du sol est telle que tous les moments se compensent, et donc le cube est dans un état stable (nous avons regardé précisement les valeurs finales, et avons tiré de là nos conclusions.

	D'autre part, dans la fonction <>class cube<tourner>> nous avons pris quelques libertés sur la réalité par rapport à la réaction du sol.

	En fait, le vrai problème est la modélisation du sol que nous avons prise. En effet, modéliser le sol par une action élastique ne rend pas réellement compte de la réalité. A la limite, on aurait pu imaginer un cube construit de ressorts reliés entre eux sur les arêtes et les diagonales (mais le problème aurait été autrement plus complexe).

	Quand le cube touche le sol sur un coin, il faut aussi tenir compte des phénomènes de précession qui entrent en jeu. Peut-être aurions-nous pu travailler directement sur les énergies et regarder les échanges qui ont lieu au contact du sol (effet Joule, transmission partielle de l'energie cinétique du centre de gravité à l'énergie cinétique de rotation du cube). On remarquera d'ailleurs dans le cas de notre cube, que si l'on annule tous les frottements, notre énergie mécanique totale tend vers l'infini.

Ainsi, notre modélisation rend compte de la réalité de manière fiable, mais imparfaite. Toute la discussion se faisant autour de l'étude du mouvement. Nous n'avons pas encore les outils mathématiques et physiques nous permettant de décrire celui-ci avec précision
