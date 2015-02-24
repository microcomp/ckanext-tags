import urllib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
import datetime
import ckan.model as model
import ckan.logic as logic
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.lib.navl.dictization_functions as df
import ckan.plugins as p
from ckan.common import _, c
import ckan.plugins.toolkit as toolkit
import urllib2
import logging
import ckan.logic
import __builtin__
import db

import json
def dataset_name(id):
    context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'auth_user_obj': c.userobj,
                   'for_view': True}

    dataset_name = model.Session.query(model.Package).filter(model.Package.id == id).first().title
    return dataset_name
def create_related_tags_table(context):
    if db.related_tags_table is None:
        db.init_db(context['model'])

@ckan.logic.side_effect_free
def new_related_tag(context, data_dict):
    create_related_tags_table(context)
    info = db.RelatedTags()
    info.dataset_id = data_dict.get('dataset_id')
    info.id = unicode(uuid.uuid4())
    info.status = 'waiting'
    info.tag = data_dict.get('tag')

    data_dict2 = {'tag': info.tag, 'dataset_id': info.dataset_id}
    checking = len(db.RelatedTags.get(**data_dict2)) == 0
    if checking:
        info.save()
        session = context['session']
        session.add(info)
        session.commit()
        return {"status":"success"}
    return {"status":"fail"}

@ckan.logic.side_effect_free
def admin_list_tags(context, data_dict):
    create_related_tags_table(context)
    result = db.RelatedTags.getALL(**data_dict)
    return result

@ckan.logic.side_effect_free
def accept_tag(context, data_dict):
    create_related_tags_table(context)
    info = db.RelatedTags.get(**data_dict)[0]
    info.status = 'accepted'


    rev = ckan.model.repo.new_revision()

    session = context['session']
    dataset_name = model.Session.query(model.Package).filter(model.Package.id== info.dataset_id).first().name
    package = ckan.model.Package.get(dataset_name)
    package.add_tags([ckan.model.Tag(info.tag)])

    info.save()
    
    session.commit()

    return {"status":"success"}
    
@ckan.logic.side_effect_free
def decline_tag(context, data_dict):
    create_related_tags_table(context)
    info = db.RelatedTags.get(**data_dict)[0]
    info.status = 'declined'
    info.save()
    session = context['session']
    session.commit()
    return {"status":"success"}

class TagsController(base.BaseController):
    def admin_list(self):
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'auth_user_obj': c.userobj,
                   'for_view': True}
        try:
            logic.check_access('tags_admin', context)
        except logic.NotAuthorized:
            base.abort(401, base._('Not authorized to see this page'))
        data_dict = {}

        status = base.request.params.get('type','waiting')

        tags = admin_list_tags(context, data_dict)
        lng = len(tags)
        if len(status) > 0:
        	if status not in ['waiting', 'accepted', 'declined']:
        		base.abort(400, (_('wrong filter type')))
        	tags = [x for x in tags if x.status == status]
        try:
            page = int(base.request.params.get('page', 1))
        except ValueError:
            base.abort(400, ('"page" parameter must be an integer'))

        c.fulltext = base.request.params.get('search','')
        tags = [x for x in tags if c.fulltext in x.tag ]
        c.page = page
        c.page_num = len(tags) // 10 +1
        c.pages =  [x for x in range(page-3, page+3) if x > 0 and x <= c.page_num]
        tags = tags[(page-1)*10:page*10]
        c.content = {'tags':tags, 'filter': status, 'page': page, 'total': lng}
        return base.render('admin/tag_admin.html')


    def add_new(self):
    	context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'auth_user_obj': c.userobj,
                   'for_view': True}

        data = logic.clean_dict(df.unflatten(logic.tuplize_dict(logic.parse_params(base.request.params))))

        tags = list(set(data['tag'].split(', ')))
        

        if c.userobj:
        	for i in tags:
        		data_dict = {'tag': i, 'status': 'waiting', 'dataset_id': data['dataset_id']}
        		new_related_tag(context, data_dict)
        else:
        	base.abort(401, base._('Not authorized'))

        return h.redirect_to(controller="package", action="read", id=data['dataset_id'])

    def accept(self):
    	context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'auth_user_obj': c.userobj,
                   'for_view': True}
        data_dict = {'id': base.request.params.get('id', '')}
        try:
            logic.check_access('tags_admin', context)
        except logic.NotAuthorized:
            base.abort(401, base._('Not authorized to see this page'))

        accept_tag(context, data_dict)
        return h.redirect_to(controller = 'ckanext.tags.tags:TagsController', action='admin_list')
    def decline(self):
    	context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'auth_user_obj': c.userobj,
                   'for_view': True}
        data_dict = {'id': base.request.params.get('id', '')}
        try:
            logic.check_access('tags_admin', context)
        except logic.NotAuthorized:
            base.abort(401, base._('Not authorized to see this page'))

        decline_tag(context, data_dict)
        return h.redirect_to(controller = 'ckanext.tags.tags:TagsController', action='admin_list')