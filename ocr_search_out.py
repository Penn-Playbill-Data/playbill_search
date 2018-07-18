import ocr_search


def word_windows_out(files):
    test = input("Run Word Windows Test Y/N?: ")
    if test == "Y" or test == "y":
        anchor = input("Please enter anchor term: ")
        context = input("Please enter context term: ")
        n = int(input("Please enter the number of words to search before\
/after the anchor term: "))
        master = []
        count = 0
        for i in files:
            matrix = ocr_search.location(i)
            master.append(ocr_search.word_windows(anchor, context, n, matrix))
            master[count][0].append(i)
            count += 1
        return master
    else:
        return False


def char_windows_out(files):
    test = input("Run Character Windows Test Y/N?: ")
    if test == "Y" or test == "y":
        anchor = input("Please enter anchor term: ")
        context = input("Please enter context term: ")
        n = int(input("Please enter the number of characters to search before\
/after the anchor term: "))
        master = []
        count = 0
        for i in files:
            matrix = ocr_search.location(i)
            master.append(ocr_search.character_windows(
                anchor, context, n, matrix))
            master[count][0].append(i)
            count += 1
        return master
    else:
        return False


def line_windows_out(files):
    test = input("Run Line Windows Test Y/N?: ")
    if test == "Y" or test == "y":
        anchor = input("Please enter anchor term: ")
        context = input("Please enter context term: ")
        n = int(input("Please enter the number of lines to test before and\
 after anchor: "))
        master = []
        count = 0
        for i in files:
            matrix = ocr_search.location(i)
            master.append(ocr_search.line_windows(anchor, context, n, matrix))
            master[count][0].append(i)
            count += 1
        return master
    else:
        return False


def playbill_windows_out(files):
    test = input("Run Playbill Windows Test Y/N?: ")
    if test == "Y" or test == "y":
        anchor = input("Please enter anchor term: ")
        context = input("Please enter context term: ")
        master = []
        count = 0
        for i in files:
            matrix = ocr_search.location(i)
            master.append(ocr_search.playbill_windows(anchor, context, matrix))
            master[count][0].append(i)
            count += 1
        return master
    else:
        return False


def loc_search_out(files):
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
        master = []
        count = 0
        for i in files:
            matrix = ocr_search.location(i)
            master.append(
                ocr_search.location_search(
                    anchor, context, index, percent, matrix))
            master[count][0].append(i)
            count += 1
        return master
    else:
        return False


def out(files):
    full = {}
    full["Word"] = word_windows_out(files)
    full["Char"] = char_windows_out(files)
    full["Line"] = line_windows_out(files)
    full["Playbill"] = playbill_windows_out(files)
    full["Loc"] = loc_search_out(files)
    return full


def out_master(full):
    for i in full:
        sum = []
        results = {}
        if full[i] is not False:
            for j in range(len(full[i])):
                info = full[i][j]
                file = info[0][len(info[0]) - 1]
                sum.append(ocr_search.print_results(
                    i + " Results", info))
                for k in range(len(full[i][j])):
                    info = full[i][j][k]
                    if info is not False:
                        if k >= 2:
                            if file in results:
                                results[file].append(info)
                            else:
                                results[file] = [info]
            full[i] = [sum, results]
    return full
