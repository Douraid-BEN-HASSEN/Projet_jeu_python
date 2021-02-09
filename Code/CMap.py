import tkinter

class CMap:
	"""
	<=== CMap ===>
	Classe correspondant au plateau du jeu, 
	elle contient tous les elements (personnage, obstacles, etc...)
	elle peut ajouter ou supprimer des elements
	"""
	def __init__(self, ptitle="Titre", pwidth=800, pheight=600, pcolor="#DCDCDC"):
		self.title = ptitle
		self.width = pwidth
		self.height = pheight
		self.color = pcolor
		self.element = [] # tableau contenant les element de la map
		self.fenetre = None # parent de la map
		self.canvas = None # corps de la map
 
	# fct qui creer la map
	def obj_init(self):
		self.canvas = tkinter.Canvas(master=self.fenetre, width=self.width, height=self.height, bg=self.color)
	# fct qui permet l'ajout d'element
	def add(self, pelement):
		if isinstance(pelement, list):
			self.element += pelement
		else:
			self.element.append(pelement)
	# fct qui indique si deux element se touchent
	def elements_intersect(self, pelement1, pelement2):		
		if (pelement1.x+pelement1.width >= pelement2.x and pelement1.x <= pelement2.x+pelement2.width) and (pelement1.y+pelement1.height >= pelement2.y and pelement1.y <= pelement2.y+pelement2.height):
		    return True # les elements se touchent
		else:
		    return False # les elements ne se touchent pas





