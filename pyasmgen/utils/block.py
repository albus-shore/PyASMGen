from functools import wraps

def catchable_block(instance):
    '''This is a decorator to catch instruction block instance.'''
    def decorator(func):
        @wraps(func)
        def wrapped_method(object,*args,**kwargs):
                instance._asm.append(object)
                return func(object,*args,**kwargs)
        return wrapped_method
    return decorator