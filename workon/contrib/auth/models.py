# encoding: utf-8


from django.conf import settings
from django.db import models
from django.utils import timezone

try:
    from django.contrib.sites.models import Site
except:
    Site = None

import workon.utils

try:
    from sorl.thumbnail import get_thumbnail
except:
    get_thumbnail = None

class ActivationToken(models.Model):

    created_date = models.DateTimeField(u"Créé le", auto_now_add=True)
    updated_date = models.DateTimeField(u"Modifié le", auto_now=True, db_index=True)

    email = models.EmailField(u"Adresse email", max_length=254, db_index=True)
    token = models.CharField(u"Token d'activation", max_length=64, unique=True, db_index=True)
    is_used = models.BooleanField(u'Utilisé ?', default=False)
    expiration_date = models.DateTimeField(u"date d'expiration", blank=True, null=True, db_index=True)
    activation_date = models.DateTimeField(u"date d'activation", blank=True, null=True)

    class Meta:
        db_table = "workon_auth_activationtoken"
        unique_together = (("email", "token"),)
        verbose_name = u"Clé d'activation"
        verbose_name_plural = u"Clés d'activation"
        ordering = ('created_date', 'activation_date',)

    def save(self, **kwargs):
        if not self.token:
            self.token = workon.utils.random_token(extra=[self.email])
        super(ActivationToken, self).save(**kwargs)

    def activate_user(self, **kwargs):
        user = workon.utils.get_or_create_user(self.email, **kwargs)
        if user:
            user.is_active = True
            user.save()

            self.is_used = user.has_usable_password()
            self.activation_date = timezone.now()
            self.save()
            return user

        return None

    # def get_activate_url(self):
    #     return "{0}://{1}{2}".format(
    #         getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http"),
    #         Site.objects.get_current() if Site else "",
    #         reverse("workon:auth-activate", args=[self.token])
    #     )

    @models.permalink
    def get_absolute_url(self):
        return ('workon:auth-activate', (self.token, ), {})

    def authenticate_user(self, request, user, remember=False, backend=None):
        return workon.utils.authenticate_user(request, user, remember=remember, backend=backend)


