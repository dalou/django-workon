def str_to_float(str):
    return float(str.replace(',', '.').strip())

def is_float(var):
    try:
        float(var)
    except (TypeError, ValueError):
        return False
    return True