

def pre_fetch(fn):
    """Method register that runs tasks prior to model fetch."""
    return tag_processor(fn, 'pre_fetch')


def post_fetch(fn):
    """Method register that runs tasks after model fetch."""
    return tag_processor(fn, 'post_fetch')


def pre_load(fn):
    """Method register that runs tasks prior to request deserialization."""
    return tag_processor(fn, 'pre_load')


def post_load(fn):
    """Method register that runs tasks after request deserialization."""
    return tag_processor(fn, 'post_load')


def pre_save(fn):
    """Method register that runs tasks prior to database commit."""
    return tag_processor(fn, 'pre_save')


def post_save(fn):
    """Method register that runs tasks after database commit."""
    return tag_processor(fn, 'post_save')


def pre_dump(fn):
    """Method register that runs tasks prior to response serialization."""
    return tag_processor(fn, 'pre_dump')


def post_dump(fn):
    """Method register that runs tasks after response serialization."""
    return tag_processor(fn, 'post_dump')


def tag_processor(fn, name):
    """Return a function tagged with its invokation type and priority."""
    if hasattr(fn, '__call__'):
        return _tag_processor(fn, name)

    priority = fn

    def wrapper(fn):
        return _tag_processor(fn, name, priority)
    return wrapper


def _tag_processor(fn, name, priority=0):
    fn.__invokation_type__ = name
    fn.__invokation_priority__ = priority
    return fn
