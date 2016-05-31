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
#    'apiVersion': '1.0',
    'swaggerVersion': '2.0',
    'info': {
          "title": "Swagger Sample App",
          "description": "This is a sample todo items application.",
          "termsOfService": "http://swagger.io/terms/",
          "contact": {
            "name": "API Support",
            "url": "http://www.swagger.io/support",
            "email": "support@swagger.io"
          },
          "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
          },
          "version": "1.0.1"
        }
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
        'opt_integer': fields.Integer(),
    }

    swagger_metadata = {
        'description': 'This will be shown as a desc.',
        'properties': {
            'a_string': {
                'description': 'A string field.',
            },
            'opt_integer': {
                'format': 'int64'
            }
        },
        'required': [
            'a_string',
        ]
    }


todo_meta = {
#    "basePath": "http://127.0.0.1:5000",
#    "resourcePath": "/todo",
#    "produces": [
#        "application/json"
#    ],
#    "authorizations": {},
#    'description': 'short desc',
}


@swagger.resource(**todo_meta)
class Todo(Resource):
    """
    Todo-Description
    Todo-Notes
    """

    @swagger.operation(
            summary='get a todo item by ID',
#            type=ModelWithResourceFields.__name__,
            operationId='getTodoItem',
            parameters=[{
                "name": "todo_id",
                "in": "path",
                "description": "ID of todo item that we should return",
                "required": True,
                "type": "string"
            }, ],
            responses={
                "200": {
                    "description": "successful operation",
                    "schema": {
                        "type": "object",
                        "properties": {
                                        "id": {
                                            "type": "integer",
                                            "format": "int64"
                                        },
                                        "name": {
                                            "type": "string"
                                        },
                                        "description": {
                                            "type": "string"
                                        },
                                    },
                        "required": ["name","id"],
                        "example": {
                            "name": "todo1",
                            "id": 1,
                            "description":"Sample todo item"
                            }
                        }
                    },
                "400": {
                    "description": "Invalid ID supplied"
                },
                "404": {
                    "description": "item not found"
                }
            }
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
            summary='create a new todo item',
            operationId='postTodoItem',
            parameters=[
                {
                    "name": "item_name",
                    "in": "formData",
                    "description": "a title of new todo item",
                    "required": True,
                    "type": "string"
                },
                {
                    "name": "description",
                    "in": "formData",
                    "description": "Text of todo item",
                    "required": False,
                    "type": "string"
                }
            ],
            responses={
                "200": {
                    "description": "successful operation, Id of new todo item returned",
                    "schema": {
                        "type": "string"
                    }
                },
                "405": {
                    "description": "Invalid input"
                },
            }
    )
    def post(self, todo_id):
        return {'status': todo_id}

#parameter name in url should be identical to parameter name in swagger.operation
swagger.add_resource(Todo, '/todo/<int:todo_id>')


# swagger.add_resource(MarshalWithExample, '/marshal')


if __name__ == '__main__':
    app.run(debug=True)
