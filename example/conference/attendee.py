# In here we test a few advanced tricks like relations and datagrid
# fields.  Well, when the right stuff can be imported, anyway.

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.dexterity.browser.add import DefaultAddView, DefaultAddForm
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.browser.view import DefaultView
from plone.directives import form
from plone.formwidget.contenttree import ContentTreeFieldWidget
from plone.formwidget.contenttree import MultiContentTreeFieldWidget
from plone.supermodel import model
from zope import schema
from zope.interface import Interface
import os.path
import plone.dexterity.browser

# We try a few imports.  If these fail we won't be doing anything
# interesting in here.  But the file is still grokked so we need
# reasonable fakedefinitions, even when they are not used.
try:
    from collective.z3cform.datagridfield import DictRow
    from collective.z3cform.datagridfield.datagridfield import \
        DataGridFieldFactory
    DictRow  # pyflakes
    DataGridFieldFactory  # pyflakes
    USE_DATAGRID = True
except ImportError:
    from zope.schema import Object as DictRow
    DataGridFieldFactory = None
    USE_DATAGRID = False
try:
    from plone.formwidget.contenttree import UUIDSourceBinder
    UUIDSourceBinder  # pyflakes
except ImportError:
    # We won't be using this, but we need a sane source definition anyway.
    from plone.formwidget.contenttree import ObjPathSourceBinder as \
        UUIDSourceBinder

from example.conference import _


class IPresenterInfo(Interface):
    # Interface that defines a datagrid row.
    presenter = schema.Choice(
        title=_(u"Presenter"),
        source=UUIDSourceBinder(),
        required=True)

    question = schema.TextLine(
        title=_(u'Question'), required=True)


class IRemarkable(Interface):
    # Interface that defines a datagrid row.
    content = schema.Choice(
        title=_(u"Content"),
        source=UUIDSourceBinder(),
        required=True)

    remark = schema.TextLine(
        title=_(u'Remark'), required=True)


class IAttendee(model.Schema):
    """A conference attendee.
    """

    title = schema.TextLine(
        title=_(u"Full name"),
    )

    # Simple choice based on uuid.
    form.widget(program=ContentTreeFieldWidget)
    program = schema.Choice(
        title=_(u"Chosen Program"),
        source=UUIDSourceBinder(portal_type='example.conference.program'),
        required=False,
        )

    # Multiple choice.
    form.widget(sessions=MultiContentTreeFieldWidget)
    sessions = schema.List(
        title=_(u"Sessions you wish to attend"),
        value_type=schema.Choice(
            title=_(u"Selection"),
            source=UUIDSourceBinder(portal_type='example.conference.session')),
        required=False,
        )

    # Data grid
    if DataGridFieldFactory is not None:
        form.widget(presenters=DataGridFieldFactory)
    presenters = schema.List(
        title=_(u'Questions for presenters'),
        description=_(u"Write down a question for a presenter."),
        value_type=DictRow(title=_(u'Presenters'), schema=IPresenterInfo),
        required=False,
       )

    # Another data grid, this time we will put it in a fieldset.
    form.fieldset('remarks', label=_(u"Remarks"), fields=['remarkables'])
    if DataGridFieldFactory is not None:
        form.widget(remarkables=DataGridFieldFactory)
    remarkables = schema.List(
        title=_(u'Remarkable content'),
        description=_(u"Select a remarkable piece of content on this site "
                      u"and add a remark about it. Fine for reporting "
                      u"typos as well."),
        value_type=DictRow(title=_(u'Remarkable'), schema=IRemarkable),
        required=False,
        )


class ISimplifiedAttendee(form.Schema):
    """A simplified conference attendee.
    """

    title = schema.TextLine(
        title=_(u"Full name"),
        )

# When some imports fail, we have a sneaky way to just ignore all the
# fun stuff.
for required in (USE_DATAGRID, UUIDSourceBinder):
    if not required:
        IAttendee = ISimplifiedAttendee
        break


class DataGridEditView(DefaultEditForm):
    """Edit form that uses the ContentTreeWidget for some fields in
    the datagrids.
    """

    def datagridInitialise(self, subform, widget):
        if widget.name == 'form.widgets.presenters':
            subform.fields['presenter'].widgetFactory = ContentTreeFieldWidget
        elif widget.name == 'form.widgets.remarkables':
            subform.fields['content'].widgetFactory = ContentTreeFieldWidget


class DataGridView(DefaultView):
    """View that uses the ContentTreeWidget for some fields in the
    datagrids.
    """

    # Just point to the original template from plone.dexterity.
    index = ViewPageTemplateFile(
        'item.pt', os.path.dirname(plone.dexterity.browser.__file__))

    def datagridInitialise(self, subform, widget):
        if widget.name == 'form.widgets.presenters':
            subform.fields['presenter'].widgetFactory = ContentTreeFieldWidget
        elif widget.name == 'form.widgets.remarkables':
            subform.fields['content'].widgetFactory = ContentTreeFieldWidget


class DatagridAddForm(DefaultAddForm):

    def datagridInitialise(self, subform, widget):
        if widget.name == 'form.widgets.presenters':
            subform.fields['presenter'].widgetFactory = ContentTreeFieldWidget
        elif widget.name == 'form.widgets.remarkables':
            subform.fields['content'].widgetFactory = ContentTreeFieldWidget


class DatagridAddView(DefaultAddView):
    """Add-view that uses the ContentTreeWidget for some fields in the
    datagrids.
    """

    form = DatagridAddForm
