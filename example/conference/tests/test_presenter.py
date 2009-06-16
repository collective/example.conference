import unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.dexterity.interfaces import IDexterityFTI

from Products.PloneTestCase.ptc import PloneTestCase
from example.conference.tests.layer import Layer

from example.conference.presenter import IPresenter

class TestPresenterIntegration(PloneTestCase):
    
    layer = Layer
    
    def test_adding(self):
        self.folder.invokeFactory('example.conference.presenter', 'presenter1')
        p1 = self.folder['presenter1']
        self.failUnless(IPresenter.providedBy(p1))
    
    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='example.conference.presenter')
        self.assertNotEquals(None, fti)
    
    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='example.conference.presenter')
        schema = fti.lookup_schema()
        self.assertEquals(IPresenter, schema)
    
    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='example.conference.presenter')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(IPresenter.providedBy(new_object))
    
def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)