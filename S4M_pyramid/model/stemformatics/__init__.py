__doc__ = """\

Setting up class for stemformatics

"""

import logging

log = logging.getLogger(__name__)

import zlib
import json

# we are trying to avoid using "import *" in the new pyramid code,
# therefore __all__ might also need to be avoided
#__all__ = [

    # From imported modules ...
    #'Stemformatics_Dataset',
    #'Stemformatics_Audit',
    #'Stemformatics_Gene',
    #'Stemformatics_Transcript',
    #'Stemformatics_Expression',
    #'Stemformatics_Probe',
    #'Stemformatics_Admin',
    #'Stemformatics_Auth',
    #'Stemformatics_Export',
    #'Stemformatics_Job',
    #'Stemformatics_Shared_Resource',
    #'Stemformatics_Ensembl_Upgrade',
    #'Stemformatics_Notification',
    #'Stemformatics_Msc_Signature',
    #'Stemformatics_Gene_Set',
    #'Stemformatics_Help'
#]


# ------------------------------------------------------------------------------
# In pylons,this is used to setup the db variable for ORM use, we do the setup
# at the controller level to make the code more readable in pyramid,therefore this
# method is deprecated
# ------------------------------------------------------------------------------

#db = None
#engine = None

def init_model(db_engine):
    pass


