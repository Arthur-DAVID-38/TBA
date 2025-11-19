class Player:
    """Joueur : position, inventaire, stats, historique, progression."""

    def __init__(self, name, starting_room):
        self.name = name
        self.current_room = starting_room

        # Inventaire
        self.inventory = {}             # {"cafe": Item(...)}
        self.max_weight = 8             # capacité totale
        self.history = []               # pile des salles visitées

        # Stats ESIEE
        self.energie = 50
        self.stress = 10
        self.charisme = 5

        # Progression des quêtes (barres + pourcentage)
        self.patch_social = 0
        self.patch_hardware = 0
        self.patch_planning = 0

        # Popularité (0–100)
        self.popularite = 50

    # --- Déplacements ---
    def move(self, direction, room_map):
        """Déplacement dans la direction donnée."""
        direction = direction.lower()
        next_room_key = self.current_room.get_exit(direction)

        if not next_room_key:
            return None  # déplacement impossible

        next_room = room_map[next_room_key]
        self.history.append(self.current_room)
        self.current_room = next_room

        self.energie -= 5
        return next_room

    # --- Gestion du poids ---
    def can_carry(self, item):
        current_weight = sum(it.weight for it in self.inventory.values())
        return current_weight + item.weight <= self.max_weight

    # --- Barre de progression ---
    def barre(self, valeur):
        taille = 20
        filled = int((valeur / 100) * taille)
        return "[" + "#" * filled + "-" * (taille - filled) + f"] {valeur}%"

    # --- Affichage global (stats + progression) ---
    def show_progress(self):
        print("\n=== PROGRESSION ===")
        print(f"Patch Social     : {self.barre(self.patch_social)}")
        print(f"Patch Hardware   : {self.barre(self.patch_hardware)}")
        print(f"Patch Planning   : {self.barre(self.patch_planning)}")
        print(f"\nPopularité       : {self.barre(self.popularite)}")
