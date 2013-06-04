from Products.CMFCore.utils import getToolByName
from example.conference import _
from five import grok
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage
from plone.supermodel import model
from zope.container.interfaces import IObjectAddedEvent
from zope import schema


class IPresenter(model.Schema):
    """A conference presenter. Presenters can be added anywhere.
    """

    title = schema.TextLine(
        title=_(u"Name"),
    )

    description = schema.Text(
        title=_(u"A short summary"),
    )

    model.primary('bio')
    bio = RichText(
        title=_(u"Bio"),
        required=False,
    )

    model.primary('picture')
    picture = NamedImage(
        title=_(u"Picture"),
        description=_(u"Please upload an image"),
        required=False,
    )


@grok.subscribe(IPresenter, IObjectAddedEvent)
def notifyUser(presenter, event):
    acl_users = getToolByName(presenter, 'acl_users')
    mail_host = getToolByName(presenter, 'MailHost')
    portal_url = getToolByName(presenter, 'portal_url')

    portal = portal_url.getPortalObject()
    sender = portal.getProperty('email_from_address')

    if not sender:
        return

    subject = "Is this you?"
    message = "A presenter called %s was added here %s" % (
        presenter.title, presenter.absolute_url())

    matching_users = acl_users.searchUsers(fullname=presenter.title)
    for user_info in matching_users:
        email = user_info.get('email', None)
        if email is not None:
            mail_host.secureSend(message, email, sender, subject)


class View(grok.View):
    grok.context(IPresenter)
    grok.require('zope2.View')
