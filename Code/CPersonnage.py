import tkinter
import time

class CPersonnage():
	"""
	<=== CPersonnage ===>
	Classe correspondant au personnage,
	elle peut permettre au joueur de se deplacer
	"""
	def __init__(self, pmap, pcolor="#FFFFFF", pwidth=20, pheight=20, px=0, py=0, pstarpos=[-1,-1]):
		self.map = pmap
		self.color = pcolor
		self.width = pwidth
		self.height = pheight
		self.x = px
		self.y = py		 
		self.personnage = None # corps du personnage
		self.speed = 10 # vitesse du personnage
		self.avancement = 1 # coefficient d'avancement (pixel)
		self.game_running = False # status du jeu
		self.startPos = pstarpos # position de depart
		self.movementTab = []
	
	# fonction qui initialise l'objet CPersonnage
	def obj_init(self):
		self.canvas = self.map.canvas
		self.personnage = self.canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, fill=self.color)	 
		#   === Lien entre les evenements avec les fonctions de deplacement ===
		self.map.fenetre.bind("<KeyPress>", lambda e: self.__keydown(e)) 
		self.map.fenetre.bind("<KeyRelease>", lambda e: self.__keyup(e)) 
		self.__movement()
		self.canvas.pack()

    #   === Gestion du deplacement === 
    # fonction qui deplace le CPersonnage a ses coordonnees x et y
	def __movement(self):
		
		if (37 in self.movementTab) or (113 in self.movementTab): # left
			self.__left()
		if (38 in self.movementTab) or (111 in self.movementTab): # up
			self.__up()
		if (39 in self.movementTab) or (114 in self.movementTab): # right
			self.__right()
		if (40 in self.movementTab) or (116 in self.movementTab): # down
			self.__down()

		if self.x != self.canvas.coords(self.personnage)[0] or self.y != self.canvas.coords(self.personnage)[1]:
			self.canvas.move(self.personnage, self.x-self.canvas.coords(self.personnage)[0], self.y-self.canvas.coords(self.personnage)[1])
		self.canvas.after(self.speed, self.__movement) # se rappelle toutes les self.speed ms	
	# fonction qui est appelee quand Left est pressee
	def __left(self):
		if self.game_running:
			if self.x-self.avancement > 0:
				self.x -= self.avancement
			else:
				self.x = 0
    # fonction qui est appelee quand Right est pressee
	def __right(self):
		if self.game_running:
			if self.x+self.avancement < self.map.width-self.width:
				self.x += self.avancement
			else:
				self.x = self.map.width-self.width
    # fonction qui est appelee quand Up est pressee
	def __up(self):
		if self.game_running:
			if self.y-self.avancement >= 0:
				self.y -= self.avancement
			else:
				self.y = 0
    # fonction qui est appelee quand Down est pressee
	def __down(self):
		if self.game_running:
			if self.y+self.avancement <= self.map.height-self.height:
				self.y += self.avancement
			else:
				self.y = self.map.height-self.height
	# fonction qui est appelee quand l'une des touches Haut, Bas, Gauche ou Droite est relachee
	def __keyup(self, e):
		if self.game_running:
			if  e.keycode in self.movementTab:
				self.movementTab.pop(self.movementTab.index(e.keycode))
	# fonction qui est appelee quand l'une des touches Haut, Bas, Gauche ou Droite est pressee
	def __keydown(self, e):
		if self.game_running:
			if not e.keycode in self.movementTab:
				self.movementTab.append(e.keycode)
