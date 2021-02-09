import time
import tkinter
import os.path
import os
from threading import Thread
from tkinter import messagebox
from CSetting import CSetting
from os import listdir
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from CMap import CMap
from PIL import ImageTk, Image
from os import path


class CGame(object):
	"""
	<=== CGame ===>
	Classe correspondant à l'interface graphique du jeu, elle utilise tous les elements 
	(zone de jeu, personnage, arrivée, obstacles, etc...). C'est le cœur du jeu : avec 
	utilisation de Thread pour la gestion des parties et la gestion des sauvegardes.
	"""
	def __init__(self):
		# ===== fenetre principale =====
		self.fenetre = tkinter.Tk() # fenetre principale
		self.fenetre.title(string='-') # titre de la fenetre
		self.fenetre.geometry(str(self.fenetre.winfo_screenwidth()) + 'x' + str(self.fenetre.winfo_screenheight())) # taille de la fenetre (dimenssion de l'ecran)
		#self.fenetre.iconbitmap(bitmap="ressource//image//icon.ico") # icone de la fenetre
		#self.fenetre.attributes("-topmost", True) # fenetre en avant
		#self.fenetre.overrideredirect(1) # fenetre sans bordure (pour plus d'imerssion dans le jeu)
		self.fenetre.protocol("WM_DELETE_WINDOW", self.__exit_game)
		self.fenetre.update()
		# ==============================

		# ===== obj map + obj constituant la map
		self.__map = CMap() # obj map
		self.__personnage = None # obj personnage
		self.__arrivee = None # obj arrivee
		self.__obstacles = None # obj obstacle[]
		# =======================================

		# ===== menu jeu =====
		self.__game_status_canvas = tkinter.Canvas(master=self.fenetre, width=200, height=200, bg='grey')
		self.__game_status_canvas.place(x=10, y=10)
		self.__game_status_canvas.update()

		self.__startBTN = tkinter.Button(master=self.__game_status_canvas, text="Lancer le jeu", state='disabled', command=self.__lancer_jeu)
		self.__startBTN.place(x=10, y=10)
		self.__startBTN.update()

		self.__restartBTN = tkinter.Button(master=self.__game_status_canvas, text="Recommencer", state='disabled', command=self.__restart_game)
		self.__restartBTN.place(x=self.__startBTN.winfo_x()+self.__startBTN.winfo_width()+10, y=10)
		self.__restartBTN.update()

		self.__nextBTN = tkinter.Button(master=self.__game_status_canvas, text="Niveau suivant", state='disabled', command=self.__niveau_suivant)
		self.__nextBTN.place(x=10, y=self.__startBTN.winfo_y()+self.__startBTN.winfo_height() + 10)
		self.__nextBTN.update()
        
		self.__pauseBTN = tkinter.Button(master=self.__game_status_canvas, text="pause", state='disabled', command=self.__pause_game)
		self.__pauseBTN.place(x=10, y=self.__nextBTN.winfo_y()+self.__nextBTN.winfo_height() + 10)
		self.__pauseBTN.update()

		self.__saveBTN = tkinter.Button(master=self.__game_status_canvas, text="Enregistrer", state='disabled', command=self.__save_game)
		self.__saveBTN.place(x=10, y=self.__pauseBTN.winfo_y()+self.__pauseBTN.winfo_height() + 10)
		self.__saveBTN.update()

		self.__show_menuBTN = tkinter.Button(master=self.__game_status_canvas, text="Settings", state='disabled', command=self.__show_setting)
		self.__show_menuBTN.place(x=10, y=self.__saveBTN.winfo_y()+self.__saveBTN.winfo_height()+10)
		self.__show_menuBTN.update()

		# map editor
		"""self.show_map_editorBTN = tkinter.Button(master=self.__game_status_canvas, text='Map editor')
		self.show_map_editorBTN.place(x=self.__show_menuBTN.winfo_x()+self.__show_menuBTN.winfo_width()+10, y=self.__show_menuBTN.winfo_y())
		self.show_map_editorBTN.update()"""

		self.__game_status_canvas['width'] = self.__startBTN.winfo_x() + self.__startBTN.winfo_width() + self.__nextBTN.winfo_x() + self.__nextBTN.winfo_width() + 5
		self.__game_status_canvas['height'] = self.__show_menuBTN.winfo_y()+self.__show_menuBTN.winfo_height() + 5
		# ====================
		
		# ===== menu popup =====
		self.__menu_popup_canvas = tkinter.Canvas(master=self.fenetre, width=250, height=250, bg='grey')
		self.__menu_popup_canvas.place(x=(self.fenetre.winfo_screenwidth()/2)-250, y=10)
		self.__menu_popup_canvas.update()
        
		self.__player_lbFM = tkinter.Frame(master=self.__menu_popup_canvas, width=500, height=500, bg='red')
		self.__player_lbSB = tkinter.Scrollbar(self.__player_lbFM)
		self.__playerLB = tkinter.Listbox(self.__player_lbFM, width=20, height=10)
		self.__playerLB.bind('<<ListboxSelect>>', self.__selectLB)
		self.__player_lbSB.config(command = self.__playerLB.yview)
		self.__playerLB.config(yscrollcommand = self.__player_lbSB.set)
		self.__playerLB.pack(side = tkinter.LEFT, fill = tkinter.Y)
		self.__player_lbSB.pack(side = tkinter.RIGHT, fill = tkinter.Y)
		self.__player_lbFM.place(x=10, y=10)
		self.__menu_popup_canvas.update() # pour avoir les nouvelles pos

		self.__select_player_okBTN = tkinter.Button(master=self.__menu_popup_canvas, text='OK', state='disabled', command=self.__set_player)
		self.__select_player_okBTN.place(x=10, y=self.__player_lbFM.winfo_y()+self.__playerLB.winfo_height() +10)
		self.__menu_popup_canvas.update()

		self.____add_playerBTN = tkinter.Button(master=self.__menu_popup_canvas, text='+', command=self.__add_player)
		self.____add_playerBTN.place(x=self.__select_player_okBTN.winfo_x()+self.__select_player_okBTN.winfo_width()+5, y=self.__player_lbFM.winfo_y()+self.__playerLB.winfo_height() +10)
		self.__menu_popup_canvas.update()

		self.____remove_playerBTN = tkinter.Button(master=self.__menu_popup_canvas, text='x', state='disabled', command=self.__remove_player)
		self.____remove_playerBTN.place(x=self.____add_playerBTN.winfo_x()+self.____add_playerBTN.winfo_width()+5, y=self.__player_lbFM.winfo_y()+self.__playerLB.winfo_height() +10)

		self.__scoreLBL = tkinter.Label(master=self.__menu_popup_canvas, text='score = 0', bg=self.__menu_popup_canvas['bg'])
		self.__scoreLBL.place(x=self.__player_lbFM.winfo_x()+self.__playerLB.winfo_width() + self.__player_lbSB.winfo_width() + 10, y=10)
		self.__scoreLBL.update()

		self.__player_niveauLBL = tkinter.Label(master=self.__menu_popup_canvas, text='niveau = 0', bg=self.__menu_popup_canvas['bg'])
		self.__player_niveauLBL.place(x=self.__player_lbFM.winfo_x()+self.__playerLB.winfo_width() + self.__player_lbSB.winfo_width() + 10, y=30)
		self.__player_niveauLBL.update()
        
		self.__menu_popup_canvas['width'] = self.__player_niveauLBL.winfo_x() + self.__player_niveauLBL.winfo_width() + 30
		self.__menu_popup_canvas['height'] = self.__select_player_okBTN.winfo_y() + self.__select_player_okBTN.winfo_height() + 10
		self.__menu_popup_canvas.update()

		self.__menu_popup_canvas.place(x=int((self.fenetre.winfo_screenwidth()/2)-(self.__menu_popup_canvas.winfo_width()/2)), y=10)
        # ====================

		# ===== menu setting =====
		# difficultee
		# son
		# enregistrement auto; toutes les, manuel
		self.__menu_setting_canvas = tkinter.Canvas(master=self.fenetre, bg='grey')
		self.__menu_setting_canvas.place(x=(self.fenetre.winfo_screenwidth()/2)-250, y=10) 
		self.__menu_setting_canvas.place_forget()
		
		self.__menu_setting_difficulteeLBL = tkinter.Label(master=self.__menu_setting_canvas, text='Difficultée = ', bg=self.__menu_setting_canvas['bg'])
		self.__menu_setting_difficulteeLBL.place(x=10, y=15)
		self.__menu_setting_difficulteeLBL.update()

		self.__img = [ImageTk.PhotoImage(Image.open('ressource//image//easy.png').resize((30,30))),
					ImageTk.PhotoImage(Image.open('ressource//image//medium.png').resize((30,30))),
					ImageTk.PhotoImage(Image.open('ressource//image//hard.png').resize((30,30)))]
        
		self.__menu_setting_difficulteeIMG = [tkinter.Label(master=self.__menu_setting_canvas, bg='green', image=self.__img[0], cursor="hand2", text='10'),
											tkinter.Label(master=self.__menu_setting_canvas, bg=self.__menu_setting_canvas['bg'], image=self.__img[1], cursor="hand2", text='7'),
											tkinter.Label(master=self.__menu_setting_canvas, bg=self.__menu_setting_canvas['bg'], image=self.__img[2], cursor="hand2", text='2')]
	
		for index in range(0, len(self.__menu_setting_difficulteeIMG)):
			if index == 0:
				self.__menu_setting_difficulteeIMG[index].place(x=self.__menu_setting_difficulteeLBL.winfo_width() + 10, y=10)
				self.__menu_setting_difficulteeIMG[index].bind('<Button-1>', self.__set_difficultee)
				self.__menu_setting_difficulteeIMG[index].update()
			else:
				self.__menu_setting_difficulteeIMG[index].place(x=self.__menu_setting_difficulteeIMG[index-1].winfo_x()+self.__menu_setting_difficulteeIMG[index-1].winfo_width() + 10, y=10)
				self.__menu_setting_difficulteeIMG[index].bind('<Button-1>', self.__set_difficultee)
				self.__menu_setting_difficulteeIMG[index].update()
	
		self.__menu_setting_son_cb_var = tkinter.IntVar(value=1)
		self.__menu_setting_sonCB = tkinter.Checkbutton(master=self.__menu_setting_canvas, text='Son', bg=self.__menu_setting_canvas['bg'], variable=self.__menu_setting_son_cb_var)
		self.__menu_setting_sonCB.place(x=10, y=self.__menu_setting_difficulteeLBL.winfo_y()+self.__menu_setting_difficulteeLBL.winfo_height()+10)
		self.__menu_setting_sonCB.update()

		self.__menu_setting_enregistrementLBL = tkinter.Label(master=self.__menu_setting_canvas, text='Enregistrement = ', bg=self.__menu_setting_canvas['bg'])
		self.__menu_setting_enregistrementLBL.place(x=10, y=self.__menu_setting_sonCB.winfo_y()+self.__menu_setting_sonCB.winfo_height()+10)
		self.__menu_setting_enregistrementLBL.update()

		self.__menu_setting_enregistrement_value_RB = tkinter.StringVar(self.__menu_setting_canvas, 'auto') # var qui contient radio la val du button auto ou manuel
		self.__menu_setting_enregistrement_manuelRB = tkinter.Radiobutton(master=self.__menu_setting_canvas, text='manuel', bg=self.__menu_setting_canvas['bg'], variable=self.__menu_setting_enregistrement_value_RB, value='manuel')
		self.__menu_setting_enregistrement_manuelRB.place(x=self.__menu_setting_enregistrementLBL.winfo_x()+self.__menu_setting_enregistrementLBL.winfo_width()+10, y=self.__menu_setting_enregistrementLBL.winfo_y())
		self.__menu_setting_enregistrement_manuelRB.update()

		self.__menu_setting_enregistrement_autoRB = tkinter.Radiobutton(master=self.__menu_setting_canvas, text='auto', bg=self.__menu_setting_canvas['bg'], variable=self.__menu_setting_enregistrement_value_RB, value='auto')
		self.__menu_setting_enregistrement_autoRB.place(x=self.__menu_setting_enregistrement_manuelRB.winfo_x()+self.__menu_setting_enregistrement_manuelRB.winfo_width()+10, y=self.__menu_setting_enregistrement_manuelRB.winfo_y())
		self.__menu_setting_enregistrement_autoRB.update()

		self.__menu_setting_okBTN = tkinter.Button(master=self.__menu_setting_canvas, text='OK', command=self.__hide_setting)
		self.__menu_setting_okBTN.place(x=10, y=self.__menu_setting_enregistrementLBL.winfo_y()+self.__menu_setting_enregistrementLBL.winfo_height()+10)
		self.__menu_setting_okBTN.update()

		self.__menu_setting_canvas['height'] = self.__menu_setting_okBTN.winfo_height() + self.__menu_setting_okBTN.winfo_y() + 10
		self.__menu_setting_canvas['width'] = self.__menu_setting_enregistrement_autoRB.winfo_x()+self.__menu_setting_enregistrement_autoRB.winfo_width() + 10
		# ====================

		# ===== menu jeu info ======
		self.__menu_jeu_info_canvas = tkinter.Canvas(master=self.fenetre, width=170, height=70, bg='grey')
		self.__menu_jeu_info_canvas.place(x=self.fenetre.winfo_width()-int(self.__menu_jeu_info_canvas['width'])-10, y=10)

		self.__player_nameLBL = tkinter.Label(master=self.__menu_jeu_info_canvas, text='joueur = -', bg=self.__menu_jeu_info_canvas['bg'])
		self.__player_nameLBL.place(x=10, y=10)
		self.__player_nameLBL.update()

		self.__player_scoreLBL = tkinter.Label(master=self.__menu_jeu_info_canvas, text='score = -', bg=self.__menu_jeu_info_canvas['bg'])
		self.__player_scoreLBL.place(x=10, y=self.__player_nameLBL.winfo_y()+self.__player_nameLBL.winfo_height()+10)
		self.__player_scoreLBL.update()

		self.__niveau_nameLBL = tkinter.Label(master=self.__menu_jeu_info_canvas, text='niveau = -', bg=self.__menu_jeu_info_canvas['bg'])
		self.__niveau_nameLBL.place(x=10, y=self.__player_scoreLBL.winfo_y()+self.__player_scoreLBL.winfo_height()+10)
		self.__niveau_nameLBL.update()
		
		self.__menu_jeu_info_canvas['height'] = self.__niveau_nameLBL.winfo_y()+self.__niveau_nameLBL.winfo_height()+10				
		# ====================

		# ===== variables propres au jeu ======
		self.__setting = CSetting() # obj CSetting pour lire les parametres dans les fichiers
		self.__playerIndex = -1 # index du joueur selectionne
		self.__joueurTab = [] # tableau information des joueurs
		self.__fichier_joueurTab = [] # tableau fichier des joueurs
		self.__game_running = False # status du jeu
		self.__objTab = [None, None, None, None, []] # map, arrivee, obstacle, [name,score,game,level]
		# --- thread ---
		self.____engineTH = None # thread du jeu
		self.__sauvegarde_autoTH = Thread(target=self.__sauvegarde_auto) # thread qui gere la sauvegarde auto
		self.__sauvegarde_autoTH.start()
		self.__difficultee = 10 # diffucltee par defaut (modifiable via le menu setting)
		# ====================
		
		self.__menu_demarrage() # affiche le menu de demarrage

		self.fenetre.mainloop() # boucle d'affichage de la fenetre (propre a tkinter)

	# ==== fonction gestion du jeu ====	
	# fct pour demarrer le jeu (mouvements, etc...)
	def __lancer_jeu(self):
		# activation/desactivation des differents boutons
		self.__startBTN['state'] = 'disabled'
		self.__saveBTN['state'] = 'normal'
		self.__pauseBTN['state'] = 'normal'

		self.__game_running = True # etat du jeu running
		self.__personnage.game_running = True # etat du jeu running (cote personnage pour les mouvements)

		self.startPos = self.__personnage.startPos # enregistre la position de depart
		
		self.____engineTH = Thread(target=self.__engine) # initialise le thread
		self.____engineTH.start() # démarre le thread du jeu
	# fct pour recommancer
	def __restart_game(self):
		# activation/desactivation des differents boutons
		self.__startBTN['state'] = 'normal'

		# reset personnage pos & var
		self.__personnage.x = self.__personnage.startPos[0]
		self.__personnage.y = self.__personnage.startPos[1]
		self.__personnage.movementTab = []
		
		# reset game running
		self.__game_running = False
		self.__personnage.game_running = False
	# fct qui enregistre la partie
	def __save_game(self):
		if self.__setting.save_game(pdata=self.__objTab): # on reseigne les objs + info joueur
			self.__personnage.game_running = False
			self.__personnage.movementTab = []
			messagebox.showinfo("OK", "Partie enregistrée avec succès")
			self.__personnage.game_running = True
		else:
			self.__personnage.game_running = False
			self.__personnage.movementTab = []
			messagebox.showerror("Erreur !", "Une erreur est survenue dans l'enregistrement")
			self.__personnage.game_running = True
	# fct pour mettre en pause le jeu
	def __pause_game(self):
		# activation/desactivation des differents boutons et variables
		if self.__game_running:
			if self.__pauseBTN['text'] == 'pause':
				self.fenetre.title('- : [PAUSED]')
				self.__pauseBTN['text'] = 'resume'
				self.__personnage.game_running = False # pause game
				self.__personnage.movementTab = []
			elif self.__pauseBTN['text'] == 'resume':
				self.fenetre.title('- : [RUNNING]')
				self.__pauseBTN['text'] = 'pause'
				self.__personnage.game_running = True # resume game
				self.__personnage.movementTab = []
	# fct appellee quand le joueur a perdu
	def __joueur_perdu(self):
		# RAZ des differentes variables
		self.__game_running = False
		self.__personnage.game_running = False
		self.__personnage.x = self.startPos[0]
		self.__personnage.y = self.startPos[1]
		self.__personnage.movementTab = []
		self.__game_running = True
		self.__personnage.game_running = True
		#vie = 100
	# fct appellee quand le joueur a gagnie
	def __joueur_gagnie(self):
		self.__nextBTN['state'] = 'normal'
		self.__saveBTN['state'] = 'disabled'
		self.__joueurTab[self.__playerIndex][2] += 10 + int(100/self.__personnage.speed) # difficultee
		self.__player_scoreLBL['text'] = 'score = ' + str(self.__joueurTab[self.__playerIndex][2])
		self.__game_running = False
		self.__personnage.game_running = False
	# fct pour afficher le niveau suivant
	def __niveau_suivant(self):
		if path.exists("ressource//level//niveau_" + str(self.__joueurTab[self.__playerIndex][4]+1)): # si niveau suivant existe
			self.__nextBTN['state'] = 'disabled'
			self.__startBTN['state'] = 'normal'
			self.__joueurTab[self.__playerIndex][4] += 1
			self.__objTab = self.__setting.lire_niveau(pfichier_niveau_path="ressource//level//niveau_" + str(self.__joueurTab[self.__playerIndex][4]))
			self.__map.canvas.destroy()
			self.__map = self.__objTab[0]
			self.__arrivee = self.__objTab[1]
			self.__personnage = self.__objTab[2]
			self.__personnage.speed = self.__difficultee
			self.__obstacles= self.__objTab[3]
			self.__objTab.append(self.__joueurTab[self.__playerIndex]) # get player info	
			self.__afficher_map() # affichage de la map
			self.__niveau_nameLBL['text'] = 'niveau = ' + str(self.__joueurTab[self.__playerIndex][4])
			
			# enregistrement de la partie
			if self.__setting.save_game(pdata=self.__objTab): # on reseigne les objs + info joueur
				print("Partie enregistrée avec succès")
			else:
				print("Une erreur est survenue dans l'enregistrement")

			print('Niveau suivant')
		else:
			messagebox.showinfo("Félicitation !", "Vous avez terminé le jeu")

	# thread gestion du jeu
	def __engine(self):
		fin = False
		while fin == False:
            # check si le personne est/touche la ligne d'arrivee
		    if self.__map.elements_intersect(pelement1=self.__personnage, pelement2=self.__arrivee):
		        print("Vous avez gagnie !")
		        self.__joueur_gagnie()
		        messagebox.showinfo("Félicitation !", "Vous avez gagnie !")
		        fin = True # fin car le joueur a gagne
            # check si le personne est/touche un des obstacles
		    for obstacle in self.__obstacles:
		        if self.__map.elements_intersect(pelement1=self.__personnage, pelement2=obstacle):
		            print("Vous avez perdu !")
		            self.__personnage.game_running = False
		            messagebox.showwarning("Perdu !", "Vous avez perdu !")
		            self.__joueur_perdu()
			# check si game is running
		    if self.__game_running == False:
		        fin = True

		    time.sleep(0.01)
	# thread sauvegarde du jeu
	def __sauvegarde_auto(self):
		while True:
			if self.__game_running: # si le jeu tourne
				if self.__menu_setting_enregistrement_value_RB.get() == 'auto': # si option auto
					if self.__setting.save_game(pdata=self.__objTab): # on reseigne les objs + info joueur
						print("Partie enregistrée avec succès")
					else:
						print("Une erreur est survenue dans l'enregistrement")
			time.sleep(10) # sauvegarde auto toutes les minutes

	# ==== fonction gestion des menus ====	
	# fct qui gere le menu de demarrage
	def __menu_demarrage(self):
		"""
		si il existe des joueurs 
		alors : -> charger tous les joueurs
				-> proposer d'en creer un nouveau
		sinon : -> proposer d'en creer un
		"""
		self.__get_all_player_info() # lecture de tous les joueurs

		if len(self.__joueurTab) == 0: # si aucun joueur trouve : on demande d'en creer un
			new_player_name = None
			while new_player_name == None or new_player_name == '':
				new_player_name = askstring('Veuillez entrer un nom de joueur', 'Nom joueur : ')

			new_player_created = False
			while new_player_created == False:
				if self.__create_new_player(pplayer_name=new_player_name):
					messagebox.showinfo("OK", 'Le joueur a été crée avec succès !')
					new_player_created = True
				else:
					messagebox.showerror("FAIL", 'Le joueur n\'a pas été crée')
	# fct qui permet de lire tous les fichiers joueurs
	def __get_all_player_info(self):
		dossier_fichier_joueur_path = 'ressource//player//'
		for fichier in listdir(dossier_fichier_joueur_path):
			if (fichier in self.__fichier_joueurTab) == False:
				self.__joueurTab += self.__setting.lire_joueur(pfichier_joueur_path=dossier_fichier_joueur_path+fichier)
				self.__fichier_joueurTab += [fichier]
		
		if self.__playerLB.size() == 0 and len(self.__joueurTab) > 0:
			for player in self.__joueurTab:
				self.__playerLB.insert('end', player[1])
		elif self.__playerLB.size() < len(self.__joueurTab):
			for index in range(self.__playerLB.size(), len(self.__joueurTab)):
				self.__playerLB.insert('end', self.__joueurTab[index][1])
	# fct qui permet la creation d'un nouveau joueur
	def __create_new_player(self, pplayer_name):
		donnee_nouveau_joueur = 'name=' + pplayer_name + ';\n'
		donnee_nouveau_joueur += 'score=0;\n'
		donnee_nouveau_joueur += 'game=;\n'
		donnee_nouveau_joueur += 'level=1;\n'

		if self.__setting.createFile(ppath='ressource//player//joueur_' + str(len(self.__joueurTab) + 1)) and self.__setting.updateFile(ppath='ressource//player//joueur_' + str(len(self.__joueurTab) + 1), pdata=donnee_nouveau_joueur):
			self.__get_all_player_info()
			return True
		else:
			return False
	# fct qui initalise le jeu avec les information du joueur choisi
	def __set_player(self):
		self.__playerIndex = self.__playerLB.curselection()[0] # enregistrement de l'index du joueur
		
		# activation/desactivation des differents boutons
		self.__nextBTN['state'] = 'disabled'
		self.__startBTN['state'] = 'normal'
		self.__restartBTN['state'] = 'normal'
		self.__show_menuBTN['state'] = 'normal'
		# affichage des informations
		self.__player_nameLBL['text'] = 'joueur = ' + self.__joueurTab[self.__playerIndex][1]
		self.__player_scoreLBL['text'] = 'score = ' + str(self.__joueurTab[self.__playerIndex][2])
		self.__niveau_nameLBL['text'] = 'niveau = ' + str(self.__joueurTab[self.__playerIndex][4])
		
		if self.__joueurTab[self.__playerIndex][3] != '': # si le joueur a une sauvegarde
			self.__objTab = self.__setting.load_game(pgame_data=self.__joueurTab[self.__playerIndex][3]) 
		else: # si le joueur n'a pas de sauvegarde
			self.__objTab = self.__setting.lire_niveau(pfichier_niveau_path="ressource//level//niveau_" + str(self.__joueurTab[self.__playerIndex][4]))

		# destruction de l'obj map pour pouvoir le remplacer
		if self.__map.canvas != None:
			self.__map.canvas.destroy()

		# initialisation des differents obj (map, personnage, obstacles, etc...)
		self.__map = self.__objTab[0] 
		self.__arrivee = self.__objTab[1]
		self.__personnage = self.__objTab[2]
		self.__obstacles= self.__objTab[3]
		self.__objTab.append(self.__joueurTab[self.__playerIndex]) # get player info
		
		self.__menu_popup_canvas.place_forget() # cache le menu popup

		self.__afficher_map() # affiche la map
	# fct qui affiche la map
	def __afficher_map(self):
		 
		self.__map.fenetre = self.fenetre # lien entre la fenetre principale et la map

		# ajout des obj dans la map
		self.__map.add(self.__arrivee)
		self.__map.add(self.__personnage)
		self.__map.add(self.__obstacles)

		# initialisation de la map & obj
		self.__map.obj_init()	# initialisation map	
		for obj in self.__map.element: # initialisation objs
			obj.obj_init()

		self.__map.canvas.place(x=int((self.fenetre.winfo_screenwidth()-int(self.__map.canvas['width']))/2), y=10) # affichage de la map
	# fct qui cache le menu setting
	def __hide_setting(self):
		# enregistrement auto, ect
		if self.__startBTN['state'] == 'disabled' and self.__pauseBTN['text'] == 'pause':		
			self.__personnage.game_running = True # resume game

		self.__map.canvas.place(x=self.__map.canvas.winfo_x(), y=self.__map.canvas.winfo_y()) # affiche la map
		self.__menu_setting_canvas.place_forget() # cache le menu
	# fct qui affiche le menu setting
	def __show_setting(self):
		if self.__startBTN['state'] == 'disabled':	
			self.__personnage.game_running = False # pause game

		self.__map.canvas.place_forget() # cache la map car elle est devant le menu
		self.__menu_setting_canvas.place(x=(self.fenetre.winfo_screenwidth()/2)-250, y=10)  # affiche le menu setting
	# fct qui permet l'ajout d'un nouveau joueur
	def __add_player(self):	
		new_player_name = None
		while new_player_name == None or new_player_name == '':
			new_player_name = askstring('Veuillez entrer un nom de joueur', 'Nom joueur : ')

		new_player_created = False
		while new_player_created == False:
			if self.__create_new_player(pplayer_name=new_player_name):
				messagebox.showinfo("OK", 'Le joueur a été crée avec succès !')
				new_player_created = True
			else:
				messagebox.showerror("FAIL", 'Le joueur n\'a pas été crée')
	# fct qui permet de supprimer un joueur
	def __remove_player(self):
		return False

	# ==== gestion des evenements ====
	# evenement qui gere le clique sur les images de difficultee
	def __set_difficultee(self, event):
		self.__difficultee = int(event.widget['text']) # get difficultee
		self.__personnage.speed = self.__difficultee # set speed/difficultee
		if event.widget['bg'] != 'green': # gestion couleur image
			for image in self.__menu_setting_difficulteeIMG:
				image['bg'] = self.__menu_setting_canvas['bg']
			event.widget['bg'] = 'green'
	# evenement qui permet l'affichage des informations des joueurs
	def __selectLB(self, event):
		# activation/desactivation des differents boutons
		self.__select_player_okBTN['state'] = 'normal'
		self.____remove_playerBTN['state'] = 'normal'
		# affichage des informations
		self.__scoreLBL['text'] = 'score = ' + str(self.__joueurTab[self.__playerLB.curselection()[0]][2])
		self.__player_niveauLBL['text'] = 'niveau = ' + str(self.__joueurTab[self.__playerLB.curselection()[0]][4])	
	
	def __exit_game(self):
		if messagebox.askokcancel("Exit", "Voulez vous vraiment quitter ?"):
			self.fenetre.destroy()
			os._exit(0)
