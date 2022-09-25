import unittest
from entities import *


class TestAttacking(unittest.TestCase):

    def test_single_attack_hit(self):
        p = Player("", "", 2)
        m = Monster("","", 2)
        m.evasion = 0
        p.attack(m)
        self.assertEqual(m.life, 1)

    def test_single_attack_miss(self):
        p = Player("", "", 2)
        m = Monster("","", 2)
        m.evasion = 1000
        p.attack(m)
        self.assertEqual(m.life, 2)

class TestGraphics(unittest.TestCase):

    def test_player_graphics(self):
        p = Player("", "", 2)
        self.assertEqual(p.graphic, '@')

    def test_monster_graphics(self):
        m = Monster("", "", 2)
        self.assertEqual(m.graphic, '2')
    
    def test_entity_changing_graphic_after_damage_taken(self):
        p = Player("", "", 2)
        m = Monster("", "", 2)
        self.assertEqual(m.graphic, '2')
        p.attack(m)
        self.assertEqual(m.graphic, '1')



if __name__ == '__main__':
    unittest.main()