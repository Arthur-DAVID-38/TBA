# game.py — moteur principal ESIEE Bug dans la Matrice

from room import Room
from player import Player
from command import Command

from config import rooms_config, items_config, pnj_config, DEBUG
from actions import Actions

class Game:

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
        """Instancie chaque salle à partir de config.py."""
        for key, data in rooms_config.items():
            self.rooms[key] = Room(
                data["name"],
                data["description"],
                data["exits"],
                data["items"],
                data["pnj"]
            )

    def setup_player(self):
        name = input("Entrez votre nom : ")
        print(f"Bienvenue {name} dans l'ESIEE… ou une version de l'ESIEE…")
        self.player = Player(name, self.rooms["rue"])

    def setup_commands(self):
        self.commands = {
            "help": Command("help", "afficher l'aide", Actions.help, 0),
            "regarder": Command("regarder", "décrire la salle", Actions.look, 0),
            "go": Command("go", "aller <direction>", Actions.go, 1),
            "take": Command("take", "prendre <objet>", Actions.take, 1),
            "drop": Command("drop", "déposer <objet>", Actions.drop, 1),
            "talk": Command("talk", "parler <pnj>", Actions.talk, 1),
            "quit": Command("quit", "quitter le jeu", Actions.quit, 0),
            "stats": Command("stats", "afficher statistiques du joueur", Actions.stats, 0),

        }

    def parse(self, line):
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

        print("Commande inconnue.")
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


