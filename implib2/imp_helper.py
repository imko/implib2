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

def _normalize(filename):
    """ .. function:: _normalize(filename)

    Prepends the filename with the path pointing to the main file.

    :type filename: string
    :rtype: string
    """
    import os
    abs_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(abs_path)
    return os.path.join(dir_name, filename)

def _load_json(filename):
    """ .. funktion:: _load_json(filename)

    Reads the spezific json file.

    :type filename: string
    :rtype: dict
    """
    import json
    filename = _normalize(filename)
    with open(filename) as js_file:
        return json.load(js_file)

