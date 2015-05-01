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

#Start fanalysis.py

import getopt
import math
from string import ascii_lowercase

usage = "Usage: fanalysis [args] <input file>"

shortdesc = """
fanalysis - Frequency Analysis
    Analyze files of ciphertext for a frequency fingerprint

{}
""".format(usage)

longdesc = """Options:
-u OR --up-to      | Analyze up to the specified phrase length (Defaults to 3)
                   |
-g OR --graph      | Create a bar graph of the results
                   |
-s OR --show-max   | Show the first and last n results (Defaults to 5)
"""

upto_default = 3 #By default analyzes up to trigrams
dograph_default = False #Doesn't graph the output by default
showmax_default = 5 #The highest number of occurances per n-gram to show in display

shortopt = "u:gs:"
longopt = ["up-to=", "graph", "show-max="]

sizes = {1:"mono", 2:"bi", 3:"tri"} #Most common analysis sizes

text_format_str = "{0[0]}: {0[1]!s} Occurrences"
graph_format_str = "{0[0]}  | {1}  Total: {0[1]!s}"

def f(arg_list):
    """
Frequency analysis - Analyzes an input file of ciphertext and graphs the frequencies of different strings of characters
    """
    try:
        opts, args = getopt.getopt(arg_list, shortopt, longopt)
    except getopt.GetoptError as err:
        print(str(err))
        return 4 #Unrecognized argument
    #End try

    upto = upto_default
    dograph = dograph_default
    showmax = showmax_default

    for o, a in opts:
        if o in ("-u", "--up-to"):
            upto = int(a)
        elif o in ("-g", "--graph"):
            dograph = True
        elif o in ("-s", "--show-max"):
            showmax = int(a)
        #End if
    #End for

    if len(args) != 1:
        print(usage)
        return 6 #Wrong number of arguments
    else:
        inputfile_name = args[0]
    #End if

    words = " ".join(list(open(inputfile_name, "r"))).split()
    words_stripped = []
    for word in words:
        word_stripped = ""
        for c in word:
            if c.isalpha():
                word_stripped += c
            else:
                word_stripped += " " #If it's nonalpha, make it a space
        #End for

        words_stripped.extend(word_stripped.lower().split()) #Split the input stream into a list of alpha-only words
    #End for

    results = []
    for size in range(1, upto + 1):
        result = {} if size != 1 else dict([(x, 0) for x in ascii_lowercase]) #Always include all possible monograms
        for word in words_stripped:
            if len(word) < size: continue

            for word_slice in range(0, len(word) + 1 - size): #Analyze all possible n-length sequences in the word
                characters =  word[word_slice: word_slice + size]
                if characters not in result: result[characters] = 1
                else: result[characters] += 1
            #End for
        #End for

        results.append(result)
    #End for

    format_str = graph_format_str if dograph else text_format_str #Output format
    print("-"*50)

    for i in range(0, len(results)): #Print the results
        size = i + 1

        if size in sizes:
            title = sizes[size] + "gram"
        else:
            title = str(size) + "-gram"
        #End if

        sorted_list = [x for x in results[i].iteritems()] #Create a list of tuples (Easier to manipulate)
        sorted_list.sort(key=lambda x: x[0]) #Sort it according to key
        sorted_list.sort(key=lambda x: x[1]) #Then sort it according to value
        sorted_list.reverse()

        divisor = math.ceil(float(sorted_list[0][1]) / 25)
        scaled_list = []
        for k, v in sorted_list:
            scaled_list.append(int(math.ceil(float(v) / divisor))) #Otherwise, the resulting graph might take up multiple lines (25 is a guess for terminal width)
        #End for

        print("")
        print("Results of the {} analysis".format(title))
        print("")

        list_len = len(results[i])

        for i in range(0, min(list_len, showmax)) + [-1] + range(list_len - showmax, list_len): #First n results plus last n results

            if i == -1: #Break in between first and last
                print("...")
                continue
            #End if

            print(format_str.format(sorted_list[i], "[]" * scaled_list[i]))
        #End for

        print("")
        print("-"*50)
    #End for

    return 0
#End def

#End fanalysis.py
