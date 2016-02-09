from django.utils import feedgenerator

class RssFeed(feedgenerator.Rss201rev2Feed):

    def rss_attributes(self):
        return {
            "version": self._version,
            "xmlns:atom": "http://www.w3.org/2005/Atom",
            "xmlns:content": "http://purl.org/rss/1.0/modules/content/" ,
            "xmlns:wfw": "http://wellformedweb.org/CommentAPI/" ,
            "xmlns:dc": "http://purl.org/dc/elements/1.1/" ,
            "xmlns:sy": "http://purl.org/rss/1.0/modules/syndication/" ,
            "xmlns:slash": "http://purl.org/rss/1.0/modules/slash/",
            "xmlns:media": "http://search.yahoo.com/mrss/"
        }

    # def add_root_elements(self, handler):
    #     super(RssFeed, self).add_root_elements(handler)
    #     if self.feed.get('image') is not None:
    #         handler.startElement(u'image', {})
    #         handler.addQuickElement(u"url", self.feed['image_url'])
    #         handler.addQuickElement(u"title", self.feed['title'])
    #         handler.addQuickElement(u"link", self.feed['link'])
    #         handler.endElement(u'image')

    def add_item_elements(self, handler, item):
        super(RssFeed, self).add_item_elements(handler, item)

        print type(handler)
        if item.get('content_encoded') is not None:

            handler.startElement(u"content:encoded", {})
            handler.characters(item['content_encoded'])

            # if item['media'] is not None:

            # figure = '<figure type="image/jpeg">'
            #     ...
            #     handler.characters(escape(figure))

            handler.endElement(u"content:encoded")



        if item.get('media') is not None:

            handler.addQuickElement(u'media:thumbnail', item['media'])

