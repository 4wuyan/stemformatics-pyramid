import S4M_pyramid.lib.deprecated_pylons_app_globals as app_globals
from S4M_pyramid.config import config
def load_environment():
    config["deprecated_pylons_app_globals"] = app_globals.Globals()
    config["deprecated_pylons_orm"] = app_globals.db_deprecated_pylons_orm
