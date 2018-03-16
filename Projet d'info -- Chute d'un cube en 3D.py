from visual import *
from math import *
from time import clock

########################
##      Principe      ##
########################

# Ce programme nécessite matlpotlib ou vpython pour fonctionner : F5 pour lancer

# Tous les calculs sont effectués, et ensuite seulement on crée l'animation, pour des questions de performances. En effet, l'animation ne requiert aucune spécification particulière, alors que les calculs peuvent saturer le processeur. Nous avons privilégié la programmation orientée objet, dans un souci de clarté et d'organisation : ceci est un travail de groupe, il était plus simple de tout séparer en classes pour que chacun puisse faire les fonctions qu'il devait faire pendant les vacances, sans se soucier du résultat de celles des autres.

# Nos commentaires sont à partir de la ligne 483 (tout en bas, à la fin)


########################
## Données à rentrer  ##
########################

module = "matplotlib"   #à  choisir : vpython (3D) ou matplotlib (courbes => rdv ligne 389 pour paramétrer)

#masse (en kg)
#L'expérience a montré que des masses plus petites engendraient des erreurs d'arrondi non négligeables
masse = 1
#longueur du coté (en m)
#L'expérience a montré que des longueurs plus petites engendraient des erreurs d'arrondi non négligeables
cote = 0.3
#inclinaison du support selon l'axe Ox (en rad)
#Dans le cas d'une inclinaison non-nulle, le cube va à  l'infini (nous n'avons pas modélisé de frottements solides)
alpha = 0
#raideur du sol (en N/m)
#L'expérience a montré que cet ordre de grandeur (1000) était le plus réaliste
raideur = 1000
#amortissement du sol (en N*s/m)
#coefficient empirique qui permet à  l'expérience d'être plus réaliste 
#(très concrètement cela permet à  l'objet de ralentir plus fortement lorsqu'il touche le sol)
#Attention, ce coefficient dépend de tc (voir ligne 316)
c3 = 0.002
#coefficients de frottement visqueux (en N*s/m)
#c1 : frottement visqueux de l'air sur le cube #c2 : frottement visqueux lié à  la rotation du cube
c1 = 0.05
c2 = 0.002
#accélération de la pesanteur (en N/kg)
g = 9.81
#angles d'euler initiaux (en rad)
theta0 = 2
phi0 = 3
psi0 = 1
#hauteur de chute (en m)
h = 2
#vitesse initiale (en m/s) selon Ox, Oy, Oz
vx0 = 0
vy0 = 0
vz0 = 0
#vitesse initiale angulaire (en rad/s)
vtheta0 =0.1
vphi0 = 0.3
vpsi0 = 0.2
#écart de temps entre chaque calcul de valeur (en s)
#0.001 est la valeur minimale à  utiliser : en dessous l'expérience ne fonctionne plus de manière optimale (erreurs d'arrondi), et puis il faut changer c3 (voir plus haut)
tc = 0.001
#fréquence de raffraichissement pour la modélisation (en fps)
fps = 100
#durée de l'animation (en s)
tps = 15


#######################
##      Classes      ##
#######################

#Le programme est divisé en 4 classes : 
# 1) classe sol : regroupe tout ce qui a trait au comportement du sol 

# 2) classe valeurs : regroupe le tableau des valeurs lors du calcul, pour permettre l'affichage ensuite

# 3) classe cube : la plus importante certainement qui regroupe tout ce qui est en rapport avec le cube (explicitée plus bas)

# 4) classe animation : classe qui regroupe tout ce qui est lié à  l'affichage des valeurs





class sol(object):
	def __init__(self,raideur,alpha,c3):
		self.k = raideur
		self.alpha = alpha
		self.amor = c3

