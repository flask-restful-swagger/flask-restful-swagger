# -*- coding: utf-8 -*-

from flask_restful_swagger.swagger_definitions.base_swagger_definition import (
    SwaggerDefinition,
)
from flask_restful_swagger.utils import (
    extract_swagger_path,
)

__author__ = 'sobolevn'


class SwaggerTag(SwaggerDefinition):
    def __init__(self, tagsList):
        self.contents = tagsList  #store all tags for particular resource class

    def render(self):
        return self.contents

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
        #extracting method names from a class that we passed to swagger as resource (at add_resource method)
        for k in dir(self.orig):
            v = getattr(self.orig, k)
            if callable(v) and hasattr(v, 'operation'): #parsing only methods marked with decorator @swagger.operation
                operation = getattr(v, 'operation')
                args = operation.extract_path_arguments(self.url)
                operation.add_path_arguments(args)
                operations.append({k: operation})

        return operations

    @staticmethod
    def _render_operations(operations):
        result = {}
        for operation in operations:
            for k, v in operation.items():
                result[k] = v.render()
        return result

    def render(self, models=None):
        operations = self._extract_operations()
#        result = self.orig.swagger_attr
        result = {}
        result[self.swagger_url] = self._render_operations(operations)

#        if models:
#            result['models'] = {k: v.render() for k, v in models.items()}

        return result


