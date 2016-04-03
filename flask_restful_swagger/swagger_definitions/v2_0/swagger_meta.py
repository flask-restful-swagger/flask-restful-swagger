# -*- coding: utf-8 -*-

from flask_restful_swagger.swagger_definitions.base_swagger_definition import (
    SwaggerDefinition,
)

__author__ = 'gdoumenc'


class SwaggerListingMeta(dict, SwaggerDefinition):
    def render(self, resources=None):
        result = {k: v for k, v in self.items()}
        result['apis'] = []
        for r in resources.values():
            result['apis'].append(r.render_listing())
        return result


class SwaggerMeta(dict, SwaggerDefinition):
    def render(self, resource):
        return resource.render()