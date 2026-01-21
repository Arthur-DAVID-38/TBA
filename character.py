"""Définit la classe Character utilisée pour les PNJ du jeu TBA."""


class Character:
    """Représente un personnage non-joueur avec des messages cycliques."""

    def __init__(self, name, description, messages):
        """Initialise un personnage avec son nom, sa description et ses messages."""
        self.name = name
        self.description = description
        self.messages = messages
        self.index = 0

    def get_msg(self):
        """Retourne le message courant du personnage et avance le dialogue."""
        if not self.messages:
            return f"{self.name} ne dit rien."
        msg = self.messages[self.index]
        self.index = (self.index + 1) % len(self.messages)
        return msg

    def __str__(self):
        """Retourne la représentation textuelle du personnage."""
        return f"{self.name} : {self.description}"
