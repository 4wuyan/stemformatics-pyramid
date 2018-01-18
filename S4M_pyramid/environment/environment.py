import S4M_pyramid.lib.app_globals as app_globals
from S4M_pyramid.config import config
def load_environment():
    config["app_global"] = app_globals.Globals()
