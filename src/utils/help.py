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

#Start help.py

import getopt

import utils
import b64
import fanalysis
import md5crack
import help

usage = "Usage: help <command name>"

shortdesc = """
help - Help
    List or get help for individual commands

{}
""".format(usage)

longdesc = """Use 'help all' to get all available commands
"""

def f(arg_list):
    """
Help - Displays help
    """
    if len(arg_list) == 0:
        help_name = "help"
    else:
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

        help_name = matches[0]
    #End if

    if help_name == "all":
        print("-"*50)
        for cmd in utils.__all__:
            print("{0.shortdesc}".format(eval(cmd)))
            print("-"*50)
        #End for

        return 0
    #End if

    if help_name not in utils.__all__:
        print("Unrecognized command {}".format(help_name))
        return 2 #Command was not found
    #End if

    print("-"*50)
    print("{0.shortdesc}".format(eval(help_name)))
    print("{0.longdesc}".format(eval(help_name)))
    print("-"*50)

    return 0
#End def
