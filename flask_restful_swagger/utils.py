# -*- coding: utf-8 -*-

import functools
import inspect
import re
import warnings

__author__ = 'sobolevn'


def deprecated(func):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    :param func: function to decorated.
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn_explicit(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            filename=func.func_code.co_filename,
            lineno=func.func_code.co_firstlineno + 1,
        )
        return func(*args, **kwargs)

    return new_func


def convert_from_camel_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def _sanitize_doc(comment):
    return comment.replace('\n', '<br/>') if comment else comment


def _parse_doc(obj):
    first_line, other_lines = None, None

    full_doc = inspect.getdoc(obj)
    if full_doc:
        line_feed = full_doc.find('\n')
        if line_feed != -1:
            first_line = _sanitize_doc(full_doc[:line_feed])
            other_lines = _sanitize_doc(full_doc[line_feed + 1:])
        else:
            first_line = full_doc

    return first_line, other_lines


def extract_operations(resource):
    operations = []
    for k in dir(resource.orig):
        v = getattr(resource.orig, k)
        if callable(v) and hasattr(v, 'swagger_operation'):
            operations.append({k: getattr(v, 'swagger_operation')})

    return operations


def extract_swagger_path(path):
    """
    Extracts a swagger type path from the given flask style path.
    This /path/<parameter> turns into this /path/{parameter}
    And this /<string(length=2):lang_code>/<string:id>/<float:probability>
    to this: /{lang_code}/{id}/{probability}
    """
    return re.sub('<(?:[^:]+:)?([^>]+)>', '{\\1}', path)


def resource_endpoint_url(resource):
    pattern = r"<class '\w+\.(\w+)'>"
    return re.findall(pattern, repr(resource).lower())[0]
