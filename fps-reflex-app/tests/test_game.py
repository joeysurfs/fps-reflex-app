import unittest
from src.game import Game

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_initial_score(self):
        self.assertEqual(self.game.score, 0)

    def test_target_generation(self):
        self.game.generate_target()
        self.assertIsNotNone(self.game.current_target)

    def test_reaction_time_calculation(self):
        self.game.start_time = 0
        self.game.end_time = 1
        self.assertEqual(self.game.calculate_reaction_time(), 1)

    def test_score_increment_on_target_click(self):
        self.game.generate_target()
        initial_score = self.game.score
        self.game.click_target(self.game.current_target.position)
        self.assertEqual(self.game.score, initial_score + 1)

if __name__ == '__main__':
    unittest.main()