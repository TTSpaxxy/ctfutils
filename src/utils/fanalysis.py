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
import string

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
analyzewords_default = False #Doesn't analyze complete words by default

shortopt = "u:gs:w"
longopt = ["up-to=", "graph", "show-max=", "analyze-words"]

sizes = {1:"mono", 2:"bi", 3:"tri"} #Most common analysis sizes

text_format_str = "{0[0]}: {0[1]!s} Occurrence{2}"
graph_format_str = "{0[0]}  | {1}  Total: {0[1]!s}"

def analyze_ngram(words, size):
    """
Get a dictionary of the occurrences of all possible n-grams in a list of words
    """
    
    result = {} if size != 1 else dict([(x, 0) for x in string.ascii_lowercase]) #Always include all possible monograms
    for word in words:
        if len(word) < size: continue
        
        for word_slice in range(0, len(word) + 1 - size): #Analyze all possible n-length sequences in the word
            characters =  word[word_slice: word_slice + size]
            if characters not in result: result[characters] = 1
            else: result[characters] += 1
        #End for
    #End for

    return result
#End def

def analyze_words(words):
    """
Get a dictionary of the occurrences of all words in the text
    """
    result = {}
    for word in words:
        if word not in result: result[word] = 1
        else: result[word] += 1
    #End for

    return result
#End def

def analyze_upto(words, maxsize):
    """
Analyze all n-grams in a list of words up to the specified maximum size
    """
    
    results = []
    for i in range(0, maxsize):
        results.append(analyze_ngram(words, i + 1))
    #End for

    return results
#End def

def sort_results(results_dict):
    sorted_list = [result for result in results_dict.iteritems()]
    sorted_list.sort(key = lambda x: x[0])
    sorted_list.sort(key = lambda x: x[1])
    sorted_list.reverse()

    return sorted_list
#End def

def scale_results(sorted_results):
    divisor = math.ceil(float(sorted_results[0][1]) / 25)
    scaled_list = []
    for k, v in sorted_results:
        scaled_list.append(int(math.ceil(float(v) / divisor))) #Otherwise, the resulting graph might take up multiple lines (25 is a guess for terminal width)
    #End for

    return scaled_list
#End def

def analyze_text(inputtext, upto = upto_default, dograph = dograph_default, showmax = showmax_default, analyzewords = analyzewords_default):
    """
Analyze a file of ciphertext and print the results
    """
    
    #Strip words to letters in the standard alphabet
    words = " ".join(inputtext.split())
    words_stripped = words.translate(string.maketrans(string.punctuation + string.digits, ' ' * (len(string.punctuation) + len(string.digits)))).split()

    results = analyze_upto(words_stripped, upto)

    format_str = graph_format_str if dograph else text_format_str #Output format
    print("-"*50)
    
    for i in range(0, len(results)): #Print the results
        size = i + 1

        if size in sizes:
            title = sizes[size] + "gram"
        else:
            title = str(size) + "-gram"
        #End if

        sorted_list = sort_results(results[i])
        scaled_list = scale_results(sorted_list)

        print("")
        print("Results of the {} analysis".format(title))
        print("")

        list_len = len(results[i])

        for i in range(0, min(list_len, showmax)) + [-1] + range(list_len - showmax, list_len): #First n results plus last n results

            if i == -1: #Break in between first and last
                print("...")
                continue
            #End if

            print(format_str.format(sorted_list[i], "[]" * scaled_list[i], "" if scaled_list[i] == 1 else "s"))
        #End for

        print("")
        print("-"*50)
    #End for

    if analyzewords is True:
        word_results = analyze_words(words_stripped)
        sorted_words = sort_results(word_results)
        scaled_words = scale_results(sorted_words)

        print("")
        print("Results of the word analysis")
        print("")

        list_len = len(word_results)

        for i in range(0, min(list_len, showmax)) + [-1] + range(list_len - showmax, list_len): #First n results plus last n results

            if i == -1: #Break in between first and last
                print("...")
                continue
            #End if

            print(format_str.format(sorted_words[i], "[]" * scaled_words[i], "" if scaled_words[i] == 1 else "s"))
        #End for

        print("")
        print("-"*50)
    #End if
#End def

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
    analyzewords = analyzewords_default

    for o, a in opts:
        if o in ("-u", "--up-to"):
            upto = int(a)
        elif o in ("-g", "--graph"):
            dograph = True
        elif o in ("-s", "--show-max"):
            showmax = int(a)
        elif o in ("-w", "--analyze-words"):
            analyzewords = True
        #End if
    #End for

    if len(args) != 1:
        print(usage)
        return 6 #Wrong number of arguments
    else:
        inputfile_name = args[0]
    #End if

    analyze_text(open(inputfile_name, "r").read(), upto, dograph, showmax, analyzewords)

    return 0
#End def

#End fanalysis.py
