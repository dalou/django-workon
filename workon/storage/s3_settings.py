
import os
from boto.s3.connection import SubdomainCallingFormat, OrdinaryCallingFormat


DEFAULT_FILE_STORAGE = 'workon.storage.s3.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'workon.storage.s3.StaticRootS3BotoStorage'
COMPRESS_STORAGE = 'workon.storage.s3.StaticRootS3BotoStorage'
THUMBNAIL_STORAGE = 'workon.storage.s3.MediaThumbRootS3BotoStorage'

########## STORAGE CONFIGURATION
# See: http://django-storages.readthedocs.org/en/latest/index.html

AWS_S3_CALLING_FORMAT = SubdomainCallingFormat()
AWS_S3_ACCESS_KEY_ID = os.environ.get('AWS_S3_ACCESS_KEY_ID', '')
AWS_S3_SECRET_ACCESS_KEY = os.environ.get('AWS_S3_SECRET_ACCESS_KEY', '')

CLOUDFRONT_KEY_PAIR_ID = os.environ.get('CLOUDFRONT_KEY_PAIR_ID', '')
CLOUDFRONT_PRIVATE_KEY = os.environ.get('CLOUDFRONT_PRIVATE_KEY', "")
CLOUDFRONT_ROTATION_SECONDS = os.environ.get('CLOUDFRONT_ROTATION_SECONDS', 3600)

AWS_S3_SECURE_URLS = bool(int(os.environ.get('AWS_S3_SECURE_URLS', '0')))
AWS_S3_MEDIA_SIGNED_URLS = bool(int(os.environ.get('AWS_S3_MEDIA_SIGNED_URLS', '0')))
AWS_S3_URL_PROTOCOL = os.environ.get('AWS_S3_URL_PROTOCOL', 'https:')

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_STORAGE_MEDIA_BUCKET_NAME = os.environ.get('AWS_STORAGE_MEDIA_BUCKET_NAME', AWS_STORAGE_BUCKET_NAME)
AWS_STORAGE_STATIC_BUCKET_NAME = os.environ.get('AWS_STORAGE_STATIC_BUCKET_NAME', AWS_STORAGE_BUCKET_NAME)

AWS_S3_MEDIA_DOMAIN = os.environ.get('AWS_S3_MEDIA_DOMAIN', '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME)
AWS_S3_STATIC_DOMAIN = os.environ.get('AWS_S3_STATIC_DOMAIN', '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME)
AWS_S3_MEDIA_PATH = os.environ.get('AWS_S3_MEDIA_PATH', 'media')
AWS_S3_STATIC_PATH = os.environ.get('AWS_S3_STATIC_PATH', 'static')

AWS_AUTO_CREATE_BUCKET = False
AWS_QUERYSTRING_AUTH = True
# AWS_PRELOAD_METADATA leads to a huge data caching in S3BotoStorage._entries which bloat up the memory
# Keep this to False to prevent memory leaks
AWS_PRELOAD_METADATA = False
# AWS cache settings, don't change unless you know what you're doing:
AWS_IS_GZIPPED = True
AWS_EXPIREY = 60 * 60 * 24 * 7
AWS_HEADERS = {
    'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIREY,
        AWS_EXPIREY)
}
STATIC_URL = '%s//%s/' % (AWS_S3_URL_PROTOCOL, os.path.join(AWS_S3_STATIC_DOMAIN, AWS_S3_STATIC_PATH).strip('/'))
MEDIA_URL = '%s//%s/' % (AWS_S3_URL_PROTOCOL, os.path.join(AWS_S3_MEDIA_DOMAIN, AWS_S3_MEDIA_PATH).strip('/'))
# CACHE_URL is auto defined as 'https://%s/cache/ via STATICFILES_CACHE_STORAGE = 'libs.storage.s3.StaticRootCachedS3BotoStorage' with location=''

########## END S3 CONFIGURATION

# <?xml version="1.0" encoding="UTF-8"?>
# <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
#     <CORSRule>
#         <AllowedOrigin>http://lepole.herokuapp.com</AllowedOrigin>
#         <AllowedMethod>PUT</AllowedMethod>
#         <AllowedMethod>POST</AllowedMethod>
#         <AllowedMethod>DELETE</AllowedMethod>
#         <AllowedHeader>*</AllowedHeader>
#     </CORSRule>
#     <CORSRule>
#         <AllowedOrigin>http://lepole.herokuapp.com</AllowedOrigin>
#         <AllowedMethod>PUT</AllowedMethod>
#         <AllowedMethod>POST</AllowedMethod>
#         <AllowedMethod>DELETE</AllowedMethod>
#         <AllowedHeader>*</AllowedHeader>
#     </CORSRule>
#     <CORSRule>
#         <AllowedOrigin>*</AllowedOrigin>
#         <AllowedMethod>GET</AllowedMethod>
#     </CORSRule>
# </CORSConfiguration>