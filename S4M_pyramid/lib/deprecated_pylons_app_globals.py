"""The application's Globals object"""
import logging

log = logging.getLogger(__name__)

from S4M_pyramid.model.stemformatics.stemformatics_expression import Stemformatics_Expression
from sqlalchemy import create_engine
import sqlsoup
from S4M_pyramid.config import config

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization (ie. at server start-up) and is available during requests via the
        'app_globals' variable.

        In the controller, use:
        	from pylons import app_globals
        	print app_globals.someAttribute

		Note that this global variable is instantiated when server starts, and is shared amongst
		all connections to the server. Hence if a user changes such a variable from one browser,
		another will see that change from another browser.
        """

        # the file is created by calling http://<base url>/expressions/setup_all_sample_metadata
        # it also sets up the g. in memory as well
        self.all_sample_metadata = Stemformatics_Expression.setup_all_sample_metadata()

        # The script portal-admin in stemformatics/scripts/sysadmin and stemformatics/sysadmin scripts
        # that runs a sql statement that downloads the gene_mappings.raw and the probe_mappings.raw
        # This task uses the gene_mappings.raw to manufacture the in memory list for quick access.
        # Get the probe mappings and gene mappings setup for bulk import manager


        """
        This is the only place I could find that runs purely on startup once.
        config is updated inside the function.
        """
        #Stemformatics_Admin.trigger_update_configs()

#setup the orm variable
engine = create_engine(config['orm_conn_string'])
db_deprecated_pylons_orm = sqlsoup.SQLSoup(engine)
