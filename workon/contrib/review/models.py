# encoding: utf-8

from django.conf import settings
from django.db import models
from django.db.models import Avg

import workon.utils

class ReviewManager(models.Manager):

    def get_or_create_review_for_user(self, request, *args, **kwargs):
        review = get_review_for_user(request, *args, **kwargs)
        if not review:
            review = Review(company=company, user=user, ip_address=ip_address, cookie=None)
        return review


    def get_review_for_user(self, request, **kwargs):
        """get_rating_for_user(user, ip_address=None, cookie=None)

        Returns the rating for a user or anonymous IP."""

        user = request.user
        ip_address = request.META['REMOTE_ADDR']
        cookies = request.COOKIES


        if not (user and user.is_authenticated()):
            if not ip_address:
                raise ValueError('``user`` or ``ip_address`` must be present.')
            kwargs['user__isnull'] = True
            kwargs['ip_address'] = ip_address
        else:
            kwargs['user'] = user

        # cookie_name = 'review-company.%s' % (company.id)
        # cookie = cookies.get(cookie_name)
        # if cookie:
        #     kwargs['cookie'] = cookie
        # else:
        kwargs['cookie__isnull'] = True

        try:
            review = Review.objects.get(**kwargs)
            return review

        except Review.MultipleObjectsReturned:
            reviews = Review.objects.filter(**kwargs)
            review = reviews.first()
            reviews.exclude(id=reviews.id).delete()
            return review

        except Review.DoesNotExist:
            if create:
                return Review(company=company, user=user, ip_address=ip_address, cookie=None)
            else:
                return None

class ReviewBase(models.Model):

    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True, db_index=True)

    company = models.ForeignKey('directory.Company', related_name='reviews')
    name = models.CharField(u"Nom", max_length=254, blank=True, null=True)
    score = models.IntegerField()
    message = models.TextField(u"Message")

    ip_address      = models.GenericIPAddressField()
    cookie          = models.CharField(max_length=32, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", verbose_name=u"Utilisateur", null=True, blank=True, on_delete=models.SET_NULL)
    user_email = models.EmailField("Email", null=True, blank=True)

    objects = ReviewManager()

    def save(self, *args, **kwargs):

        # existing = bool(self._meta.model.objects.get_rating_for_user(request.user, request.META['REMOTE_ADDR'], request.COOKIES))

        if self.user_id and not self.user_email:
            self.user_email = self.user.email

        self.score = int(min(5, max(1, self.score)))
        self.message = self.message.strip()

        super(ReviewBase, self).save(*args, **kwargs)

        self.company.rating_score = self.company.reviews.all().aggregate(Avg('score')).get('score__avg', 0.0)
        self.company.save()

    class Meta:
        ordering = ('-created_at', )
        verbose_name = u"Avis"
        verbose_name_plural = u"Avis"
        abstract = True

    def __unicode__(self):
        return u"%s (%s)s" % (self.name, self.score)

