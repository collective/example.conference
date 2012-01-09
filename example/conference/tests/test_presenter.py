import unittest2 as unittest

from plone.mocktestcase import MockTestCase

from zope.component import createObject
from zope.component import queryUtility

from zope.app.container.contained import ObjectAddedEvent

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from example.conference.presenter import IPresenter
from example.conference.presenter import notifyUser

from example.conference.testing import INTEGRATION_TESTING


class TestPresenterMock(MockTestCase):

    def test_notify_user(self):

        # dummy presenter
        presenter = self.create_dummy(
                __parent__=None,
                __name__=None,
                title="Jim",
                absolute_url=lambda: 'http://example.org/presenter',
            )

        # dummy event
        event = ObjectAddedEvent(presenter)

        # search result for acl_users
        user_info = [{'email': 'jim@example.org', 'id': 'jim'}]

        # email data
        message = "A presenter called Jim was added here http://example.org/presenter"
        email = "jim@example.org"
        sender = "test@example.org"
        subject = "Is this you?"

        # mock tools/portal

        portal_mock = self.mocker.mock()
        self.expect(portal_mock.getProperty('email_from_address')).result('test@example.org')

        portal_url_mock = self.mocker.mock()
        self.mock_tool(portal_url_mock, 'portal_url')
        self.expect(portal_url_mock.getPortalObject()).result(portal_mock)

        acl_users_mock = self.mocker.mock()
        self.mock_tool(acl_users_mock, 'acl_users')
        self.expect(acl_users_mock.searchUsers(fullname='Jim')).result(user_info)

        mail_host_mock = self.mocker.mock()
        self.mock_tool(mail_host_mock, 'MailHost')
        self.expect(mail_host_mock.secureSend(message, email, sender, subject))

        # put mock framework into replay mode
        self.replay()

        # call the method under test
        notifyUser(presenter, event)

        # we could make additional assertions here, e.g. if the function
        # returned something. The mock framework will verify the assertions
        # about expected call sequences.


class TestPresenterIntegration(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_adding(self):
        self.folder.invokeFactory('example.conference.presenter', 'presenter1')
        p1 = self.folder['presenter1']
        self.failUnless(IPresenter.providedBy(p1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='example.conference.presenter')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='example.conference.presenter')
        schema = fti.lookupSchema()
        self.assertEquals(IPresenter, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='example.conference.presenter')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(IPresenter.providedBy(new_object))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
