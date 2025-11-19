class Character:
    """Personnage non joueur (PNJ)"""

    def __init__(self, name, description, messages):
        self.name = name
        self.description = description
        self.messages = messages
        self.index = 0

    def get_msg(self):
        if not self.messages:
            return f"{self.name} ne dit rien."
        msg = self.messages[self.index]
        self.index = (self.index + 1) % len(self.messages)
        return msg

    def __str__(self):
        return f"{self.name} : {self.description}"


