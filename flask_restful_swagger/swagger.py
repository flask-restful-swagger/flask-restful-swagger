# -*- coding: utf-8 -*-

from __future__ import absolute_import

import importlib
import os
from collections import OrderedDict

import six
from flask import Blueprint
from flask_restful import Api
from flask_restful_swagger import swagger_definitions
from flask_restful_swagger.producers import (
    JsonResourceListingProducer,
    JsonResourceProducer,
    HtmlProducer,
    BaseProducer,
)

__author__ = 'sobolevn'

DEFAULTS_META_VALUES = {
}
DEFAULTS_LISTING_META_VALUES = {
    'swaggerVersion': '1.2',
}


class SwaggerDocs(object):
    _known_producers = [
        JsonResourceListingProducer,
        JsonResourceProducer,
        HtmlProducer,
    ]

    def _import_required_version(self, version):
        """
        This method is used to dynamically import the required swagger
        api version. It loads modules based on version number from
        the `swagger_definitions` package.
        It sets `self.definitions` to the appropriate module.
        :param version: version to be loaded, eg: 1.2
        :return: None
        """
        try:
            version_name = 'v' + version.replace('.', '_')
            import_path = '{}.{}'.format(
                swagger_definitions.__name__, version_name)
            self.definitions = importlib.import_module(
                import_path
            )
        except ImportError as e:
            raise ValueError('No such swagger version: ' + version)

    @staticmethod
    def _set_default_values(values, defaults_values):
        for k, v in six.iteritems(defaults_values):
            values.setdefault(k, v)

    def __init__(self, api, swagger_meta=None, swagger_listing_meta=None,
                 api_spec_url='/api/spec', template_folder=None,
                 static_folder=None, static_url_path=None):
        if not isinstance(api, Api):
            raise ValueError(
                "Provided `api` object is not flask-restful's Api")

        self.api = api
        self.swagger_meta = swagger_meta
        self._set_default_values(self.swagger_meta, DEFAULTS_META_VALUES)
        self.swagger_listing_meta = swagger_listing_meta
        self._set_default_values(self.swagger_listing_meta, DEFAULTS_LISTING_META_VALUES)

        self.definitions = None
        # This will set `self.definitions` to the appropriate module:
        swagger_version = swagger_listing_meta.pop('swagger', None)
        if swagger_version:
            swagger_listing_meta.pop('swaggerVersion', None)
        else:
            swagger_version = swagger_listing_meta.pop('swaggerVersion', None)
        self._import_required_version(swagger_version)
        self.swagger_meta = self.definitions.SwaggerMeta()
        self.swagger_listing_meta = self.definitions.SwaggerListingMeta(
            self.swagger_listing_meta
        )

        self._detect_producers(self.swagger_meta)

        self.operations = []
        self.models = []
        self.resources = {}
        self.tags = OrderedDict()

        self.api_spec_url = api_spec_url
        self.static_url_path = static_url_path or ''
        self.static_folder = static_folder
        dir_name = os.path.dirname(__file__)

        self.template_folder = template_folder
        if self.template_folder is None:
            # There's not separation between static folder and templates
            # folder, just because swagger-ui is made that way. But
            # Both of these folders are required for agile customisation.
            self.template_folder = os.path.join(
                dir_name, 'static', 'swagger-ui')

        if self.static_folder is None:
            self.static_folder = os.path.join(
                dir_name, 'static', 'swagger-ui')

        self.app = api.app
        self.blueprint = None

        if self.app:
            # noinspection PyTypeChecker
            self.init_app(self.app)

    def init_app(self, app_or_api=None):
        try:
            self.app = app_or_api.app  # we suppose, that this is Api
        except AttributeError:
            self.app = app_or_api  # it was just app
            self.api.init_app(self.app)

        self.blueprint = Blueprint(
            self.__class__.__name__,
            self.__class__.__name__,
            url_prefix=self.api_spec_url,
            static_folder=self.static_folder,
            template_folder=self.template_folder,
            static_url_path=self.static_url_path,
        )

        # TODO: move url creation inside the producers!
        for producer_class in self.produces:
            producer_class(self).create_endpoint()

        self.app.register_blueprint(self.blueprint)

    def add_resource(self, resource, url, **kwargs):
        # TODO: multiple url support?
        swagger_resource = self.definitions.SwaggerResource(resource, url=url)

        self.api.add_resource(resource, url, **kwargs)
        self.resources.update({resource.endpoint: swagger_resource})

    def add_tag(self, name, order, description, **kwargs):
        self.tags.update({order: self.definitions.SwaggerTag(name, order, description)})

    def resource(self, **kwargs):
        def _inner(resource_class):
            resource_class.swagger_attr = kwargs
            return resource_class

        return _inner

    def operation(self, *args, **kwargs):
        def _inner(func):
            operation = self.definitions.SwaggerOperation(*args, **kwargs)
            func.swagger_operation = operation
            func.operation = operation
            return func

        return _inner

    def model(self, func):
        return func

    def _detect_producers(self, produces):
        if not produces:
            self.produces = self.__class__._known_producers
        else:
            self.produces = []
            for wanted_producer in produces:
                if wanted_producer in self.produces:
                    continue

                if issubclass(wanted_producer, BaseProducer):
                    self.produces.append(wanted_producer)
                    continue

                for producer in self.__class__._known_producers:
                    if producer.content_type == wanted_producer:
                        self.produces.append(producer)
