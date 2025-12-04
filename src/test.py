import unittest
import io
from contextlib import redirect_stdout

from tests.library.dataTest import TestChallenge, TestChallengeFileLoad, TestChallengeFileWrite, TestPage

if __name__ == '__main__':
    
    with io.StringIO() as buf, redirect_stdout(buf):
        unittest.main()
