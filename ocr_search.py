import sys
import re
from LocationMatrix import LocationMatrix as location


# Check to see if the context word(s) are even there before checking where
# they are. Returns list of 3 booleans - is the word before the anchor,
# after the anchor, and / or right next to the anchor? Has special option for
# location search, as before or after may be rendered moot. Takes in the
# matrix, the context search term, and a private indicator of if the matrix
# is from a location search, and whether to test the matrix for before or
# after.
def get_bools(matrix, context, test):
    # compile the context term
    # For list of regex characters, see https://github.com/tartley/python-regex
    # -cheatsheet/blob/master/cheatsheet.rst
    context = re.compile(context)
    # Is the term even there? Should we even bother?
    if matrix.search(context):
        # Yes, let's get the locations for all the times the term shows up
        terms = matrix.get_index(context)
        # Any other test
        if test == "":
            bef = matrix.check_context(terms, 0)
            aft = matrix.check_context(terms, 1)
            tog = matrix.check_together(terms)
        # Location test option - search only before the anchor
        elif test == 0:
            bef = True
            aft = False
            tog = matrix.check_together_frac(terms, 0)
        # Location test option - search only after the anchor
        elif test == 1:
            bef = False
            aft = True
            tog = matrix.check_together_frac(terms, 1)
        # Return the results
        return [bef, aft, tog]
    else:
        #  Context not present - return False
        return [False, False, False]


def word_windows_start(matrix):
    test = input("Run Word Windows Test Y/N?: ")
    if test == "Y" or test == "y":
        anchor = input("Please enter anchor term: ")
        context = input("Please enter context term: ")
        n = int(input("Please enter the number of words to search before\
/after the anchor term: "))
        master = word_windows(anchor, context, n, matrix)
        master[0].append(matrix.get_file())
        master = csv_results("Word", master)
        return master
    else:
        return False


# Search for the context term within n words of the anchor term
# Currently only searches for first instance of anchor term.
def word_windows(anchor, context, n, matrix):
    # Restart the matrix
    matrix.refresh_matrix()
    search = [anchor, context, n]
    lines = []
    master_results = [search, lines]
    # Are the anchor term and the context term even there?
    if matrix.search(anchor) and matrix.search(context):
        # Get index for the anchor
        anchors = matrix.get_index(anchor)
        for index in anchors:
            # Cuts the matrix down to n words before and n words after anchor
            matrix.refresh_matrix()
            lines.append(matrix.get_line(index))
            matrix.get_n_range(n, index)
            results = get_bools(matrix, context, "")
            master_results.append(results)
    else:
        # Not Here, set / print  False
        results = [False, False, False]
        lines.append("")
        master_results.append(results)
    return master_results


def char_windows_start(matrix):
    test = input("Run Character Windows Test Y/N?: ")
    if test == "Y" or test == "y":
        anchor = input("Please enter anchor term: ")
        context = input("Please enter context term: ")
        n = int(input("Please enter the number of characters to search before\
/after the anchor term: "))
        master = character_windows(anchor, context, n, matrix)
        master[0].append(matrix.get_file())
        master = csv_results("Character", master)
        return master
    else:
        return False


# Search for context term n chars before and n chars after anchor term
def character_windows(anchor, context, n, matrix):
    # Restart the matrix
    matrix.refresh_matrix()
    search = [anchor, context, n]
    lines = []
    master_results = [search, lines]
    # Is the term there?
    if matrix.search(anchor) and matrix.search(context):
        # Get anchor index
        anchors = matrix.get_index(anchor)
        for index in anchors:
            matrix.refresh_matrix()
            lines.append(matrix.get_line(index))
            # Translate the matrix lines to strings, replace anchor with ^
            sym = matrix.get_chars(index)
            # Trim the matrix into chunk consisting of n characters before
            # and n characters after ^
            matrix.trim_matrix_full(sym - n, 2 * n)
            # resplit the lines into lists of words
            matrix.re_split()
            # Get the new index of ^
            sym = matrix.get_index("\\^")
            # Split the matrix into before ^ and after ^, removing ^
            matrix.split(sym[0])
            # Get / print results
            results = get_bools(matrix, context, "")
            master_results.append(results)
    else:
        # Not here, get / print results
        results = [False, False, False]
        lines.append("")
        master_results.append(results)
    return master_results


def line_windows_start(matrix):
    test = input("Run Line Windows Test Y/N?: ")
    if test == "Y" or test == "y":
        anchor = input("Please enter anchor term: ")
        context = input("Please enter context term: ")
        n = int(input("Please enter the number of lines to test before and\
 after anchor: "))
        master = line_windows(anchor, context, n, matrix)
        master[0].append(matrix.get_file())
        master = csv_results("Line", master)
        return master
    else:
        return False


# Search for term within n lines before and after anchor
def line_windows(anchor, context, n, matrix):
    # Restart matrix
    matrix.refresh_matrix()
    search = [anchor, context, n]
    lines = []
    master_results = [search, lines]
    # Is it there?
    if matrix.search(anchor) and matrix.search(context):
        # Get index of anchor
        anchors = matrix.get_index(anchor)
        for index in anchors:
            matrix.refresh_matrix()
            lines.append(matrix.get_line(index))
            #  Split the matrix into lines before and after anchor
            matrix.get_lines(index, n)
            # Get / print  results
            results = get_bools(matrix, context, "")
            master_results.append(results)
    else:
        # Not here - Get / print / return results
        results = [False, False, False]
        lines.append("")
        master_results.append(results)
    return master_results


