# -*- coding: utf-8 -*-

from flask_restful_swagger.swagger_definitions.base_swagger_definition import (
    SwaggerDefinition,
)
from flask_restful_swagger.utils import (
    extract_operations,
    extract_swagger_path,
)

__author__ = 'gdoumenc'


class SwaggerTag(SwaggerDefinition):
    def __init__(self, name, order, description):
        self.name = name
        self.description = description

    def render(self):
        return dict(name=self.name, description=self.description)


class SwaggerResource(SwaggerDefinition):
    def __init__(self, resource, url=None):
        self.orig = resource
        self.url = url
        self.swagger_url = extract_swagger_path(url)
        self.listing_path = '/' + url.split('/')[1]

    @staticmethod
    def _render_operations(operations):
        result = {}
        for operation in operations:
            for k, v in operation.items():
                result[k] = v.render()

        return result

    def render(self):
        operations = extract_operations(self)
        result = dict({
            self.url: self._render_operations(operations),
        })
        return result
