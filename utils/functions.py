def is_integer(variable):
    try:
        int(variable)
        return True
    except (ValueError, TypeError):
        return False