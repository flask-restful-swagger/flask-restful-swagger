# -*- coding: utf-8 -*-
from collections import defaultdict

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
    def __init__(self, resource, *urls):
        self.orig = resource
        self.operations = defaultdict(dict)
        self.urls = urls

    @staticmethod
    def _render_operations(operations):
        result = {}
        for k, v in operations.items():
            result[k] = v.render()

        return result

    def render(self):
        result = {}
        for url in self.urls:
            operations = extract_operations(self, url)
            result[url] = self._render_operations(operations)
        return result