class valeurs(object):
	def __init__(self):
		self.x = []
		self.y = []
		self.z = []
		self.theta = []
		self.phi = []
		self.psi = []
		self.temps = []
		self.ec = []
		self.vx = []
		self.vy = []
		self.vz = []
		self.vtheta = []
		self.vphi = []
		self.vpsi = []


		self.nb = 0

	def ajouter(self,x,y,z,theta,phi,psi,tc,vx,vy,vz,m,vtheta,vphi,vpsi): 
		# Ajout de toutes les nouvelles valeurs au tableau
		self.temps += [self.nb*tc]
		self.nb += 1
		self.x += [x]
		self.y += [y]
		self.z += [z]
		self.ec += [(vy*vy + vz*vz + vx*vx)*1/2*m]
		self.theta += [theta]
		self.phi += [phi]
		self.psi += [psi]
		self.vx += [vx]
		self.vy += [vy]
		self.vz += [vz]
		self.vtheta += [vtheta]
		self.vphi += [vphi]
		self.vpsi += [vpsi]

class cube(object):
	def __init__(self,cote,masse,x,y,z,vx,vy,vz,theta,phi,psi,vtheta,vphi,vpsi,c1,c2,g):
		
		self.J = masse*cote*cote/6.
		self.masse = masse
		self.cote = cote

		self.fp = vector(0,0,0)
		self.fg = -9.81*masse

		self.x = x
		self.y = y
		self.z = z
		self.vx = vx
		self.vy = vy
		self.vz = vz
		self.theta = theta
		self.phi = phi
		self.psi = psi

		self.vtheta = vtheta
		self.vphi = vphi
		self.vpsi = vpsi

		self.c1 = c1
		self.c2 = c2

		# Les coordonnées des vecteurs allant du centre vers chacun des coins nous permettront plus tard de calculer les moments
		self.coins = [vector(cote/2,cote/2.,-cote/2.),vector(cote/2,cote/2.,cote/2.),
					vector(cote/2,-cote/2.,cote/2.),vector(cote/2,-cote/2.,-cote/2.),
					vector(-cote/2,cote/2.,-cote/2.),vector(-cote/2,cote/2.,cote/2.),
					vector(-cote/2,-cote/2.,cote/2.),vector(-cote/2,-cote/2.,-cote/2.)]


		# Les axes seront mis à  jour constamment
		self.axetheta = vector(1,0,0)
		self.axephi = vector(0,1,0)
		self.axepsi = vector(0,0,1)

		# Un axe qui joue le role de case vide à  remplir avec n'importe lequel des autres axes
		# Il a son utilité dans la fonction tourner
		self.taxe = vector(0,0,0)

	def tourner(self,angle,axe):
		# Cette fonction porte bien son nom : elle fait tourner le cube d'un certain angle selon un certain axe
		# De ce fait, toutes les grandeurs liées au cube varient avec elle

		if axe == 1:
			self.taxe = self.axetheta 
			vivitesse = self.vtheta
		else:
			if axe == 2:
				self.taxe = self.axephi
				vivitesse = self.vphi
			else:
				self.taxe = self.axepsi
				vivitesse = self.vpsi

		for i in range(len(self.coins)):
			# On fait tourner tous les coins
			self.coins[i] = self.coins[i].rotate(angle,self.taxe)

		if axe == 1:
			# On doit aussi faire tourner les autres axes
			self.axephi = self.axephi.rotate(angle,self.taxe)
			self.axepsi = self.axepsi.rotate(angle,self.taxe)

			# On récupère un angle entre -2Pi et 2Pi 
			angle = fmod(angle + self.theta,2*pi)
			self.theta = angle

			# On fait varier la réaction du sol pour qu'elle soit plus réaliste
			# C'est empirique, validé par l'expérience
			angle = fmod(angle,pi/17)
			self.fp = self.fp.rotate(-angle*vivitesse/10,self.taxe)

		else:
			if axe == 2:

				self.axetheta = self.axetheta.rotate(angle,self.taxe)
				self.axepsi = self.axepsi.rotate(angle,self.taxe)

				angle = fmod(angle + self.phi,2*pi)
				self.phi = angle
				angle = fmod(angle,pi/17)
				self.fp = self.fp.rotate(-angle*vivitesse/10,self.taxe)
			else:

				self.axetheta = self.axetheta.rotate(angle,self.taxe)
				self.axephi = self.axephi.rotate(-angle,self.taxe)

				angle = fmod(angle + self.psi,2*pi)
				self.psi = angle
				angle = fmod(angle,pi/17)
				self.fp = self.fp.rotate(-angle*vivitesse/10,self.taxe)

		return()

	def checkcoins(self,sol):
		# cette fonction vérifie si un ou plusieurs coins sont en contact avec le sol
		# elle renvoie une liste avec les coordonnées de chaque coin concerné et sa perforation dans le sol

		reste = []
		for coin in self.coins:
			dessous = coin[2] + self.z - sin(sol.alpha) * self.y
			if dessous < 0:
				reste += [[coin,dessous]]
		return(reste)

	def calculfp(self,sol):
		# Calcule la force de réaction du sol en fonction de la réponse de checkcoins
		reste = self.checkcoins(sol)
		cocorico = []
		claire = vector(0,0,0)
		for elem in reste:
			epsilon = cos(sol.alpha)*elem[1]
			fpy =  sin(alpha) * sol.k * epsilon
			fpz = -  cos(alpha) * sol.k * epsilon
			fp = vector(0,fpy,fpz)
			cocorico += [[elem[0],fp]]
			claire += fp



		return cocorico,claire

	def calculmfp(self,cocorico,axe):
		# Calcule les moments scalaires
		toutou = vector(0,0,0)
		for elem in cocorico:
			toutou += cross(elem[0],elem[1])
		return dot(toutou,axe)




	def calculchute(self,sol,tc,tps):

		# On crée un tableau de valeurs
		valeur = valeurs()
		nombre = int(tps / tc)

		print( str(nombre) + " valeurs à  calculer en tout")
		
		# On ajoute les valeurs initiales
		valeur.ajouter(self.x,self.y,self.z,self.theta,self.phi,self.psi,tc,self.vx,self.vy,self.vz,self.masse,self.vtheta,self.vphi,self.vpsi)

		for i in range(nombre):
			
			cocorico,self.fp = self.calculfp(sol)

			if mag(self.fp) > 0: # si la norme de la force de réaction du support est non nulle, le sol amortit
				coefs = sol.amor
			else:
				coefs = 0 # sinon on amortit pas


			# après c'est la méthode d'euler, triviale, et remarquablement peu fiable et imprécise.

			temp = self.calculmfp(cocorico,self.axetheta)
			deltatheta = tc * self.vtheta
			dtheta = (temp - self.c2 * self.vtheta) / self.J
			self.vtheta = self.vtheta + tc * dtheta

			self.tourner(deltatheta,1)

			temp = self.calculmfp(cocorico,self.axephi)
			deltaphi = tc * self.vphi
			dphi = (temp - self.c2 * self.vphi) / self.J
			self.vphi = self.vphi + tc * dphi

			self.tourner(deltaphi,2)

			temp = self.calculmfp(cocorico,self.axepsi)
			deltapsi = tc * self.vpsi
			dpsi = (temp - self.c2 * self.vpsi) / self.J
			self.vpsi = self.vpsi + tc * dpsi

			self.tourner(deltapsi,3)

			self.vx = self.vx / (1. + coefs)
			self.vy = self.vy / (1. + coefs)
			self.vz = self.vz / (1. + coefs)
			self.vtheta = self.vtheta / (1. + 10*coefs)  # L'action du sol sur les vitesses des chacune des grandeurs
			self.vphi = self.vphi / (1. + 10*coefs)
			self.vpsi = self.vpsi / (1. + 10*coefs)

			#Cet ammortissement du sol se fait à chaque itération, il dépend donc de tc (l'échantillonage), mais c'est la meilleure modélisation que nous ayons pu faire
			#En effet, l'on pourrait inclure ce nouveau coefficient dans l'équation différentielle, mais le résultat n'est pas optimal


			temp = self.vx
			dx = (self.fp[0] - self.c1 * self.vx) / self.masse
			self.vx = self.vx + tc * dx
			self.x = self.x + tc * temp

			temp = self.vy
			dy = (self.fp[1] - self.c1 * self.vy) / self.masse
			self.vy = self.vy + tc * dy
			self.y = self.y + tc * temp


			temp = self.vz
			dz = (self.fg + self.fp[2] - self.c1 * self.vz) / self.masse
			self.vz = self.vz + tc * dz
			self.z = self.z + tc * temp


			# Après tous les calculs, on ajoute chacune des nouvelles valeurs au tableau de valeurs
			valeur.ajouter(self.x,self.y,self.z,self.theta,self.phi,self.psi,tc,self.vx,self.vy,self.vz,self.masse,self.vtheta,self.vphi,self.vpsi)


		return (valeur) # On renvoie les valeurs, par principe


