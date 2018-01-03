__doc__ = """\

Setting up class for stemformatics

"""

import logging

log = logging.getLogger(__name__)

from sqlalchemy import *
from sqlalchemy.ext.sqlsoup import SqlSoup


from stemformatics_dataset import *

import zlib
import json

__all__ = [
    # From this module ...
    'db', 'engine', 'init_model',

    # From imported modules ...
    'Stemformatics_Dataset',
    'Stemformatics_Audit',
    'Stemformatics_Gene',
    'Stemformatics_Transcript',
    'Stemformatics_Expression',
    'Stemformatics_Probe',
    'Stemformatics_Admin',
    'Stemformatics_Auth',
    'Stemformatics_Export',
    'Stemformatics_Job',
    'Stemformatics_Shared_Resource',
    'Stemformatics_Ensembl_Upgrade',
    'Stemformatics_Notification',
    'Stemformatics_Msc_Signature',
    'Stemformatics_Gene_Set',
    'Stemformatics_Help'
]

db = None
engine = None


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def init_model(db_engine):
    global db, engine

    engine = db_engine

    log.debug('just setting up sqlsoup')

    db = SqlSoup(engine, use_labels=True)

    log.debug('just finished setting up sqlsoup')


