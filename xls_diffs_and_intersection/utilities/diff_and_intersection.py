from datetime import datetime
import shutil
import csv
import os
import sys


def get_duplicates(lst):
    res = []
    for i in range(len(lst) - 1):
        for j in range(i + 1, len(lst)):
            if equal(lst[i], lst[j]):
                res.append([lst[i], lst[j]])
    return res


def get_rows(reader):
    rows = []
    for row in reader:
        rows.append(row)
    return rows


def equal(row1, row2):
    return (
        row1["First\nName"] == row2["First\nName"] and
        row1["Last\nName"] == row2["Last\nName"] and
        row1["Birth\nDate"] == row2["Birth\nDate"]
    )


def set_difference(set1, set2):
    difference = []
    for elem1 in set1:
        found = False
        for elem2 in set2:
            if equal(elem1, elem2):
                found = True
                break
        if not found:
            difference.append(elem1)
    return difference


def set_intersection(set1, set2):
    intersection = []
    for elem1 in set1:
        found = False
        for elem2 in set2:
            if equal(elem1, elem2):
                found = True
                break
        if found:
            intersection.append(elem1)
    return intersection


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python3 {__file__} OLD_FILE_PATH NEW_FILE_PATH")
        sys.exit(1)

    old_file = open(sys.argv[1], "r", encoding="utf-8")
    new_file = open(sys.argv[2], "r", encoding="utf-8")

    old_reader = csv.DictReader(old_file, delimiter=",", quotechar="\"")
    new_reader = csv.DictReader(new_file, delimiter=",", quotechar="\"")

    old_rows = get_rows(old_reader)
    new_rows = get_rows(new_reader)

    old_but_not_new = set_difference(old_rows, new_rows)
    new_but_not_old = set_difference(new_rows, old_rows)
    intersection = set_intersection(old_rows, new_rows)

    current_time = datetime.now()
    output_dir = f"xls_diffs_and_intersection/tmp/differences-intersection_{current_time.year}-{str(current_time.month).zfill(2)}-{str(current_time.day).zfill(2)}_{str(current_time.hour).zfill(2)}.{str(current_time.minute).zfill(2)}.{str(current_time.second).zfill(2)}"
    os.mkdir(output_dir)

    with open(f"{output_dir}/old_but_not_new.csv", "w", encoding="utf-8") as handle_old_but_not_new:
        writer_old_but_not_new = csv.DictWriter(handle_old_but_not_new, old_reader.fieldnames, delimiter=",", quotechar="\"")
        writer_old_but_not_new.writeheader()
        writer_old_but_not_new.writerows(old_but_not_new)
    with open(f"{output_dir}/new_but_not_old.csv", "w", encoding="utf-8") as handle_new_but_not_old:
        writer_new_but_not_old = csv.DictWriter(handle_new_but_not_old, old_reader.fieldnames, delimiter=",", quotechar="\"")
        writer_new_but_not_old.writeheader()
        writer_new_but_not_old.writerows(new_but_not_old)
    with open(f"{output_dir}/intersection.csv", "w", encoding="utf-8") as handle_intersection:
        writer_intersection = csv.DictWriter(handle_intersection, old_reader.fieldnames, delimiter=",", quotechar="\"")
        writer_intersection.writeheader()
        writer_intersection.writerows(intersection)

    old_file.close()
    new_file.close()

    shutil.make_archive(output_dir, "zip", output_dir)
    print(f"{output_dir}.zip")

