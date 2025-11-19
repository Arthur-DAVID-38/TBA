from item import Item
from config import DEBUG

class Actions:

    @staticmethod
    def help(game, cmd, params):
        print("Commandes disponibles :")
        for name, command in game.commands.items():
            print(f"  {name} : {command.help_msg}")

    @staticmethod
    def look(game, cmd, params):
        room = game.player.current_room
        items = room.items
        pnj = room.pnj

        items_str = ""
        if items:
            items_str = "\n".join(f"- {game.items[i]}" for i in items)

        pnj_str = ""
        if pnj:
            pnj_str = "\n".join(f"- {game.pnj[p]}" for p in pnj)

        print(room.get_long_description(items_str, pnj_str))

    @staticmethod
    def go(game, cmd, params):
        direction = params[0].lower()
        new_room = game.player.move(direction, game.rooms)

        if not new_room:
            print("Impossible d'aller dans cette direction.")
            return

        Actions.look(game, None, None)

    @staticmethod
    def take(game, cmd, params):
        item_name = params[0]
        room = game.player.current_room

        if item_name not in room.items:
            print("Cet objet n'est pas ici.")
            return

        item = game.items[item_name]

        if not game.player.can_carry(item):
            print("Vous ne pouvez pas porter cet objet, trop lourd.")
            return

        room.items.remove(item_name)
        game.player.inventory[item_name] = item

        print(f"Vous avez pris {item_name}.")

    @staticmethod
    def drop(game, cmd, params):
        item_name = params[0]
        player = game.player

        if item_name not in player.inventory:
            print("Cet objet n'est pas dans votre inventaire.")
            return

        item = player.inventory.pop(item_name)
        player.current_room.items.append(item_name)

        print(f"Vous avez déposé {item_name}.")

    @staticmethod
    def talk(game, cmd, params):
        name = params[0]
        room = game.player.current_room

        if name not in room.pnj:
            print("Impossible de lui parler ici.")
            return

        print(game.pnj[name].get_msg())

    @staticmethod
    def quit(game, cmd, params):
        print("À bientôt dans l'ESIEE...")
        game.running = False


