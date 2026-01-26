"""Mini-jeu Fortnite simplifié en mode texte."""

import random


class PlayerState:
    """État du joueur dans la partie de Fortnite."""

    def __init__(self):
        """Initialise l'état du joueur."""
        self.health = 100
        self.shields = 50
        self.ammo = 30
        self.materials = 0

    def reset(self):
        """Réinitialise l'état du joueur."""
        self.health = 100
        self.shields = 50
        self.ammo = 30
        self.materials = 0

    def take_damage(self, damage):
        """Applique des dégâts au joueur via les boucliers et la santé."""
        if self.shields > 0:
            shield_damage = min(damage, self.shields)
            self.shields -= shield_damage
            health_damage = damage - shield_damage
        else:
            health_damage = damage
        self.health -= health_damage
        return health_damage

    def heal(self, amount):
        """Soigne le joueur jusqu'à 100 PV."""
        old_health = self.health
        self.health = min(100, self.health + amount)
        return self.health - old_health



class EnemyState:
    """État de l'ennemi dans la partie de Fortnite."""

    def __init__(self):
        """Initialise l'état de l'ennemi."""
        self.health = 100
        self.shields = 30

    def reset(self):
        """Réinitialise l'état de l'ennemi."""
        self.health = 100
        self.shields = 30

    def take_damage(self, damage):
        """Applique des dégâts à l'ennemi via les boucliers et la santé."""
        if self.shields > 0:
            shield_damage = min(damage, self.shields)
            self.shields -= shield_damage
            health_damage = damage - shield_damage
        else:
            health_damage = damage
        self.health -= health_damage
        return health_damage

    def heal(self, amount):
        """Soigne l'ennemi jusqu'à 100 PV."""
        old_health = self.health
        self.health = min(100, self.health + amount)
        return self.health - old_health



class FortniteGame:
    """Simulateur simplifié de Fortnite basé sur les choix et les combats."""

    def __init__(self):
        """Initialise une partie de Fortnite."""
        self.player = PlayerState()
        self.enemy = EnemyState()
        self.turn = 1
        self.won = False
        self.turns_played = 0
        self.wall_active = False

    def reset(self):
        """Réinitialise l'état du jeu."""
        self.player.reset()
        self.enemy.reset()
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

        while self.player.health > 0 and self.enemy.health > 0:
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

            if self.enemy.health <= 0:
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
            f"\n📊 VOTRE ÉTAT: ❤️  {self.player.health}/100 | "
            f"🛡️  {self.player.shields}/50 | 🔫 {self.player.ammo} | "
            f"🪨 {self.player.materials}"
        )
        print(
            f"👾 ENNEMI: ❤️  {self.enemy.health}/100 | "
            f"🛡️  {self.enemy.shields}/30"
        )

    def _player_action(self, choice):
        """Exécute l'action du joueur."""
        self.wall_active = False

        action_map = {
            1: self._action_shoot,
            2: self._action_ammo,
            3: self._action_build,
            4: self._action_collect,
            5: self._action_precision_shot,
            6: self._action_flee
        }

        action_method = action_map.get(choice)
        if action_method:
            action_method()

    def _action_shoot(self):
        """Tirer sur l'ennemi."""
        if self.player.ammo <= 0:
            print("❌ Pas assez de munitions!")
            return

        hit_chance = random.random()
        if hit_chance < 0.6:
            damage = random.randint(15, 35)
            self._deal_damage(damage, "tir")
        else:
            print("❌ Coup manqué!")
        self.player.ammo -= 1

    def _action_ammo(self):
        """Chercher des munitions."""
        found = random.randint(15, 30)
        self.player.ammo += found
        print(f"📦 Vous avez trouvé {found} munitions! Total: {self.player.ammo}")

    def _action_build(self):
        """Construire un mur de protection."""
        if self.player.materials < 20:
            print("❌ Pas assez de matériaux pour construire! (besoin: 20)")
            return
        print("🏗️  Vous construisez un mur de protection...")
        print("   L'attaque ennemie sera bloquée ce tour!")
        self.player.materials -= 20
        self.wall_active = True
        self.turns_played += 1
        self.turn += 1

    def _action_collect(self):
        """Collecter des matériaux."""
        found = random.randint(25, 50)
        self.player.materials += found
        print(f"🪨 Vous avez collecté {found} matériaux! Total: {self.player.materials}")

    def _action_precision_shot(self):
        """Tir de précision sur l'ennemi."""
        if self.player.ammo < 30:
            print(f"❌ Pas assez de munitions! (vous en avez {self.player.ammo}, besoin: 30)")
            return

        hit_chance = random.random()
        if hit_chance < 0.9:
            damage = random.randint(40, 60)
            self._deal_damage(damage, "tir de précision")
        else:
            print("❌ Tir de précision manqué!")
        self.player.ammo -= 30

    def _action_flee(self):
        """Fuir et se soigner."""
        healing = random.randint(15, 25)
        old_health = self.player.health
        self.player.health = min(100, self.player.health + healing)
        actual_healing = self.player.health - old_health
        print(f"🏃 Vous prenez la fuite et vous soignez! +{actual_healing} PV")
        self.turns_played += 1
        self._enemy_action()
        self.turn += 1

    def _deal_damage(self, damage, action_name):
        """Applique les dégâts à l'ennemi."""
        if self.enemy.shields > 0:
            shield_damage = min(damage, self.enemy.shields)
            self.enemy.shields -= shield_damage
            health_damage = damage - shield_damage
            print(
                f"✅ {action_name} réussi! "
                f"Bouclier: -{shield_damage}, Santé: -{health_damage}"
            )
            self.enemy.health -= health_damage
        else:
            self.enemy.health -= damage
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
                if self.player.shields > 0:
                    shield_damage = min(damage, self.player.shields)
                    self.player.shields -= shield_damage
                    health_damage = damage - shield_damage
                    print(
                        f"🎯 L'ennemi tire! "
                        f"Bouclier: -{shield_damage}, Santé: -{health_damage}"
                    )
                    self.player.health -= health_damage
                else:
                    self.player.health -= damage
                    print(f"🎯 L'ennemi tire! Dégâts: {damage}")
            else:
                print("🤖 L'ennemi rate son coup!")

        elif action == "heal":
            healing = random.randint(15, 30)
            self.enemy.health = min(100, self.enemy.health + healing)
            print(f"🤖 L'ennemi se soigne! +{healing} PV")

        elif action == "ammo":
            print("🤖 L'ennemi cherche des munitions...")

        elif action == "build":
            print("🤖 L'ennemi construit un mur de protection...")

    def _victory(self):
        """Gère la victoire."""
        print("\n🏆 VICTOIRE! 🏆")
        print(f"Vous avez remporté la partie en {self.turns_played} tours!")
        print(f"Santé restante: {self.player.health} PV")
        print(f"Bouclier restant: {self.player.shields}")
        players_remaining = random.randint(1, 5)
        print(f"\n📊 Vous êtes classé 1er! Joueurs restants: {players_remaining}/100")

    def _defeat(self):
        """Gère la défaite."""
        print("\n💀 DÉFAITE! 💀")
        print(f"Vous avez été éliminé après {self.turns_played} tours...")
        print(f"L'ennemi avait encore {self.enemy.health} PV")

def play_fortnite_minigame():
    """Lance une partie de Fortnite et retourne si le joueur a gagné."""
    game = FortniteGame()
    return game.play()
