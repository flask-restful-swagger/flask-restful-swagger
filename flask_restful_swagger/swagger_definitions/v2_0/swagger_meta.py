# -*- coding: utf-8 -*-
from flask_restful_swagger.swagger_definitions.base_swagger_definition import (
    SwaggerDefinition,
)

__author__ = 'gdoumenc'


class SwaggerListingMeta(dict, SwaggerDefinition):
    def render(self, resources=None, tags=None):
        result = ({k: v for k, v in self.items()})
        result.setdefault('swagger', "2.0")

        result['paths'] = {}
        for r in resources.values():
            result['paths'].update(r.render())

        result['tags'] = []
        if hasattr(tags, 'values'):
            for r in tags.values():
                result['tags'].append(r.render())

        return result


class SwaggerMeta(dict, SwaggerDefinition):
    def render(self, resource, models):
        return resource.render()
