"""Définit la classe Room pour les salles du jeu TBA."""


class Room:
    """Lieu de la map, avec descriptions, sorties, objets, et PNJ."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, name, description, exits=None, items=None, pnj=None,
                 locked=False, key_name=None):
        self.name = name
        self.description = description
        self.exits = exits or {}
        self.items = items or []
        self.pnj = pnj or []

        self.locked = locked
        self.key_name = key_name

    def get_exit(self, direction):
        """Retourne la salle accessible via direction, sinon None."""
        return self.exits.get(direction)

    def get_exit_string(self):
        """Retourne la liste des sorties sous forme de texte."""
        if not self.exits:
            return "Aucune sortie."
        return "Sorties : " + ", ".join(self.exits.keys())

    def get_long_description(self, items_str="", pnj_str=""):
        """Retourne la description complète de la pièce."""
        base = f"Vous êtes {self.description}\n\n"
        base += self.get_exit_string()
        if items_str:
            base += f"\n\nObjets visibles :\n{items_str}"
        if pnj_str:
            base += f"\n\nPersonnes présentes :\n{pnj_str}"
        return base
