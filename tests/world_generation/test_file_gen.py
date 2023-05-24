import unittest
import os
from src.world_generation.file_gen import generate_world

def prepare_files():
    f = open("tests/world_generation/m.sdf", "w")
    f.write("m{a}/m{b}")
    f.close()

    f = open("tests/world_generation/a.sdf", "w")
    f.write("1{c}")
    f.close()

    f = open("tests/world_generation/b.sdf", "w")
    f.write("{c}2{d}")
    f.close()

class TestGenerateWorld(unittest.TestCase):
    def test_gen(self):
        prepare_files()

        generate_world(
            main_file="tests/world_generation/m.sdf",
            output_path="tests/world_generation/o.sdf",
            include_map={ 
                "{a}": "tests/world_generation/a.sdf",
                "{b}": "tests/world_generation/b.sdf",
            },
            replace_map={
                "{c}": "x",
                "{d}": "y",
            }
        )

        f = open("tests/world_generation/o.sdf", "r")
        actual = f.read()
        f.close()

        self.assertEqual(actual, "m1x/mx2y")

        os.remove("tests/world_generation/m.sdf")
        os.remove("tests/world_generation/a.sdf")
        os.remove("tests/world_generation/b.sdf")
        os.remove("tests/world_generation/o.sdf")

if __name__ == "__main__":
    unittest.main()



