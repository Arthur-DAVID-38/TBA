import unittest
from unittest.mock import patch
from game import Game
from actions import Actions

class TestInventory(unittest.TestCase):

    def test_take_inventory_and_drop(self):
        with patch('builtins.input', return_value='Tester'):
            game = Game()
        # place an object in the room
        game.player.current_room = game.rooms['self']
        # ensure item exists in room
        self.assertIn('plateau_glitch', game.player.current_room.items)

        # take it
        Actions.take(game, None, ['plateau_glitch'])

        # inventory should contain it
        import io, sys
        buf = io.StringIO()
        old = sys.stdout
        try:
            sys.stdout = buf
            Actions.inventory(game, None, [])
        finally:
            sys.stdout = old
        out = buf.getvalue()
        self.assertIn('plateau_glitch', out)

        # drop it
        Actions.drop(game, None, ['plateau_glitch'])
        self.assertNotIn('plateau_glitch', game.player.inventory)
        self.assertIn('plateau_glitch', game.player.current_room.items)

if __name__ == '__main__':
    unittest.main()
