# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api

__author__ = 'sobolevn'


def assert_each(*args):
    for arg in args:
        assert arg


class TestImports(object):
    def test_import_swagger(self):
        from flask_restful_swagger.swagger import SwaggerDocs
        assert SwaggerDocs

    def test_import_docs_v1_2(self):
        from flask_restful_swagger.swagger import SwaggerDocs
        app = Flask(__name__, static_folder='../static')
        swagger = SwaggerDocs(Api(app), {}, {'swaggerVersion': '1.2'})
        assert_each(
            swagger,
            swagger.model,
            swagger.resource,
            swagger.operation,
            swagger.nested,
        )

    def test_import_docs_v2_0(self):
        from flask_restful_swagger.swagger import SwaggerDocs
        app = Flask(__name__, static_folder='../static')
        swagger = SwaggerDocs(Api(app), {}, {'swagger': '2.0'})
        assert_each(
            swagger,
            swagger.model,
            swagger.resource,
            swagger.operation,
            swagger.nested,
        )
