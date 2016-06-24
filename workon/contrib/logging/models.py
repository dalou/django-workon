# encoding: utf-8

from django.db import models
from django.conf import settings

class DisallowedHost(models.Model):

    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True, db_index=True)

    http_host = models.CharField(u"HTTP_HOST", max_length=254, null=True, blank=True)
    remote_addr = models.CharField(u"REMOTE_ADDR", max_length=254, null=True, blank=True)
    http_x_forwarded_for = models.CharField(u"HTTP_X_FORWARDED_FOR", max_length=254, null=True, blank=True)

    request_uri = models.CharField(u"REQUEST_URI", max_length=254, null=True, blank=True)
    request_method = models.CharField(u"REQUEST_METHOD", max_length=254, null=True, blank=True)
    query_string = models.CharField(u"QUERY_STRING", max_length=254, null=True, blank=True)
    path_info = models.CharField(u"PATH_INFO", max_length=254, null=True, blank=True)
    http_user_agent = models.CharField(u"HTTP_USER_AGENT", max_length=254, null=True, blank=True)

    html_report = models.TextField(u"HTML report", null=True, blank=True)

    def __unicode__(self):
        return "%s througt %s" % ( self.http_host, self.http_x_forwarded_for )


    class Meta:
        db_table = "workon_security_disallowedhost"
        verbose_name = 'Intrusion'
        verbose_name_plural = 'Intrusions'
        ordering = ['-created_at']