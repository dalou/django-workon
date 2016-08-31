from django.apps import apps
from ...apps import WorkonConfig

#: :type: DefaultConfig
workon_admin_config = apps.get_app_config('workon_adminv3')

#: :type: DefaultConfig()
workon_admin_config_cls = WorkonConfig


def get_config(param=None):
    if param:
        value = getattr(workon_admin_config, param, None)
        if value is None:
            value = getattr(workon_admin_config_cls, param, None)
        return value

    return workon_admin_config


def set_config_value(name, value):
    config = get_config()
    # Store previous value to reset later if needed
    prev_value_key = '_%s' % name
    if not hasattr(config, prev_value_key):
        setattr(config, prev_value_key, getattr(config, name))
        setattr(config, name, value)


def reset_config_value(name):
    config = get_config()
    prev_value_key = '_%s' % name
    if hasattr(config, prev_value_key):
        setattr(config, name, getattr(config, prev_value_key))
        del config.__dict__[prev_value_key]
