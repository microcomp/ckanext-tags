
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
import json
import os
import logging
import tags

import ckan.logic
import ckan.model as model
from ckan.common import _, c
controller = 'ckanext.tags.tags:TagsController'

class TagsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITemplateHelpers, inherit=False)
    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')

    def before_map(self, map):
        map.connect('admin_list', '/admin/tags', action='admin_list', controller=controller)
        map.connect('add_new', '/tags/new', action='add_new', controller=controller)
        map.connect('accept', '/tags/accept', action='accept', controller=controller)
        map.connect('decline', '/tags/decline', action='decline', controller=controller)
        return map
    def get_helpers(self):
    	return{'dts_n': tags.dtsn  }