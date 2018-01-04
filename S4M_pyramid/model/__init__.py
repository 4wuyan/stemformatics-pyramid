"""The application's model objects"""

# enable use of guide specific python modules outside pylons
import os, sys
import sqlalchemy as sa


from S4M_pyramid.model import stemformatics

# This doesn't need to (nor should it) used polled connections.
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def init_model():
    """
    Note that this init_model expects to be passed the app_conf part of config
    from which it will pass along config info to the constituent modules.
    If other, more global config is required, import config from pylons.
    """
    engine=create_engine('postgresql://portaladmin@localhost/portal_beta')
    stemformatics.init_model(engine)

