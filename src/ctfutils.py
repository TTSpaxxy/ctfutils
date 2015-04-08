#!/usr/bin/python
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

#Start ctfutils.py

import sys
import utils

error = {1:"Ambiguous command", 2:"Invalid command", 3:"Not implemented", 4:"Unrecognized argument", 5:"Missing required argument", 6:"Wrong number of arguments"}

def util_exec(arg_list):
    """
Interfaces with the utils package to actually run the command
    """
    command_name = arg_list[0]
    matches = []
    for module_name in utils.__all__:
        if command_name == module_name[0:len(command_name) if len(command_name) <= len(module_name) else len(module_name)]: #So we don't have to type everything out
            matches.append(module_name)
        #End if
    #End for

    if len(matches) == 0:
        print("For a list of all available commands, use 'help all'")
        return 2 #Command was not found
    elif len(matches) > 1:
        return 1 #Ambiguous command
    #End if

    exit_code = utils.run_mod(matches[0], arg_list[1:])

    return exit_code
#End def

if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    if argc < 2:
        sys.exit("Usage: {} [Command] <Arguments>".format(argv[0]))
    #End if

    exit_status = util_exec(argv[1:])
    if exit_status != 0:
        sys.exit(error[exit_status])
    #End if
#End if

#End ctfutils.py
