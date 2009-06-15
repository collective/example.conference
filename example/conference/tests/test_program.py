import unittest
import datetime

from example.conference.program import start_default_value
from example.conference.program import end_default_value
from example.conference.program import IProgram
from example.conference.program import StartBeforeEnd

class MockProgram(object):
    pass

class ProgramTest(unittest.TestCase):
    """Unit test for the Program type
    """
    
    def test_start_defaults(self):
        data = MockProgram()
        default_value = start_default_value(data)
        today = datetime.datetime.today()
        delta = default_value - today
        self.assertEquals(6, delta.days)

    def test_end_default(self):
        data = MockProgram()
        default_value = end_default_value(data)
        today = datetime.datetime.today()
        delta = default_value - today
        self.assertEquals(9, delta.days)
    
    def test_validate_invariants_ok(self):
        data = MockProgram()
        data.start = datetime.datetime(2009, 1, 1)
        data.end = datetime.datetime(2009, 1, 2)
        
        try:
            IProgram.validateInvariants(data)
        except:
            self.fail()
    
    def test_validate_invariants_fail(self):
        data = MockProgram()
        data.start = datetime.datetime(2009, 1, 2)
        data.end = datetime.datetime(2009, 1, 1)
        
        try:
            IProgram.validateInvariants(data)
            self.fail()
        except StartBeforeEnd:
            pass
    
    def test_validate_invariants_edge(self):
        data = MockProgram()
        data.start = datetime.datetime(2009, 1, 2)
        data.end = datetime.datetime(2009, 1, 2)
        
        try:
            IProgram.validateInvariants(data)
        except:
            self.fail()

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)