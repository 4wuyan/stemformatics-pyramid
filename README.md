Introduction
========================

[Stemformatics](https://www.stemformatics.org/) is an online portal that allows stem cell biologists to visually analyse and explore interesting datasets quickly and easily. It is a worldwide resource for collaborators in Australia, North America, Asia and Europe.

Stemformatics website was initially built in 2010 and needs modifications. Currently it is using the Python [Pylons](https://docs.pylonsproject.org/projects/pylons-webframework/en/latest/index.html) web framework and needs to be migrated to the Python [Pyramid](https://docs.pylonsproject.org/projects/pyramid/en/latest/) web framework.

This repo is the place where migration takes place. It is a Stemformatics website running in Pyramid.


Getting Started
===============

Setup your database
-------------------------------

Please make sure the databases in your environment are correctly setup, and contain all the necessary infomation.

### Get connected to your database

An example of database connection configurations can be found in `development.ini`:
```ini
psycopg2_conn_string =  host='localhost' dbname='portal_beta' user='portaladmin'
model.stemformatics.db.url  = postgresql://portaladmin@localhost/portal_beta
```

### Update your database info (optional)

Use SQL queries to insert or update information necessary for the application.
An example that adds some configuration settings into the configuration table in the database can be found in `db_scripts` folder:
```bash
psql -U portaladmin portal_beta -c "insert into stemformatics.configs (ref_type,ref_id) values('validation_regex', '(?=^.{12,}$)(?=.*\s+).*$');"
psql -U portaladmin portal_beta -c "insert into stemformatics.configs (ref_type,ref_id) values('from_email', 'noreply@stemformatics.org');"
psql -U portaladmin portal_beta -c "insert into stemformatics.configs (ref_type,ref_id) values('secret_hash_parameter_for_unsubscribe', 'I LOVE WY');"
psql -U portaladmin portal_beta -c "insert into stemformatics.configs (ref_type,ref_id) values('publish_gene_set_email_address', 'fake_email');"
```

Setup your virtual environment (optional, but recommended)
-------------------------

It is recommended to use a virtual environment of Python 3. According to [Quick Tour of Pyramid](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tour.html), this is an example to set up a virtual environment.

```bash
# set an environment variable to where you want your virtual environment
$ export VENV=~/env
# create the virtual environment
$ python3 -m venv $VENV
```


Start the application!
----------------------

You can run the application by

```bash
$ cd directory/containing/this/file
# install required packages
$ $VENV/bin/pip install -e .
# run the application with development configuration
$ $VENV/bin/pserve development.ini
```

------------------------------------------------------

Our migration tries to reach a balance point between "do it in pyramid's way" and "just make it Pylons compatible for the sake of workload." General migration strategies can be found [here](https://docs.pylonsproject.org/projects/pyramid-cookbook/en/latest/pylons/index.html). Some specific tips or tracks related to Stemformatics project are listed below.

Deprecated pylons globals
========================================

The `lib.deprecated_pylons_global` file is the place where we support and mimic the behaviour of
```python
from pylons import request, response, session, tmpl_context as c, app_globals as g, url, config
```

Request, response, and session
--------------------------------

I personally think it is a bad design, since it makes module testing difficult, and sometimes it lures developers to access the `request`, `response` or `session` object in the model layer.

In Pyramid, you can use the `request.response` and the `request.session` objects wrapped in `request` for convenicne, if you don't want to create your own. Thus the focus is how to access `request` in places where pylons uses a global.

### Access in controllers

Our base controller follows the normal pattern, in which a `request` argument is passed into the constructor and stored in `self.request`. Hence in an action method of a controller, you should access them by
```python
class SomeController(BaseController):
    # other code
    def some_action(self):
        # other code
        request = self.request
        response = self.request.response
        session = self.request.session
        # other code
    # other code
```

### Access in models

Though models shouldn't access `request` in my opinion, this does happen. In that case, you will need to use
```python
request = pyramid.threadlocal.get_current_request()
response = request.response
session = request.session
```
The `magic_globals` object in `lib.deprecated_pylons_globals` provides a shortcut when you have to access them in models.

For more information, see [this page](https://docs.pylonsproject.org/projects/pyramid-cookbook/en/latest/pylons/request.html).

tmpl\_context as c
--------------------------------

It looks like `c` in Pylons is a global container, while not exactly.
Actually it's **local to each request** (refer to
[this page](https://thejimmyg.github.io/pylonsbook/en/1.0/exploring-pylons.html#context-object),
[this page](https://docs.pylonsproject.org/projects/pylons-webframework/en/latest/views.html#strict-vs-attribute-safe-tmpl-context-objects),
and *pylons.tmpl\_context* in [this page](https://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/pylons/request.html)),
which means attributes set by different controller actions do not interfere with each other.

That means we shouldn't simply use a global empty class as a container to mimic the behaviours of `c` in Pyramid. Potentially, there might be 2 risks:

1. If a request invokes an action that modifies some attribute of `c`, say, `c.some_attr`, then `c.some_attr` will not be reset to default as it should in Pylons,
which might affect the behaviour of upcoming requests.
2. In a multithreaded environment, the attributes of `c` set by one request might be modified by another concurrent request before a response is successfully returned.

I think Pyramid does the right thing: If `c` is local to each request, then why not make `c` an attribute of the `request` object?
Seeing `self.request.c` in a class definition feels way better than a `from pylons import tmpl_context as c` on the top, as *the Zen of Python* tells us:
> Explicit is better than implicit.
> Simple is better than complex.

### Access `c` in controllers

In BaseContrller, we have set `self.request.c = self.request.tmpl_context` in the constructor.
Hence **remember to add** `c = self.request.c` at the beginning of an action that uses `c`.

### Access `c` in models

Unfortunately, though very rarely, `c` is still occasionally accessed in the models.
Information provided by `c` is based on each incoming request, thus we need to use our omnipotent `magic_globals`, which helps us catch the current request.
```python
from S4M_pyramid.lib.deprecated_pylons_globals import magic_globals

### other code ###

magic_globals.fetch()
c = magic_globals.c

### some code that sets attributes of c ###
```

URL generator
-------------------

Pyramid has it's own mechanism to generate urls, which you should follow. The global `url` generator object you can find in `lib.deprecated_pylons_globals` is used to be compatible with the old Pylons patterns, namely:
```python
url(controller = 'c', action = 'a')
    -> '/c/a'
url(controller = 'c', action = 'a', qualified = True)
    -> 'https://www.s4m.org/c/a'
url('/c/a')
    ->  '/c/a'
url('c/a')
    ->  'c/a'
url('c/a', qualified = True)
    ->  'https://www.s4m.org/c/a'
url('https://example.com/index')
    -> 'https://example.com/index'
```

The `set_environ()` method of the url generator is designed to work around the `url.environ['pylons.routes_dict']` dictionary used to get the name of the controller or action. It adopts a naive method in which path info is parsed with the pattern `/{controller}/{action}/{id}`. Those special routing rules should redirect to the "orthodox" url first if they need a correct `url.environ['pylons.routes_dict']['controller']` or `url.environ['pylons.routes_dict']['action']` value.

g and config
------------------------
`app_globals` and `config` are _real_ globals, and you can see in `deprecated_pylons_globals` they are both an initially-empty container shared globally.

Defending the design of _magic_ globals and _real_ globals
-----------------------------------------

### *Real* globals

`config`,`g`, and `db` imported from the model are "real" globals, which means you aren't supposed to define them in every function once you import them on the top. By doing so, we shouldn't treat them as _magic_ globals, because it's the intrinsic property as a globally shared container that other parts of the application want to visit; they're supposed to behave so (though it's another topic whether it's necessary to use global containers).

### *Fake* globals

However, `request`, `resposne`, `session` and `c` are on the contrary. I want everyone to tell what `c` is in _every_ function in advance (if `c` exists of course), namely `c = self.request.c` in controllers or `magic_globals.fetch(); c = magic_globals.c` in models. The same applies to `request`, `resposne` and `session`.  The rationale behind it is that they are **request-local**; they are "fake globals." That's why all 4 of them sit in the `MagicGlobalsFromRequest` object, and where _magic_ comes from.


Setting cache headers
================================

Replace
```python
del response.headers['Cache-Control']
del response.headers['Pragma']
```
with
```python
response.headers.pop('Cache-Control', None)
response.headers.pop('Pragma', None)
```
if you see them.

[Pylons documentation](https://docs.pylonsproject.org/projects/pylons-webframework/en/latest/caching.html#cache-headers) explains what happened with those headers.
In Pyramid, those keys might not exist in the response header dictionary, and the preferred more Pythonic solution is as above.
(Refer to [this](https://stackoverflow.com/questions/11277432/how-to-remove-a-key-from-a-python-dictionary).)

Redirect
======================================

`lib.deprecated_pylons_abort_and_redirect` provides a handy shortcut to be compatible with Pylons `redirect`. However, `HTTPFound` and `HTTPNotFound` in Pyramid are `Response` as well as `HTTPException`, which means you can either return or raise them.

`lib.deprecated_pylons_abort_and_redirect` always _return_ an object to you, and it's up to you, the one who calls `redirect`, to decide whether to return or raise it.

### When to return

Return them in **action methods**, where you need to return a response anyway.
This is to avoid overwhelming the log, because to some degree they can be considered as legal responses here.

### When to raise

Raise them in **helper functions**, because they are _real exceptions_.
Raising `HTTPException` simply breaks the calling function(s), throws the exception until Pyramid handles it internally, namely returning it directly as a response.
Otherwise you'll need to do a type check using `isinstance` in each calling function(s) above in the call stack,
which is tedious, annoying and error-prone, and also reduces readability.

Specify a renderer
=======================================

In Pyramid, every action needs to return a `Response` object, unless it is explicitly associated with a renderer which can transform the returned value into a `Response` object.

While in Pylons, controller actions return strings. Those strings are the contents of the responses, and Pylons middlewares will wrap them into real `Response` objects. Please note `render('something.mako')` returns a string as well.

Nuances of returning JSON
--------------------------

As a result, when we want to return JSON:
```python
# In Pylons, it is:
def foo(self):
    return json.dumps({'1': None})

# In Pyramid, Option 1:
@action(renderer = 'string')
def foo1(self):
    return json.dumps({'1': None})

# Or Option 2:
@action(renderer = 'json')
def foo2(self):
    return {'1': None}
```

The two options in Pyramid return the same Response object. But there are some differences you should be aware of.

Let's have a look at this architecture:

1. **Action Method** returns an _object of any type_ to **Pyramid Middleware**
2. **Pyramid Middleware** will transform the received object into a _Response_ object, if the received object is not a _Response_ object.
3. **Pyramid Middleware** finally passes a _Response_ object to **Your Browser**.

Though the final _Response_ objects you get in **Your Browser** are the same in those 2 actions, what `foo1` and `foo2` directly return are different: `foo1` returns `str`, while `foo2` returns `dict` (Try testing it yourself!). Hence if other parts of the code want to call the action method, `foo1` and `foo2` provide different results, since we are still beneath **Pyramid Middleware**.

Thus `foo1` in Pyramid is more similar to the behaviour of `foo` in Pylons; both of them have `json.dumps` finalised inside the action method and give the middleware a string to wrap, while `foo2` returns a dictionary, and `json.dumps` is finalised in the middleware. This may explain why we use string renderer more often in our implementation.

### If you're still interested

Wait! What about the `action` decorator? It specifies a renderer! You can check that it actually doesn't change what the function returns. Then how does **Pyramid Middleware** kick in later? Remember functions in Python are objects as well! They are just _callable_ objects. So `@action` is merely a wrapper that doesn't change the `__call__` attribute, but it sets other attributes in the function object so that the renderer info can be picked up later in Pyramid Middleware (You can check `view_config` class in Pyramid's [source code](https://github.com/Pylons/pyramid/blob/master/pyramid/view.py); note `venusian.attach` in it).



Database Connection
=====================

Wrapper Class for later initialisation
---------------------------------------

The database connection objects for both PostgreSQL and Redis are instantiated at the initial importing phase,
which means the objects would have been initialised before `config` info is retrieved. To defer the actual initialisation, wrapper classes are used.
```python
class WrapperClassWithLazyInit(class_):
    def __init__(self):
        pass

    def lazy_init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
```

PostgreSQL
--------------------------------

The connection info for our PostgreSQL server is stored in the `ini` file you use with `pserve`.


Redis
--------------------------------

Redis connection info is retrieved from our PostgreSQL database. Note that there are two interfaces for Redis data retrieval.

1) `redis_interface_normal` is for general data retrieval. Normal text data are utf-8-encoded Bytes in Redis, and this interface has `decode_responses` on.
2) `redis_interface_for_pickle` is for pickle info retrieval. Though pickle info is byte strings as well, it can't be utf-8-decoded. Hence this interface doesn't decode responses and returns bytes.

### What happened in Python 2?

Python 2 uses Bytes as its default string type, while Python 3 uses Unicode. Hence, Redis returning Bytes is fine and straightforward in Python 2, while it should be taken good care of in Python 3.

Except for pickle data, the reason that Bytes should be decoded into Unicode immediately is according to [Unicode HOWTO](https://docs.python.org/3/howto/unicode.html#tips-for-writing-unicode-aware-programs):

> Software should only work with Unicode strings internally, decoding the input data as soon as possible and encoding the output only at the end.

You might want to google more about the string differences in Python 2 and 3.

Python2 vs Python3
=====================
Although the most tricky python2 vs python3 bugs (e.g. string vs unicode) were mentioned above. There are also other minor differences that can cause a page to crash
for example, dict.itervalues.next() is a one that's being used quite often, it needs to be replaced with next(iter(dict.values))
Those bugs should be quite easy to fix, with some research on the differences and alternatives.

Export PDF (STILL NEED TO BE FIXED)
======================================

In the pylons code, a tool called "prince" is used to convert the svg format graphs to PDF for the users to download. As of now, prince produces serveral major visual errors when converting svg with our pyramid server.
The alternative is using rsvg-convert(librsvg), however it still produces other minor visual errors, e.g. the error occurs when exporting yugene graphs. This still needs to be investigated further.