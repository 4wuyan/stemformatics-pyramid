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
# from .stemformatics_export import *
# from .stemformatics_msc_signature import *
# from .stemformatics_transcript import *
# from .stemformatics_job import *
# from .stemformatics_shared_resource import *
# from .stemformatics_ensembl_upgrade import *

import zlib
import json

import sqlsoup
class _sqlsoup_wrapper(sqlsoup.SQLSoup):
    def __init__(self):
        pass

    def lazy_init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

db_deprecated_pylons_orm = _sqlsoup_wrapper()



