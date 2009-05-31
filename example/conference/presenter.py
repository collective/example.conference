from five import grok
from zope import schema

from plone.directives import form, dexterity
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from example.conference import _

from plone.namedfile.field import NamedImage

class IPresenter(form.Schema):
    """A conference presenter. Presenters can be added anywhere.
    """
    
    title = schema.TextLine(
            title=_(u"Name"),
        )
    
    description = schema.Text(
            title=_(u"A short summary"),
        )
    
    form.widget(bio=WysiwygFieldWidget)
    bio = schema.Text(
            title=_(u"Bio"),
            required=False
        )
    
    picture = NamedImage(
            title=_(u"Please upload an image"),
            required=False,
        )

class View(grok.View):
    grok.context(IPresenter)
    grok.require('zope2.View')