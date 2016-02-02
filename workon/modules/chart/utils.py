from .templatetags import WORKON_CHARTS

def register_chart(name, method, label=''):

    print 'REGISTER CHART', name, method, label
    WORKON_CHARTS[name] = {
        'method': method,
        'label': label
    }