import datetime

from zope.interface import invariant, Invalid

from five import grok
from zope import schema

from DateTime import DateTime
from plone.indexer import indexer

from plone.directives import form, dexterity
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.z3cform.textlines.textlines import TextLinesFieldWidget

from example.conference import _

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from example.conference.session import ISession

class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start or end date is invalid")

class IProgram(form.Schema):
    """A conference program. Programs can contain Sessions.
    """
    
    title = schema.TextLine(
            title=_(u"Program name"),
        )
    
    description = schema.Text(
            title=_(u"Program summary"),
        )
    
    start = schema.Datetime(
            title=_(u"Start date"),
            required=False,
        )

    end = schema.Datetime(
            title=_(u"End date"),
            required=False,
        )
    
    form.widget(details=WysiwygFieldWidget)
    details = schema.Text(
            title=_(u"Details"),
            description=_(u"Details about the program"),
            required=False,
        )
    
    form.widget(organizer=AutocompleteFieldWidget)
    organizer = schema.Choice(
            title=_(u"Organiser"),
            vocabulary=u"plone.principalsource.Users",
            required=False,
        )
    
    form.widget(tracks=TextLinesFieldWidget)
    tracks = schema.List(
            title=_(u"Tracks"),
            required=False,
            default=[],
            value_type=schema.TextLine(),
        )
    
    @invariant
    def validate_start_end(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_(u"The start date must be before the end date."))

@form.default_value(field=IProgram['start'])
def start_default_value(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(7)


@form.default_value(field=IProgram['end'])
def end_default_value(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(10)

# Indexers

@indexer(IProgram)
def start_indexer(obj):
    if obj.start is None:
        return None
    return DateTime(obj.start.isoformat())
grok.global_adapter(start_indexer, name="start")

@indexer(IProgram)
def end_indexer(obj):
    if obj.end is None:
        return None
    return DateTime(obj.end.isoformat())
grok.global_adapter(end_indexer, name="end")

@indexer(IProgram)
def tracks_indexer(obj):
    return obj.tracks
grok.global_adapter(tracks_indexer, name="Subjec")

# Views

class View(grok.View):
    grok.context(IProgram)
    grok.require('zope2.View')
    
    def sessions(self):
        """Return a catalog search result of sessions to show
        """
        
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        return catalog(object_provides=ISession.__identifier__,
                       path='/'.join(context.getPhysicalPath()),
                       sort_order='sortable_title')
