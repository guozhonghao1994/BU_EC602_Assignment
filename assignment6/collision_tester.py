# Copyright 2017 J Carruthers jbc@bu.edu
# Solution to HW 5: collision_tester

import unittest
import subprocess
import random
import math
import numpy

AUTHORS = ['jbc@bu.edu']

PROGRAM_TO_TEST = "collisionc_0"

# r = random.randint
# random_twenty=[ (1000+x,r(-2000,2000),r(-2000,2000),
#                  r(-10,10),r(-10,10)) for x in range(20)]
# print(random_twenty)

BAD_ARGS_RC = 2
BAD_INPUT_RC = 1

random_twenty = [(1000, -1663, -1068, 4, 3), (1001, 1771, 1241, 4,
                                              -9), (1002, 531, -1842, 5, -7),
                 (1003, -1999, 576, 9, 7), (1004, 282, -338, 0,
                                            -5), (1005, 1432, 1146, -3, -10),
                 (1006, 1818, 1972, 9,
                  10), (1007, -1819, 365, -6,
                        6), (1008, 1896, 1553, 4,
                             -8), (1009, 1561, 952, 5,
                                   4), (1010, -1937, -1948, -2,
                                        -6), (1011, 110, 1424, 1,
                                              7), (1012, 1754, 1794, -2, -7),
                 (1013, 1042, -193, 5,
                  -4), (1014, 563, 1074, 8,
                        -9), (1015, 243, 62, 5,
                              10), (1016, 1749, 923, -10,
                                    -5), (1017, -1365, -346, -5,
                                          7), (1018, 495, -769, -10,
                                               -1), (1019, -548, -841, 5, -2)]

basic_input = """a 10 20 -1.5 2
b 90 90 -3 -3
c 100 100 1 1
"""

basic_output = """1
a 8.5 22 -1.5 2
b 87 87 -3 -3
c 101 101 1 1
2
a 7 24 -1.5 2
b 84 84 -3 -3
c 102 102 1 1
3
a 5.5 26 -1.5 2
b 81 81 -3 -3
c 103 103 1 1
"""

bad_args = [('-4', "-5"), ("one", "two"), ("one", "4", "5"), ("4", "5",
                                                              "alpha")]

bad_inputs = [
    """a
b 0 0 1 1
c 20 20 1 1
""", """a 0 0 0 0
b 10 10 10 10 10
""", """a b c 0 0
d 10 10 10 10
e 30 30 30 30
""", """a 10 10 1 1


"""
]

collision_input_one = """one -10 -10 2 2
two 10 10 -1 -1
"""

collision_output_one = """12
one -9.0710678 -9.0710678 -1 -1
two 21.071068 21.071068 2 2
"""
large_time_input = "a 0 0 0 0\n"

large_time_list = ['1000', '100000']
large_time_output = """1000
a 0 0 0 0
100000
a 0 0 0 0
"""
runners = [("for", 100, -100, 100, 100), ('back', 0, 0, -100, 100)]

big_locations_input = """one 1000000 1000000 -100 -100
two -1000000 1000000 100 -100
three 1000000 -1000000 -100 100
four -1000000 -1000000 100 100
"""
big_locations_output = """9999
one 100 100 -100 -100
two -100 100 100 -100
three 100 -100 -100 100
four -100 -100 100 100
"""

dup_names = """one 0 0 1 1
one 10 10 10 10
two 20 20 20 20
"""

dup_names_out = """1
one 1 1 1 1
one 20 20 10 10
two 40 40 20 20
2
one 2 2 1 1
one 30 30 10 10
two 60 60 20 20
"""


def runprogram(program, args, inputstr):
    coll_run = subprocess.run(
        [program, *args],
        input=inputstr.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=1)
    "run a program and get result: wrapper for subprocess.run"

    ret_code = coll_run.returncode
    program_output = coll_run.stdout.decode()
    program_errors = coll_run.stderr.decode()
    return (ret_code, program_output, program_errors)


