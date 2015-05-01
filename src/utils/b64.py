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

#Start b64.py

import base64
import getopt
import string

usage = "Usage: b64 <encode/decode> [args] <input file>"

shortdesc = """
b64 - Base 64
    Encode or decode text into Base 64

{}
""".format(usage)

longdesc = """Options:
-l OR --last-two | Specify the last two characters of the encoding scheme
                 | (Defaults to +/)
"""

lasttwo_default = "+/"

shortopt = "l:"
longopt = ["last-two="]

def f(arg_list):
    """
Base 64 encoding or decoding
    """
    try:
        opts, args = getopt.getopt(arg_list, shortopt, longopt)
    except getopt.GetoptError as err:
        print(str(err))
        return 4 #Unrecognized argument
    #End try

    lasttwo = lasttwo_default

    for o, a in opts:
        if o in ["-l", "--last-two"]:
            if len(a) != 2:
                print("-l/--last-two must be two characters long")
                return 4 #Unrecognized argument
            #End if

            lasttwo = a
        #End if
    #End for

    if len(args) != 2:
        print(usage)
        return 6 #Wrong number of arguments
    #End if

    if len(args[0]) > 6:
        print(usage)
        return 2 #Invalid command
    #End if

    if args[0] == "encode"[0:len(args[0])]:
        function = "e"
    elif args[0] == "decode"[0:len(args[0])]:
        function = "d"
    else:
        print(usage)
        return 2 #Invalid command
    #End if

    inputtext = open(args[-1], "r").read()

    try:
        if function == "e":
            result = base64.b64encode(inputtext, lasttwo)
        else:
            result = base64.b64decode(inputtext, lasttwo)
        #End if
    except TypeError as err:
        print(str(err))
        print("Invalid Base64")
        return 2 #Invalid command
    #End try

    print("-"*50)
    print("")
    print("Result:\n{}\n".format(result))
    print("-"*50)

    return 0
#End def
