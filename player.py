"""Définition de la classe Player : position, inventaire, stats et progression."""


class Stats:
    """Gère les statistiques du joueur (énergie, stress, charisme, popularité)."""

    def __init__(self):
        self.energie = 50
        self.stress = 10
        self.charisme = 5
        self.popularite = 50

    def get_status(self):
        """Retourne un résumé textuel des statistiques principales."""
        return f"Énergie: {self.energie}, Stress: {self.stress}, Popularité: {self.popularite}"

    def update_popularite(self, delta):
        """Met à jour la popularité (utilisé par les interactions PNJ)."""
        self.popularite = max(0, min(100, self.popularite + delta))


class InventoryManager:
    """Gère l'inventaire et la capacité de portage du joueur."""

    def __init__(self):
        self.items = {}  # {"cafe": Item(...)}
        self.max_weight = 8

    def get_inventory_string(self):
        """Retourne l'inventaire sous forme de texte."""
        if not self.items:
            return "Votre inventaire est vide."
        lines = []
        total_weight = 0
        for item in self.items.values():
            lines.append(
                f"- {item.name} : {item.description} "
                f"(poids: {item.weight})"
            )
            total_weight += item.weight
        lines.append(f"\nPoids total : {total_weight}/{self.max_weight}")
        return "\n".join(lines)

    def can_carry(self, item):
        """Indique si le joueur peut porter un objet supplémentaire."""
        current_weight = sum(
            it.weight for it in self.items.values()
        )
        return current_weight + item.weight <= self.max_weight


class QuestsTracker:
    """Gère les quêtes, flags et progression des patchs."""

    def __init__(self):
        self.quests = {}  # ex: {'bde_conflict': 'completed'}
        self.talked_to = set()
        self.patch_social = 0
        self.patch_hardware = 0
        self.patch_planning = 0
        self.log = []

    def barre(self, valeur):
        """Retourne une barre de progression textuelle."""
        taille = 20
        filled = int((valeur / 100) * taille)
        return "[" + "#" * filled + "-" * (taille - filled) + f"] {valeur}%"

    def show_progress(self):
        """Affiche les barres de progression des patchs et popularité."""
        print("\n=== PROGRESSION ===")
        print(f"Patch Social     : {self.barre(self.patch_social)}")
        print(f"Patch Hardware   : {self.barre(self.patch_hardware)}")
        print(f"Patch Planning   : {self.barre(self.patch_planning)}")


class Player:
    """Joueur principal avec position et gestionnaires spécialisés."""

    def __init__(self, name, starting_room):
        """Initialise un joueur avec son nom et sa salle de départ."""
        self.name = name
        self.current_room = starting_room
        self.stats = Stats()
        self.inventory = InventoryManager()
        self.quests = QuestsTracker()
        self.history = []  # pile des salles visitées

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
            if not key_needed or key_needed not in self.inventory.items:
                print("La porte est verrouillée. Il faut une clé pour y entrer.")
                return None
            # On a la clé : on l'utilise pour ouvrir la porte (consommée)
            print(
                "Vous utilisez la clé pour ouvrir la porte. "
                "Elle s'enfonce dans la serrure et tourne."
            )
            # Consommer la clé
            self.inventory.items.pop(key_needed, None)
            # Déverrouiller la salle pour la suite
            next_room.locked = False

        self.history.append(self.current_room)
        self.current_room = next_room
        self.stats.energie -= 5
        return next_room

    def show_inventory(self):
        """Affiche l'inventaire du joueur."""
        print(self.inventory.get_inventory_string())
        print(self.stats.popularite)

    def show_progress(self):
        """Affiche la progression globale."""
        self.quests.show_progress()
