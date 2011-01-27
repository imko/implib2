#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2009-2012, Markus Hubig <mhubig@imko.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
from serialdevice import SerialDevice, SerialDeviceException 
from basecommands import BaseCommands, BaseCommandsException
from baseresponce import BaseResponce, BaseResponceException

class CommandsException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Commands(SerialPort, BaseCommands, BaseResponce):
    """ Class to combine the basic IMPBUS2 commands to
        higher level command cascades.
        
        Befor using any other command you first have to
        call init_bus() to get the device up and all modules
        talking at the same baudrate!
    
    >>> impbus = Commands('/dev/ttyS0')
    >>> impbus.synchronise_bus()
    >>> impbus.scan_bus()
    [71562, 72366, 77654]
    >>> impbus.measure_moist('71562')
    {'value': 77, 'unit': '%'}
    >>> impbus.measure_temp('77654')
    {'value': 23, 'unit': '°C'}
    >>> impbus.close_device()
    """
    
    def __init__(self):
        BaseCommands.__init__(self)
        BaseResponce.__init__(self)
        SerialDevice.__init__(self, port)
    
    def _divide_and_conquer(self, low, high, found):
        """ Recursiv divide-and-conquer algorythm to scan the IMPBUS.
        
        Divides the 24bit address range [0 - 16777215] in equal parts
        and uses the get_acknowledge_for_serial_number_range() methode
        to sort out the rages without a module. The found module serials
        are stored in the parameter list 'found'.
        """
        # if we have only two serials left check them direct.
        if high-low == 1:
            if self.short_probe_module(high):
                found.append(high)
            if short_probe_module(low):
                self.found.append(low)
            return True
        else:
            # calculate the broadcast address for range [low-high] and check
            # if there are some modules whithin the range, abort if not!
            broadcast = low + (high-low+1)/2
            if not self.get_acknowledge_for_serial_number_range(broadcast):
                return False
            
        # divide-and-conquer by splitting the range into two pices. 
        mid = (low + high)/2
        self._divide_and_conquer(low, mid, found)
        self._divide_and_conquer(mid+1, high, found)
        return True
    
    ####################################
    # Initialize the bus communication #
    ####################################
    
    def synchronise_bus(self, baudrate=9600):
        """ IMPBUS BAUDRATE SYNCHRONIZATION
        
        The communication between master and slaves can only be successful
        if they are on the same baud rate. In order to synchronise SM-modules
        on a given baud rate, the bus master has to transmit the broadcast 
        command "SetSysPara" with the parameter Baudrate on all possible baud
        rates (1200-2400-4800-9600). There must be a delay of at least 500ms
        after each command! The SM-modules understands one of these commands
        and will switch to the desired baud rate.
        """
        
        table = 'SYSTEM_PARAMETER_TABLE'
        parameter = 'Baudrate'
        address = 16777215
        
        # trying to set baudrate at 1200
        self.ser.baudrate = 1200
        self.open_device()
        self.set_parameter()
        package = self.set_parameter(address, table, baudrate)
        bytes_send = self.write(package)
        self.close_device()
        
        # trying to set baudrate at 2400
        self.ser.baudrate = 2400
        self.open_device()
        self.set_parameter()
        package = self.set_parameter(address, table, baudrate)
        bytes_send = self.write(package)
        self.close_device()
        
        # trying to set baudrate at 4800
        self.ser.baudrate = 4800
        self.open_device()
        self.set_parameter()
        package = self.set_parameter(address, table, baudrate)
        bytes_send = self.write(package)
        self.close_device()
        
        # trying to set baudrate at 9600
        self.ser.baudrate = 9600
        self.open_device()
        self.set_parameter()
        package = self.set_parameter(address, table, baudrate)
        bytes_send = self.write(package)
        self.close_device()
    
    #################################
    # finding connected modules     #
    #################################
    
    def scan_bus(self):
        """ High level command to scan the IMPBUS for connected probes.
        
        This command is very similar to the short_probe_module()
        one. However, it addresses not just one single serial number,
        but a serial number range. This value of byte 4 to byte 6
        symbolizes a whole range.
        
        It's basiclly just a small wrapper for _divide_and_conquer().
        For details see the provided docstring of _divide_and_conquer.
        Usable like this:
        
        >>> c = Commands('/dev/ttyS0')
        >>> modules = c.scan_bus()
        """
        found = list()
        self._divide_and_conquer(0, 16777215, found)
        return found
    
    def probe_module(self, serno):
        package = self.get_long_acknowledge(serno)
        bytes_send = self.write(package)
        
        # Trying to get a respoce ...
        try:
            bytes_recv = self.read()
        except:
            bytes_recv = None
        
        if not bytes_recv:
            return False    
        else:
            responce = self.responce_get_long_acknowledge(bytes_recv)
            if not serno == responce:
                raise CommandsException("Couldn't PING that serial number!")
        
        return True
    
    def short_probe_module(self, serno):
        package = self.get_short_acknowledge(serno)
        crc = self.calc_crc(serno)
        bytes_send = self.write(package)
        
        # Trying to get a respoce ...
        try:
            responce = self.ser.read(1)
        except:
            responce = None
        
        if not crc == responce:
            raise CommandsException("Couldn't PING that serial number!")
        
        return True
    
    #################################
    # change the module settings    #  
    #################################
    
    
    
    #################################
    # getting data from the modules #
    #################################
    
    def measure_moist(self, serno):
        pass
    
    def measure_temp(self, serno):
        pass
        
    def set_serial(self, serno):
        pass
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
