
__all__ = ["str_to_float", "is_float"]

def str_to_float(str, default=None):
    try:
        return float(str.replace(',', '.').strip())
    except:
        return default

def is_float(var):
    try:
        float(var)
    except (TypeError, ValueError):
        return False
    return True

