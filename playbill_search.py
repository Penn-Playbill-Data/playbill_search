# Search Program
#
# By Anastasia Hutnick
#
# Goal: To search through a folder and pull the resulting files into
# a new folder with the name of the search criteria. Currently can search for
# every instance of every search term (i.e. Drury Lane) or every instance
# of the search terms together (i.e. Drury && Lane). Works with .json and
# .txt files.

# Import os, copy, and mkpath for folder / file reading and writing magic.
import os
from shutil import copy
from distutils.dir_util import mkpath
# Import json so we can access the json files.
import json
# Import datetime
from datetime import datetime


# key_check - takes in a list key and str text. Checks to see if any of the
# word(s) in the list is/are in the text and returns True/False accordingly.
def key_check(key, text):
    if len(key) > 1:
        for item in key:
            if item in text:
                return True
        return False
    else:
        if key[0] in text:
            return True
        return False


# split - takes in the raw text of the search criteria and parses it into a
# list of word or words. If searching for two+ terms exclusively together, will
# put all terms in as one string in the list. Returns the list for later use.
def split(query):
    # If only one word, just put that word into an array
    query = query.lower()
    if query.isalpha():
        return [query]
    elif "&&" in query:
        literal = query.split()
        literal.remove("&&")
        return [" ".join(literal)]
    # If multiple words, split each word up in an array
    else:
        return query.split()


# Read a json file
def json_reader(filename):
    if filename.endswith(".json"):
        json_text = filename.read()
        return json.loads(json_text)


# Crack the json file - isolate the text
def json_cracker(json_data, json_text):
    # Loop through the file
    for i in json_data:
        print i
        # If it's something we can use in the search function, keep and return
        if type(i) == "str" or type(i) == "int":
            json_text += json_data
            return json_text
        # Otherwise, continue recursively searching through the file!
        elif type(i) == "list" or type(i) == "dict":
            return json_cracker(i, json_text)


def check_continuity(continuity_check):
        if continuity_check == "Y" or "y":
            return True
        elif continuity_check == "N" or "n":
            return False
        return raw_input("\nSorry, I don't understand. Please answer Y or N: ")


# Creating the main function - takes in the word(s) to be found and the folder
# path
def search(query, directory):
    # Change directory into something we can use.
    path = os.path.expanduser(directory)
    # Parsing the query into a key
    key = split(query)
    # Create an array to store files
    files = []
    # Create an array to store successful files
    matches = []
    filetypes = []
    # Get the files
    for i in os.listdir(path):
        if i.endswith('.txt') or i.endswith(".json"):
            files.append(os.path.join(path, i))
            filetypes.append(1)
        elif i.endswith('.json'):
            files.append(os.path.join(path, i))
            filetypes.append(2)

    # Cracking open the folder
    for filename in files:
        count = 0
        # Did we find the word / words? - Set variable that checks.
        # Opening the file
        with open(filename, "r") as my_file:
            # Loop through each line
            if filetypes[count] == 1:
                for i, line in enumerate(my_file):
                        # Splitting up the line into words, saving to an array
                        line_text = line.lower()
                        if key_check(key, line_text):
                            matches.append(filename)
            elif filetypes[count] == 2:
                json_data = json_reader(my_file)
                json_text = json_cracker(json_data, "")
                if key_check(key, json_text):
                    matches.append(filename)
            count += 1

    # Did we get any files? Let's check before we make a folder!
    # Yes?
    if len(matches) > 0:
        folder = path + "/" + query
        # Does this folder already exist? If so, add the current date/time
        # to provide a unique / helpful new name
        if os.path.isdir(folder):
            folder = folder + str(datetime.now())
        mkpath(folder)
        for file in matches:
            copy(file, folder)
        print "\nSearch item found! Folder created!"
    # No?
    else:
        print "Sorry, we couldn't find it!"


# Welcome message
print """Please enter your search criteria after the prompt! You will
receive a new folder with every file containing your search item(s) in a given
folder! This new folder will be named after your search criteria.

(Note: If you want to search "Drury Lane" and ONLY get instances of the two
together, please format your search "Drury && Lane". Failure to do so will earn
you a folder containing every instance of Drury and every instance of Lane!)
- AH

"""
continuity = True

while continuity:
    # Getting the Key
    query = input("What do you want to search for?: ")
    # Getting the directory
    directory = input("""Please provide the absolute path for the folder
    you wish to access (i.e. ~/Downloads/Test): """)
    # Actually running the function
    search(query, directory)
    continuity_check = raw_input("\nWould you like to search again? Y/N: ")
    while continuity_check.upper() != "Y" or continuity_check.upper() != "N":
        continuity = check_continuity(continuity_check)
