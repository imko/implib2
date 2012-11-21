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
from nose.tools import ok_, eq_, raises
from binascii import b2a_hex as b2a, a2b_hex as a2b

from implib2.imp_crc import MaximCRC, MaximCRCError
from implib2.imp_tables import Tables, TablesError
from implib2.imp_packages import Package, PackageError
from implib2.imp_responces import Responce, ResponceError

class TestResponce(object):

    def __init__(self):
        self.res = Responce(Tables(), Package())

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_long_ack_right_serno(self):
        pkg = a2b('0002001a7900a7')
        ok_(self.res.get_long_ack(pkg, 31002))

    def test_get_long_ack_wrong_serno(self):
        pkg = a2b('0002001a7900a7')
        eq_(self.res.get_long_ack(pkg, 31003), False)

    def test_get_short_ack_right_serno(self):
        pkg = a2b('24')
        ok_(self.res.get_short_ack(pkg, 31002))

    def test_get_short_ack_wrong_serno(self):
        pkg = a2b('24')
        eq_(self.res.get_short_ack(pkg, 31003), False)

    def test_get_range_ack_responce(self):
        pkg = a2b('24')
        ok_(self.res.get_range_ack(pkg))

    def test_get_range_ack_no_responce(self):
        pkg = a2b('')
        eq_(self.res.get_range_ack(pkg), False)

    def test_get_negative_ack(self):
        pkg = a2b('000805ffffffd91a79000042')
        eq_(self.res.get_negative_ack(pkg), 31002)

    def test_get_parameter(self):
        pkg = a2b('000a051a7900181a79000042')
        eq_(self.res.get_parameter(pkg,
            'SYSTEM_PARAMETER_TABLE', 'SerialNum'), (31002,))

    def test_set_parameter(self):
        pkg = a2b('0011001a790095')
        ok_(self.res.set_parameter(pkg, 31002,
            'PROBE_CONFIGURATION_PARAMETER_TABLE'))

    @raises(ResponceError)
    def test_set_parameter_wrong_table(self):
        pkg = a2b('0011001a790095')
        self.res.set_parameter(pkg, 31002, 'SYSTEM_PARAMETER_TABLE')

    @raises(ResponceError)
    def test_set_parameter_wrong_serno(self):
        pkg = a2b('0011001a790095')
        self.res.set_parameter(pkg, 31003,
            'PROBE_CONFIGURATION_PARAMETER_TABLE')

    def test_do_tdr_scan(self):
        pkg = a2b('001e0b1a79006e112fc44e3702f3e7fb3dc5')
        point0 = {'tdr': 17, 'time': 1.232423437613761e-05}
        point1 = {'tdr': 2, 'time': 0.12300100177526474}
        dat = self.res.do_tdr_scan(pkg)
        eq_((dat[0], dat[1]), (point0, point1))

    @raises(ResponceError)
    def test_do_tdr_scan_strange_length(self):
        pkg = a2b('001e0c1a7900e811112fc44e3702f3e7fb3df5')
        self.res.do_tdr_scan(pkg)

    def test_get_epr_image(self):
        pkg = a2b('003c0b1a790015112fc44e3702f3e7fb3dc5')
        page = [17, 47, 196, 78, 55, 2, 243, 231, 251, 61]
        eq_(self.res.get_epr_image(pkg), page)

    def test_set_epr_image(self):
        pkg = a2b('003d001a79004c')
        ok_(self.res.set_epr_image(pkg))
