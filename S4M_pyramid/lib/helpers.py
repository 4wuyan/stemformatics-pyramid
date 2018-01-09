"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
# Import helpers as desired, or define your own, ie:
from webhelpers2.html import escape, HTML, literal, url_escape
from webhelpers2.html.tags import *
import paginate
from routes import url_for

from S4M_pyramid.lib.deprecated_pylons_globals import url

from S4M_pyramid.lib.stemformatics_helper import print_paginate,setup_accession_ids_for_viewing,get_citations,get_citations_part,setup_email_to_contributing_author,create_letter_for_annotator,web_asset_url,external_dependency_url