def playbill_windows_start(matrix):
    test = input("Run Playbill Windows Test Y/N?: ")
    if test == "Y" or test == "y":
        anchor = input("Please enter anchor term: ")
        context = input("Please enter context term: ")
        master = playbill_windows(anchor, context, matrix)
        master[0].append(matrix.get_file())
        master = csv_results("Playbill", master)
        return master
    else:
        return False


# Search the entire playbill for the context term in regard to the anchor term
def playbill_windows(anchor, context, matrix):
    # Restart matrix
    matrix.refresh_matrix()
    search = [anchor, context]
    lines = []
    master_results = [search, lines]
    # Are they there?
    if matrix.search(anchor) and matrix.search(context):
        # Get anchor index
        anchors = matrix.get_index(anchor)
        for index in anchors:
            lines.append(matrix.get_line(index))
            # Split matrix into before anchor and after anchor
            matrix.split(index)
            # get / print / return results
            results = get_bools(matrix, context, "")
            master_results.append(results)
    else:
        # Not there - get / print / return results
        results = [False, False, False]
        lines.append("")
        master_results.append(results)
    return master_results


def loc_search_start(matrix):
    test = input("Run Location Search Test Y/N?: ")
    if test == "Y" or test == "y":
        anchor = input("Please enter anchor term: ")
        context = input("Please enter context term: ")
        index = input("Please enter where you would like to start your \
location search (enter 0 to start from the beginning or leave blank \
to use the anchor word as an index): ")
        if index != "":
            index = int(index)
        percent = float(input("Please enter what percentage of the playbill\
 you would like to search: "))
        master = location_search(anchor, context, index, percent, matrix)
        master[0].append(matrix.get_file())
        master = csv_results("Location", master)
        return master
    else:
        return False


# Takes in index and percent - index = where to start, percent = how much to
# use. Index - enter number of words, Percent - number between 0 and 1. If no
# index entered, runs the program using the anchor as the starting / ending
# point.
def location_search(anchor, context, index, percent, matrix):
    # Restart matrix
    matrix.refresh_matrix()
    search = [anchor, context, index, percent]
    lines = []
    master_results = [search, lines]
    # Are they there?
    if matrix.search(anchor) and matrix.search(context):
        # No index - use anchor as start / end point
        # get words
        words = matrix.calc_frac_percent(percent)
        if type(index) != int:
            # get anchor index
            anchors = matrix.get_index(anchor)
            for index in anchors:
                lines.append(matrix.get_line(index))
                # trim matrix to before or after anchor (+ percent = aft,
                # - = bef)
                matrix.trim_matrix(index, words)
                matrix.update_matrix()
                # Get results for after ancher
                if percent > 0:
                    results = get_bools(matrix, context, 1)
                # Get results for before anchor
                else:
                    results = get_bools(matrix, context, 0)
                master_results.append(results)
        # Index present
        else:
            # trim matrix to number of words before / after index point
            matrix.trim_matrix_full(index, words)
            # Is anchor present here?
            if matrix.search(anchor):
                # Get anchor index
                anchors = matrix.get_index(anchor)
                for index in anchors:
                    lines.append(matrix.get_line(index))
                    # Split to before anchor and after anchor
                    matrix.split(index)
                    # Get results
                    results = get_bools(matrix, context, "")
                    master_results.append(results)
            # Anchor not present - results = False
            else:
                results = [False, False, False]
                lines.append("")
                master_results.append(results)
    else:
        # Not present - get / print / results
        results = [False, False, False]
        lines.append("")
        master_results.append(results)
    return master_results


def csv_results(test, master):
    search = master[0]
    lines = master[1]
    results = []
    line = [" "] * 11
    for i in range(2, len(master)):
        line[0] = test
        line[1] = search[len(search) - 1]
        line[2] = master[i][0]
        line[3] = master[i][1]
        line[4] = master[i][2]
        line[5] = search[0]
        line[6] = search[1]
        if len(search) == 4:
            line[7] = search[2]
        elif len(search) == 5:
            line[8] = search[2]
            line[9] = search[3]
        line[10] = lines[i - 2]
        results += line
    return results


# Print the results in an orderly fashion. Takes in which test, and the results
def format_results(master):
    str = ""
    results = ""
    str += "{} Results:\n".format(master[0])
    str += "File: {}\n".format(master[1])
    str += "\tBefore:   {}\n".format(master[2])
    str += "\tAfter:    {}\n".format(master[3])
    str += "\tTogether: {}\n".format(master[4])
    str += "\t\tAnchor:         {}\n".format(master[5])
    str += "\t\tContext:        {}\n".format(master[6])
    if master[0] == "Location":
        str += "\t\tStarting Index: {}\n".format(master[8])
        str += "\t\tPercent Taken:  {}\n".format(master[9])
    elif master[0] != "Playbill":
        str += "\t\tWindow Size:    {}\n".format(master[7])
    str += master[10] + "\n\n"
    results += str
    return results


def print_results(master):
    if type(master[0]) == list:
        for i in master:
            print(format_results(master))
    else:
        print(format_results(master))


# Get the variables and run the tests!
def main():
    file = sys.argv[1]
    matrix = location(file)
    full = {}
    full["Word"] = word_windows_start(matrix)
    full["Char"] = char_windows_start(matrix)
    full["Line"] = line_windows_start(matrix)
    full["Playbill"] = playbill_windows_start(matrix)
    full["Loc"] = loc_search_start(matrix)

    return full


if __name__ == "__main__":
    full = main()
    for i in full:
        if full[i] is not False:
            print_results(i + " Results", full[i])
