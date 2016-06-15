# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.restful import Api, fields
from flask_restful import Resource

from flask_restful_swagger.swagger import SwaggerDocs

from tests.apps import config


__author__ = 'sobolevn'


app = Flask(__name__, static_folder='../static')
app.config.from_object(config)


api_listing_meta = {
    'apiVersion': '0.1',
    'swaggerVersion': '1.2',
    'info': {
        "title": "Swagger Sample App",
        "description": "This is a sample server Petstore server.",
        "termsOfServiceUrl": "http://swagger.io/terms/",
        "contact": "apiteam@wordnik.com",
        "license": "Apache 2.0",
        "licenseUrl": "http://www.apache.org/licenses/LICENSE-2.0.html"
    },
    'apiVersion': '0.1',
    'resourcePath': '/',
    'produces': [
            'application/json',
            'text/html',
    ],
    'api_spec_url': '/api/spec',
    'description': 'A Basic API',
}

api_meta = {

}

swagger = SwaggerDocs(
    Api(app),
    swagger_meta=api_meta,
    swagger_listing_meta=api_listing_meta,
)


@swagger.model
class TodoItem(object):
    def __init__(self, arg1, arg2, arg3='123'):
        pass


@swagger.model
class ModelWithResourceFields(object):
    resource_fields = {
        'a_string': fields.String(),
    }


todo_meta = {
    "basePath": "http://127.0.0.1:5000",
    "resourcePath": "/todo",
    "produces": [
        "application/json"
    ],
    "authorizations": {},
    'description': 'short desc',
}


@swagger.resource(**todo_meta)
class Todo(Resource):
    """
    Todo-Description
    Todo-Notes
    """

    @swagger.operation(
        notes='get a todo item by ID',
        nickname='get',
        parameters=[{
            "name": "todo_id",
            "description": "ID of pet that needs to be fetched",
            "required": True,
            "type": "string",
            "paramType": "path"
        }, ],
        responseMessages= [
            {
              "code": 400,
              "message": "Invalid ID supplied"
            },
            {
              "code": 404,
              "message": "Order not found"
            }
          ]
    )
    def get(self, todo_id):
        """Summary"""

        # We expect this method to be in our specs.
        return {
           'todo_item': '{}{}'.format('todo', todo_id)
        }, 200, {
            'Access-Control-Allow-Origin': '*',
        }

    @swagger.operation(
        notes='post a todo item by ID',
        nickname='get',
        parameters=[{
            "name": "todo_id",
            "description": "ID of pet that needs to be fetched",
            "required": True,
            "type": "string",
            "paramType": "path"
        }, ],
        responseMessages= [
            {
              "code": 400,
              "message": "Invalid ID supplied"
            },
            {
              "code": 404,
              "message": "Order not found"
            }
          ]
    )
    def post(self, todo_id):
        return {'status': todo_id}


swagger.add_resource(Todo, '/todo/<string:todo_id>')
# swagger.add_resource(MarshalWithExample, '/marshal')


if __name__ == '__main__':
    app.run(debug=True)
