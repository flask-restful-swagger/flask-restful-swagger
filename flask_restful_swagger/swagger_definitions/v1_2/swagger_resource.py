# -*- coding: utf-8 -*-

from flask_restful_swagger.swagger_definitions.base_swagger_definition import (
    SwaggerDefinition,
)
from flask_restful_swagger.utils import (
    extract_swagger_path,
)

__author__ = 'sobolevn'


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

    def _extract_operations(self):
        operations = []
        for k, v in self.orig.__dict__.items():
            if callable(v) and hasattr(v, 'operation'):
                operation = getattr(v, 'operation')
                args = operation.extract_path_arguments(self.url)
                operation.add_path_arguments(args)
                operations.append({k: operation})

        return operations

    def _render_operations(self, operations):
        result = []
        for operation in operations:
            for k, v in operation.items():
                rendered = v.render()
                rendered.update({'method': k})
                result.append(rendered)

        return result

    def render(self, models=None):
        operations = self._extract_operations()
        result = self.orig.swagger_attr

        result['apis'] = []
        result['apis'].append({
            'path': self.swagger_url,
            'operations': self._render_operations(operations),
        })

        if models:
            result['models'] = {k: v.render() for k, v in models.items()}

        return result
