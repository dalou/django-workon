from django.db import models

class Unique(models.Model):

    class Meta:
        abstract = True

    @classmethod
    def get(cls):
        instance = cls._default_manager.first()
        if not instance:
            instance = self.__class__()
        return instance

    def save(self, *args, **kwargs):
        previous = self._default_manager.first()
        if previous:
            self.pk = previous.pk
        super(Unique, self).save(*args, **kwargs)
