def pluralize(count, singular, plural=None):
    return singular if count == 1 else (plural or singular + 's')
