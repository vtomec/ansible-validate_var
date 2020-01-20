#
# Copyright: (c) 2019, Vaclav Tomec <vaclav.tomec@gmail.com>
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.module_utils._text import to_native
import json
from jsonschema import validate, FormatChecker
from jsonschema.exceptions import _Error


class ActionModule(ActionBase):
    """Validate if a given variable is compliant with JSON schema"""

    _VALID_ARGS = frozenset(('var', 'schema'))

    def run(self, tmp=None, task_vars=None):

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        # check if arguments are provided
        __var = self._task.args.get('var', None)
        __schema = self._task.args.get('schema', None)

        if __var is None:
            result['failed'] = True
            result['msg'] = "'var' argument needs to be provided"
            return result

        if __schema is None:
            result['failed'] = True
            result['msg'] = "'schema' argument needs to be provided"
            return result

        try:
            # open file
            schema_path = self._find_needle('files', __schema)
            result['schema_path'] = schema_path
            f_schema = open(schema_path, 'r')
        except IOError as e:
            result['failed'] = True
            result['msg'] = "Failed to open %s: %s" % (to_native(__schema), to_native(e))
            return result

        try:
            # load schema
            schema = json.loads(f_schema.read())
            f_schema.close()
        except ValueError as e:
            result['failed'] = True
            result['msg'] = "Failed to load schema %s: %s" % (to_native(__schema), to_native(e))
            return result

        try:
            # validate data
            validate(__var, schema, format_checker=FormatChecker())
        except _Error as e:
            result['failed'] = True
            result['msg'] = "Validation failed: %s" % to_native(e)
            return result

        return result
