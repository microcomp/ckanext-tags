
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
import json
import os
import logging

import ckan.logic
import ckan.model as model
from ckan.common import _, c


class TagsPlugin(plugins.SingletonPlugin):
    pass