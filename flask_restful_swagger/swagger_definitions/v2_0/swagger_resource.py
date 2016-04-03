# -*- coding: utf-8 -*-

from flask_restful_swagger.swagger_definitions.base_swagger_definition import (
    SwaggerDefinition,
)
from flask_restful_swagger.utils import (
    extract_operations,
    extract_swagger_path,
)

__author__ = 'gdoumenc'


class SwaggerResource(SwaggerDefinition):
    def __init__(self, resource, url=None):
        self.orig = resource
        self.url = url
        self.swagger_url = extract_swagger_path(url)
        self.listing_path = '/' + url.split('/')[1]

    def render_listing(self):
        return {
            'path': self.listing_path,
            'description': '',
        }

    def _render_operations(self, operations):
        result = []
        for operation in operations:
            for k, v in operation.items():
                rendered = v.render()
                rendered.update({'method': k})
                result.append(rendered)

        return result

    def render(self):
        operations = extract_operations(self)
        result = self.orig.swagger_attr

        result['apis'] = []
        result['apis'].append({
            'path': self.swagger_url,
            'operations': self._render_operations(operations),
        })

        return result
