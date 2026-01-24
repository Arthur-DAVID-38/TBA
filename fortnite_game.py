"""Mini-jeu Fortnite simplifié en mode texte."""

import random


class FortniteGame:
    """Simulateur simplifié de Fortnite basé sur les choix et les combats."""

    def __init__(self):
        """Initialise une partie de Fortnite."""
        self.player_health = 100
        self.player_shields = 50
        self.player_ammo = 30
        self.player_materials = 0
        self.enemy_health = 100
        self.enemy_shields = 30
        self.turn = 1
        self.won = False
        self.turns_played = 0
        self.wall_active = False

    def play(self):
        """Lance une partie complète de Fortnite."""
        print("\n" + "=" * 60)
        print("🎮 FORTNITE - MINI MATCH")
        print("=" * 60)
        print("\nVous êtes en train de parachuter dans l'île de Fortnite...")
        print("Soudain, vous repérez un ennemi!")
        print("\n" + "-" * 60)

        while self.player_health > 0 and self.enemy_health > 0:
            self._display_status()
            print(f"\n--- Tour {self.turn} ---")
            print("Que faites-vous?")
            print("1. 🔫 Tirer (60% de chance de toucher)")
            print("2. 📦 Chercher des munitions (+20 munitions)")
            print("3. 🏗️  Construire un mur (bloque l'attaque ennemie)")
            print("4. 🪨 Collecter des matériaux (+30 matériaux)")
            print("5. 🎯 Tir de précision (90% chance, 30 ammo, plus de dégâts)")
            print("6. 🏃 Fuir et se soigner (+20 PV, ennemi gagne un tour)")

            choice = input("\nVotre choix (1-6): ").strip()

            if choice in ["1", "2", "3", "4", "5", "6"]:
                self._player_action(int(choice))
            else:
                print("❌ Choix invalide, vous perdez un tour!")
                self.turns_played += 1
                self._enemy_action()
                continue

            if self.enemy_health <= 0:
                self.won = True
                break

            self.turns_played += 1
            self._enemy_action()
            self.turn += 1

        print("\n" + "=" * 60)
        if self.won:
            self._victory()
        else:
            self._defeat()
        print("=" * 60)

        return self.won

    def _display_status(self):
        """Affiche l'état actuel de la partie."""
        print(
            f"\n📊 VOTRE ÉTAT: ❤️  {self.player_health}/100 | "
            f"🛡️  {self.player_shields}/50 | 🔫 {self.player_ammo} | "
            f"🪨 {self.player_materials}"
        )
        print(
            f"👾 ENNEMI: ❤️  {self.enemy_health}/100 | "
            f"🛡️  {self.enemy_shields}/30\n"
        )

    def _player_action(self, choice):
        """Exécute l'action du joueur."""
        self.wall_active = False
        
        if choice == 1:
            # Tirer
            if self.player_ammo <= 0:
                print("❌ Pas assez de munitions!")
                return
            
            hit_chance = random.random()
            if hit_chance < 0.6:
                damage = random.randint(15, 35)
                self._deal_damage(damage, "tir")
                self.player_ammo -= 1
            else:
                print("❌ Coup manqué!")
                self.player_ammo -= 1

        elif choice == 2:
            # Chercher des munitions
            found = random.randint(15, 30)
            self.player_ammo += found
            print(f"📦 Vous avez trouvé {found} munitions! Total: {self.player_ammo}")

        elif choice == 3:
            # Construire un mur
            if self.player_materials < 20:
                print("❌ Pas assez de matériaux pour construire! (besoin: 20)")
                return
            print("🏗️  Vous construisez un mur de protection...")
            print("   L'attaque ennemie sera bloquée ce tour!")
            self.player_materials -= 20
            self.wall_active = True
            self.turns_played += 1
            self.turn += 1
            return  # Skip enemy action

        elif choice == 4:
            # Collecter des matériaux
            found = random.randint(25, 50)
            self.player_materials += found
            print(f"🪨 Vous avez collecté {found} matériaux! Total: {self.player_materials}")

        elif choice == 5:
            # Tir de précision
            if self.player_ammo < 30:
                print(f"❌ Pas assez de munitions! (vous en avez {self.player_ammo}, besoin: 30)")
                return
            
            hit_chance = random.random()
            if hit_chance < 0.9:
                damage = random.randint(40, 60)
                self._deal_damage(damage, "tir de précision")
                self.player_ammo -= 30
            else:
                print("❌ Tir de précision manqué!")
                self.player_ammo -= 30

        elif choice == 6:
            # Fuir et se soigner
            healing = random.randint(15, 25)
            old_health = self.player_health
            self.player_health = min(100, self.player_health + healing)
            actual_healing = self.player_health - old_health
            print(f"🏃 Vous prenez la fuite et vous soignez! +{actual_healing} PV")
            self.turns_played += 1
            self._enemy_action()
            self.turn += 1
            return  # On saute le deuxième enemy_action

    def _deal_damage(self, damage, action_name):
        """Applique les dégâts à l'ennemi."""
        if self.enemy_shields > 0:
            shield_damage = min(damage, self.enemy_shields)
            self.enemy_shields -= shield_damage
            health_damage = damage - shield_damage
            print(
                f"✅ {action_name} réussi! "
                f"Bouclier: -{shield_damage}, Santé: -{health_damage}"
            )
            self.enemy_health -= health_damage
        else:
            self.enemy_health -= damage
            print(f"✅ {action_name} réussi! Dégâts: {damage}")

    def _enemy_action(self):
        """Exécute une action ennemie."""
        actions = ["shoot", "heal", "ammo", "build"]
        action = random.choice(actions)

        if action == "shoot":
            hit_chance = random.random()
            if hit_chance < 0.5:
                if self.wall_active:
                    print("🤖 L'ennemi tire mais le mur bloque l'attaque!")
                    self.wall_active = False
                    return
                
                damage = random.randint(10, 25)
                # D'abord les shields
                if self.player_shields > 0:
                    shield_damage = min(damage, self.player_shields)
                    self.player_shields -= shield_damage
                    health_damage = damage - shield_damage
                    print(
                        f"🎯 L'ennemi tire! "
                        f"Bouclier: -{shield_damage}, Santé: -{health_damage}"
                    )
                    self.player_health -= health_damage
                else:
                    self.player_health -= damage
                    print(f"🎯 L'ennemi tire! Dégâts: {damage}")
            else:
                print("🤖 L'ennemi rate son coup!")

        elif action == "heal":
            healing = random.randint(15, 30)
            self.enemy_health = min(100, self.enemy_health + healing)
            print(f"🤖 L'ennemi se soigne! +{healing} PV")

        elif action == "ammo":
            found = random.randint(10, 20)
            print("🤖 L'ennemi cherche des munitions...")

        elif action == "build":
            print("🤖 L'ennemi construit un mur de protection...")

    def _victory(self):
        """Gère la victoire."""
        print("\n🏆 VICTOIRE! 🏆")
        print(f"Vous avez remporté la partie en {self.turns_played} tours!")
        print(f"Santé restante: {self.player_health} PV")
        print(f"Bouclier restant: {self.player_shields}")
        players_remaining = random.randint(1, 5)
        print(f"\n📊 Vous êtes classé 1er! Joueurs restants: {players_remaining}/100")

    def _defeat(self):
        """Gère la défaite."""
        print("\n💀 DÉFAITE! 💀")
        print(f"Vous avez été éliminé après {self.turns_played} tours...")
        print(f"L'ennemi avait encore {self.enemy_health} PV")


def play_fortnite_minigame():
    """Lance une partie de Fortnite et retourne si le joueur a gagné."""
    game = FortniteGame()
    return game.play()

