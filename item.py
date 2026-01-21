"""Définition de la classe Item pour les objets du jeu."""


class Item:
    """Objet manipulable dans le jeu.

    Attributes:
        name (str): Nom affiché de l'objet.
        description (str): Description textuelle de l'objet.
        weight (int | float): Poids de l'objet, utilisé pour la capacité de port.
    """

    def __init__(self, name, description, weight):
        """Initialise un nouvel objet de jeu."""
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        """Retourne une représentation textuelle lisible de l'objet."""
        return f"{self.name} : {self.description} ({self.weight} kg)"

    def to_dict(self):
        """Retourne une représentation simple de l'objet sous forme de dictionnaire."""
        return {
            "name": self.name,
            "description": self.description,
            "weight": self.weight,
        }
