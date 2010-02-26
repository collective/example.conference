import unittest

from zExceptions import Unauthorized

from zope.component import createObject
from zope.component import queryUtility

from plone.dexterity.interfaces import IDexterityFTI

from Products.PloneTestCase.ptc import PloneTestCase
from example.conference.tests.layer import Layer

from example.conference.session import ISession
from example.conference.session import possibleTracks

class TestSessionIntegration(PloneTestCase):
    
    layer = Layer
    
    def test_adding(self):
        
        # We can't add this directly
        try:
            self.folder.invokeFactory('example.conference.session', 'session1')
            self.fail('Conference sessions should not be addable except within conference programs.')
        except (ValueError, Unauthorized):
            pass
        
        self.folder.invokeFactory('example.conference.program', 'program1')
        p1 = self.folder['program1']
        
        p1.invokeFactory('example.conference.session', 'session1')
        s1 = p1['session1']
        self.failUnless(ISession.providedBy(s1))
    
    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='example.conference.session')
        self.assertNotEquals(None, fti)
    
    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='example.conference.session')
        schema = fti.lookupSchema()
        self.assertEquals(ISession, schema)
    
    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='example.conference.session')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(ISession.providedBy(new_object))
    
    def test_tracks_vocabulary(self):
        self.folder.invokeFactory('example.conference.program', 'program1')
        p1 = self.folder['program1']
        p1.tracks = ['T1', 'T2', 'T3']
        
        p1.invokeFactory('example.conference.session', 'session1')
        s1 = p1['session1']
        
        vocab = possibleTracks(s1)
        
        self.assertEquals(['T1', 'T2', 'T3'], [t.value for t in vocab])
        self.assertEquals(['T1', 'T2', 'T3'], [t.token for t in vocab])
    
    def test_catalog_index_metadata(self):
        self.failUnless('track' in self.portal.portal_catalog.indexes())
        self.failUnless('track' in self.portal.portal_catalog.schema())
    
    def test_workflow_installed(self):
        self.folder.invokeFactory('example.conference.program', 'program1')
        p1 = self.folder['program1']
        
        p1.invokeFactory('example.conference.session', 'session1')
        s1 = p1['session1']
        
        chain = self.portal.portal_workflow.getChainFor(s1)
        self.assertEquals(('example.conference.session_workflow',), chain)

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)