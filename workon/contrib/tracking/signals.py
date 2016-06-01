from django.dispatch import Signal

tracking_event_created = Signal(providing_args=['sender', 'instance', 'event', 'action'])
