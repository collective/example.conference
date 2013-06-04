from Acquisition import aq_inner, aq_parent
from example.conference import _
from example.conference.presenter import IPresenter
from five import grok
from plone.app.textfield import RichText
from plone.directives import dexterity
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.security import checkPermission
import plone.autoform.directives as form


@grok.provider(IContextSourceBinder)
def possibleTracks(context):

    # we put the import here to avoid a circular import
    from example.conference.program import IProgram
    while context is not None and not IProgram.providedBy(context):
        context = aq_parent(aq_inner(context))

    values = []
    if context is not None and context.tracks:
        values = context.tracks

    return SimpleVocabulary.fromValues(values)


class ISession(model.Schema):
    """A conference session. Sessions are managed inside Programs.
    """

    title = schema.TextLine(
        title=_(u"Title"),
        description=_(u"Session title"),
    )

    description = schema.Text(
        title=_(u"Session summary"),
    )

    model.primary('details')
    details = RichText(
        title=_(u"Session details"),
        required=False
    )

    # use an autocomplete selection widget instead of the default content tree
    form.widget(presenter=AutocompleteFieldWidget)
    presenter = RelationChoice(
        title=_(u"Presenter"),
        source=ObjPathSourceBinder(
            object_provides=IPresenter.__identifier__),
        required=False,
    )

    dexterity.write_permission(track='example.conference.ModifyTrack')
    track = schema.Choice(
        title=_(u"Track"),
        source=possibleTracks,
        required=False,
    )


class View(dexterity.DisplayForm):
    grok.context(ISession)
    grok.require('zope2.View')

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)
