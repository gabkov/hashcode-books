#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
import sys
import time


INPUT_FILES_NAMES = ["a_example.txt", "b_read_on.txt", "c_incunabula.txt",
                     "d_tough_choices.txt", "e_so_many_books.txt", "f_libraries_of_the_world.txt"]
OUTPUT_FILE_NAMES = ["a_example_out.txt", "b_read_on_out.txt", "c_incunabula_out.txt",
                     "d_tough_choices_out.txt", "e_so_many_books_out.txt", "f_libraries_of_the_world_out.txt"]
FILE_NAME_INDEX = int(sys.argv[1])

def write_result_into_file(packed_scanned_books, lib_order):
    with open('output/' + OUTPUT_FILE_NAMES[FILE_NAME_INDEX], 'w+') as f:
        f.write(str(len(packed_scanned_books)) + "\n")
        for i, pack in enumerate(packed_scanned_books):
            f.writelines("{} {}\n".format(lib_order[i], len(pack)))
            for book in pack:
                f.write(str(book) + " ")
            f.write("\n")
        f.close()

def convert_data_to_list_of_int(data):
    return [int(d) for d in data.split()]


def convert_data_to_set_of_int(data):
    return {int(d) for d in data.split()}

def pack_libraries_with_books(libraries_and_books):
    libs_packed = []
    for i in range(0, len(libraries_and_books), 2):
        current_lib = libraries_and_books[i:i+2]
        # adding the real library index to the pack for later reference
        current_lib.append(int(i / 2))
        libs_packed.append(current_lib)
    return libs_packed


def main():
    raw_data = []
    with open("input/" + INPUT_FILES_NAMES[FILE_NAME_INDEX]) as f:
        raw_data = f.read().strip().split("\n")
        f.close()

    booknum_libraries_days = convert_data_to_list_of_int(raw_data.pop(0))
    book_scores = convert_data_to_list_of_int(raw_data.pop(0))

    # the libs will be list of int the books are set of int -> sample output [[5, 3, 2], {1..5}, 0] lib, books, id
    libraries_and_books = [convert_data_to_list_of_int(data)
                           if not i % 2 else
                           convert_data_to_set_of_int(data)
                           for i, data in enumerate(raw_data)]

    libs_packed_unsorted = pack_libraries_with_books(libraries_and_books)

    # sort by signup time (asc) and number of books (desc)
    libs_packed = sorted(libs_packed_unsorted, key=lambda x: (x[0][1], -len(x[1])))


    #print([print("index: " + str(i) + " " + str(libs[0]) + " real len: " + str(len(libs[1]))) for i, libs in enumerate(libs_packed)])

    days = booknum_libraries_days[2]

    current_lib_under_signup = None
    scanned_books = set()
    signup_is_going = False
    scannable_libs = []
    current_signup_count = None
    packed_scanned_books = []
    lib_order = []

    for day in range(days):
        if not signup_is_going:
            current_lib_under_signup = libs_packed.pop(0)
            signup_is_going = True
            current_signup_count = current_lib_under_signup[0][1]

        if(current_signup_count > 0):
            current_signup_count -= 1
        else:
            signup_is_going = False
            scannable_libs.append(current_lib_under_signup)
            current_lib_under_signup = None

        len_packed_scanned_books = len(packed_scanned_books)

        for lib_index, lib in enumerate(scannable_libs):
            books = lib[1]
            if not books:
                continue

            scan_count = lib[0][2]
            id_of_the_lib = lib[2]

            # keep track of the order of the libraries for the output
            if id_of_the_lib not in lib_order:
                lib_order.append(id_of_the_lib)

            # if a new library will post books
            if len_packed_scanned_books <= lib_index:
                packed_scanned_books.append([])

            for i in range(scan_count):
                if books:
                    book = books.pop()
                    while book in scanned_books:
                        if books:
                            book = books.pop()
                        else:
                            break
                    scanned_books.add(book)
                    packed_scanned_books[lib_index].append(book)
                else:
                    break

    write_result_into_file(packed_scanned_books, lib_order)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
