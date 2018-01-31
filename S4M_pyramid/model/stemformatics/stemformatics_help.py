# TODO-1
import logging

log = logging.getLogger(__name__)

import sqlalchemy as SA
from sqlalchemy import or_, and_, desc

from S4M_pyramid.model import r_server

import re
import string
import json
import urllib

import os
import shutil
import zipfile
from S4M_pyramid.lib.deprecated_pylons_globals import config
__all__ = ['Stemformatics_Help']


class Stemformatics_Help(object):
    all_pages_key = "help|pages|all"
    all_tutorials_key = "help|tutorials|all"
    all_page_guides_key = "help|page_guides|all"

    @staticmethod
    def get_tutorial_key(tutorial):
        return "help|tutorials|%s" % (tutorial,)

    @staticmethod
    def get_tutorial_start_key(tutorial):
        return "help|tutorials|%s|start" % (tutorial,)

    @staticmethod
    def get_tutorial_page_key(tutorial, page):
        return "help|tutorials|%s|%s" % (tutorial, page)

    @staticmethod
    def get_page_key(page):
        return "help|pages|%s" % (page,)

    @staticmethod
    def get_page_guide_key(page):
        return "help|page_guides|%s" % (page,)

    @staticmethod
    def get_helptype_from_key(key):
        helptype = key.split('|')[1]
        if helptype == "tutorials":
            return "tutorial"
        elif helptype == "page_guides":
            return "page_guide"
        else:
            return None

    @staticmethod
    def get_helpname_from_key(key):
        return key.split('|')[2]

    @staticmethod
    def get_page_details_from_key(page_key):
        page_info = page_key.split('|')[-1].split("?")
        page_query = {}
        page_query["path"] = page_info[0]
        if len(page_info) != 1:
            for query in page_info[1].split("&"):
                query = query.split("=")
                if len(query) == 2:
                    page_query[query[0]] = query[1]
                else:
                    page_query[query[0]] = "-"
        return page_query

    @staticmethod
    def get_help_for_page(actual_page, request_params):

        page_keys = Stemformatics_Help.get_all_page_keys()

        page_keys_matched = []  # will be a list of tuples
        for page_key in page_keys:
            key_matched = Stemformatics_Help.key_matched(page_key, actual_page, request_params)
            if key_matched is not None:
                page_keys_matched.append(key_matched)
        # convert to dict
        page_keys_matched = dict(page_keys_matched)
        # finally grab and return the help for the best matched page
        final_page_data = {}
        if page_keys_matched:
            sorted_keys = sorted(page_keys_matched, key=page_keys_matched.get, reverse=True)
            final_page_data = Stemformatics_Help.get_all_help_from_page_key(sorted_keys[0])
            if final_page_data[
                'page_guide'] is None:  # check if page contains page guide, and if it doesn't iterate over other
                for page_key in sorted_keys:
                    page_data = Stemformatics_Help.get_all_help_from_page_key(page_key)
                    if page_data['page_guide'] is None:
                        continue
                    else:
                        final_page_data['page_guide'] = page_data['page_guide']
                        break

        return final_page_data

    @staticmethod
    def key_matched(page_key, actual_page, request_params):
        ''' this is a helper function for help controller '''

        page_details = Stemformatics_Help.get_page_details_from_key(page_key)
        path = page_details['path']
        del page_details['path']

        if path == actual_page:
            matched = 100
            if len(page_details) - 1 <= len(request_params):
                # if reached there are multiple details in the request, but only if retrieved page doesn't have more than the request.
                # retrieved pages therefore can't be more specific than the request

                # now iterate over requests details to calculate how good a match the retreived page is.
                # this will always run at least once as both will always include a 'path' detail
                for param, value in page_details.iteritems():
                    request_value = request_params.get(param, None)

                    # if detail is not in request, key fails as match
                    if request_value is None:
                        return None

                    # if detail is good there are 2 options
                    # one is if value is an exact match, the other is when detail was present but contained no value.
                    # the numbering of 100 and 101 is so an exact match is given a slightly higher preference.
                    if value == request_value:
                        matched += 101
                    elif value == "-":
                        matched += 100
                    else:
                        return None

                return (page_key, matched)

        return None

    @staticmethod
    def help_exists(help):
        has_tute = r_server.exists(Stemformatics_Help.get_tutorial_key(help))
        has_guide = r_server.exists(Stemformatics_Help.get_page_guide_key(help))
        return has_tute or has_guide

    @staticmethod
    def check_remove_page(r_server, page_key):
        # This removes a page key from the list of all pages if it no longer exists.
        if not r_server.exists(page_key):
            r_server.srem(Stemformatics_Help.all_pages_key, page_key)

    @staticmethod
    def get_all_help_from_page_key(page_key):

        pageguide_key = Stemformatics_Help.get_page_guide_key(page_key.split('|')[2])

        help_keys = r_server.smembers(page_key)

        page_data = {
            "tutorials": {},
            "page_guide": None
        }

        for help_key in help_keys:
            helptype = Stemformatics_Help.get_helptype_from_key(help_key)
            if helptype == "tutorial":
                page_data["tutorials"][help_key.split('|')[2]] = json.loads(r_server.get(help_key))
            elif helptype == "page_guide":
                page_data["page_guide"] = json.loads(r_server.get(help_key))

        return page_data

    @staticmethod
    def get_all_tutorial_keys():
        return list(r_server.smembers(Stemformatics_Help.all_tutorials_key))

    @staticmethod
    def get_all_pageguide_keys():
        return list(r_server.smembers(Stemformatics_Help.all_page_guides_key))

    @staticmethod
    def get_all_page_keys():
        return list(r_server.smembers(Stemformatics_Help.all_pages_key))

    @staticmethod
    def get_tutorial_list():
        tutorial_keys = Stemformatics_Help.get_all_tutorial_keys()
        tutorial_list = {}
        for tutorial_key in tutorial_keys:
            tutorial = tutorial_key.split('|')[2]
            tutorial_list[tutorial] = Stemformatics_Help.get_tutorial_start_page(tutorial)
        return tutorial_list

    @staticmethod
    def get_pageguide_list():
        page_guide_keys = Stemformatics_Help.get_all_pageguide_keys()
        page_guide_list = []
        for page_guide_key in page_guide_keys:
            page_guide_list.append(page_guide_key.split('|')[2])
        return page_guide_list

    @staticmethod
    def get_all_help_list():
        return {
            'tutorials': Stemformatics_Help.get_tutorial_list().keys(),
            'page_guides': Stemformatics_Help.get_pageguide_list()
        }

    @staticmethod
    def delete_all_help():
        help_list = Stemformatics_Help.get_all_help_list()

        for tutorial_name in help_list["tutorials"]:
            Stemformatics_Help.delete_tutorial(tutorial_name)

        for page_name in help_list["page_guides"]:
            Stemformatics_Help.delete_pageguide(page_name)

    @staticmethod
    def get_tutorial(tutorial):
        tutorial_key = Stemformatics_Help.get_tutorial_key(tutorial)
        tutorial_pages = r_server.smembers(tutorial_key)
        tutorial_start_page = r_server.get(Stemformatics_Help.get_tutorial_start_key(tutorial))
        tutorial_data = {"name": tutorial, "start_page": tutorial_start_page, "data": {}}
        for tutorial_page_key in tutorial_pages:
            page = tutorial_page_key.split('|')[-1]
            data = r_server.get(tutorial_page_key)
            tutorial_data["data"][page] = json.loads(data)
        return tutorial_data

    @staticmethod
    def save_tutorial(tutorial, start_page, json_data):
        tutorial_key = Stemformatics_Help.get_tutorial_key(tutorial)
        tutorial_start_key = Stemformatics_Help.get_tutorial_start_key(tutorial)

        r_server.sadd(Stemformatics_Help.all_tutorials_key, tutorial_key)

        if not isinstance(json_data, dict):
            json_data = json.loads(json_data)

        for page_name, page_data in json_data.iteritems():
            tutorial_page_key = Stemformatics_Help.get_tutorial_page_key(tutorial, page_name)
            page_key = Stemformatics_Help.get_page_key(page_name)

            r_server.set(tutorial_page_key, json.dumps(page_data))
            r_server.set(tutorial_start_key, start_page)
            r_server.sadd(tutorial_key, tutorial_page_key)
            r_server.sadd(page_key, tutorial_page_key)
            r_server.sadd(Stemformatics_Help.all_pages_key, page_key)

    @staticmethod
    def delete_tutorial(tutorial):

        tutorial_key = Stemformatics_Help.get_tutorial_key(tutorial)
        tutorial_start_key = Stemformatics_Help.get_tutorial_start_key(tutorial)
        tutorial_pages = r_server.smembers(tutorial_key)

        # Remove all tutorial pages from their associated page set
        for tutorial_page_key in tutorial_pages:
            page_key = Stemformatics_Help.get_page_key(tutorial_page_key.split('|')[-1])
            r_server.srem(page_key, tutorial_page_key)
            Stemformatics_Help.check_remove_page(r_server, page_key)

        # Delete tutorial start page data
        r_server.delete(tutorial_start_key)
        # Delete all tutorial page data
        if len(tutorial_pages) > 0:  # incase someone creates an empty tutorial
            r_server.delete(*tutorial_pages)
        # Delete tutorial
        r_server.delete(tutorial_key)
        # Remove tutorial from tutorial set
        r_server.srem(Stemformatics_Help.all_tutorials_key, tutorial_key)

    @staticmethod
    def get_tutorial_start_page(tutorial):
        tutorial_start_key = Stemformatics_Help.get_tutorial_start_key(tutorial)
        return r_server.get(tutorial_start_key)

    @staticmethod
    def get_pageguide(page):
        page_guide_key = Stemformatics_Help.get_page_guide_key(page)
        data = r_server.get(page_guide_key)
        return json.loads(data)

    @staticmethod
    def save_pageguide(page, json_data):

        page_guide_key = Stemformatics_Help.get_page_guide_key(page)
        page_key = Stemformatics_Help.get_page_key(page)

        if isinstance(json_data, list):
            json_data = json.dumps(json_data)

        r_server.set(page_guide_key, json_data)
        r_server.sadd(Stemformatics_Help.all_page_guides_key, page_guide_key)
        r_server.sadd(page_key, page_guide_key)
        r_server.sadd(Stemformatics_Help.all_pages_key, page_key)

    @staticmethod
    def delete_pageguide(page):

        page_guide_key = Stemformatics_Help.get_page_guide_key(page)
        page_key = Stemformatics_Help.get_page_key(page)

        # Delete all page guide data
        r_server.delete(page_guide_key)
        # Remove page guide from page guides set
        r_server.srem(Stemformatics_Help.all_page_guides_key, page_guide_key)
        # Remove page guide from their associated page set
        r_server.srem(page_key, page_guide_key)

        Stemformatics_Help.check_remove_page(r_server, page_key)

    @staticmethod
    def get_all_tutorials():
        tutorial_keys = Stemformatics_Help.get_all_tutorial_keys();
        tutorials = {}
        for tutorial_key in tutorial_keys:
            tutename = Stemformatics_Help.get_helpname_from_key(tutorial_key)
            tutorials[tutename] = Stemformatics_Help.get_tutorial(tutename)
        return tutorials

    @staticmethod
    def get_all_pageguides():
        pageguide_keys = Stemformatics_Help.get_all_pageguide_keys();
        pageguides = {}
        for pageguide_key in pageguide_keys:
            pageguide_name = Stemformatics_Help.get_helpname_from_key(pageguide_key)
            pageguides[pageguide_name] = Stemformatics_Help.get_pageguide(pageguide_name)
        return pageguides

    @staticmethod
    def get_help_dump(self):
        base_path = config['s4m_help_base_path']
        helpfiles_path = base_path + "/helpfiles"
        tutorials_path = base_path + "/helpfiles/tutorials"
        pageguides_path = base_path + "/helpfiles/pageguides"
        help_dump_path = base_path + "/help_dump"

        if os.path.exists(base_path):
            shutil.rmtree(base_path)

        os.makedirs(tutorials_path)
        os.makedirs(pageguides_path)

        tutorials = Stemformatics_Help.get_all_tutorials()
        pageguides = Stemformatics_Help.get_all_pageguides()

        for tutorial, json_data in tutorials.iteritems():
            with open(os.path.join(tutorials_path, tutorial + ".json"), "w") as helpfile:
                helpfile.write(json.dumps(json_data))

        for pageguide, json_data in pageguides.iteritems():
            save_data = {
                "page": pageguide,
                "data": json_data
            }
            with open(os.path.join(pageguides_path, urllib.quote(pageguide, "") + ".json"), "w") as helpfile:
                helpfile.write(json.dumps(save_data))

        return shutil.make_archive(help_dump_path, 'zip', helpfiles_path)

    @staticmethod
    def save_help_dump(self, upload_file):
        base_path = config['s4m_help_base_path']
        dump_dir = base_path + "/uploads"
        dump_tutes_dir = base_path + "/uploads/tutorials"
        dump_guides_dir = base_path + "/uploads/pageguides"
        dump_file_path = base_path + "/uploads/help_upload.zip"

        if os.path.exists(base_path):
            shutil.rmtree(base_path)

        os.makedirs(dump_dir)

        dump_file = open(dump_file_path, 'wb')
        shutil.copyfileobj(upload_file.file, dump_file)
        upload_file.file.close()
        dump_file.close()

        dump_zip = zipfile.ZipFile(dump_file_path)
        dump_zip.extractall(dump_dir)

        if os.path.exists(dump_tutes_dir):
            for tute_file_name in os.listdir(dump_tutes_dir):
                with open(os.path.join(dump_tutes_dir, tute_file_name), "r") as tute_file:
                    tutorial = json.loads(tute_file.read())
                    Stemformatics_Help.save_tutorial(tutorial["name"], tutorial["start_page"], tutorial["data"])

        if os.path.exists(dump_guides_dir):
            for guides_file_name in os.listdir(dump_guides_dir):
                with open(os.path.join(dump_guides_dir, guides_file_name), "r") as guide_file:
                    page_guide = json.loads(guide_file.read())
                    Stemformatics_Help.save_pageguide(page_guide["page"], page_guide["data"])



