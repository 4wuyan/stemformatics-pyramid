"""The application's model objects"""

# enable use of guide specific python modules outside pylons
import os, sys

from S4M_pyramid.model import stemformatics



# ------------------------------------------------------------------------------
# In pylons,this is used to setup the db variable for ORM use, we do the setup
# at the controller level to make the code more readable in pyramid,therefore this
# method is deprecated
# ------------------------------------------------------------------------------
def init_model():
    pass