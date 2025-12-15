import unittest
from unittest.mock import patch
from game import Game
from actions import Actions

class TestBDEQuest(unittest.TestCase):

    def test_bde_conflict_gives_key(self):
        with patch('builtins.input', return_value='Tester'):
            game = Game()
        # se placer dans le BDE
        game.player.current_room = game.rooms['bde']
        # parler aux deux membres en choisissant des réponses conciliatrices
        with patch('builtins.input', side_effect=['2', '1']):
            Actions.talk(game, None, ['bde_alpha'])
            Actions.talk(game, None, ['bde_omega'])
        # la clé doit être dans l'inventaire ou dans la salle
        self.assertTrue('cle_bureau_courivaud' in game.player.inventory or 'cle_bureau_courivaud' in game.player.current_room.items)
        # la quête doit être marquée comme complétée
        self.assertEqual(game.player.quests.get('bde_conflict'), 'completed')

    def test_bde_conflict_wrong_choices_no_key(self):
        with patch('builtins.input', return_value='Tester'):
            game = Game()
        game.player.current_room = game.rooms['bde']
        # choix non conciliateurs
        with patch('builtins.input', side_effect=['1', '2']):
            Actions.talk(game, None, ['bde_alpha'])
            Actions.talk(game, None, ['bde_omega'])
        # pas de clé et pas de quête complétée
        self.assertFalse('cle_bureau_courivaud' in game.player.inventory or 'cle_bureau_courivaud' in game.player.current_room.items)
        self.assertIsNone(game.player.quests.get('bde_conflict'))

    def test_courivaud_starts_machine_quest(self):
        with patch('builtins.input', return_value='Tester'):
            game = Game()
        # simuler qu'on a déjà résolu le conflit et qu'on est dans le bureau
        game.player.quests['bde_conflict'] = 'completed'
        game.player.current_room = game.rooms['bureau_courivaud']
        # parler à Courivaud démarre la quête
        Actions.talk(game, None, ['courivaud'])
        self.assertEqual(game.player.quests.get('courivaud_machine'), 'started')

    def test_collect_all_pieces_and_assemble(self):
        with patch('builtins.input', return_value='Tester'):
            game = Game()
        # lancer la quête
        game.player.quests['bde_conflict'] = 'completed'
        game.player.current_room = game.rooms['bureau_courivaud']
        Actions.talk(game, None, ['courivaud_illusoire'])
        self.assertEqual(game.player.quests.get('courivaud_machine'), 'started')

        # Aller à AssistEtud et obtenir la pièce (réponse 5)
        game.player.current_room = game.rooms['assistetud']
        with patch('builtins.input', side_effect=['5']):
            Actions.talk(game, None, ['agent_multivers'])
        self.assertTrue(game.player.quests.get('piece_assistetud_obtained'))
        self.assertIn('piece_assistetud', game.player.inventory)

        # Aller à Salle 3142 et obtenir la pièce (réponse 3142)
        game.player.current_room = game.rooms['salle_3142']
        with patch('builtins.input', side_effect=['3142']):
            Actions.talk(game, None, ['ton_double'])
        self.assertTrue(game.player.quests.get('piece_salle_3142_obtained'))
        self.assertIn('piece_salle_3142', game.player.inventory)

        # Aller au BDE et obtenir la pièce (réponse 2)
        game.player.current_room = game.rooms['bde']
        with patch('builtins.input', side_effect=['2']):
            Actions.talk(game, None, ['bde_alpha'])
        self.assertTrue(game.player.quests.get('piece_bde_obtained'))
        self.assertIn('piece_bde', game.player.inventory)

        # Assembler dans la Salle Blanche
        game.player.current_room = game.rooms['salle_blanche']
        Actions.assemble(game, None, [])
        self.assertEqual(game.player.quests.get('machine_assembled'), 'completed')
        self.assertIn('machine_quantique', game.player.inventory)

    def test_locked_bureau_requires_key(self):
        with patch('builtins.input', return_value='Tester'):
            game = Game()
        # tenter d'entrer dans le bureau verrouillé depuis la rue sans clé
        game.player.current_room = game.rooms['rue']
        Actions.go(game, None, ['bureau_courivaud'])
        # si échoué, le joueur n'est pas dans le bureau
        self.assertNotEqual(game.player.current_room, game.rooms['bureau_courivaud'])
        # maintenant obtenir la clé (simuler la quête)
        game.player.inventory['cle_bureau_courivaud'] = game.items['cle_bureau_courivaud']
        # retenter l'accès
        Actions.go(game, None, ['bureau_courivaud'])
        # le joueur doit maintenant être dans le bureau
        self.assertEqual(game.player.current_room, game.rooms['bureau_courivaud'])
        # la clé doit avoir été consommée lors de l'ouverture
        self.assertNotIn('cle_bureau_courivaud', game.player.inventory)

if __name__ == '__main__':
    unittest.main()
