from django import template
register = template.Library()


class CommentNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        return self.nodelist.render(context)

def compress(parser, token):
    print "FAKE COMPRESS"
    nodelist = parser.parse(('endcompress',))
    parser.delete_first_token()
    return CommentNode(nodelist)

register.tag('compress', compress)