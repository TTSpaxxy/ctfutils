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

#Start md5crack.py

import getopt
import hashlib
import string
import time

usage = "Usage: md5crack [args] <input hash>"

shortdesc = """
md5crack - MD5 Hash Cracker
    Crack an MD5 hash with brute force or with rainbow tables

{}
""".format(usage)

longdesc = """Options:
-c OR --character-sets | Specify the character sets to be tried
                       | a = a-z
                       | A = A-Z
                       | d = 0-9
                       | s = Special Characters
                       | (Defaults to aAd)
                       |
-l OR --key-len        | Specify the max key length to be tried (Defaults to 4)
                       |
-s OR --show-progress  | Show the progress and hashes/second
"""

charactersets_all = "aAds"

charactersets_default = "aAd"
keylen_default = 4
showprogress_default = False

shortopt = "c:l:s"
longopt = ["character-sets=", "key-len=", "show-progress"]

def f(arg_list):
    """
Crack an MD5 hash with brute force or via rainbow tables
    """
    try:
        opts, args = getopt.getopt(arg_list, shortopt, longopt)
    except getopt.GetoptError as err:
        print(str(err))
        return 4 #Unrecognized argument
    #End try

    charactersets = charactersets_default
    keylen = keylen_default
    showprogress = showprogress_default

    for o, a in opts:
        if o in ("-c", "--character-sets"):
            charactersets = str([c for c in a if c in charactersets_all])
        elif o in ("-l", "--key-len"):
            keylen = int(a)
        elif o in ("-s", "--show-progress"):
            showprogress = True
        #End if
    #End for

    if len(args) != 1:
        print("Usage: md5crack [args] <input file>")
        return 6 #Wrong number of arguments
    else:
        inputhash = args[0]
    #End if

    #Make sure hash is valid
    if len(inputhash) != 32 or not all(c in string.hexdigits for c in inputhash):
        print("Error: Not a valid MD5 hash!")
        return 4 #Unrecognized argument
    #End if

    #Decode character sets
    chars = ""
    for setname in charactersets:
        if setname == "a":
            chars += string.ascii_lowercase
        elif setname == "A":
            chars += string.ascii_uppercase
        elif setname == "d":
            chars += string.digits
        elif setname == "s":
            chars += string.punctuation
        #End if
    #End for

    #Actually brute force it
    test_progress = [-1] * keylen
    set_len = len(chars)
    matches = []
    start = time.time()
    hashes = 0
    while test_progress[0] != set_len:
        test_str = "".join([chars[i] for i in test_progress if i >= 0])
        test_result = hashlib.md5(test_str).hexdigest()
        hashes += 1
        if test_result == inputhash:
            print("Match found: {}".format(test_str))
            matches.append(test_str)
        #End if

        if showprogress is True:
            now = time.time()
            if now - start >= 1:
                print("Current test: {0} | Hashes per second: {1!s}".format(test_str, hashes))
                start = now
                hashes = 0
            #End if
        #End if

        test_progress[-1] += 1
        for i in reversed(range(0, len(test_progress))):
            if test_progress[i] == set_len and i != 0:
                test_progress[i] = 0
                test_progress[i - 1] += 1
            #End if
        #End for
    #End while

    print("")
    print("Results ({0!s} match(es) found): ".format(len(matches)))
    for result in matches:
        print(result)
    #End for
    print("")

    return 0
#End def
