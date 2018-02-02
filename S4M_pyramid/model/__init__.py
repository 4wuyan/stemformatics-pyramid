import redis

from S4M_pyramid.lib.helpers import make_lazy_init_wrapper_class
'''
    For Redis, though it seems to work if I setup an "empty" connection via r = Redis()
    and then "re-init" it by directly calling r.__init__(), I still decide to switch to a wrapper
    class for the sake of safety.

    __init__ is not designed to be called multiple times, and is not supposed to be explicitly
    called from outside as its naming convention suggests. Though it seems fine for now, there
    is no guarentee. It's possible that future Redis versions won't work.

    Moreover, calling __init__ twice might not produce the exactly same result as just once.
    It depends on the internal design of __init__. Here's an example
    class Demo(object):
        def __init__(self, x = None):
            if x is None:
                self.dangerous_attribute = True
            # other init settings
    1) d = Demo(); d.__init__('aha')
    2) d = Demo('aha')
    The 2 choices above produce different results. The risk it leads to is a potential bomb that
    may explode anytime in the future, and it might kill the future developer, no I mean
    engineer, who tries to locate the bug it causes.
'''
RedisWrapper = make_lazy_init_wrapper_class(redis.Redis)
redis_interface_normal = RedisWrapper()
redis_interface_for_pickle = RedisWrapper()

