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

#start hex2text.py

import getopt
import string

usage = "hex2text [args] <input file>"

shortdesc = """
hex2text - Hexadecimal to Text Conversion
    Convert files of hexadecimal numbers to human-readable text

{}
""".format(usage)

longdesc = """Options:
-a OR --ascii    | Use the ASCII charset (Default)
                 |
-e OR --extended | Use the Extended ASCII charset
                 |
-8 OR --utf-8    | Use the UTF-8 charset
                 |
-u OR --utf-16   | Use the UTF-16 charset
                 |
                 | (Only one of these encodings may be used at a time)
"""

charset_default = "ascii"

shortopt = "ae8u"
longopt = ["ascii", "extended-ascii", "utf-8", "utf-16"]

def f(arg_list):
    """
Hex to Text - Convert hexadecimal numbers to text
    """
    try:
        opts, args = getopt.getopt(arg_list, shortopt, longopt)
    except getopt.GetoptError as err:
        print(str(err))
        return 4 #Unrecognized argument
    #End try

    charset = charset_default

    for o, a in opts:
        if o in ("-a", "--ascii"):
            charset = "ascii"
            break
        elif o in ("-e", "--extended-ascii"):
            charset = "extended ascii"
            break
        elif o in ("-8", "--utf-8"):
            charset = "utf-8"
            break
        elif o in ("-u", "--utf-16"):
            charset = "utf-16"
            break
        #End if
    #End for
    
    if len(args) != 1:
        print(usage)
        return 6 #Wrong number of arguments
    else:
        inputfile_name = args[0]
    #End if

    inputfile = open(inputfile_name, "r").read().split() #Split the file into bytes or words (If it's UTF-16)
    output = ""

    numleft = 0
    for point in inputfile:
        num = int("0x" + point)
        output += chr(num)
    #End for

    print(output)
    
    return 0
#End def
