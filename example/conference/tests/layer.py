from Products.PloneTestCase import ptc
import collective.testcaselayer.ptc

ptc.setupPloneSite()

class _Layer(collective.testcaselayer.ptc.BasePTCLayer):
    """Test case layer for functional testing.
    """

    def afterSetUp(self):
        self.addProfile('example.conference:default')

Layer = _Layer([collective.testcaselayer.ptc.ptc_layer])
