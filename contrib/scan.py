#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import numpy as np
import logging
from implib2 import Bus, Module

logging.basicConfig(
        format='%(message)s',
        filename='scan.log',
        level=logging.DEBUG)

bus = Bus('/dev/ttyUSB0', rs485=False)

def scan():

    try:
        tic = time.time()
        probes = bus.scan_bus()
        s_time = time.time() - tic
    except:
        logging.debug('ERROR: Exception caught!')
        probes = []
        s_time = 0.0
    finally:
        time.sleep(0.1)

    return len(probes), s_time, probes

reference = set([10000, 10001, 10002, 10003, 10004,
    10005, 10006, 10007, 10008, 10009, 10010, 10011])

logging.debug("nr;found;scan_time;probes")

bus.dev.open_device()
bus.wakeup()
bus.synchronise_bus()

for nr in range(1,11):
    print "== Nr: {} =================================".format(nr)
    found, scan_time, probes = scan()
    probes = list(reference - set(probes))
    logging.debug("{:03};{:02};{:.6f};{}" .format(nr, found,
        scan_time, probes))

bus.dev.close_device()
