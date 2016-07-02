# -*- coding: utf-8 -*-
from flask_restful_swagger.swagger_definitions.base_swagger_definition import (
    SwaggerDefinition,
)

__author__ = 'gdoumenc'


class SwaggerListingMeta(dict, SwaggerDefinition):
    def render(self, resources=None, tags=None, models=None):
        result = ({k: v for k, v in self.items()})

        result['paths'] = {}
        for r in resources.values():
            result['paths'].update(r.render())

        result['tags'] = []
        for t in tags:
            result['tags'].extend(t.render())

        if models:
            result['definitions'] = {k: v.render() for k, v in models.items()}


        return result


class SwaggerMeta(dict, SwaggerDefinition):
    def render(self, resource, models):
        return resource.render(models=models)
