"""Moteur principal du jeu textuel TBA « Bug dans la Matrice ».

Ce module initialise le jeu, charge les salles, le joueur et les commandes,
puis gère la boucle principale d’exécution et l’interprétation des commandes
saisies par l’utilisateur.
"""
# game.py — moteur principal ESIEE Bug dans la Matrice

from room import Room
from player import Player
from command import Command

from config import rooms_config, items_config, pnj_config, DEBUG
from actions import Actions

class Game:
    """Classe principale du jeu.

    Elle centralise l’état du jeu, le joueur, les salles,
    les commandes et la boucle principale d’exécution.
    """

    def __init__(self):
        self.running = True
        self.rooms = {}
        self.items = items_config
        self.pnj = pnj_config
        self.commands = {}

        self.setup_rooms()
        self.setup_player()
        self.setup_commands()

    def setup_rooms(self):
        """Instancie chaque salle à partir de config.py"""
        for key, data in rooms_config.items():
            self.rooms[key] = Room(
                data["name"],
                data["description"],
                data.get("exits", {}),
                data.get("items", []),
                data.get("pnj", []),
                locked=data.get("locked", False),
                key_name=data.get("key_name")
            )

    def setup_player(self):
        """Crée le joueur et l’associe à la salle de départ."""
        name = input("Entrez votre nom : ")
        print(f"Bienvenue {name} dans l'ESIEE… ou une version de l'ESIEE…")
        self.player = Player(name, self.rooms["rue"])

    def setup_commands(self):
        """Initialise l’ensemble des commandes disponibles dans le jeu."""
        self.commands = {
            "help": Command("help", "afficher l'aide", Actions.help, 0),
            "look": Command("look", "décrire la salle", Actions.look, 0),
            "go": Command("go", "aller <direction>", Actions.go, 1),
            "take": Command("take", "prendre <objet>", Actions.take, 1),
            "drop": Command("drop", "déposer <objet>", Actions.drop, 1),
            "talk": Command("talk", "parler <pnj>", Actions.talk, 1),
            "quit": Command("quit", "quitter le jeu", Actions.quit, 0),
            "stats": Command("stats", "afficher statistiques du joueur", Actions.stats, 0),
            "hist": Command("hist", "afficher historique des déplacements", Actions.hist, 0),
            "back": Command("back", "Retourner en arrière", Actions.back, 0),
            "assemble": Command(
                "assemble",
                "assembler la machine (dans la salle blanche)",
                Actions.assemble, 0),
            "inv": Command("inventory", "afficher l'inventaire", Actions.inventory, 0),

        }

    def parse(self, line):
        """Analyse la commande saisie par l’utilisateur.
        Vérifie la validité de la commande et retourne son nom,
        ainsi que la liste des paramètres associés.
    """
        if not line:
            return None, []

        parts = line.split()
        cmd = parts[0]
        params = parts[1:]

        if cmd in self.commands:
            expected = self.commands[cmd].param_count
            if len(params) != expected:
                print("Paramètres incorrects.")
                return None, []
            return cmd, params

        print("Commande inconnue. Faites 'help' pour la liste des commandes.")
        return None, []

    def main_loop(self):
        Actions.look(self, None, None)

        while self.running:
            cmd_raw = input("\n> ").strip().lower()
            cmd_name, params = self.parse(cmd_raw)

            if cmd_name:
                action = self.commands[cmd_name].action
                action(self, cmd_name, params)


if __name__ == "__main__":
    game = Game()
    game.main_loop()
