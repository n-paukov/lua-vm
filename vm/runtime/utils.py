def is_float_literal(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
