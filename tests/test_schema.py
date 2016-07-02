# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api
import os
import json

from jsonschema import validate

from tests.utils import BaseIntegrationTest
from tests.apps.swg_app_20 import app


__author__ = 'evlampieva'

"""
Here are the tests to be sure, that basic_app produces the
right swagger's spec-json. It is possible to read the documentation
about swagger 2.0 specification here:
https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md
"""


class TestSpecJson(BaseIntegrationTest):
    app = app

    def _load_spec_json(self):
        response = self.get_raw_link('/api/spec/json')
        return json.loads(response.data)

    def _load_json_schema(self, filename):
        base = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(base,'tests' ,'fixtures', filename)
        with open(path) as f:
            return json.load(f)

    def test_swagger_schema_v2_0(self):
        swagger_schema = self._load_json_schema('schema.json')
        real = self._load_spec_json()
        validate(real, swagger_schema)



