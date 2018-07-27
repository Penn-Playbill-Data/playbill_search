import ocr_search_out
import ocr_search
import csv_dict_writer
import playbill_search
import glob
import os
import sys


def check_here(cond, loc):
    return [loc == cond, cond]


def set_cond():
    test = input("Search results that match criteria Y/N?: ")
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
            file = ""
            count = 0
            for j in range(len(full[i])):
                info = full[i][j]
                if file != info[1]:
                    count = 0
                file = info[1]
                loc = [info[2], info[3], info[4]]
                res = check_bools(bools[0], bools[1], loc)
                cond = res[1]
                check = res[0]
                if check and info[1] not in matches:
                    if cond is True or count == 0:
                        matches.append(info[1])
                elif not check and info[1] in matches and cond is False:
                    matches.remove(info[1])
                count += 1
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
    if matches != []:
        return playbill_search.make_folder(matches, folder, query)
    else:
        return folder


def get_path(folder, ext):
    path = "{}/results.{}".format(folder, ext)
    if os.path.isfile(path):
        file = "results{}.{}".format(playbill_search.get_date(), ext)
        path = "{}/{}".format(folder, file)
    return path


def csv_file(folder, full):
    path = get_path(folder, "csv")
    data = ocr_search_out.csv_writer(full)
    csv_dict_writer.run_csv_writer(data, path)


# Create Textfile with results
def results_file(folder, full):
    path = get_path(folder, "txt")
    # with open(path, "a") as file:
    for i in full:
        if full[i] is not False:
            for j in range(len(full[i])):
                with open(path, "a", encoding="utf-8") as file:
                    file.write(ocr_search.format_results(full[i][j]))


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
    if sys.argv[1] == "1":
        matches = parse(full)
        filter(matches, folder)
        results_file(folder, full)
        csv_file(folder, full)
    elif sys.argv[1] == "2":
        matches = parse(full)
        folder = subfolder(
            matches, folder, "Search_{}".format(playbill_search.get_date()))
        results_file(folder, full)
        csv_file(folder, full)
    else:
        results_file(folder, full)
        csv_file(folder, full)


if __name__ == "__main__":
    main()
