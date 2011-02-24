#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Copyright (C) 2011, Markus Hubig <mhubig@imko.de>

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
from imp_packets import IMPPackets, IMPPacketsException
from imp_tables import IMPTables, IMPTablesException

class ModuleResponcesException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ModuleResponces(IMPPackets, IMPTables):
    def __init__(self):
        self.DEBUG = False
        IMPPackets.__init__(self)
        IMPTables.__init__(self)
    
    def _hex2float(self, s):
        bins = ''.join(chr(int(s[x:x+2], 16)) for x in range(0, len(s), 2))
        return struct.unpack('>f', bins)[0]
    
    def responce_get_long_acknowledge(self, packet):
        responce = self.unpack(packet)
        return responce['serno']
        
    def responce_get_short_acknowledge(self, packet):
        # not a standart responce packet, just the CRC of the serial
        pass
        
    def responce_get_acknowledge_for_serial_number_range(self, packet):
        # not a standart responce packet, just the CRC of the serial
        pass
        
    def responce_get_negative_acknowledge(self, packet):
        responce = self.unpack(packet)
        return responce['serno']
        
    def responce_get_parameter(self, packet, table, param):
        responce = self.unpack(packet)
        data = self._reflect_bytes(responce['data'])
        table = getattr(self, table)
        param = getattr(table, param)
        
        # 32-bit float
        if param.Type == 6:
            data = self._hex2float(data)
            data = '%.6f' % data
        
        # 16-bit unsigned
        if param.Type == 2:
            data = int(data, 16)
            
        return data
        
    def responce_set_parameter(self, packet):
        responce = self.unpack(packet)
        return True
        
    def responce_do_tdr_scan(self, packet):
        responce = self.unpack(packet)
        return responce['serno'], responce['cmd'], responce['data']
        
    def responce_get_epr_image(self, packet):
        responce = self.unpack(packet)
        return responce['data']
        
    def responce_set_erp_image(self, packet):
        responce = self.unpack(packet)
        return responce['serno'], responce['cmd']
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
