# -*- coding: utf-8 -*-

import mimetypes

from flask import url_for, redirect, jsonify, request, render_template

__author__ = 'sobolevn'


class BaseProducer(object):
    content_type = None
    swagger = None

    def __init__(self, swagger):
        self.swagger = swagger

    def _create_view_function(self, ext):
        def _inner(*args, **kwargs):
            return self.get(*args, **kwargs)

        _inner.__name__ = ext
        return _inner

    def create_endpoint(self):
        content_type = self.__class__.content_type
        ext = mimetypes.guess_extension(content_type).replace('.', '')

        main_view_path = '/' + ext
        self.swagger.blueprint.add_url_rule(
            main_view_path, view_func=self._create_view_function(ext),
        )

    def get(self, *args, **kwargs):
        raise NotImplemented


class HtmlProducer(BaseProducer):
    content_type = 'text/html'

    def get(self, *args, **kwargs):
        if request.method == 'GET':
            json_url = request.args.get('url', None)
            if not json_url:
                json_url = url_for('SwaggerDocs.json', _external=True)
                return redirect('{}?url={}'.format(
                    request.url_rule.rule, json_url))
            else:
                return render_template('index.html')


class JsonResourceListingProducer(BaseProducer):
    content_type = 'application/json'

    def get(self, *args, **kwargs):
        meta = self.swagger.swagger_listing_meta.render(
            resources=self.swagger.resources, tags = self.swagger.tags)
        return jsonify(meta)


class JsonResourceProducer(BaseProducer):
    content_type = 'application/json'

    def create_endpoint(self):
        self.swagger.blueprint.add_url_rule(
            '/json/<string:resource>',
            view_func=self._create_view_function('resources'),
        )

    def get(self, *args, **kwargs):
        resource = kwargs.pop('resource')
        resource = self.swagger.resources[resource]
        meta = self.swagger.swagger_meta.render(
            resource=resource,
            models=self.swagger.models,
        )

        return jsonify(meta)