class animation(object):
	def __init__(self,tc,tps,fps,cube,sol,module):
		self.tc = tc
		self.tps = tps
		self.fps = fps

		self.cube = cube
		self.sol = sol
		self.axetheta = vector(1,0,0)
		self.axephi = vector(0,1,0)
		self.axepsi = vector(0,0,1)


		if module == "matplotlib":
			self.mode = 1
		else:
			self.mode = 2


	def demarrer(self):

		print("Début des calculs")
		tps1 = clock()

		#Notre joli tableau de valeur de type <valeurs> est calculé
		valeurs = self.cube.calculchute(self.sol,self.tc,self.tps)

		print("Calculs effectués en " + str(clock() - tps1) + "s") 
		print("Lancement de l'animation")

		if self.mode == 1:

			import matplotlib.pyplot as plt

			# Avec matplotlib il est possible d'afficher un très grand nombre de grandeurs :

			# les trois angles d'euler : theta, phi, psi
			# les trois vitesses angulaires selon chacun des axes : vtheta, vphi, vpsi
			# les trois composantes de la position du centre de gravité : x, y, z
			# les trois composantes de la vitesse du centre de gravité : vx, vy, vz
			# l'énergie cinétique du cube (juste celle du mouvement, pas de la rotation)

			# Cela a été primordial lors du débogage du programme : en effet il est beaucoup plus simple d'apercevoir 
			# une abberation sur un graphe en deux dimensions que sur une animation 3D biscornue

			plt.plot(valeurs.x,valeurs.z)



		else:

			mainscene = display(title='The MasterCube',x=0, y=0, width=1200, height=800)
			mainscene.range = vector(self.cube.cote*7,self.cube.cote*7,self.cube.cote*7)

			pas = int (1. / (self.tc * self.fps))
			nb = int(self.tps/self.tc) / pas

			m = (max(abs(max(valeurs.y)), abs(min(valeurs.y))) + cube.cote)*2.2
			p = (max(abs(max(valeurs.x)), abs(min(valeurs.x))) + cube.cote)*2.2
			mmmm = max(valeurs.z)

			soli = box(pos = (0,0,-0.01), length = p, height = m, width = 0.02, color = color.red, material = materials.wood)
			soli.rotate(angle = self.sol.alpha, axis = (1,0,0))  #création du sol (remarque : la couleur est modifiable à souhait, pour peu que l'on connaisse la langue de Shakespeare : mais seules les couleurs principales marchent)

			cubi = box(pos = (valeurs.x[0],valeurs.y[0],valeurs.z[0]), length = cube.cote, height = cube.cote, width = cube.cote, color = color.blue ) #Création du cube (on peut aussi changer sa couleur)

			deltatheta = valeurs.theta[0]
			deltaphi = valeurs.phi[0]
			deltapsi = valeurs.psi[0]

			cubi.rotate(angle = deltatheta, axis = self.axetheta)
			self.axephi = self.axephi.rotate(deltatheta,self.axetheta)
			self.axepsi = self.axepsi.rotate(deltatheta,self.axetheta)

			cubi.rotate(angle = deltaphi, axis = self.axephi)
			self.axetheta = self.axetheta.rotate(deltaphi,self.axephi)
			self.axepsi = self.axepsi.rotate(deltaphi,self.axephi)

			cubi.rotate(angle = deltapsi, axis = self.axepsi)
			self.axetheta = self.axetheta.rotate(deltapsi,self.axepsi)
			self.axephi = self.axephi.rotate(deltapsi,self.axepsi)


			# Pour le rendu de l'animation, c'est un banal problème d'arithmétique, à  savoir dans un premier temps
			# combien de valeurs on va afficher et puis, après, quelles valeurs on va selectionner pour l'affichage


			for i in range(1,nb):


				deltatheta = valeurs.theta[pas*i] - valeurs.theta[pas*(i-1)]
				deltaphi = valeurs.phi[pas*i] - valeurs.phi[pas*(i-1)]
				deltapsi = valeurs.psi[pas*i] - valeurs.psi[pas*(i-1)]

				cubi.rotate(angle = deltatheta, axis = self.axetheta)
				self.axephi = self.axephi.rotate(deltatheta,self.axetheta)
				self.axepsi = self.axepsi.rotate(deltatheta,self.axetheta)

				cubi.rotate(angle = deltaphi, axis = self.axephi)
				self.axetheta = self.axetheta.rotate(deltaphi,self.axephi)
				self.axepsi = self.axepsi.rotate(deltaphi,self.axephi)

				cubi.rotate(angle = deltapsi, axis = self.axepsi)
				self.axetheta = self.axetheta.rotate(deltapsi,self.axepsi)
				self.axephi = self.axephi.rotate(deltapsi,self.axepsi)

				cubi.x = valeurs.x[pas*i]
				cubi.y = valeurs.y[pas*i]
				cubi.z = valeurs.z[pas*i]

				mainscene.center  = vector(cubi.x, cubi.y, 0)
				mainscene.forward = vector(-self.cube.cote,-self.cube.cote,-self.cube.cote)

				rate(self.fps)
				

		print("Animation terminée")



		return()


