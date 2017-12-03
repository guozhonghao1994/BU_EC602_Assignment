""" 2017 checker for duplicatefinder.py"""
import unittest
import subprocess
import os
import random
import urllib.request
import time
import logging
from io import StringIO

import ec602lib

TIMEOUT = 30
ONSERVER = False
GOAL_TIME = 9.0  # seconds to run unit tests on all directories
ref_code = {'lines': 68, 'words': 215}


python3exec = 'python3'
sourcecode = "duplicatefinder.py"
original_name = "duplicatefinder.py"

# grades for 6 tests.
Tests = {'zero': 7, 'one': 5, 'two': 5, 'three': 5, 'four': 10, 'five': 8}

Digests = {
    'zero': b'0ed59a9dbdaf7f16488dd7c036e87287e82fa888fdc23e4aa18d01c1bbf002d1',
    'one': b'91a954fb39e19ee2eec5bedae817828437d61222c7acaa08205fa4f2e17fceb3',
    'two': b'36450ab140e4530a69007ccfd2136944c404a7f65c1a67b42f554d3f55fec069',
    'three': b'12deb6312220253dbbb14988e40f79e18befa13d91a6e6723db939123c481eaa',
    'four': b'79c8d14f7e5d7316488498b67bd5301cabdae145385df48d069505492f0eed63',
    'five': b'185ae4f31e010e405a3ec0b0bea4055a37511ce9e4c3dac3625f35e971a575a3'
}

this_dir = os.getcwd()

msg = """
Your answers.txt file was:
------------
{}
------------
The correct answers.txt file is
------------
{}
------------
"""
bad_digest_msg = """Mismatched hexdigests!
correct: {} 
yours:   {}
"""


class duplicate_spec_TestCase(unittest.TestCase):
    def setUp(self):
        rd = random.randint(10000, 100000)
        self.thedir = "df_test" + str(rd)
        print('setup unittest')
        print('creating temporary test directory', self.thedir)
        try:
            os.mkdir(self.thedir)
        except:
            pass
        os.chdir(self.thedir)
        os.system('unzip -o ../duplicate_checker_dirs.zip >/dev/null')
        os.chdir('checker_files')
        self.answers = {}
        for test in Tests:
            try:
                with open(test + '/answers.txt') as f:
                    self.answers[test] = f.read()
                print('found {} answers'.format(test))
            except:
                pass

    def test_specs(self):
        "a. run the duplicatefinder on each directory of files."
        for test in Tests:
            with self.subTest(CASE=test):
                res = ""
                try:
                    print('checking directory:', test)
                    start_time = time.time()
                    os.chdir(test)
                    stud_answer = 'your_answer{}.txt'.format(
                        random.randint(30000, 40000))
                    A = subprocess.run([python3exec, os.path.join(
                        orig_dir, sourcecode), stud_answer], stdout=subprocess.PIPE, timeout=TIMEOUT)
                    res = ""

                    if A.returncode != 0:
                        res += "Bad return code: {}\n".format(A.returncode)

                    if test in self.answers:
                        CreatedText = ""
                        try:
                            with open(stud_answer) as f:
                                CreatedText = f.read()
                            os.remove(stud_answer)
                        except:
                            res += 'unable to read answers file specified on command line.\n'

                        if CreatedText != self.answers[test]:
                            res += msg.format(CreatedText, self.answers[test])

                    hexd = A.stdout.strip()
                    if Digests[test] != hexd:
                        res += bad_digest_msg.format(Digests[test], hexd)
                except Exception as e:
                    res += "Exception!\n{}\n".format(e)
                finally:
                    for fname in os.listdir('.'):
                        os.remove(fname)
                    os.chdir('..')
                    os.rmdir(test)
                    print('  {:.1f} seconds'.format(time.time() - start_time))
                    if res:
                        self.fail(res)

    def tearDown(self):
        print('..cleanup.')
        os.chdir('..')

        os.rmdir('checker_files')

        os.chdir(this_dir)
        os.rmdir(self.thedir)


