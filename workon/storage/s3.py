
"""
!! VERY IMPORTANT

Custom Amazon S3 storage system.
It's needed for :
    - generate private crypted url for user media files
    - point the cache folder into s3://{{media_bucket}}/cache/
    - point the media folder into s3://{{media_bucket}}/media/
    - point the static files into s3://{{static_bucket}}/ root


"""

import time, os

from django.conf import settings
from django.core.files.storage import get_storage_class
from django.utils.functional import SimpleLazyObject

from storages.backends.s3boto import S3BotoStorage
from boto.cloudfront.distribution import Distribution



# Very important to store private files in cbien-media bucket folders et customise url crypting
MediaRootS3BotoStorage        = lambda: MediaS3BotoStorage(location=settings.AWS_S3_MEDIA_PATH)
MediaThumbRootS3BotoStorage        = lambda: MediaS3BotoStorage(location='') # implicitly /cache/

# Not very important because static are directly called from static.cbien.com and synchronised via aws s3 CLI.
StaticRootS3BotoStorage       = lambda: StaticS3BotoStorage(location=settings.AWS_S3_STATIC_PATH)
StaticRootCachedS3BotoStorage = lambda: StaticCachedS3BotoStorage(location=settings.AWS_S3_STATIC_PATH)

class MediaS3BotoStorage(S3BotoStorage):

    bucket_name = settings.AWS_STORAGE_MEDIA_BUCKET_NAME
    custom_domain = settings.AWS_S3_MEDIA_DOMAIN
    custom_path = settings.AWS_S3_MEDIA_PATH
    signed_urls = settings.AWS_S3_MEDIA_SIGNED_URLS

    """
        Overrided FielField storage based url method
        Its generated an authorized key-pair signature to secure urls.
        Be carreful this method fail silently.
    """
    def url(self, name):
        if name.startswith('http://') or name.startswith('https://'):
            return name
        if self.secure_urls:
            # Get crypted url from cloudfront, ex : https://media.cbien.com
            name = self._normalize_name(self._clean_name(name))
            url = "%s//%s" % (self.url_protocol,
                                os.path.join(self.custom_domain, self.custom_path, name))
            dist = Distribution()
            return dist.create_signed_url(
                url=url,
                keypair_id=settings.CLOUDFRONT_KEY_PAIR_ID,
                private_key_string=settings.CLOUDFRONT_PRIVATE_KEY,
                expire_time=int(time.time() + int(settings.CLOUDFRONT_ROTATION_SECONDS))
            )
        elif self.signed_urls:
            name = os.path.join(self.location,  name)
            return self.connection.generate_url(self.querystring_expire,
                method='GET', bucket=self.bucket.name, key=self._encode_name(name),
                query_auth=self.querystring_auth, force_http=not self.secure_urls)
        else:
            name = self._normalize_name(self._clean_name(name))
            return "%s//%s" % (self.url_protocol,
                                  os.path.join(self.custom_domain, name))


class StaticS3BotoStorage(S3BotoStorage):

    bucket_name = settings.AWS_STORAGE_STATIC_BUCKET_NAME
    custom_domain = settings.AWS_S3_STATIC_DOMAIN
    custom_path = settings.AWS_S3_STATIC_PATH
    def url(self, name):
        name = self._normalize_name(self._clean_name(name))
        return "%s//%s" % (self.url_protocol,
                              os.path.join(self.custom_domain, name))

class StaticCachedS3BotoStorage(StaticS3BotoStorage):

    """
    S3 storage backend that saves the files locally, and gzip the remote version.
    """
    def __init__(self, *args, **kwargs):
        kwargs['querystring_auth'] = False
        super(StaticCachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        non_gzipped_file_content = content.file
        name = super(StaticCachedS3BotoStorage, self).save(name, content)
        content.file = non_gzipped_file_content
        self.local_storage._save(name, content)
        return name
