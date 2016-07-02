# -*- coding: utf-8 -*-

import inspect
from itertools import izip_longest

from flask_restful import fields

from flask_restful_swagger.swagger_definitions.base_swagger_definition import (
    SwaggerDefinition,
)

__author__ = 'sobolevn'


class SwaggerModel(SwaggerDefinition):
    NUMBER = (float, fields.Float, fields.Arbitrary, fields.Fixed, )
    BOOLEAN = (bool, fields.Boolean, )
    DATETIME = (fields.DateTime, )
    INTEGER = (int, fields.Integer, )
    STRING = (str, fields.String, fields.FormattedString, fields.Url, )

    @classmethod
    def all_types(cls):
        return cls.NUMBER + cls.BOOLEAN + cls.DATETIME + \
               cls.INTEGER + cls.STRING

    @classmethod
    def predicate(cls, obj):
        return issubclass if inspect.isclass(obj) else isinstance

    @classmethod
    def deduce_swagger_type(cls, obj, nested_type=None):
        predicate = cls.predicate(obj)
        if predicate(obj, cls.all_types()):
            return {'type': cls.deduce_swagger_type_flat(obj)}

        if predicate(obj, (fields.List, )):
             if inspect.isclass(obj):
                 return {'type': 'array'}
             else:
                 return {
                     'type': 'array',
                     'items': {
                         '$ref': "#/definitions/" + cls.deduce_swagger_type_flat(
                                 obj.container, nested_type)
                     }
                 }

        if predicate(obj, (fields.Nested, )):
            return {'$ref': "#/definitions/" + cls.deduce_swagger_type_flat(
                                 obj, nested_type)}

        return {'type': 'null'}

    @classmethod
    def deduce_swagger_type_flat(cls, obj, nested_type=None):
        if nested_type:
            return nested_type

        mapping = [
            ('string', cls.STRING),
            ('integer', cls.INTEGER),
            ('number', cls.NUMBER),
            ('boolean', cls.BOOLEAN),
            ('date-time', cls.DATETIME), #TODO: this type is not supported by swagger JSON schema!
        ]

        predicate = cls.predicate(obj)
        for value, classes in mapping:
            if predicate(obj, classes):
                return value

        # This is not going to happen in normal situations:
        raise ValueError('{} is not a valid type'.format(
            obj.__name__ if inspect.isclass(
                obj) else obj.__class__.__name__
        ))

    def __init__(self, model_class):
        self.model_class = model_class
        self.swagger_model = self._construct_swagger_model()

    def _parse_resource_fields(self):
        resource_fields = self.model_class.resource_fields

        is_nested = isinstance(self.model_class, SwaggerNestedModel)
        nested = self.model_class.nested() if is_nested else {}

        properties = {}
        for name, field in resource_fields.items():
            nested_type = nested[name] if name in nested else None
            values = self.deduce_swagger_type(field, nested_type)
            properties[name] = values

        return properties

    def _parse_constructor(self):
        arg_spec = inspect.getargspec(self.model_class.__init__)
        arg_spec.args.remove('self')

        properties = {}
        for arg, default in izip_longest(arg_spec.args, arg_spec.defaults):
            if default:
                arg_type = self.deduce_swagger_type(default)
                arg_type.update({'default': default})
                properties[arg] = arg_type
            else:
                properties[arg] = self.deduce_swagger_type('string')

        return properties

    def _construct_swagger_model(self):
        result = {
            'type': 'object',
        }

        try:
            # At first, try to load meta from `resource_fields`:
            properties = self._parse_resource_fields()
        except AttributeError:
            # There was no `resource_fields` attr, parse constructor:
            properties = self._parse_constructor()
        except Exception:
            # This model is not valid, `resource_fields` nor `init` provided.
            raise AttributeError('{} model is not a valid swagger model.'.format(
                self.model_class.__name__
            ))

        try:
            # Updating properties based on custom metadata:
            model_meta = self.model_class.swagger_metadata
            meta_properties = model_meta.pop('properties', {})
            model_meta.pop('id', None)  # id is not suited for changes

            for field_name, field_metadata in model_meta.items():
                result[field_name] = field_metadata

            # updating properties metas: description, format, enums:
            for name, values in meta_properties.items():
                values.pop('type', None)  # type is not suited for change
                properties[name].update(values)
        except AttributeError:
            pass

        result['properties'] = properties

        try:  # trying to parse `required` field at first:
            required = self.model_class.required
            result['required'] = required
        except AttributeError:
            required = []  # there's no required field provided.

        return result

    def render(self):
        return self.swagger_model


class SwaggerNestedModel(object):
    def __init__(self, klass, **kwargs):
        self._nested = kwargs
        self._klass = klass

    def __call__(self, *args, **kwargs):
        return self._klass(*args, **kwargs)

    def nested(self):
        return self._nested