class CollisionTestCase(unittest.TestCase):
    def check_collision_output(self, bad, good):
        "process and numerically compare two outputs (helper function)"
        badlines = bad.splitlines()
        goodlines = good.splitlines()
        self.assertEqual(len(badlines), len(goodlines))
        for badline, goodline in zip(badlines, goodlines):
            goodvals = goodline.split()
            badvals = badline.split()
            if len(goodvals) != len(badvals):
                self.fail('improper line format')
            elif len(goodvals) == 1:  # time line
                self.assertTrue(
                    math.isclose(float(goodvals[0]), float(badvals[0])))
            else:
                self.assertEqual(goodvals[0], badvals[0])
                self.assertTrue(
                    numpy.allclose([float(x) for x in goodvals[1:]],
                                   [float(x) for x in badvals[1:]]))

    def test_collision_one(self):
        "test a simple collision event"
        (rc, out, errs) = runprogram(PROGRAM_TO_TEST, ["12"],
                                     collision_input_one)
        self.assertEqual(rc, 0)
        self.check_collision_output(out, collision_output_one)
        self.assertEqual(errs, "")

    def test_twenty(self):
        "twenty objects with random motion, no collisions"
        strin = "\n".join(" ".join(str(n) for n in x) for x in random_twenty)
        correct_out = "12\n" + "\n".join("{} {} {} {} {}".format(
            x[0], x[1] + 12 * x[3], x[2] + 12 * x[4], x[3], x[4])
                                         for x in random_twenty) + "\n"
        (rc, out, errs) = runprogram(PROGRAM_TO_TEST, ["12"], strin)
        self.assertEqual(rc, 0)
        self.check_collision_output(out, correct_out)
        self.assertEqual(errs, "")

    def test_three_args(self):
        """three arguments, out of order, and with negatives.
        use non-integer values for velocity."""
        (rc, out, errs) = runprogram(PROGRAM_TO_TEST, ["1", "-2", "3", "2"],
                                     basic_input)
        self.assertEqual((rc, errs), (0, ""))
        self.check_collision_output(out, basic_output)

    def test_bad_args(self):
        "bad argument examples: negative or alpha"
        for bad_arg in bad_args:
            with self.subTest(CASE=repr(bad_arg)):
                (rc, out, errs) = runprogram(PROGRAM_TO_TEST, bad_arg,
                                             basic_input)
                if rc != BAD_ARGS_RC:
                    self.fail('rc')

    def test_bad_inputs(self):
        "bad input formatting."
        for bad_in in bad_inputs:
            with self.subTest(CASE=repr(bad_in)):
                (rc, out, errs) = runprogram(PROGRAM_TO_TEST, ["1", "2"],
                                             bad_in)
                if rc != BAD_INPUT_RC:
                    self.fail('rc')

    def test_many_args(self):
        "handle 100+ arguments and large distances"
        many_args = list(range(1, 110))
        strin = "\n".join(" ".join(str(n) for n in x) for x in runners)
        outlines = []
        for time in many_args:
            outlines.append("{}\n".format(time))
            for name, x, y, vx, vy in runners:
                outlines.append("{} {} {} {} {}\n".format(
                    name, x + vx * time, y + vy * time, vx, vy))
        correct_out = "".join(outlines)

        (rc, out, errs) = runprogram(PROGRAM_TO_TEST,
                                     [str(x) for x in many_args], strin)
        self.assertEqual(rc, 0)
        self.check_collision_output(out, correct_out)
        self.assertEqual(errs, "")

    def test_large_time(self):
        "large time values"
        (rc, out, errs) = runprogram(PROGRAM_TO_TEST, large_time_list,
                                     large_time_input)
        self.check_collision_output(out, large_time_output)

    def test_big_locations(self):
        "wide field of motion"
        (rc, out, errs) = runprogram(PROGRAM_TO_TEST, ['9999'],
                                     big_locations_input)
        self.check_collision_output(out, big_locations_output)

    def test_dup_names(self):
        "handle duplicate named objects"
        (rc, out, errs) = runprogram(PROGRAM_TO_TEST, ['1', "2"], dup_names)
        self.check_collision_output(out, dup_names_out)
        self.assertEqual(rc, 0)
        self.assertEqual(errs, "")

    def test_many_collisions(self):
        "handle multiple collisions"
        inlines = ["mover 0 0 0 1\n"]
        outlines = ["2000\n", "mover 0 10 0 0\n"]
        for i, ypos in enumerate(range(20, 3000, 20)):
            inlines.append("mover{} 0 {} 0 0\n".format(i, ypos))
            outlines.append("mover{} 0 {} 0 0\n".format(i, ypos + 10))

        input_str = "".join(inlines)
        outlines[-1] = "mover148 0 3490 0 1\n"

        correct_out = "".join(outlines)
        (rc, out, errs) = runprogram(PROGRAM_TO_TEST, ['2000'], input_str)
        self.check_collision_output(out, correct_out)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
