# Authors: JURDIC Lucas
# Creation date: 2024/12/16
# Description: Interface de jeu pour Motus.

import random
import tkinter as tk

class GamePage(tk.Toplevel):
    """Fenêtre de jeu pour Motus"""
    
    def __init__(self,parent):
        """
        Constructeur de la classe GamePage.
        Args:
            parent (tk.Tk): Fenêtre parent.
        Returns:
            None
        """
        super().__init__(parent)
        self.parent = parent
        self.title("Motus")
        self.geometry("800x800")
        self.resizable(False, False)
        self.focus_force()

        self.score = 0
        self.tentative = 0
        self.mot = ''
        self.motsTeste = []
        self.getMotFromFile()
        self.createWidgets()
        self.AffichageEssaies()

    def createWidgets(self):
        """Crée les widgets de l'interface.
        Args:
            None
        Returns:
            None
        """
        # Scoreboard
        self.scoreboard = tk.Frame(self, bg="black")
        self.scoreboard.pack(side=tk.TOP, fill=tk.BOTH, ipadx=15, ipady=15)

        tk.Button(self.scoreboard, text="Quitter", command=self.onClosing).pack(side=tk.LEFT, padx=20)

        self.labelScore = tk.Label(
            self.scoreboard, text="Score : 0", font=("Helvetica", 18, "bold"), fg="white", bg="black"
        )
        self.labelScore.pack(side=tk.LEFT, padx=20)

        self.tentativeLabel = tk.Label(
            self.scoreboard,text="Tentative : 0", font=("Helvetica", 18, "bold"), fg="white", bg="black"
        )
        self.tentativeLabel.pack(side=tk.LEFT, padx=20)

        # InputBoard
        self.inputBoard = tk.Frame(self, bg="black")
        self.inputBoard.pack(side=tk.TOP, fill=tk.BOTH, ipadx=15, ipady=15)
        self.chaine = tk.StringVar()
        self.entree = tk.Entry(self.inputBoard, textvariable=self.chaine)
        self.entree.pack(pady=10)
        self.sendBtn = tk.Button(self.inputBoard, text='Essayer', command=self.onEssaie)
        self.sendBtn.pack()

        # Gameboard
        gameboard = tk.Frame(self, bg="black")
        gameboard.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, ipadx=15, ipady=15)
        self.canvasBackground = tk.Canvas(gameboard, width=490, height=600)
        self.canvasBackground.pack(expand=True, padx=15)

    def getMotFromFile(self):
        """
        Lit les mots à partir d'un fichier et en choisi un au hasard.
        Args:
            None
        Returns:
            None
        """
        try:
            # Lecture des scores depuis un fichier texte
            with open("data/MotsDeSixLettres.txt", "r") as file:
                mots = file.readlines()
                mots = [str(mot.strip()) for mot in mots if mot.strip()]
                self.mot = random.choice(mots)
                mot_init = self.mot[0]
                for i in range(1,len(self.mot)):
                    if (self.mot[i] == mot_init[0]):
                        mot_init += self.mot[i]
                    else:
                       mot_init += '_'
                self.motsTeste.append(mot_init)
                print(self.mot)
        except FileNotFoundError:
            # Gestion du cas où le fichier n'existe pas
            self.mot = ''
        except Exception as e:
            print(f"Error reading mots: {e}")
            self.mot = ''

    def onEssaie(self):
        """
        Recupere le mot entré et regarde s'il fait 6 lettres. Si oui l'ajoute dans les tentatives et demande l'affichage
        Args:
            None
        Returns:
            None
        """
        essaie = self.chaine.get()
        self.chaine.set("")
        self.tentative += 1 
        if self.tentative >= 6:
            self.entree.config(state="disabled")
            self.sendBtn.config(state="disabled")
            self.AffichageEssaies()
        elif essaie == self.mot:
            self.score += 1
            self.labelScore.config(text="Score : " + str(self.score))
            self.canvasBackground.delete('all')
            self.tentative = 0
            self.mot = ''
            self.motsTeste = []
            self.getMotFromFile()
            self.AffichageEssaies()
        elif len(essaie) == 6:
            self.motsTeste.append(essaie)
            self.AffichageEssaies()
        self.tentativeLabel.config(text="Tentatives : " + str(self.tentative))

    def AffichageEssaies(self):
        """
        Affiche les tentatives. Change la couleur de la case en fonction de la validité de la lettre
        Args:
            None
        Returns:
            None
        """
        largeurCase,hauteurCase = 80,80
        rougeClair='#f39686'
        vertClair='#91f286'
        jauneClair='#fff100'
        x,y=5,5
        for mot in self.motsTeste:
            for i in range(0,len(mot)):
                if mot[i].upper()==self.mot[i].upper():
                    self.canvasBackground.create_rectangle(x,y,x+largeurCase , y+hauteurCase, fill=vertClair)
                    self.canvasBackground.create_text((x+x+largeurCase)/2, y+hauteurCase/2+5, text=mot[i].upper(),fill='white', font="Arial 60")
                else:
                    if mot[i] in self.mot :
                        self.canvasBackground.create_rectangle(x,y,x+largeurCase , y+hauteurCase, fill=jauneClair)
                        self.canvasBackground.create_text((x+x+largeurCase)/2, y+hauteurCase/2+5, text=mot[i].upper(),fill='white', font="Arial 60")
                    else:
                        self.canvasBackground.create_rectangle(x,y,x+largeurCase , y+hauteurCase, fill=rougeClair)
                        if (mot[i] == "_") :
                            self.canvasBackground.create_text((x+x+largeurCase)/2,  y+hauteurCase/2-10, text=mot[i],fill='white', font="Arial 60 ")
                        else:
                            self.canvasBackground.create_text((x+x+largeurCase)/2,  y+hauteurCase/2+5, text=mot[i].upper(),fill='white', font="Arial 60 ")
                x += largeurCase
            x = 5
            y += hauteurCase

    def onClosing(self):
        """Ferme la fenetre de jeu et retourne sur le menu.  
        Args:
            None
        Returns:
            None
        """
        self.parent.deiconify()
        self.destroy()