def main():

    fh = StringIO()

    print('Checking {} for EC602 submission.\n'.format(original_name), file=fh)

    Grade = {}

    s1 = time.time()
    the_program = ec602lib.read_file(sourcecode)
    authors = ec602lib.get_authors(the_program, 'py')
    imported = ec602lib.get_python_imports(the_program)
    logging.info('init %f', time.time() - s1)

    if 'from os import listdir' not in the_program or the_program.count(' os') > 1:
        print('Please import os as specified.', file=fh)
        return Grade, fh.getvalue()

    s1 = time.time()
    errors, passed, gradesummary = ec602lib.check_program(
        duplicate_spec_TestCase)

    check_time = time.time() - s1
    logging.info('df time %f', check_time)

    your_time = check_time * faster_than_server

    if False:
        return Grade, fh.getvalue()

    s1 = time.time()
    pep8_errors, pep8_report = ec602lib.pep8_check(sourcecode)
    logging.info('pep8 %f', time.time() - s1)

    s1 = time.time()
    pylint_score, pylint_report = ec602lib.pylint_check(sourcecode)
    logging.info('pylint %f', time.time() - s1)

    s1 = time.time()
    code_metrics = ec602lib.code_analysis_py(the_program)
    logging.info('analysis %f', time.time() - s1)

    complexity = code_metrics['words']

    print('---- program check ----\n', file=fh)

    if errors:
        Grade['specs'] = 0
        print('Grades for passed test cases:', file=fh)
        for case in Tests:
            points = Tests[case] if 'CASE: {}'.format(
                case) not in errors[0] else 0
            Grade['specs'] += points
            print("{:<6}".format(case),
                  "{}/{} points".format(points, Tests[case]), file=fh)
    else:
        print('All tests passed.', file=fh)
        Grade['specs'] = sum(Tests[case] for case in Tests)

    Grade['pep8'] = 10 - pep8_errors

    Grade['pylint'] = pylint_score

    Grade['elegance'] = 20 * min(1, 215 / complexity)

    print('---- analysis of your program ----\n', file=fh)

    print('authors          : {}'.format(" ".join(authors)
                                         if authors else ec602lib.AUTHWARN), file=fh)

    print('imported modules : {}'.format(" ".join(imported)), file=fh)
    print(ec602lib.code_size_report(code_metrics, ref_code), file=fh)

    print('pep8 check       : {} problems.'.format(pep8_errors), file=fh)
    if pep8_errors:
        print('pep8 report', file=fh)
        print(pep8_report, file=fh)

    print('pylint score     : {}/10'.format(pylint_score), file=fh)
    print(file=fh)

    print('your time {:.1f}, goal is {:.1f}'.format(
        your_time, GOAL_TIME), file=fh)
    Grade['efficiency'] = 20 * min(1, GOAL_TIME / your_time)

    print('---- grading ----\n', file=fh)

    print('grades           :', Grade, file=fh)
    print(
        'grade total      : {:.2f} / 100'.format(sum(Grade[x] for x in Grade)), file=fh)

    return Grade, fh.getvalue()


if __name__ == '__main__':
    print('----begin debugging info')
    FilesNeeded = ['duplicate_checker_dirs.zip']
    orig_dir = os.getcwd()

    dir_listing = os.listdir('.')
    for fneeded in FilesNeeded:
        if fneeded not in dir_listing:
            print('getting', fneeded, 'from server')
            req = 'http://128.197.128.215:60217/static/content/' + fneeded
            with urllib.request.urlopen(req) as f:
                with open(fneeded, 'wb') as g:
                    g.write(f.read())

    if ONSERVER:
        faster_than_server = 1
    else:
        for i in range(2):
            subprocess.run(
                [python3exec, "-c", "import skimage.io"], stdout=subprocess.PIPE)
        st = time.time()
        subprocess.run([python3exec, "-c", "import skimage.io"],
                       stdout=subprocess.PIPE)
        en = time.time()

        # server's measured time on this task is 20 ms.
        print('your python test time {:.1f}'.format(en - st))
        faster_than_server = 1.1 / (en - st)
        print('your computer is {:.1f} times faster than the server. adjusting.'.format(
            faster_than_server))

    Grade, res = main()
    print('----end debugging info')

    print('\n' * 3)
    print(res)

    # optional
    # unittest.main()