########################
## Début du programme  #
########################


sol = sol(raideur,alpha,c3)

cube = cube(cote,masse,0.,0.,h,vx0,vy0,vz0,theta0,phi0,psi0,vtheta0,vphi0,vpsi0,c1,c2,g)

animation = animation(tc,tps,fps,cube,sol,module)

animation.demarrer()



#######################
##    Commentaires   ##
#######################


# Notre modélisation semble restranscrire la réalité avec une fidélité acceptable, du moins au début de l'animation. L'évolution quelque peu chaotique du mouvement du cube est fidèle à la réalité.
# Mais il faut cependant soulever 2 problèmes majeurs :
	#1) Notre programme est déterministe (aux erreurs de python près): pour un état initial donné, l'état final sera systématiquement le même (et heureusement sinon ça ne serait pas aussi évident à programmer), alors qu'en réalité, l'état final est aléatoire (la distribution des résultats de faces d'un lancer de dé parfaitement équilibré est équiprobable)

	#2) On remarquera que le cube à la fin de l'animation ne se stoppe pas sur une face, comme le voudrait la réalité. Notre explication à ce résultat quelque peu inattendu est qu'à cet instant là, la force de réaction du sol est telle que tous les moments se compensent, et donc le cube est dans un état stable (nous avons regardé précisement les valeurs finales, et avons tiré de là nos conclusions.

	#D'autre part, dans la fonction <>class cube<tourner>> nous avons pris quelques libertés sur la réalité par rapport à la réaction du sol.

	#En fait, le vrai problème est la modélisation du sol que nous avons prise. En effet, modéliser le sol par une action élastique ne rend pas réellement compte de la réalité. A la limite, on aurait pu imaginer un cube construit de ressorts reliés entre eux sur les arêtes et les diagonales (mais le problème aurait été autrement plus complexe).

	#Quand le cube touche le sol sur un coin, il faut aussi tenir compte des phénomènes de précession qui entrent en jeu. Peut-être aurions-nous pu travailler directement sur les énergies et regarder les échanges qui ont lieu au contact du sol (effet Joule, transmission partielle de l'energie cinétique du centre de gravité à l'énergie cinétique de rotation du cube). On remarquera d'ailleurs dans le cas de notre cube, que si l'on annule tous les frottements, notre énergie mécanique totale tend vers l'infini.


# Ainsi, notre modélisation rend compte de la réalité de manière fiable, mais imparfaite. Toute la discussion se faisant autour de l'étude du mouvement. Nous n'avons pas encore les outils mathématiques et physiques nous permettant de décrire celui-ci avec précision





#######################
##  Fin du programme ##
#######################