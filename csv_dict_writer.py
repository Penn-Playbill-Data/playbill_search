import csv


def csv_dict_writer(path, fieldnames, data):
    with open(path, "w", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(
            out_file, delimiter=",", fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def run_csv_writer(data, path):
    fieldnames = data[0]
    my_list = []
    for values in data:
        if values != data[0]:
            inner_dict = dict(zip(fieldnames, values))
            my_list.append(inner_dict)
            csv_dict_writer(path, fieldnames, my_list)
