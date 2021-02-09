class CArrivee(object):
    """
	<=== CArrivee ===>
	Cette classe représente la classe mère des objets arrivées, elle correspond à 
    l'emplacement d'arrivée dans la zone de jeu : si un objet de type CPersonnage est en contact avec
	"""
    def __init__(self, pmap, pcolor="#00FF00", pwidth=50, pheight=50, px=0, py=0):
        self.map = pmap
        self.color = pcolor
        self.width = pwidth
        self.height = pheight
        self.x = px
        self.y = py
        self.canvas = None
        self.arrivee = None
        self.speed = 1

    def obj_init(self):
        self.canvas = self.map.canvas
        self.arrivee = self.canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, fill=self.color)
        self.movement()
         
    def movement(self):
        if self.x != self.canvas.coords(self.arrivee)[0] or self.y != self.canvas.coords(self.arrivee)[1]:
            self.canvas.move(self.arrivee, self.x-self.canvas.coords(self.arrivee)[0], self.y-self.canvas.coords(self.arrivee)[1])
        self.canvas.after(1, self.movement) # se rappelle toutes les 1 ms

    def move(self, px, py):
        self.x = px
        self.y = py
