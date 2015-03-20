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

upto_default = 3 #By default analyzes up to trigrams
dograph_default = False #Doesn't graph the output by default (NOT IMPLEMENTED)
graphtype_default = "bar" #Uses a bar graph by default (NOT IMPLEMENTED)
showmax_default = 5 #The highest number of occurances per n-gram to show in display

shortopt = "u:gt:s:i:"
longopt = ["up-to=", "graph", "graph-type=", "show-max=", "input-file="]

sizes = {1:"mono", 2:"bi", 3:"tri"}

def display(result_dict, size, showmax):
    """
Display the results of the frequency analysis in a text, non-graph format
    """
    if size in sizes: title = sizes[size] + "gram"
    else: title = str(size) + "-gram"
    
    sorted_list = [x for x in result_dict.iteritems()] #Create a list of tuples (Easier to manipulate)
    sorted_list.sort(key=lambda x: x[0])
    sorted_list.sort(key=lambda x: x[1])
    sorted_list.reverse()
    
    print("")
    print("Results of the %s analysis:" % title)
    for i in range(0, min(len(sorted_list), showmax)):
        print(sorted_list[i][0] + ": " + str(sorted_list[i][1]) + " Occurrences")
    #End for

    print("...")
    for i in range(len(sorted_list) - showmax, len(sorted_list)):
        print(sorted_list[i][0] + ": " + str(sorted_list[i][1]) + " Occurrences")
    #End for

    print("")
    print("-"*50)
#End def

def graph(result_dict, showmax):
    """
Display the results of the frequency analysis in a graph format
    """
    size = len(result_dict.keys()[0])
    if size in sizes: title = sizes[size] + "gram"
    else: title = str(size) + "-gram"
    
    sorted_list = [x for x in result_dict.iteritems()]
    sorted_list.sort(key=lambda x: x[0])
    sorted_list.reverse()
    sorted_list.sort(key=lambda x: x[1])
    sorted_list.reverse()
    
    divisor = math.ceil(float(sorted_list[0][1]) / 25)
    scaled_list = []
    for k, v in sorted_list:
        scaled_list.append(int(math.ceil(float(v) / divisor)))
    #End for
    
    print("")
    print("   Results of the %s analysis" % title)
    for i in range(0, min(len(sorted_list), showmax)):
        print("%s  | " % sorted_list[i][0] + "[]" * scaled_list[i] + " Total: %d" % sorted_list[i][1])
    #End for
    
    print("...")
    for i in range(len(sorted_list) - showmax, len(sorted_list)):
        print("%s  | " % sorted_list[i][0] + "[]" * scaled_list[i] + " Total: %d" % sorted_list[i][1])
    #End for
    print("")
    print("-"*50)
#End def

def f(arg_list):
    """
Frequency analysis - Analyzes an input file of ciphertext and graphs the frequencies of different strings of characters
    """
    global shortopt
    global longopt
    
    try:
        opts, args = getopt.getopt(arg_list, shortopt, longopt)
    except getopt.GetoptError as err:
        print(str(err))
        return 4 #Unrecognized argument
    #End try
    
    upto = upto_default
    dograph = dograph_default
    graphtype = graphtype_default
    showmax = showmax_default
    inputfile_name = ""
    
    for o, a in opts:
        if o in ("-u", "--up-to"):
            upto = int(a)
        elif o in ("-g", "--graph"):
            dograph = True
        elif o in ("-t", "--graph-type"):
            graphtype = a
        elif o in ("-s", "--show-max"):
            showmax = int(a)
        elif o in ("-i", "--input-file"):
            inputfile_name = a
        #End if
    #End for
    
    if inputfile_name == "":
        print("Missing input file")
        return 5 #Missing required argument
    #End if
    
    words = " ".join(list(open(inputfile_name, "r"))).split()
    words_stripped = []
    for word in words:
        word_stripped = ""
        for c in word:
            if c.isalpha(): word_stripped += c
        #End for

        words_stripped.extend(word_stripped.lower().split())
    #End for
    
    results = []
    for size in range(1, upto + 1):
        result = {} if size != 1 else dict([(x, 0) for x in ascii_lowercase]) #Always include all monograms
        for word in words_stripped:
            if len(word) < size: continue
            
            for word_slice in range(0, len(word) + 1 - size):
                characters =  word[word_slice: word_slice + size]
                if characters not in result: result[characters] = 1
                else: result[characters] += 1
            #End for
        #End for
        
        results.append(result)
    #End for
    
    if dograph is True:
        for i in range(0, len(results)):
            graph(results[i], showmax)
        #End for
    else:
        for i in range(0, len(results)):
            display(results[i], i + 1, showmax)
        #End for
    #End if
    
    return 0
#End def

#End fanalysis.py
