
# Authors: JURDIC Lucas
# Creation date: 2024/12/16
# Description: Interface principale pour le jeu Motus.


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from src.Ui.GamePage import GamePage

class MainPage(tk.Tk):
    """Fenêtre principale du jeu Motus"""
    def __init__(self):
        """
        Constructeur de la classe MainPage.
        Args:
            None
        Returns:
            None
        """
        super().__init__()
        self.title("Motus")
        self.geometry("800x600")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        """
        Crée et configure les widgets de la fenêtre principale.
        Args:
            None
        Returns:
            None
        """
        # Charger et redimensionner l'image de fond
        self.bg_image = Image.open("assets/motus-bg.jpg")
        self.bg_image = self.bg_image.resize((800, 600))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Création d'un canvas pour afficher l'image de fond
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Titre du jeu affiché sur le canvas
        self.titleText = self.canvas.create_text(
            400, 125, text="Motus", font=("Helvetica", 50, "bold"), fill="white"
        )

        # Bouton pour démarrer une nouvelle partie
        self.gameBtn = ttk.Button(self, text="Jouer", command=self.open_game)
        self.canvas.create_window(400, 240, window=self.gameBtn)

        # Bouton pour afficher les scores
        # self.scoreBtn = ttk.Button(self, text="Scores", command=self.open_scores)
        # self.canvas.create_window(400, 300, window=self.scoreBtn)

        # Bouton pour quitter l'application
        self.exitBtn = ttk.Button(self, text="Quitter", command=self.destroy)
        self.canvas.create_window(400, 360, window=self.exitBtn)

    def open_game(self):
        """
        Ouvre la fenêtre de jeu et masque la fenêtre principale.
        Args:
            None
        Returns:
            None
        """
        self.withdraw()
        GamePage(self)