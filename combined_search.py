import ocr_search_out
import playbill_search
import glob
import os
import sys


def check_here(cond, loc):
    return [loc == cond, cond]


def set_cond():
    test = input("Search True Y/N?: ")
    return test == "Y" or test == "y"


def get_test():
    bef = False
    aft = False
    tog = False
    cond = [False, False, False]
    bef_check = input("Search for before results Y/N?: ")
    if bef_check == "Y" or bef_check == "y":
        bef = True
        cond[0] = set_cond()
    aft_check = input("Search for after results Y/N?: ")
    if aft_check == "Y" or aft_check == "y":
        aft = True
        cond[1] = set_cond()
    tog_check = input("Search for together results Y/N?: ")
    if tog_check == "Y" or tog_check == "y":
        tog = True
        cond[2] = set_cond()
    return [[bef, aft, tog], cond]


def check_bools(place, cond, loc):
    if place[0] is True:
        check = check_here(cond[0], loc[0])
        if place[1] is True:
            check = check or check_here(cond[1], loc[1])
        if place[2] is True:
            check = check or check_here(cond[2], loc[2])
    elif place[1] is True:
        check = check_here(cond[1], loc[1])
        if place[2] is True:
            check = check or check_here(cond[2], loc[2])
    else:
        check = check_here(cond[2], loc[2])
    return check


# Parse the Results
def parse(full):
    matches = []
    for i in full:
        if full[i] is not False:
            bools = get_test()
            for j in full[i][1]:
                if type(full[i][1][j][0]) == list:
                    count = 0
                    for k in full[i][1][j]:
                        res = check_bools(bools[0], bools[1], k)
                        cond = res[1]
                        check = res[0]
                        if check and j not in matches:
                            if cond is True or count == 0:
                                print(check, cond, count)
                                matches.append(j)
                        elif not check and j in matches and cond is False:
                            matches.remove(j)
                        count += 1
                else:
                    check = check_bools(bools[0], bools[1], k)
                    cond = check[1]
                    check = check[0]
                    if check and j not in matches:
                        matches.append(j)
                    elif not check and j in matches and cond is False:
                        matches.remove(j)
    return matches


# Filter Results
def filter(matches, folder):
    if matches != []:
        paths = glob.glob(os.path.join(folder, "*.txt"))
        for file in paths:
            if file not in matches:
                os.remove(file)


# Create subfolders
def subfolder(matches, folder, query):
    return playbill_search.make_folder(matches, folder, query)


# Create Textfile with results
def results_file(folder, full):
    file = "results.txt"
    path = "{}/{}".format(folder, file)
    if os.path.isfile(path):
        file = "results{}.txt".format(playbill_search.get_date())
        path = "{}/{}".format(folder, file)
    with open(path, "a") as file:
        for i in full:
            if full[i] is not False:
                for k in range(len(full[i][0])):
                    file.write(full[i][0][k])


def main():
    playbill = input("Run Playbill Search Y/N?: ")
    if playbill == "Y" or playbill == "y":
        folder = playbill_search.main()
    else:
        folder = input("Please input the folder path: ")
        folder = os.path.expanduser(folder)
    files = []
    files = playbill_search.file_reader(folder, files)
    full = ocr_search_out.out(files)
    full = ocr_search_out.out_master(full)
    matches = parse(full)
    if sys.argv[1] == "1":
        filter(matches, folder)
        results_file(folder, full)
    elif sys.argv[1] == "2":
        folder = subfolder(
            matches, folder, "Search_{}".format(playbill_search.get_date()))
        results_file(folder, full)
    else:
        results_file(folder, full)


if __name__ == "__main__":
    main()
