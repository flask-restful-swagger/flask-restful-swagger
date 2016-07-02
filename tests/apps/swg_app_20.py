# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with

from flask_restful_swagger.swagger import SwaggerDocs

from tests.apps import config

__author__ = 'sobolevn'

app = Flask(__name__, static_folder='../static')
app.config.from_object(config)

api_listing_meta = {
    'swagger': '2.0',
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
        },
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


@swagger.model
@swagger.nested(
    a_nested_attribute=ModelWithResourceFields.__name__,
    a_list_of_nested_types=ModelWithResourceFields.__name__,
)
class TodoItemWithResourceFields(object):
    """This is an example of how Output Fields work
    (http://flask-restful.readthedocs.org/en/latest/fields.html).
    Output Fields lets you add resource_fields to your model in which you specify
    the output of the model when it gets sent as an HTTP response.
    flask-restful-swagger takes advantage of this to specify the fields in
    the model"""
    resource_fields = {
        'a_string': fields.String(attribute='a_string_field_name'),
        'a_formatted_string': fields.FormattedString,
        'an_int': fields.Integer,
        'a_bool': fields.Boolean,
        'a_url': fields.Url,
        'a_float': fields.Float,
        'an_float_with_arbitrary_precision': fields.Arbitrary,
        'a_fixed_point_decimal': fields.Fixed,
#        'a_datetime': fields.DateTime,  #not supported by swagger JSON schema, test will fail
        'a_list_of_strings': fields.List(fields.String),
        'a_nested_attribute': fields.Nested(
            ModelWithResourceFields.resource_fields),
        'a_list_of_nested_types': fields.List(
            fields.Nested(ModelWithResourceFields.resource_fields)),
    }

    # Specify which of the resource fields are required
    required = ['a_string', ]

todo_tags = [
        {
            "name": "todo",
            "description": "Everything about your Pets",
            "externalDocs": {
                "description": "Find out more",
                "url": "http://swagger.io"
            }
    },
]


@swagger.resource(tags=todo_tags)
class Todo(Resource):
    """
    Todo-Description
    Todo-Notes
    In get operation inline model of response is used. If you gonna use common model in several operations
    it's better to describe it as swagger.model and put references in each response
    as shown in marshal_with example
    """

    @swagger.operation(
            tags= ["todo"],
            summary='get a todo item by ID',
            operationId='getTodoItem',
            parameters=[{
                "name": "todo_id",
                "in": "path",
                "description": "ID of todo item to return",
                "required": True,
                "type": "integer",
                "format": "int64"
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
            tags=["todo"],
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

marshal_tags = [
    {
        "name": "marshal",
        "description": "Marshal with example",
        "externalDocs": {
            "description": "Find out more",
            "url": "http://swagger.io"
        }
    },
]


@swagger.resource(tags=marshal_tags)
class MarshalWithExample(Resource):
    @swagger.operation(
        tags=["marshal"],
        summary='marshalling with example',
        operationId='marshal_with',
        parameters=[{
			"in": "body",
			"name": "body",
			"description": "simple model that is used as a parameter structure",
			"required": True,
			"schema": {
			  "$ref": "#/definitions/TodoItem"
			}
		  }, ],
        responses={
            "200": {
                "description": "successful operation",
                "schema": {
                    "$ref": "#/definitions/TodoItemWithResourceFields"
                },
            }
        }
    )
    @marshal_with(ModelWithResourceFields.resource_fields)
    def get(self, **kwargs):
        return {
            'a_string': 'marshaled',
        }, 200, {
            'Access-Control-Allow-Origin': '*',
        }

#parameter name in url should be identical to parameter name in swagger.operation
#swagger.add_resource(Todo, '/todo/<int:todo_id>')
swagger.add_resource(Todo, '/todo')

swagger.add_resource(MarshalWithExample, '/marshal')


if __name__ == '__main__':
    app.run(debug=True)
