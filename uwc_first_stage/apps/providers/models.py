from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import get_upload_path


class Provider(models.Model):
    """
        Provides Model
    """
    name = models.CharField(_('Provider name'), max_length=120)
    logo = models.ImageField(
        _('Provider logo'),
        null=True,
        blank=True,
        upload_to=get_upload_path
    )
    description = models.TextField(_('description'), null=True, blank=True)

    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.name




