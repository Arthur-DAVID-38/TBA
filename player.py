class Player:
    """Joueur : position, inventaire, stats, historique."""

    def __init__(self, name, starting_room):
        self.name = name
        self.current_room = starting_room
        self.inventory = {}        # {"cafe": Item(...)}
        self.history = []          # pile de salles déjà visitées
        self.max_weight = 8        # capacité totale de poids transportable

        # stats spécifiques à ton univers ESIEE
        self.energie = 50
        self.stress = 10
        self.charisme = 5

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

    def can_carry(self, item):
        current_weight = sum(it.weight for it in self.inventory.values())
        return current_weight + item.weight <= self.max_weight

