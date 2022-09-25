import unittest
from entities import *


class TestAttacking(unittest.TestCase):

    def test_single_attack_hit(self):
        difficulty = 0
        p = Player("", "", 2, 0)
        m = Monster("","", 2, 0)
        p.attack(m)
        self.assertEqual(m.life, 1)

    def test_single_attack_miss(self):
        difficulty = 1
        p = Player("", "", 2, 0)
        m = Monster("","", 2, 100)
        p.attack(m)
        self.assertEqual(m.life, 2)

if __name__ == '__main__':
    unittest.main()