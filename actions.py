"""Définit l’ensemble des actions possibles du joueur 
dans le jeu TBA."""

from item import Item
from config import DEBUG

class Actions:
    """Regroupe les actions exécutables par le joueur."""
    @staticmethod
    def help(game, cmd, params):
        """Affiche la liste des commandes disponibles."""
        if DEBUG:
            print("[DEBUG] Action: help")
        print("Commandes disponibles :")
        for name, command in game.commands.items():
            print(f"  {name} : {command.help_msg}")

    @staticmethod
    def inventory(game, cmd, params):
        """Affiche le contenu de l’inventaire du joueur."""
        if not game.player.inventory:
            print("Votre inventaire est vide.")
            return

        print("Votre inventaire contient :")
        for item_name, item in game.player.inventory.items():
            print(f"- {item}")  

    @staticmethod
    def back(game, cmd, params):
        if not game.player.history:
            print("Aucun déplacement précédent.")
            return

        last_room = game.player.history.pop()
        game.player.current_room = last_room
        print(f"Vous êtes retourné à {last_room.name}.")
        Actions.look(game, None, None)

    @staticmethod
    def look(game, cmd, params):
        """Affiche la description de la salle courante."""
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

        if DEBUG:
            print(f"[DEBUG] Tentative de déplacement vers : {direction}")
       
        new_room = game.player.move(direction, game.rooms)

        if not new_room:
            # Player.move already printed a specific message (ex: porte verrouillée)
            return

        game.player.energie -= 1
        game.player.stress += 1
        game.player.log.append(f"Déplacé vers {new_room.name} via {direction}")
        Actions.look(game, None, None)

    @staticmethod
    def hist(game, cmd, params):
        if not game.player.history:
            print("Aucun déplacement précédent.")
            return

        print("Historique des déplacements :")
        for idx, room in enumerate(game.player.history):
            print(f"{idx + 1}. {room.name}")


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
        """Permet de dialoguer avec un PNJ et de déclencher des événements."""
        name = params[0]
        room = game.player.current_room

        if DEBUG:
            print(f"[DEBUG] Interaction avec PNJ : {name}")

        if name not in room.pnj:
            print("Impossible de lui parler ici.")
            return
        # Afficher le message du PNJ
        print(game.pnj[name].get_msg())

        # Interaction spéciale avec les membres du BDE : choix de dialogue ou mini-jeu selon le contexte
        if name in ["bde_alpha", "bde_omega"]:
            game.player.patch_social = min(100, game.player.patch_social + 20)
            print("Patch Social : progression ++ !")
            game.player.popularite += 3

            # Si le conflit n'est pas encore résolu, proposer les choix conciliateurs
            if not game.player.quests.get('bde_conflict'):
                # Choix de dialogue différents selon le membre
                if name == "bde_alpha":
                    choices = [
                        "1) On se battra pour la cafetière jusqu'au bout !",
                        "2) Et si vous partagiez la cafetière et organisiez une soirée commune ?",
                        "3) C'est juste une cafetière, laissez tomber."
                    ]
                    good_answers = {"2"}
                else:  # bde_omega
                    choices = [
                        "1) On peut proposer un compromis : soirée partagée et alternance d'utilisation.",
                        "2) Nous devons absolument garder la cafetière pour notre camp.",
                        "3) Pourquoi ne pas demander à Courivaud ce qu'il en pense ?"
                    ]
                    good_answers = {"1", "3"}  # plusieurs approches conciliatrices possibles

                print("Choisissez une réponse :")
                for c in choices:
                    print(c)

                reply = input("> ").strip()

                # Marquer qu'on a parlé (indépendamment du contenu)
                game.player.talked_to.add(name)

                # Si la réponse est considérée comme conciliatrice, on marque ce membre comme résolu
                resolved_key = f"resolved_{name}"
                if reply in good_answers:
                    game.player.quests[resolved_key] = 'ok'
                    print("Votre réponse aide à apaiser les tensions.")
                else:
                    print("Votre réponse ne convainc pas ce membre. Il reste méfiant.")

                # Si les deux membres sont résolus, on donne la clé
                resolved_set = {k for k in game.player.quests.keys() if k.startswith('resolved_') and game.player.quests[k] == 'ok'}
                if {"resolved_bde_alpha", "resolved_bde_omega"}.issubset(resolved_set) and not game.player.quests.get('bde_conflict'):
                    game.player.quests['bde_conflict'] = 'completed'
                    key_name = 'cle_bureau_courivaud'
                    key_item = game.items.get(key_name)
                    if key_item and game.player.can_carry(key_item):
                        game.player.inventory[key_name] = key_item
                        print("Les membres du BDE se réconcilient et vous remettent une clé : vous avez obtenu 'cle_bureau_courivaud'.")
                    else:
                        room.items.append(key_name)
                        print("Les membres du BDE se réconcilient et déposent une clé dans la salle : 'cle_bureau_courivaud'.")

            # Si la quête de Courivaud est active, proposer un mini-jeu pour obtenir la pièce du BDE
            elif game.player.quests.get('courivaud_machine') == 'started' and not game.player.quests.get('piece_bde_obtained'):
                print("Les membres du BDE semblent prêts à aider, mais veulent un défi : devinez le nombre mystère de 1 à 3.")
                guess = input("(Entrez 1, 2 ou 3) > ").strip()
                if guess == '2':
                    item_name = 'piece_bde'
                    item = game.items.get(item_name)
                    if item and game.player.can_carry(item):
                        game.player.inventory[item_name] = item
                        print("Vous avez récupéré la pièce du BDE !")
                    else:
                        room.items.append(item_name)
                        print("La pièce du BDE a été déposée dans la salle (inventaire plein).")
                    game.player.quests['piece_bde_obtained'] = True
                else:
                    print("Mauvaise réponse, les membres du BDE gardent la pièce pour l'instant.")

        if name in ["agent_multivers", "courivaud_illusoire"]:
            game.player.patch_planning = min(100, game.player.patch_planning + 25)
            print("Patch Planning : progression ++ !")

        # Mini-jeu à AssistEtud pour obtenir la première pièce
        if name == 'agent_multivers' and game.player.quests.get('courivaud_machine') == 'started' and not game.player.quests.get('piece_assistetud_obtained'):
            print("L'agent vous propose un petit calcul pour obtenir une pièce : combien font 2 + 3 ?")
            ans = input("> ").strip()
            if ans == '5':
                item_name = 'piece_assistetud'
                item = game.items.get(item_name)
                if item and game.player.can_carry(item):
                    game.player.inventory[item_name] = item
                    print("Vous avez obtenu la pièce d'AssistEtud !")
                else:
                    room.items.append(item_name)
                    print("La pièce d'AssistEtud a été déposée dans la salle (inventaire plein).")
                game.player.quests['piece_assistetud_obtained'] = True
            else:
                print("Mauvaise réponse, l'agent ne vous remet pas la pièce.")

        # Mini-jeu à la Salle 3142 pour obtenir la deuxième pièce
        if name == 'ton_double' and game.player.quests.get('courivaud_machine') == 'started' and not game.player.quests.get('piece_salle_3142_obtained'):
            print("Ton Double exige une preuve que vous connaissez sa salle : tapez '3142' pour prouver que vous êtes dans la bonne salle.")
            ans = input("> ").strip()
            if ans == '3142':
                item_name = 'piece_salle_3142'
                item = game.items.get(item_name)
                if item and game.player.can_carry(item):
                    game.player.inventory[item_name] = item
                    print("Vous avez obtenu la pièce de la salle 3142 !")
                else:
                    room.items.append(item_name)
                    print("La pièce de la salle 3142 a été déposée dans la salle (inventaire plein).")
                game.player.quests['piece_salle_3142_obtained'] = True
            else:
                print("Mauvaise réponse, Ton Double vous ignore.")

        if name == "etudiant_panique":
            game.player.popularite += 4

        if name == "prof_glitch":
            game.player.stress += 3
        
        # Conversation finale / instructions de Courivaud : démarrer la quête machine
        if name == 'courivaud_illusoire':
            # On ne démarre la quête que si le BDE a rendu la clé (bureau ouvert/logique déjà) :
            if game.player.quests.get('bde_conflict') == 'completed' and not game.player.quests.get('courivaud_machine'):
                game.player.quests['courivaud_machine'] = 'started'
                game.player.quests['piece_assistetud_obtained'] = False
                game.player.quests['piece_salle_3142_obtained'] = False
                game.player.quests['piece_bde_obtained'] = False
                print("Courivaud : J'ai besoin que tu récupères trois pièces pour assembler une machine qui réparera partiellement nos bugs.")
                print("Va chercher une pièce à AssistEtud, une à la Salle 3142, et une au BDE. Reviens me voir quand tu les as toutes.")
            # Si le joueur a déjà les 3 pièces
            if game.player.quests.get('courivaud_machine') == 'started' and all(game.player.quests.get(k) for k in ['piece_assistetud_obtained','piece_salle_3142_obtained','piece_bde_obtained']):
                print("Courivaud : Parfait, retourne à la Salle Blanche et assemble la machine là-bas avec la commande 'assemble'.")

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

    @staticmethod
    def assemble(game, cmd, params):
        # Assembler la machine dans la salle blanche si toutes les pièces sont présentes
        current = game.player.current_room
        if current is not game.rooms.get('salle_blanche'):
            print("Vous devez être dans la Salle Blanche pour assembler la machine.")
            return

        needed = ['piece_assistetud', 'piece_salle_3142', 'piece_bde']
        missing = [p for p in needed if p not in game.player.inventory]
        if missing:
            print(f"Il vous manque des pièces pour assembler la machine : {', '.join(missing)}")
            return

        # Consommer les pièces
        for p in needed:
            game.player.inventory.pop(p, None)

        # Ajouter la machine et marquer la progression
        machine = game.items.get('machine_quantique')
        if machine:
            game.player.inventory['machine_quantique'] = machine
        game.player.quests['machine_assembled'] = 'completed'
        game.player.patch_hardware = min(100, game.player.patch_hardware + 40)
        print("Vous avez assemblé la machine quantique ! Une partie des bugs de l'ESIEE est désormais réparée.")
