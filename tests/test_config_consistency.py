import unittest
from unittest.mock import patch
import config
from game import Game
from actions import Actions

class TestConfigConsistency(unittest.TestCase):

    def test_room_items_and_pnj_exist(self):
        # every item and pnj referenced in rooms_config should exist in configs
        for rkey, rdata in config.rooms_config.items():
            for item in rdata.get('items', []):
                self.assertIn(item, config.items_config, f"Item '{item}' referenced in room '{rkey}' missing from items_config")
            for p in rdata.get('pnj', []):
                self.assertIn(p, config.pnj_config, f"PNJ '{p}' referenced in room '{rkey}' missing from pnj_config")

    def test_actions_look_no_exception(self):
        # instantiate Game with patched input to avoid prompt
        with patch('builtins.input', return_value='TestRunner'):
            game = Game()
        # calling look should not raise even if configs changed
        try:
            Actions.look(game, None, None)
        except Exception as e:
            self.fail(f"Actions.look raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
