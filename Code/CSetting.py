import sys
import re
from tkinter import messagebox
from CMap import CMap
from CArrivee import CArrivee
from CPersonnage import CPersonnage
from CObstacle import CObstacle

class CSetting():
    """
    Cette classe créer un outils permettant de gérer, créer, lire et écrire dans des fichiers propres au jeu
    à l'aide d'expression régulière simple
    """
    def readFile(self, ppath):
        try:
            content = ""
            with open(ppath, "r") as fichier:
                content = content + fichier.read()
        except:
            e = sys.exc_info()
            messagebox.showwarning("Erreur !", e)
            return False
        finally:
            fichier.close()
        
        return content 

    def createFile(self, ppath):
        try:
            fichier = open(ppath, 'x')
        except:
            e = sys.exc_info()
            messagebox.showwarning("Erreur !", e)
            return False
        finally:
            fichier.close()
            return True

    def updateFile(self, ppath, pdata):
        try:
            fichier = open(ppath, 'w')
            fichier.write(pdata)
        except:
            e = sys.exc_info()
            messagebox.showwarning("Erreur !", e)
            return False
        finally:
            fichier.close()
            return True

    def lire_niveau(self, pfichier_niveau_path):
        """
        lire chaque parametre a l'aide d'expression reguliere
        """
        contenu = self.readFile(ppath=pfichier_niveau_path)
        
        ########## MAP OBJECT ##########
        map_title = re.search("map_title=(.*?);", contenu).group(1)
        map_height = int(re.search("map_height=(.*?);", contenu).group(1))
        map_width = int(re.search("map_width=(.*?);", contenu).group(1))
        map_color = re.search("map_color=(.*?);", contenu).group(1)
        ########## ARRIVEE OBJECT ##########
        arrivee_x = int(re.search("arrivee_x=(.*?);", contenu).group(1))
        arrivee_y = int(re.search("arrivee_y=(.*?);", contenu).group(1))
        arrivee_width = int(re.search("arrivee_width=(.*?);", contenu).group(1))
        arrivee_height = int(re.search("arrivee_height=(.*?);", contenu).group(1))
        arrivee_color = re.search("arrivee_color=(.*?);", contenu).group(1)
        ########## PERSONNAGE OBJECT ##########
        personnage_color=re.search("personnage_color=(.*?);", contenu).group(1)
        personnage_width=int(re.search("personnage_width=(.*?);", contenu).group(1))
        personnage_height=int(re.search("personnage_height=(.*?);", contenu).group(1))
        personnage_x=int(re.search("personnage_x=(.*?);", contenu).group(1))
        personnage_y=int(re.search("personnage_y=(.*?);", contenu).group(1))
        ########## OBSTACLE OBJECT ##########
        obstacleTab = []
        obstacleTab.append(re.findall("obstacle_color=(.*?);", contenu))
        obstacleTab.append(re.findall("obstacle_x=(.*?);", contenu))
        obstacleTab.append(re.findall("obstacle_y=(.*?);", contenu))
        obstacleTab.append(re.findall("obstacle_width=(.*?);", contenu))
        obstacleTab.append(re.findall("obstacle_height=(.*?);", contenu))
        cobstacle_objTab = []

        # creer les objs
        cmap_obj = CMap(ptitle=map_title, pheight=map_height, pwidth=map_width, pcolor=map_color)
        carrivee_obj = CArrivee(pmap=cmap_obj, px=arrivee_x, py=arrivee_y, pwidth=arrivee_width, pheight=arrivee_height, pcolor=arrivee_color)
        cpersonnage_obj = CPersonnage(pmap=cmap_obj, pcolor=personnage_color, pwidth=personnage_width, pheight=personnage_height, px=personnage_x, py=personnage_y, pstarpos=[personnage_x,personnage_y])
        # plusieurs obstacles a creer
        for nb in range(0, len(obstacleTab[0])):
            cobstacle_objTab.append(CObstacle(pmap=cmap_obj, pcolor=obstacleTab[0][nb],px=obstacleTab[1][nb], py=obstacleTab[2][nb], pwidth=obstacleTab[3][nb], pheight=obstacleTab[4][nb]))
        
        return [cmap_obj, carrivee_obj, cpersonnage_obj, cobstacle_objTab]

    def lire_joueur(self, pfichier_joueur_path):
        """
        lire chaque parametre a l'aide d'expression reguliere
        """
        contenu = self.readFile(ppath=pfichier_joueur_path)
        data = [pfichier_joueur_path]
        data.append(re.search("name=(.*?);", contenu).group(1))
        data.append(int(re.search("score=(.*?);", contenu).group(1)))
        data.append(re.search("game=(.*?);", contenu).group(1))
        data.append(int(re.search("level=(.*?);", contenu).group(1)))
        return [data] # [nom_du_fichier, nom_du_joueur, score, sauvegarde, niveau]
    
    def load_game(self, pgame_data):
        
        # get map data
        map_data = '[' + re.search(r"map:\[(.*?)\],", pgame_data).group(1) + ']'
        cmap_obj = CMap()
        if re.search("map_title=(.*?)(?:,|])", map_data):
            cmap_obj.title = re.search("map_title=(.*?)(?:,|])", map_data).group(1)
        if re.search("map_color=(.*?)(?:,|])", map_data):
            cmap_obj.color = re.search("map_color=(.*?)(?:,|])", map_data).group(1)
        if re.search("map_height=(.*?)(?:,|])", map_data):
            cmap_obj.height = int(re.search("map_height=(.*?)(?:,|])", map_data).group(1))
        if re.search("map_width=(.*?)(?:,|])", map_data):
            cmap_obj.width = int(re.search("map_width=(.*?)(?:,|])", map_data).group(1))

        # get arrivee data
        arrivee_data = '[' + re.search(r"arrivee:\[(.*?)\],", pgame_data).group(1) + ']'
        carrivee_obj = CArrivee(pmap=cmap_obj)
        if re.search("arrivee_color=(.*?)(?:,|])", arrivee_data):
            carrivee_obj.color = re.search("arrivee_color=(.*?)(?:,|])", arrivee_data).group(1)
        if re.search("arrivee_x=(.*?)(?:,|])", arrivee_data):
            carrivee_obj.x = int(re.search("arrivee_x=(.*?)(?:,|])", arrivee_data).group(1))
        if re.search("arrivee_y=(.*?)(?:,|])", arrivee_data):
            carrivee_obj.y = int(re.search("arrivee_y=(.*?)(?:,|])", arrivee_data).group(1))
        if re.search("arrivee_width=(.*?)(?:,|])", arrivee_data):
            carrivee_obj.width = int(re.search("arrivee_width=(.*?)(?:,|])", arrivee_data).group(1))
        if re.search("arrivee_height=(.*?)(?:,|])", arrivee_data):
            carrivee_obj.height = int(re.search("arrivee_height=(.*?)(?:,|])", arrivee_data).group(1))
        
        # get personnage data
        personnage_data = '[' + re.search(r"personnage:\[(.*?)\],", pgame_data).group(1) + ']'
        cpersonnage_obj = CPersonnage(pmap=cmap_obj)
        if re.search("pcolor=(.*?)(?:,|])", personnage_data):
            cpersonnage_obj.color = re.search("pcolor=(.*?)(?:,|])", personnage_data).group(1)
        if re.search("pwidth=(.*?)(?:,|])", personnage_data):
            cpersonnage_obj.width = int(re.search("pwidth=(.*?)(?:,|])", personnage_data).group(1))
        if re.search("pheight=(.*?)(?:,|])", personnage_data):
            cpersonnage_obj.height = int(re.search("pheight=(.*?)(?:,|])", personnage_data).group(1))
        if re.search("px=(.*?)(?:,|])", personnage_data):
            cpersonnage_obj.x = int(re.search("px=(.*?)(?:,|])", personnage_data).group(1))
        if re.search("py=(.*?)(?:,|])", personnage_data):
            cpersonnage_obj.y = int(re.search("py=(.*?)(?:,|])", personnage_data).group(1))
        if re.search("pstarpos_x=(.*?)(?:,|])", personnage_data):
            cpersonnage_obj.startPos[0] = int(re.search("pstarpos_x=(.*?)(?:,|])", personnage_data).group(1))
        if re.search("pstarpos_y=(.*?)(?:,|])", personnage_data):
            cpersonnage_obj.startPos[1] = int(re.search("pstarpos_y=(.*?)(?:,|])", personnage_data).group(1))

        # get obstacle data
        obstacle_data = re.findall("{(.*?)}", re.search(r"obstacle:\[(.*?)\]", pgame_data).group(1))
        cobstacle_objTab = []
        for obstacle in obstacle_data:
            obstacle = '[' + obstacle + ']'
            cobstacle_objTab.append(CObstacle(pmap=cmap_obj))
            if re.search("obstacle_color=(.*?)(?:,|])", obstacle):
                cobstacle_objTab[-1].color = re.search("obstacle_color=(.*?)(?:,|])", obstacle).group(1)
            if re.search("obstacle_x=(.*?)(?:,|])", obstacle):
                cobstacle_objTab[-1].x = int(re.search("obstacle_x=(.*?)(?:,|])", obstacle).group(1))
            if re.search("obstacle_y=(.*?)(?:,|])", obstacle):
                cobstacle_objTab[-1].y = int(re.search("obstacle_y=(.*?)(?:,|])", obstacle).group(1))
            if re.search("obstacle_width=(.*?)(?:,|])", obstacle):
                cobstacle_objTab[-1].width = int(re.search("obstacle_width=(.*?)(?:,|])", obstacle).group(1))
            if re.search("obstacle_height=(.*?)(?:,|])", obstacle):
                cobstacle_objTab[-1].height = int(re.search("obstacle_height=(.*?)(?:,|])", obstacle).group(1))
        
        return [cmap_obj, carrivee_obj, cpersonnage_obj, cobstacle_objTab]
    
    def save_game(self, pdata):
        contenu = 'name=' + pdata[4][1] + ';\n'
        contenu += 'score=' + str(pdata[4][2]) + ';\n'
        contenu += 'game=map:[map_title=' + str(pdata[0].title) + ', map_color=' + str(pdata[0].color) + ', map_height=' + str(pdata[0].height) + ', map_width=' + str(pdata[0].width) + '],'
        contenu += 'arrivee:[arrivee_color=' + str(pdata[1].color) + ', arrivee_x=' + str(pdata[1].x) + ', arrivee_y=' + str(pdata[1].y) + ', arrivee_width=' + str(pdata[1].width) + ', arrivee_height=' + str(pdata[1].height) + '],'
        contenu += 'personnage:[pcolor=' + str(pdata[2].color) + ', pwidth=' + str(pdata[2].width) + ', pheight=' + str(pdata[2].height) + ', px=' + str(pdata[2].x) + ', py=' + str(pdata[2].y) + ', pstarpos_x=' + str(pdata[2].startPos[0]) + ', pstarpos_y=' + str(pdata[2].startPos[1]) + '],'      
        contenu += 'obstacle:['
        for obstacle in pdata[3]:
            contenu += '{obstacle_color=' + str(obstacle.color) + ', obstacle_x=' + str(obstacle.x) + ', obstacle_y=' + str(obstacle.y) + ', obstacle_width=' + str(obstacle.width) + ', obstacle_height=' + str(obstacle.height) + '},'
        contenu += '];\n'
        contenu = contenu.replace(',]', ']')

        contenu += 'level=' + str(pdata[4][4]) + ';\n'
 
        return self.updateFile(ppath=pdata[4][0], pdata=contenu)