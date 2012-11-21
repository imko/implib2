#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (C) 2011-2012, Markus Hubig <mhubig@imko.de>

This file is part of IMPLib2 a small Python library implementing
the IMPBUS-2 data transmission protocol.

IMPLib2 is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

IMPLib2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with IMPLib2. If not, see <http://www.gnu.org/licenses/>.
"""

import json
from nose.tools import ok_, eq_, raises, with_setup
from implib2.imp_tables import Tables, TablesError

class TestTables(object):

    def __init__(self):
        with open('implib2/imp_tables.json') as js:
            self.j = json.load(js)

    def setUp(self):
        self.t = Tables()

    def tearDown(self):
        pass

    def test_load_json(self):
        eq_(self.t._tables, self.j)

    @raises(IOError)
    def test_load_json_no_file(self):
        json = Tables('dont_exists.json')

    @raises(ValueError)
    def test_load_json_falty_file(self):
        json = self.t._load_json('imp_tables.py')

    @raises(TablesError)
    def test_lookup_unknown_table(self):
        self.t.lookup('UNKNOWN', 'UNKNOWN')

    @raises(TablesError)
    def test_lookup_unknown_param(self):
        self.t.lookup('APPLICATION_PARAMETER_TABLE', 'UNKNOWN')

    def _lookup_value(self, table, param):
        row = self.j[table][param]
        value = self.t.lookup(table, param)
        if param == 'Table':
            eq_(len(row), len(value))
        else:
            eq_(len(row) + 2, len(value))

    def _test_lookup_value(self):
        for table in self.j:
            for param in self.j[table]:
                yield _lookup_value, table, param

    def _lookup_value_has_get(self, table, param):
        row = self.t.lookup(table, param)
        ok_(row.has_key('Get'))

    def test_has_get(self):
        for table in self.j:
            for param in self.j[table]:
                yield self._lookup_value_has_get, table, param

    def _lookup_value_has_set(self, table, param):
        row = self.t.lookup(table, param)
        ok_(row.has_key('Set'))

    def test_has_set(self):
        for table in self.j:
            for param in self.j[table]:
                yield self._lookup_value_has_set, table, param

