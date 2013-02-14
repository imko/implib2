#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (C) 2011-2013, Markus Hubig <mhubig@imko.de>

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
import struct
from cStringIO import StringIO


class CommandError(Exception):
    pass


class Command(object):
    def __init__(self, package):
        self.pkg = package

    def get_long_ack(self, serno):
        return self.pkg.pack(serno=serno, cmd=0x02)

    def get_short_ack(self, serno):
        return self.pkg.pack(serno=serno, cmd=0x04)

    def get_range_ack(self, rng):
        return self.pkg.pack(serno=rng, cmd=0x06)

    def get_negative_ack(self):
        return self.pkg.pack(serno=16777215, cmd=0x08)

    def get_parameter(self, serno, table):
        data = StringIO()
        data.write(struct.pack('<B', table.cmd))
        data.write(struct.pack('<B', 0))

        return self.pkg.pack(serno=serno, cmd=table.get, data=data.getvalue())

    def set_parameter(self, serno, table, values, ad_param=0):
        data = StringIO()
        data.write(struct.pack('<B', table.cmd))
        data.write(struct.pack('<B', ad_param))
        
        for param in table:
            try:
                data.write(struct.pack(param.fmt, values[param.name]))
            except KeyError:
                CommandError("Param {} needed, but not given!".format(param)

        return self.pkg.pack(serno=serno, cmd=table.set, data=data.getvalue())

    def do_tdr_scan(self, serno, scan_start, scan_end, scan_span, scan_count):
        # pylint: disable=R0913
        scan_start = struct.pack('<B', scan_start)
        scan_end   = struct.pack('<B', scan_end)
        scan_span  = struct.pack('<B', scan_span)
        scan_count = struct.pack('<H', scan_count)
        data = scan_start + scan_end + scan_span + scan_count

        return self.pkg.pack(serno=serno, cmd=0x1e, data=data)

    def get_epr_page(self, serno, page_nr):
        param_no = struct.pack('<B', 255)
        param_ad = struct.pack('<B', page_nr)
        data = param_no + param_ad

        return self.pkg.pack(serno=serno, cmd=0x3c, data=data)

    def set_epr_page(self, serno, page_nr, page):
        if len(page) > 250:
            raise CommandError("Page to big, exeeds 250 Bytes!")

        param_no = struct.pack('<B', 255)
        param_ad = struct.pack('<B', page_nr)
        param    = str()

        for byte in page:
            param += struct.pack('<B', byte)

        data = param_no + param_ad + param

        return self.pkg.pack(serno=serno, cmd=0x3d, data=data)