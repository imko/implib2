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
from imp_packets import Packets, PacketsException
from imp_tables import Tables, TablesException

class ModuleResponcesException(Exception):
    pass

class ModuleResponces(Packets, Tables):
    def __init__(self):
        self.DEBUG = False
        Packets.__init__(self)
        Tables.__init__(self)
    
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
        
        # 8-bit unsigned char
        if param.Type == 0:
            data = int(data, 16)
        
        # 8-bit signed char
        if param.Type == 1:
            data = int(data, 16)
        
        # 16-bit unsigned integer
        if param.Type == 2:
            data = int(data, 16)
        
        # 16-bit signed integer
        if param.Type == 3:
            data = int(data, 16)
        
        # 32-bit unsigned integer 
        if param.Type == 4:
            data = int(data, 16)
        
        # 32-bit signed integer
        if param.Type == 5:
            data = int(data, 16)
        
        # 32-bit float
        if param.Type == 6:
            data = self._hex2float(data)
            data = '%.6f' % data
            
        # 64-bit double
        if param.Type == 7:
            data = data = self._hex2float(data)
            data = '%.6f' % data
        
        return data
        
    def responce_set_parameter(self, packet, table):
        responce = self.unpack(packet)
        table = getattr(self, table)
        param = getattr(table, "Table")
        if not int(responce['cmd'],16) == param.Set:
            raise ModuleResponcesException("CMD doesn't match SetValue of Tbl!")
        return True
        
    def responce_do_tdr_scan(self, packet):
        responce = self.unpack(packet)
        return responce['serno'], responce['cmd'], responce['data']
        
    def responce_get_epr_image(self, packet):
        responce = self.unpack(packet)
        return responce['data']
        
    def responce_set_erp_image(self, packet):
        responce = self.unpack(packet)
        if not int(responce['cmd'], 16) == 61:
            raise ModuleResponcesException("CMD doesn't match SetERPImage!")
        return True
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
