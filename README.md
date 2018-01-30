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

Choose an action renderer type
=======================================

In Pyramid, every action needs to return a response, and the response needs to be associated with a renderer.
The renderer type needs to be explicitly specified, and this is different in Pylons.
In Pylons, an action can just return a piece of String in JSON format without specifying anything.
In Pyramid, returning anything without specifying a renderer type will result in an error.
Therefore, if an action returns a `mako` page, the renderer should point to a `mako` file. If an action returns some data, it's best to specify
the renderer type as `renderer='string'`. (This is because our code does the formatting already; returning them as a string will keep the format as we process.)

String encode and decode
=======================================
Python2 and Python3 have different format for strings(Unicode vs bytes). In our redis configuration, The data stored in redis is in byte format 
so in pylons server(python2), there is no encode/decode needed. But this is a issue for pyramid server, as we need to encode the string when pass data
into redis and decode string when getting data from redis. 

Atm we are doing this encode/decode process manually inside the code. Another options would be to change the redis configuration to suit python3's requirement.
But because the migration process didn't finish and if we change the configuration for redis our pylons server will break. Therefore we have to settle for this 
more complicated solution so that both servers are compatible.


Database ORM
=====================

We still use an `SQLSoup` object as the representation of the database in `model/stemformatics`.

However, a simple `SQLSoup` wrapper is designed to defer the initialisation of `SQLSoup`. I couldn't find another way to setup an "empty" `SQLSoup` instance, and bind the db connection later after we get the db configuration info (i.e. in the `main` function).
```python
class _SQLSoupWrapper(sqlsoup.SQLSoup):
    def __init__(self):
        pass

    def lazy_init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
```

We need to defer the _actual_ initialisation where the db connection is made, because the instantiation happens during the initial importing phase, **before** the `main` function of the application is run. That means you don't have the db url when db is initialised, and an exception is raised.

Defending the wrapper design
---------------

### Why does Pyramid's tutorial not use a wrapper

Pyramid's tutorial doesn't use `sqlsoup`; that's why they can have an idle `DBSession`, then bind it to the url fetched from `ini` later in the `main` function.

### Why not stick with our original design in Pylons

In our Pylons code, we made `db = None` first, then called a function that uses global variables to modify `db`.
```python
db = None

def init_model(db_engine):
    global db
    db = blah blah....
```
The main disadvantages of this design are:

* You __must__ make sure that you have called `init_model` absolutely before any other parts of the application that import `db`. This is very error-prone, especially when there are so many complicated dependencies of import on the top of your file. "Pain in the ass."
* It reduces the readability. People who want to import a `NoneType` `db` will easily get confused by that the `db` imported is not `None` as stated in the source code, if they are unaware of the `init_model` executed before.

The first thing you need to do in Pyramid if you adopt that design, is to put those `import SomeController` lines from the top of the file into the `main` function. Otherwise you will receive a `NoneType` error arising from `db`, because `BaseController` has imported a `db` of `NoneType` way ahead of `init_model`.
