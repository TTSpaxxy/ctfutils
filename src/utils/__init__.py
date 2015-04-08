# ctfutils - A variety of mini programs designed to be useful in "Capture the Flag" competitions
# Copyright (C) 2015 Aaron Cohen
# This file is part of ctfutils
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

#Start __init__.py

import os
import sys

import b64
import fanalysis
import help
import md5crack
__all__ = list(( mod[0:-3] for mod in os.listdir(os.path.dirname(sys.argv[0]) + "/utils/") if (mod[-3:] == ".py" and mod != "__init__.py") ))

def run_mod(name, arg_list):
    """
Run individual commands with arguments
    """
    return eval("%s.f(arg_list)" % name)
#End def

#End __init__.py
