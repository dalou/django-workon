# encoding: utf-8

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import magic, os, urllib2
from django.core.files.storage import default_storage as storage

class FileTypeTester(models.Model):
    class Meta:
        abstract = True

    file_type_tester_fieldname = 'file'
    file_type_tester_file = None
    file_type_tester_url = None
    file_typemime = models.CharField(_(u"Type Mime"), max_length=254, blank=True, null=True)

    def get_file_file(self, **kwargs):
        if self.file_type_tester_file:
            return self.file_type_tester_file
        fieldname = self.file_type_tester_fieldname
        if not hasattr(self, fieldname):
            raise Exception("Field '%s' doesn't exists in this FileTypeTesterMixin model" % fieldname)
        else:
            file = getattr(self, fieldname)
            self.file_type_tester_file = file.file
            return file.file

    def get_file_url(self, **kwargs):
        if self.file_type_tester_url:
            return self.file_type_tester_url
        fieldname = self.file_type_tester_fieldname
        if not hasattr(self, fieldname):
            raise Exception("Field '%s' doesn't exists in this FileTypeTesterMixin model" % fieldname)
        else:
            file = getattr(self, fieldname)
            self.file_type_tester_url = file.url
            return file.url

    #TODO: open file with S3 storage system to retrieve typemime (storage.open(file) -> and get headers)
    def get_file_mimetype(self, fieldname=None, **kwargs):
        if self.file_typemime:
            return self.file_typemime
        if fieldname == None:
            fieldname = self.file_type_tester_fieldname
        if not hasattr(self, fieldname):
            raise Exception("Field '%s' doesn't exists in this FileTypeTesterMixin model" % fieldname)
        else:
            file = getattr(self, fieldname)
            #return magic.from_file(str(storage.open(file.name)), mime=True)
            try:
                # Normal storage condition
                self.file_typemime = magic.from_file(file.path, mime=True)
                self.save()
                return self.file_typemime
            except:
                # if there is no name, stop right here
                if not file.name:
                    self.file_typemime = None
                    return self.file_typemime

                # Type static S3 amazon collection
                try:
                    url = os.path.join(settings.MEDIA_URL, file.name)

                    # stop if the url is not a valid url
                    if any([
                        url.startswith('//'),
                        url.startswith('http://'),
                        url.startswith('https://')]):

                        file = urllib2.urlopen(url)
                        self.file_typemime = file.info().gettype()
                        self.save()
                    else:

                        self.file_typemime = None
                except:
                    self.file_typemime = None

            return self.file_typemime

    def is_image(self, **kwargs):
        mimetype = self.get_file_mimetype()
        return mimetype in ['image/rgb', 'image/gif', 'image/pbm', 'image/pgm', 'image/ppm',
            'image/tiff', 'image/rast', 'image/xbm', 'image/jpeg', 'image/bmp', 'image/png', 'image/x-icon']


    def is_zip(self, **kwargs):
        return self.get_file_mimetype() in ['application/zip']

    def is_pdf(self, **kwargs):
        return self.get_file_mimetype() in ['application/pdf']

    def is_powerpoint(self, **kwargs):
        return self.get_file_mimetype() in ['application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                                            'application/vnd.openxmlformats-officedocument.presentationml.slideshow']

    def is_word(self, **kwargs):
        return self.get_file_mimetype() in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                                            'application/vnd.ms-excel', 'vnd.ms-word.document']

    def is_zip(self, **kwargs):
        return self.get_file_mimetype() in ['application/zip']