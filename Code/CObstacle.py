class CObstacle(object):
    """
	<=== CObstacle ===>
	Cette classe représente la classe mère des objets obstacles, elle correspond à un obstacle dans 
    la zone de jeu qui fait perdre l'utilisateur : si un objet de type CPersonnage est en contact avec
	"""
    
    def __init__(self, pmap, pcolor="#696969", pwidth=100, pheight=20, px=0, py=0):
        self.map = pmap
        self.color = pcolor
        self.width = int(pwidth)
        self.height = int(pheight)
        self.x = int(px)
        self.y = int(py)
        self.canvas = None
        self.obstacle = None
        self.speed = 1

    def obj_init(self):
        self.canvas = self.map.canvas
        self.obstacle = self.canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, fill=self.color)
        self.__movement()

    def __movement(self):
        if self.x != self.canvas.coords(self.obstacle)[0] or self.y != self.canvas.coords(self.obstacle)[1]:
            self.canvas.move(self.obstacle, self.x-self.canvas.coords(self.obstacle)[0], self.y-self.canvas.coords(self.obstacle)[1])
        self.canvas.after(1, self.__movement) # se rappelle toutes les 1 ms

    def move(self, px, py):
        self.x = px
        self.y = py
