Introduction
========================

[Stemformatics](https://www.stemformatics.org/) is an online portal that allows stem cell biologists to visually analyse and explore interesting datasets quickly and easily. It is a worldwide resource for collaborators in Australia, North America, Asia and Europe.

Stemformatics website was initially built in 2010 and needs modifications. Currently it is using the Python [Pylons](https://docs.pylonsproject.org/projects/pylons-webframework/en/latest/index.html) web framework and needs to be migrated to the Python [Pyramid](https://docs.pylonsproject.org/projects/pyramid/en/latest/) web framework.

This repo is the place where migration takes place. It is a Stemformatics website running in Pyramid.


Getting Started
===============

It is recommended to use a virtual environment of Python 3. According to [Quick Tour of Pyramid](https://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tour.html), this is an example to set up a virtual environment.

```bash
# set an environment variable to where you want your virtual environment
$ export VENV=~/env
# create the virtual environment
$ python3 -m venv $VENV
```

Then you can run the application by

```bash
$ cd directory/containing/this/file
# install required packages
$ $VENV/bin/pip install -e .
# run the application with development configuration
$ $VENV/bin/pserve development.ini
```

Migrating Memo
===================

Our migration tries to reach a balance point between "do it in pyramid's way" and "just make it Pylons compatible for the sake of workload." General migration strategies can be found [here](https://docs.pylonsproject.org/projects/pyramid-cookbook/en/latest/pylons/index.html). Some specific tips or tracks related to Stemformatics project are listed below.

DB info
-----------------
Database info is used in `config` to connect to the database.

```python
host = 'localhost'
dbname = 'portal_beta'
user = 'portaladmin'
```

Namely,
```python
config['psycopg2_conn_string'] = "host='localhost' dbname='portal_beta' user='portaladmin'"
```

Request, response, and session
--------------------------------
Pylons provides a global object of `request`, `response`, and `session` respectively via
```python
from pylons import request, response, session
```
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

A shortcut `magic_globals` object can be found in `lib.deprecated_pylons_globals`.

For more information, see [this page](https://docs.pylonsproject.org/projects/pyramid-cookbook/en/latest/pylons/request.html).

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

Redirect
------------------------
Pyramid officially recommends returning a redirect, i.e. a `HTTPFound` object that's a subclass of `Response`, instead of raising one. Raising `HTTPFound` just causes lots of Traceback in your log. Hence you can see `return` in `redirect` in `lib.deprecated_pylons_abort_and_redirect`.

As a result, though the `redirect` in `lib.deprecated_pytlons_abort_and_redirect` is a handy shortcut which avoids changing every `redirect` call, you should **remember to add a `return`** when there isn't one.
```python
# This doesn't work if HTTPFound is returned, but not raised,
# because the response object is discarded after this line.
redirect(some info)

# Remember to add a return
return redirect(some info)
```

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
choose an action renderer type
--------------------------------
In pyramid, every action needs to return a response, and the response needs to be associated with a renderer.
The renderer type needs to be explicitly specified, and this is different pylons.
In pylons, an action and just return a piece of String in JSON format without specify anything. 
In pyramid, returning anything with out specify a renderer type will result in an error.
Therefore, if the action returns a .mako page, the renderer will need to be pointing to the mako file. If the action returns some data,it's best to specify
the renderer type as "renderer='string'". (This is because our code does the formatting already, return them as string will keep the format as we processed)
