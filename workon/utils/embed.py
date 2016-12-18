# encoding: utf-8

import re

__all__ = [
    "str_to_embed",
]

EMBED_TYPES = {
    'youtube': [
        [
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?\s"]{11})',

            '<iframe class="workon-media" src="'
            'https://www.youtube.com/embed/\\6?autoplay=%(autoplay)s&amp;controls=2&amp;showinfo=0"'
            'scrolling="no" frameborder="no" allowfullscreen></iframe>'
        ]
    ],
    'soundcloud': [
        [
            r'(http[s]?\:\/\/w\.soundcloud\.com\/player\/\?url=([^"]+))',
            '<iframe class="workon-media" src="https://w.soundcloud.com/player/?url=\\2" scrolling="no" frameborder="no" allowfullscreen></iframe>'
        ],
        [
            r'(http[s]?\:\/\/soundcloud\.com\/[\d\w\-_]+/[\d\w\-_]+)',
            '<iframe class="workon-media" src="https://w.soundcloud.com/player/?url=\\1" scrolling="no" frameborder="no" allowfullscreen></iframe>'
        ]
    ],
    'vimeo': [
        [
            r'(http[s]?\:\/\/(player\.)?vimeo\.com\/([\/\w]+)\/([\d]+))',
            """<iframe class="workon-media" src="https://player.vimeo.com/video/\\4" scrolling="no" frameborder="no" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>"""
        ]
    ]
}

def str_to_embed(str, autoplay=False):
    for type_name, patterns in EMBED_TYPES.items():
        for pattern in patterns:
            # regex = re.compile(pattern)
            result = re.search(pattern[0], str)
            if result:
                name = result.group(0)
                iframe = pattern[1] % {
                    'autoplay': '1' if autoplay else '0'
                }
                html = re.sub(pattern[0], iframe, name)
                if html != name:
                    return html
    return None