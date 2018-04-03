import unittest
import doctest

import yurlungur.core.enviroment as env


class TestApp(unittest.TestCase):
    def test_env(self):
        env.Windows()

if __name__ == '__main__':
    unittest.main()