from item import Item
from config import DEBUG

class Actions:

    # ======================
    #        HELP
    # ======================
    @staticmethod
    def help(game, cmd, params):
        print("Commandes disponibles :")
        for name, command in game.commands.items():
            print(f"  {name} : {command.help_msg}")

    # ======================
    #        LOOK
    # ======================
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

    # ======================
    #         GO
    # ======================
    @staticmethod
    def go(game, cmd, params):
        direction = params[0].lower()
        new_room = game.player.move(direction, game.rooms)

        if not new_room:
            print("Impossible d'aller dans cette direction.")
            return

        # Fatigue en marchant :
        game.player.energie -= 1

        # Petit stress en se déplaçant trop souvent :
        game.player.stress += 1

        Actions.look(game, None, None)

    # ======================
    #        TAKE
    # ======================
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

        # === POPULARITÉ : voler des petits objets = -2 ===
        if item_name in ["cafe_douteux", "slide_quantique"]:
            game.player.popularite -= 2

        # === PATCH HARDWARE (Salle Blanche / 3142) ===
        if item_name in ["gants_antisurvol", "rapport_bugge"]:
            game.player.patch_hardware = min(100, game.player.patch_hardware + 25)
            print("⚙ Patch Hardware : progression ++ !")

    # ======================
    #        DROP
    # ======================
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

        # Déposer un objet important = baisse de popularité
        if item_name == "rapport_bugge":
            player.popularite -= 5

    # ======================
    #        TALK
    # ======================
    @staticmethod
    def talk(game, cmd, params):
        name = params[0]
        room = game.player.current_room

        if name not in room.pnj:
            print("Impossible de lui parler ici.")
            return

        print(game.pnj[name].get_msg())

        # === PATCH SOCIAL ===
        if name in ["bde_alpha", "bde_omega"]:
            game.player.patch_social = min(100, game.player.patch_social + 20)
            print("🤝 Patch Social : progression ++ !")
            game.player.popularite += 3

        # === PATCH PLANNING ===
        if name in ["agent_multivers", "courivaud_illusoire"]:
            game.player.patch_planning = min(100, game.player.patch_planning + 25)
            print("📅 Patch Planning : progression ++ !")

        # Étudiant paniqué = popularité ++
        if name == "etudiant_panique":
            game.player.popularite += 4

        # Prof glitch = stress ++
        if name == "prof_glitch":
            game.player.stress += 3

    # ======================
    #        QUIT
    # ======================
    @staticmethod
    def quit(game, cmd, params):
        print("À bientôt dans l'ESIEE...")
        game.running = False

    # ======================
    #        STATS
    # ======================
    @staticmethod
    def stats(game, cmd, params):
        print(f"\n=== STATISTIQUES DE {game.player.name} ===")
        print(f"Énergie :  {game.player.energie}")
        print(f"Stress  :  {game.player.stress}")
        print(f"Charisme : {game.player.charisme}")
        game.player.show_progress()
