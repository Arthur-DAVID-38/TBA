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
            lines = []
            for i in items:
                if i in game.items:
                    lines.append(f"- {game.items[i]}")
                else:
                    lines.append(f"- (inconnu: {i})")
            items_str = "\n".join(lines)

        pnj_str = ""
        if pnj:
            lines = []
            for p in pnj:
                if p in game.pnj:
                    lines.append(f"- {game.pnj[p]}")
                else:
                    lines.append(f"- (inconnu: {p})")
            pnj_str = "\n".join(lines)

        print(room.get_long_description(items_str, pnj_str))

    @staticmethod
    def go(game, cmd, params):
        direction = params[0].lower()
        new_room = game.player.move(direction, game.rooms)

        if not new_room:
            print("Impossible d'aller dans cette direction.")
            return

        game.player.energie -= 1
        game.player.stress += 1

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

        if item_name in ["cafe_douteux", "slide_quantique"]:
            game.player.popularite -= 2

        if item_name in ["gants_antisurvol", "rapport_bugge"]:
            game.player.patch_hardware = min(100, game.player.patch_hardware + 25)
            print("Patch Hardware : progression ++ !")

    @staticmethod
    def drop(game, cmd, params):
        item_name = params[0]
        player = game.player

        if item_name not in player.inventory:
            print("Cet objet n'est pas dans votre inventaire.")
            return

        player.inventory.pop(item_name)
        player.current_room.items.append(item_name)

        print(f"Vous avez déposé {item_name}.")

        if item_name == "rapport_bugge":
            player.popularite -= 5

    @staticmethod
    def talk(game, cmd, params):
        name = params[0]
        room = game.player.current_room

        if name not in room.pnj:
            print("Impossible de lui parler ici.")
            return

        print(game.pnj[name].get_msg())

        if name in ["bde_alpha", "bde_omega"]:
            game.player.patch_social = min(100, game.player.patch_social + 20)
            print("Patch Social : progression ++ !")
            game.player.popularite += 3

        if name in ["agent_multivers", "courivaud_illusoire"]:
            game.player.patch_planning = min(100, game.player.patch_planning + 25)
            print("Patch Planning : progression ++ !")

        if name == "etudiant_panique":
            game.player.popularite += 4

        if name == "prof_glitch":
            game.player.stress += 3

    @staticmethod
    def quit(game, cmd, params):
        print("À bientôt dans l'ESIEE...")
        game.running = False

    @staticmethod
    def stats(game, cmd, params):
        print(f"\n=== STATISTIQUES DE {game.player.name} ===")
        print(f"Énergie :  {game.player.energie}")
        print(f"Stress  :  {game.player.stress}")
        print(f"Charisme : {game.player.charisme}")
        print()
        game.player.show_progress()



