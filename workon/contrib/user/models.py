# encoding: utf-8

import datetime
import operator
import hashlib
import urllib
import random

from django.db import models
from django.conf import settings
from django.core import validators
from django.core.urlresolvers import reverse
from django.contrib import auth, messages
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, User as BaseUser, UserManager, PermissionsMixin
from django.contrib.humanize.templatetags.humanize import naturaltime

import workon.utils

from sorl.thumbnail import get_thumbnail

class User(AbstractBaseUser, PermissionsMixin):
    #timezone = models.CharField(max_length=50, default='Europe/Paris')
    email = models.EmailField(_('Email'), unique=True, db_index=True)

    username = models.CharField(_('username'), blank=True, null=True, max_length=254, db_index=True
        # help_text=_('Required. 30 characters or fewer. Letters, digits and '
        #             '@/./+/-/_ only.'),
        # validators=[
        #     validators.RegexValidator(r'^[\w.@+-]+$',
        #                               _('Enter a valid username. '
        #                                 'This value may contain only letters, numbers '
        #                                 'and @/./+/-/_ characters.'), 'invalid'),
        # ]
    )
    first_name = models.CharField(_('first name'), max_length=254, blank=True, null=True, db_index=True)
    last_name = models.CharField(_('last name'), max_length=254, blank=True, null=True, db_index=True)
    phone_number = models.CharField(u'Téléphone', max_length=254, blank=True, null=True)

    avatar = models.ImageField(u"Photo de profil", blank=True, null=True,
        upload_to=workon.utils.unique_filename("user/avatar/%Y/%m/", original_filename_field='avatar_filename')
    )

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    # is_connection_email_sent = models.BooleanField(u'Email de connexion envoyé', default=False)
    is_fake = models.BooleanField('Fake', default=False)
    is_never_login = models.BooleanField('Ne s\'est jamais connecté', default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    public_key = models.CharField(_(u"Clé publique"), max_length=64, unique=True, db_index=True, null=True)
    private_key = models.CharField(_(u"Clé privée"), max_length=64, unique=True, db_index=True, null=True)


    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    DEFAULT_AVATAR_URL = "http://www.gravatar.com/avatar/00000000000000000000000000000000?d=mm&amp;f=y"

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        # unique_together = ('email',)
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        if not self.first_name and not self.last_name:
            if self.username:
                return self.username.strip()
            else:
                return self.email.strip()
        names = []
        if self.first_name:
            names.append(self.first_name)
        if self.last_name:
            names.append(self.last_name)
        full_name = " ".join(names)
        return full_name.strip()

    def get_username(self):
        "Return the identifying username for this User"
        return self.get_username_or_email()

    def get_username_or_email(self):
        return self.username if self.username else self.email.split('@')[0]

    def get_short_name(self):
        "Returns the short name for the user."
        if not self.first_name:
            if self.username:
                return self.username.strip()
            else:
                return self.email.split('@')[0].strip()
        return self.first_name

    def activate(self):
        if not self.is_active:
            self.is_active = True
            self.save()

    def authenticate(self, request, remember=False, backend=None):
        return workon.utils.authenticate_user(request, self, remember=remember, backend=backend)

    def get_avatar_small(self):
        return self.get_avatar_url(size=40)

    def get_avatar_medium(self):
        return self.get_avatar_url(size=150)

    def get_avatar_large(self):
        return self.get_avatar_url(size=500)

    def get_avatar_url(self, size=200, default=DEFAULT_AVATAR_URL):
        if self.avatar:
            if get_thumbnail:
                return get_thumbnail(self.avatar, '%sx%s' % (size,size), crop='center', format="PNG", quality=99).url
            else:
                return self.avatar.url
        else:
            gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
            gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
            return gravatar_url

    def save(self, **kwargs):
        if not self.public_key:
            self.set_public_key()
        if not self.private_key:
            self.set_private_key()
        super(User, self).save(**kwargs)

    def set_public_key(self, hash_func=hashlib.sha256):
        self.public_key = self.generate_random_token()

    def set_private_key(self, hash_func=hashlib.sha256):
        self.private_key = self.generate_random_token()

    def generate_random_token(self, hash_func=hashlib.sha256):
        return workon.utils.random_token(extra=[self.id if self.id else self.email, self.email])




