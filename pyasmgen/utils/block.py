from functools import wraps

def catchable_block(attribute:list):
    '''This is a decorator to catch instruction block instance.'''
    def decorator(func):
        @wraps(func)
        def wrapped_method(object,*args,**kwargs):
                attribute.append(object)
                return func(object,*args,**kwargs)
        return wrapped_method
    return decorator