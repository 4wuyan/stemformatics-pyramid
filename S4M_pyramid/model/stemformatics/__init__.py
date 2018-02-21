#-------Last synchronised with Pylons repo (master) on---------------#
#-------------------------8 Feb 2018---------------------------------#
#-------------------------by WU Yan----------------------------------#

__doc__ = """\

Setting up class for stemformatics

"""

import logging

log = logging.getLogger(__name__)

from .stemformatics_dataset import Stemformatics_Dataset
from .stemformatics_expression import Stemformatics_Expression
from .stemformatics_gene import Stemformatics_Gene
from .stemformatics_audit import Stemformatics_Audit
from .stemformatics_auth import Stemformatics_Auth
from .stemformatics_admin import Stemformatics_Admin
from .stemformatics_probe import Stemformatics_Probe
from .stemformatics_gene_set import Stemformatics_Gene_Set
from .stemformatics_notification import Stemformatics_Notification
from .stemformatics_help import Stemformatics_Help
from .stemformatics_job import Stemformatics_Job
from .stemformatics_export import Stemformatics_Export
from .stemformatics_shared_resource import Stemformatics_Shared_Resource
from .stemformatics_msc_signature import Stemformatics_Msc_Signature
from .stemformatics_ensembl_upgrade import Stemformatics_Ensembl_Upgrade
# from .stemformatics_export import *
# from .stemformatics_msc_signature import *
# from .stemformatics_transcript import *
# from .stemformatics_job import *
# from .stemformatics_shared_resource import *
# from .stemformatics_ensembl_upgrade import *

import zlib
import json

import sqlsoup

from S4M_pyramid.lib.helpers import make_lazy_init_wrapper_class
'''
    This wrapper is designed to defer the initialisation of the SQLSoup instance.
    I couldn't find another way to setup an "empty" SQLSoup instance,
    and bind the db connection later after we get the db configuration info (i.e. in main function).

    I need to defer the initialisation, because this file will be executed during the initial
    importing phase, before the main function of the application is run.
    That means you don't have the db url when db is initialised, and an exception is raised.

    In Pyramid's tutorial, they don't use sqlsoup; that's why they can have an idle
    DBSession initialised here, then bind it to the url fetched from ini later in main.
'''
SQLSoupWrapper = make_lazy_init_wrapper_class(sqlsoup.SQLSoup)

db_deprecated_pylons_orm = SQLSoupWrapper()



