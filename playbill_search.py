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
import re
from distutils.dir_util import mkpath
from datetime import datetime


# key_check - takes in a list key and str text. Checks to see if any of the
# word(s) in the list is/are in the text and returns True/False accordingly.
def key_check(key, text):
    if len(key) > 1:
        for item in key:
            if re.search(item, text):
                return True
        return False
    else:
        if re.search(key[0], text):
            return True
        return False


# split - takes in the raw text of the search criteria and parses it into a
# list of word or words. If searching for two+ terms exclusively together, will
# put all terms in as one string in the list. Returns the list for later use.
def split(query):
    # If only one word, just put that word into an array
    query = query.lower()
    if query.isalpha():
        query = re.compile(query)
        return [query]
    elif "&&" in query:
        literal = query.split()
        literal.remove("&&")
        query = re.compile(" ".join(literal))
        return [query]
    # If multiple words, split each word up in an array
    else:
        query = query.split()
        for item in query:
            item = re.compile(item)
        return query


def file_reader(path, files):
    for i in os.listdir(path):
        test = "{}/{}".format(path, i)
        if i.endswith('.txt'):
            files.append(os.path.join(path, i))
        elif os.path.isdir(test):
            files = file_reader(test, files)
    return files


def get_date():
    now = datetime.now()
    return '%002d-%002d-%004d_%02d-%02d-%02d' % (
        now.month, now.day, now.year, now.hour, now.minute, now.second)


def make_folder(matches, path, query):
    folder = path + "/" + query
    # Does this folder already exist? If so, add the current date/time
    # to provide a unique / helpful new name
    if os.path.isdir(folder):
        folder = folder + get_date()
    mkpath(folder)
    for file in matches:
        copy(file, folder)
    return folder


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
    # Get the files
    files = file_reader(path, files)

    # Cracking open the folder
    for filename in files:
        # Did we find the word / words? - Set variable that checks.
        # Opening the file
        with open(filename, "r", encoding="utf-8") as my_file:
            # Loop through each line
            for i, line in enumerate(my_file):
                # Splitting up the line into words, saving to an array
                line_text = line.lower()
                if key_check(key, line_text):
                    matches.append(filename)

    # Did we get any files? Let's check before we make a folder!
    # Yes?
    if len(matches) > 0:
        folder = make_folder(matches, path, query)
        print ("\nSearch item found! Folder created!")
        return folder
    # No?
    else:
        print ("Sorry, we couldn't find it!")
        return None


def main():
    # Welcome message
    print ("""Please enter your search criteria after the prompt! You will
receive a new folder with every file containing your search item(s) in a
given folder! This new folder will be named after your search criteria.

(Note: If you want to search "Drury Lane" and ONLY get instances of the two
together, please format your search "Drury && Lane". Failure to do so will earn
you a folder containing every instance of Drury and every instance of Lane!)

- AH
    """)

    # Getting the Key
    query = input("What do you want to search for?: ")
    # Getting the directory
    directory = input("""Please provide the absolute path for the folder you
 wish to access (i.e. ~/Downloads/Test): """)
    # Actually running the function
    return search(query, directory)


if __name__ == "__main__":
    main()
