#!/bin/sh

# Copyright (C) 2011-2012, Markus Hubig <mhubig@imko.de>
#
# This file is part of IMPLib2 a small Python library implementing
# the IMPBUS-2 data transmission protocol.
#
# IMPLib2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# IMPLib2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with IMPLib2. If not, see <http://www.gnu.org/licenses/>.

function usage () {
    echo "usage: bump-version <version-id>"
}

function update_version_init () {
    sed "s/^__version__ = .*$/__version__ = 'release-$1'/g" \
        implib2/__init__.py > .__init__.new
}

function update_version_setup () {
    sed "s/version = .*$/version = 'release-$1',/g" \
        setup.py > .setup.new
}


if [ $# -ne 1 ]; then
    usage
    exit 1
fi

if ! update_version_init $1; then
    echo "Could not replace version in '__init__.py'!" >&2
    exit 2
else
    mv .__init__.new implib2/__init__.py
fi

if ! update_version_setup $1; then
    echo "Could not replace version in 'setup.py'!" >&2
    exit 2
else
    mv .setup.new setup.py
fi

git add __init__.py
git commit -s -m "Bumped version number to release-$1" __init__.py
