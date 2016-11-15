
import datetime, re, cStringIO, base64, uuid
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

__all__ = ["base64image_iter"]


base64img_finder = re.compile(r'(data\:image\/(\w+)\;base64\,([\w\+\/\d\=\n]+))')

def base64image_iter(text, uploaded_file=False):

    for m in base64img_finder.finditer(text):

        src = m.group(1)
        image_type = m.group(2).lower()
        base64img = m.group(3)
        if image_type in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'ico']:
            image = base64.decodestring(base64img)
            if uploaded_file:
                image = SimpleUploadedFile('%s.png' % str(uuid.uuid4()), image, content_type='image/%s' % image_type)
            yield src, image