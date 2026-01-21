"""Définit l’ensemble des actions possibles du joueur
dans le jeu TBA."""

from config import DEBUG

class Actions:
    """Regroupe les actions exécutables par le joueur."""
    @staticmethod
    def help(game, _cmd, _params):
        """Affiche la liste des commandes disponibles."""
        if DEBUG:
            print("[DEBUG] Action: help")
        print("Commandes disponibles :")
        for name, command in game.commands.items():
            print(f"  {name} : {command.help_msg}")

    @staticmethod
    def inventory(game, _cmd, _params):
        """Affiche le contenu de l’inventaire du joueur."""
        if not game.player.inventory:
            print("Votre inventaire est vide.")
            return

        print("Votre inventaire contient :")
        for _item_name, item in game.player.inventory.items():
            print(f"- {item}")

    @staticmethod
    def back(game, _cmd, _params):
        """Retourne le joueur dans la salle précédente."""
        if not game.player.history:
            print("Aucun déplacement précédent.")
            return

        last_room = game.player.history.pop()
        game.player.current_room = last_room
        print(f"Vous êtes retourné à {last_room.name}.")
        Actions.look(game, None, None)

    @staticmethod
    def look(game, _cmd, _params):
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
    def go(game, _cmd, _params):
        """Déplace le joueur vers une salle adjacente."""
        direction = _params[0].lower()

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
    def hist(game, _cmd, _params):
        """Affiche l’historique des déplacements du joueur."""
        if not game.player.history:
            print("Aucun déplacement précédent.")
            return

        print("Historique des déplacements :")
        for idx, room in enumerate(game.player.history):
            print(f"{idx + 1}. {room.name}")


    @staticmethod
    def take(game, _cmd, _params):
        """Permet au joueur de ramasser un objet."""
        item_name = _params[0]
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
    def drop(game, _cmd, _params):
        """Permet au joueur de déposer un objet."""
        item_name = _params[0]
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
    def talk(game, _cmd, _params):
        """Dialogue avec un PNJ et déclenche les événements associés."""
        name = _params[0]
        room = game.player.current_room

        if DEBUG:
            print(f"[DEBUG] Interaction avec PNJ : {name}")

        if name not in room.pnj:
            print("Impossible de lui parler ici.")
            return

        # Afficher le message du PNJ
        print(game.pnj[name].get_msg())

        # BDE
        if name in {"bde_alpha", "bde_omega"}:
            Actions._talk_bde(game, name)

        # Agent multivers
        elif name == "agent_multivers":
            Actions._talk_agent_multivers(game)

        # Ton double
        elif name == "ton_double":
            Actions._talk_ton_double(game)

        # Courivaud illusoire
        elif name == "courivaud_illusoire":
            Actions._talk_courivaud(game)

        # Étudiant paniqué
        elif name == "etudiant_panique":
            game.player.popularite += 4

        # Prof glitch
        elif name == "prof_glitch":
            game.player.stress += 3

    # ======================
    # BDE
    # ======================

    @staticmethod
    def _talk_bde(game, name):
        """Gère les interactions avec les membres du BDE (conflit + mini-jeu)."""

        # Patch social et popularité comme avant
        game.player.patch_social = min(100, game.player.patch_social + 20)
        print("Patch Social : progression ++ !")
        game.player.popularite += 3

        # Si le conflit n'est pas encore résolu, proposer les choix conciliateurs
        if not game.player.quests.get("bde_conflict"):
            choices, good_answers = Actions._bde_choices(name)

            print("Choisissez une réponse :")
            for c in choices:
                print(c)

            reply = input("> ").strip()

            # Marquer qu'on a parlé (indépendamment du contenu)
            game.player.talked_to.add(name)

            # Si la réponse est conciliatrice, marquer ce membre comme résolu
            resolved_key = f"resolved_{name}"
            if reply in good_answers:
                game.player.quests[resolved_key] = "ok"
                print("Votre réponse aide à apaiser les tensions.")
            else:
                print("Votre réponse ne convainc pas ce membre. Il reste méfiant.")

            # Vérifier si les deux membres sont résolus
            Actions._check_bde_resolution(game)

        # Si la quête de Courivaud est active, proposer le mini-jeu pour la pièce
        elif (
            game.player.quests.get("courivaud_machine") == "started"
            and not game.player.quests.get("piece_bde_obtained")
        ):
            Actions._bde_piece_minigame(game)

    @staticmethod
    def _bde_choices(name):
        """Retourne les choix et bonnes réponses du BDE (texte identique à l'ancien code)."""
        if name == "bde_alpha":
            choices = [
                "1) On se battra pour la cafetière jusqu'au bout !",
                "2) Et si vous partagiez la cafetière et organisiez une soirée commune ?",
                "3) C'est juste une cafetière, laissez tomber.",
            ]
            good_answers = {"2"}
        else:  # bde_omega
            choices = [
                "1) On peut proposer un compromis :"
                "soirée partagée et alternance d'utilisation.",
                "2) Nous devons absolument garder la cafetière pour notre camp.",
                "3) Pourquoi ne pas demander à Courivaud ce qu'il en pense ?",
            ]
            good_answers = {"1", "3"}

        return choices, good_answers

    @staticmethod
    def _check_bde_resolution(game):
        """Vérifie si les deux membres du BDE sont réconciliés et donne la clé."""
        room = game.player.current_room

        resolved_set = {
            k
            for k, v in game.player.quests.items()
            if k.startswith("resolved_") and v == "ok"
        }

        if (
            {"resolved_bde_alpha", "resolved_bde_omega"}.issubset(resolved_set)
            and not game.player.quests.get("bde_conflict")
        ):
            game.player.quests["bde_conflict"] = "completed"

            key_name = "cle_bureau_courivaud"
            item = game.items.get(key_name)

            if item and game.player.can_carry(item):
                game.player.inventory[key_name] = item
                print(
                    "Les membres du BDE se réconcilient et vous remettent une clé : "
                    "vous avez obtenu 'cle_bureau_courivaud'."
                )
            else:
                room.items.append(key_name)
                print(
                    "Les membres du BDE se réconcilient "
                    "et déposent une clé dans la salle : "
                    "'cle_bureau_courivaud'."
                )

    @staticmethod
    def _bde_piece_minigame(game):
        """Mini-jeu du BDE pour obtenir la pièce, texte identique à l'ancien code."""
        room = game.player.current_room

        print(
            "Les membres du BDE semblent prêts à aider, "
            "mais veulent un défi : devinez le nombre mystère de 1 à 3."
        )
        guess = input("(Entrez 1, 2 ou 3) > ").strip()
        if guess == "2":
            item_name = "piece_bde"
            item = game.items.get(item_name)
            if item and game.player.can_carry(item):
                game.player.inventory[item_name] = item
                print("Vous avez récupéré la pièce du BDE !")
            else:
                room.items.append(item_name)
                print(
                    "La pièce du BDE a été déposée dans la salle (inventaire plein)."
                )
            game.player.quests["piece_bde_obtained"] = True
        else:
            print(
                "Mauvaise réponse, les membres du BDE gardent la pièce pour l'instant."
            )

    # ======================
    # AGENT MULTIVERS
    # ======================

    @staticmethod
    def _talk_agent_multivers(game):
        """Mini-jeu AssistEtud + Patch Planning (comme ancien code)."""
        room = game.player.current_room

        # Bonus Patch Planning comme dans l'ancien code
        game.player.patch_planning = min(100, game.player.patch_planning + 25)
        print("Patch Planning : progression ++ !")

        # Mini-jeu pour la pièce AssistEtud
        if (
            game.player.quests.get("courivaud_machine") == "started"
            and not game.player.quests.get("piece_assistetud_obtained")
        ):
            print(
                "L'agent vous propose un petit calcul "
                "pour obtenir une pièce : combien font 2 + 3 ?"
            )
            ans = input("> ").strip()
            if ans == "5":
                item_name = "piece_assistetud"
                item = game.items.get(item_name)
                if item and game.player.can_carry(item):
                    game.player.inventory[item_name] = item
                    print("Vous avez obtenu la pièce d'AssistEtud !")
                else:
                    room.items.append(item_name)
                    print(
                        "La pièce d'AssistEtud a été déposée "
                        "dans la salle (inventaire plein)."
                    )
                game.player.quests["piece_assistetud_obtained"] = True
            else:
                print("Mauvaise réponse, l'agent ne vous remet pas la pièce.")

    # ======================
    # TON DOUBLE
    # ======================

    @staticmethod
    def _talk_ton_double(game):
        """Mini-jeu Salle 3142 pour obtenir la pièce."""
        room = game.player.current_room

        if (
            game.player.quests.get("courivaud_machine") == "started"
            and not game.player.quests.get("piece_salle_3142_obtained")
        ):
            print(
                "Ton Double exige une preuve que vous connaissez sa salle : "
                "tapez '3142' pour prouver que vous êtes dans la bonne salle."
            )
            ans = input("> ").strip()
            if ans == "3142":
                item_name = "piece_salle_3142"
                item = game.items.get(item_name)
                if item and game.player.can_carry(item):
                    game.player.inventory[item_name] = item
                    print("Vous avez obtenu la pièce de la salle 3142 !")
                else:
                    room.items.append(item_name)
                    print(
                        "La pièce de la salle 3142 a été déposée dans la salle "
                        "(inventaire plein)."
                    )
                game.player.quests["piece_salle_3142_obtained"] = True
            else:
                print("Mauvaise réponse, Ton Double vous ignore.")

    # ======================
    # COURIVAUD
    # ======================

    @staticmethod
    def _talk_courivaud(game):
        """Déclenche et conclut la quête de la machine, avec le texte de l'ancien code."""
        # Bonus Patch Planning comme dans l'ancien code
        game.player.patch_planning = min(100, game.player.patch_planning + 25)
        print("Patch Planning : progression ++ !")

        # Démarrer la quête de la machine si le BDE a rendu la clé
        if (
            game.player.quests.get("bde_conflict") == "completed"
            and not game.player.quests.get("courivaud_machine")
        ):
            game.player.quests["courivaud_machine"] = "started"
            game.player.quests["piece_assistetud_obtained"] = False
            game.player.quests["piece_salle_3142_obtained"] = False
            game.player.quests["piece_bde_obtained"] = False

            print(
                "Courivaud : J'ai besoin que tu récupères "
                "trois pièces pour assembler une machine qui réparera partiellement nos bugs."
            )
            print(
                "Va chercher une pièce à AssistEtud, une à la Salle 3142, "
                "et une au BDE. Reviens me voir quand tu les as toutes."
            )
            return

        # Si le joueur a déjà les 3 pièces
        if (
            game.player.quests.get("courivaud_machine") == "started"
            and all(
                game.player.quests.get(k)
                for k in [
                    "piece_assistetud_obtained",
                    "piece_salle_3142_obtained",
                    "piece_bde_obtained",
                ]
            )
        ):
            print(
                "Courivaud : Parfait, retourne à la Salle Blanche "
                "et assemble la machine là-bas avec la commande 'assemble'."
            )

    # ======================
    # (Optionnel) UTILITAIRE COMMUN
    # ======================

    @staticmethod
    def _give_item(game, item_name):
        """
        Version utilitaire générique si tu veux l'utiliser ailleurs.
        (Ici, pour mimer exactement l'ancien code, tout est déjà inline,
        donc cette fonction est surtout là pour d'autres parties du jeu.)
        """
        item = game.items.get(item_name)
        room = game.player.current_room

        if item and game.player.can_carry(item):
            game.player.inventory[item_name] = item
        else:
            room.items.append(item_name)

    @staticmethod
    def quit(game, _cmd, _params):
        """Quitte le jeu."""
        print("À bientôt dans l'ESIEE...")
        game.running = False

    @staticmethod
    def stats(game, _cmd, _params):
        """Affiche les statistiques du joueur."""
        print(f"\n=== STATISTIQUES DE {game.player.name} ===")
        print(f"Énergie :  {game.player.energie}")
        print(f"Stress  :  {game.player.stress}")
        print(f"Charisme : {game.player.charisme}")
        print()
        game.player.show_progress()

    @staticmethod
    def assemble(game, _cmd, _params):
        """Assemble la machine finale si toutes les pièces sont réunies."""
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
        print("Vous avez assemblé la machine quantique !"
        "Une partie des bugs de l'ESIEE est désormais réparée.")
