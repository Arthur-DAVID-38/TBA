"""Définition de la classe Player : position, inventaire, stats et progression."""

class Player:
    """Joueur : position, inventaire, stats, historique, progression."""

    def __init__(self, name, starting_room):
        """Initialise un joueur avec son nom et sa salle de départ."""
        self.name = name
        self.current_room = starting_room

        # Inventaire
        # {"cafe": Item(...)}
        self.inventory = {}
        # Capacité totale
        self.max_weight = 8
        # Pile des salles visitées
        self.history = []

        # Stats ESIEE
        self.energie = 50
        self.stress = 10
        self.charisme = 5

        # Journal d'événements
        self.log = []

        # Progression des quêtes (barres + pourcentage)
        self.patch_social = 0
        self.patch_hardware = 0
        self.patch_planning = 0

        # Quêtes et flags (suivi d'état simple)
        # ex: self.quests['bde_conflict'] = 'completed'
        self.quests = {}
        # Suivi des PNJ auxquels on a parlé (utile pour résoudre des conflits)
        self.talked_to = set()

        # Popularité (0–100)
        self.popularite = 50

    def get_inventory_string(self):
        """Retourne l'inventaire sous forme de texte."""
        if not self.inventory:
            return "Votre inventaire est vide."
        lines = []
        total_weight = 0
        for item in self.inventory.values():
            lines.append(
                f"- {item.name} : {item.description} "
                f"(poids: {item.weight})"
            )
            total_weight += item.weight
        lines.append(f"\nPoids total : {total_weight}/{self.max_weight}")
        return "\n".join(lines)

    # Déplacements
    def move(self, direction, room_map):
        """Déplace le joueur dans la direction donnée si possible."""
        direction = direction.lower()
        next_room_key = self.current_room.get_exit(direction)

        if not next_room_key:
            return None  # déplacement impossible

        next_room = room_map[next_room_key]

        # Vérifier si la salle cible est verrouillée
        if getattr(next_room, "locked", False):
            key_needed = getattr(next_room, "key_name", None)
            if not key_needed or key_needed not in self.inventory:
                print("La porte est verrouillée. Il faut une clé pour y entrer.")
                return None
            # On a la clé : on l'utilise pour ouvrir la porte (consommée)
            print(
                "Vous utilisez la clé pour ouvrir la porte. "
                "Elle s'enfonce dans la serrure et tourne."
            )
            # Consommer la clé
            self.inventory.pop(key_needed, None)
            # Déverrouiller la salle pour la suite
            next_room.locked = False

        self.history.append(self.current_room)
        self.current_room = next_room
        self.energie -= 5
        return next_room

    # Gestion du poids
    def can_carry(self, item):
        """Indique si le joueur peut porter un objet supplémentaire."""
        current_weight = sum(
            it.weight for it in self.inventory.values()
        )
        return current_weight + item.weight <= self.max_weight

    # Barre de progression
    def barre(self, valeur):
        """Retourne une barre de progression textuelle pour une valeur donnée."""
        taille = 20
        filled = int((valeur / 100) * taille)
        return "[" + "#" * filled + "-" * (taille - filled) + f"] {valeur}%"

    # Affichage global (stats + progression)
    def show_progress(self):
        """Affiche les barres de progression des patchs et de la popularité."""
        print("\n=== PROGRESSION ===")
        print(f"Patch Social     : {self.barre(self.patch_social)}")
        print(f"Patch Hardware   : {self.barre(self.patch_hardware)}")
        print(f"Patch Planning   : {self.barre(self.patch_planning)}")
        print(f"\nPopularité       : {self.barre(self.popularite)}")
