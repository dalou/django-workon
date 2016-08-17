import os
from django.views import generic
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import base64
import cStringIO
import random

SIZE = 500
MESSAGE = "Boh i don't know what I know to be knowing"
FILENAME = "Crypted.png"

IMAGE = Image.new("RGB", (SIZE,SIZE))

class TextImage(generic.View):
    text = "workon"
    size = 500
    fontname = os.path.join(os.path.dirname(__file__), "textimage_font.ttf")
    colorText = "black"
    colorOutline = (255, 0, 0, 0)#"red"
    colorBackground = (0, 0, 0, 0)#"white"
    fontsize = 20
    base64 = False
    padding = 0

    def get_text(self):
        return self.text

    def getSize(self, txt, font):
        testImg = Image.new('RGB', (1, 1))
        testDraw = ImageDraw.Draw(testImg)
        return testDraw.textsize(txt, font)

    def get(self, *args, **kwargs):
        text = self.get_text()
        text = text if text else ""

        font = ImageFont.truetype(self.fontname, self.fontsize)
        width, height = self.getSize(text, font)
        img = Image.new('RGB', (width+self.padding*2, height+self.padding*2), self.colorBackground)
        d = ImageDraw.Draw(img)
        d.text((self.padding,self.padding), text, fill=self.colorText, font=font)

        # img = img.filter(ImageFilter.BLUR)
        # d.rectangle((0, 0, width+3, height+3), outline=colorOutline)


        if self.base64:
            base64_img_buffer = cStringIO.StringIO()
            img.save(base64_img_buffer, format="PNG")
            base64_img = base64.b64encode(base64_img_buffer.getvalue())

            response = HttpResponse(base64_img, content_type="image/png;base64")
            response['Content-Length'] = len(base64_img)
            return response

        else:
            response = HttpResponse(content_type="image/png")
            img.save(response, "PNG")
            return response
