class Command:
    """Structure d'une commande joueur."""

    def __init__(self, name, help_msg, action, param_count):
        self.name = name
        self.help_msg = help_msg
        self.action = action
        self.param_count = param_count


