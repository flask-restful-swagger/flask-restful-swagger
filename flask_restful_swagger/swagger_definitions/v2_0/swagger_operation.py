# -*- coding: utf-8 -*-

import re

from flask_restful_swagger.swagger_definitions.base_swagger_definition import (
    SwaggerDefinition,
)

__author__ = 'sobolevn'


class SwaggerOperation(SwaggerDefinition):
    def __init__(self, **kwargs):
        self.data = kwargs

    def extract_path_arguments(self, path):
        """
        Extracts a swagger path arguments from the given flask path.
        This /path/<parameter> extracts [{name: 'parameter'}]
        And this /<string(length=2):lang_code>/<string:id>/<float:probability>
        extracts: [
        {name: 'lang_code', dataType: 'string'},
        {name: 'id', dataType: 'string'}
        {name: 'probability', dataType: 'float'}]
        :param path: flask-formatted path string
        :return: a list of dicts with swagger-formatted path arguments.
        """
        path = re.sub('\([^\)]*\)', '', path)  # Remove all parentheses
        args = re.findall('<([^>]+)>', path)

        return list(map(self.render_path_arg, args))

    def render(self):
        return self.data

    def has_parameter_named(self, name):
        return any(p['name'] == name for p in self.data['parameters'])

    def add_path_arguments(self, args):
        validated_args = filter(
            lambda arg: not self.has_parameter_named(arg['name']), args
        )
        self.data.setdefault('parameters', []).extend(validated_args)

    def render_path_arg(self, arg):
        spl = arg.split(':')
        try:
            data_type, name = spl
        except ValueError:
            name = spl[0]
            data_type = 'string'

        return {
            'name': name,
            'dataType': data_type,
            'paramType': 'path',
        }
