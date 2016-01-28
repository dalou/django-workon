
from django.views import generic
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

SIZE = 500
MESSAGE = "Boh i don't know what I know to be knowing"
FILENAME = "Crypted.png"

IMAGE = Image.new("RGB", (SIZE,SIZE))

class TextImage(generic.View):
    text = "workon"
    size = 500

    def get_text(self):
        return self.text

    def getSize(self, txt, font):
        testImg = Image.new('RGB', (1, 1))
        testDraw = ImageDraw.Draw(testImg)
        return testDraw.textsize(txt, font)

    def get(self, *args, **kwargs):
        text = self.get_text()
        text = text if text else ""

        fontname = "Arial.ttf"
        fontsize = 29

        colorText = "black"
        colorOutline = "red"
        colorBackground = "white"

        font = ImageFont.truetype(fontname, fontsize)
        width, height = self.getSize(text, font)
        img = Image.new('RGB', (width+30, height+30), colorBackground)
        d = ImageDraw.Draw(img)
        d.text((15, height/2), text, fill=colorText, font=font)

        img = img.filter(ImageFilter.BLUR)
        # d.rectangle((0, 0, width+3, height+3), outline=colorOutline)




        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response
